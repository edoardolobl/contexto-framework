"""Testes de gerar_saidas: schemas publicados, documentos por id@versão, índice, kit, zip e llms.txt."""
import json
import os
from pathlib import Path
import zipfile

from referencing import Registry, Resource
import jsonschema
import pytest

import enderecos
import gerar_saidas as g
import kit

SITE = enderecos.URL_DO_SITE


def doc(id_, versao, tipo, titulo, status="approved", extra="", corpo="Comentário do documento.\n"):
    return (
        f'---\nid: {id_}\nschema_version: "1.1.0"\ntype: {tipo}\ntitle: "{titulo}"\nversion: "{versao}"\n'
        f'revision_id: "{id_}@{versao}"\nstatus: {status}\nvalid_from: "2026-09-15"\nvalid_to: null\n'
        f'intent:\n  question: "Qual é a pergunta de {id_}?"\nplain_summary: "Resumo de {id_}."\n{extra}---\n{corpo}'
    )


def schema(versao, slug, extra=None):
    base = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"urn:contexto:schemas:{versao}:{slug}",
            "title": "Título com acento: ção", "type": "object"}
    if slug == "common":
        base["$defs"] = {"nome": {"type": "string", "minLength": 1}}
    else:
        base["allOf"] = [{"$ref": f"urn:contexto:schemas:{versao}:common"}]
        base["properties"] = {"nome": {"$ref": f"urn:contexto:schemas:{versao}:common#/$defs/nome"}}
    return json.dumps({**base, **(extra or {})}, ensure_ascii=False, indent=2) + "\n"


KIT_YAML = """pasta: contexto-kit-agentes
dados: [aurora-fixture.sql]
skills:
  auditar-coleta: [EVENT-AURORA-GENERATE-LEAD]
"""
AGENTS = "# Kit\n\nÍndice:\n\n<!-- contexto:kit-indice -->\n\nVeja [o glossário](glossario.md) e [a skill](skills/auditar-coleta/SKILL.md).\n"
RESSALVA = kit.FRASE_DA_RESSALVA + "\n\nVersão alvo: especificação Agent Skills, conferida em 17/11/2026.\n"
SKILL = "---\nname: auditar-coleta\ndescription: Audita a coleta de eventos.\n---\n# Auditar coleta\n\n" + RESSALVA + "\nLeia [o evento](references/EVENT-AURORA-GENERATE-LEAD@1.1.md).\n"


def escrever(caminho: Path, texto: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8")


def montar(raiz: Path) -> Path:
    for versao, pasta in (("1.0.0", raiz / "schemas/historico/1.0.0"), ("1.1.0", raiz / "schemas")):
        for slug in ("common", "kpi"):
            escrever(pasta / f"{slug}.schema.json", schema(versao, slug))
    ex = raiz / "src/exemplos"
    escrever(ex / "exemplo-kpi-completo.md", doc("KPI-AURORA-001", "2.0", "kpi", "Taxa de conversão", extra='domain: ecommerce\nsynonyms: ["conversão web"]\nvocabulary:\n  altLabel: ["CR"]\n  not_synonyms: ["Pedidos por sessão"]\n'))
    escrever(ex / "exemplo-kpi-lacunas.md", doc("KPI-AURORA-001", "0.1", "kpi", "Rascunho de conversão", status="draft"))
    escrever(ex / "historico/exemplo-kpi-v1.0.md", doc("KPI-AURORA-001", "1.0", "kpi", "Conversão antiga", status="superseded"))
    escrever(ex / "exemplo-evento-coleta-completo.md", doc("EVENT-AURORA-GENERATE-LEAD", "1.1", "evento-coleta", "Evento generate_lead"))
    escrever(ex / "exemplo-perguntas-de-negocio-completo.md", doc("QA-AURORA-001", "1.1", "perguntas-de-negocio", "Perguntas da Aurora"))
    escrever(raiz / "src/kit/kit.yaml", KIT_YAML)
    escrever(raiz / "src/kit/AGENTS.md", AGENTS)
    escrever(raiz / "src/kit/skills/auditar-coleta/SKILL.md", SKILL)
    escrever(raiz / "public/downloads/aurora-fixture.sql", "select 1;\n")
    return raiz


@pytest.fixture
def raiz(tmp_path: Path) -> Path:
    return montar(tmp_path)


def rodar(raiz: Path, check: bool = False):
    return g.executar(raiz, check=check)


def instantaneo(pasta: Path) -> dict[str, bytes]:
    return {p.relative_to(pasta).as_posix(): p.read_bytes() for p in sorted(pasta.rglob("*")) if p.is_file()}


def publicado(raiz: Path) -> Path:
    return raiz / "public"


# ---------- schemas ----------
def test_schemas_reescrevem_id_e_ref_preservando_fragmento(raiz):
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []
    kpi = json.loads((raiz / "public/schemas/1.1.0/kpi.schema.json").read_text(encoding="utf-8"))
    assert kpi["$id"] == f"{SITE}/schemas/1.1.0/kpi.schema.json"
    assert kpi["allOf"][0]["$ref"] == f"{SITE}/schemas/1.1.0/common.schema.json"
    assert kpi["properties"]["nome"]["$ref"] == f"{SITE}/schemas/1.1.0/common.schema.json#/$defs/nome"
    assert kpi["title"] == "Título com acento: ção"


def test_schemas_da_1_0_0_vem_da_pasta_historica(raiz):
    rodar(raiz)
    antigo = json.loads((raiz / "public/schemas/1.0.0/kpi.schema.json").read_text(encoding="utf-8"))
    assert antigo["$id"] == f"{SITE}/schemas/1.0.0/kpi.schema.json"
    assert sorted(p.name for p in (raiz / "public/schemas/1.0.0").iterdir()) == ["common.schema.json", "kpi.schema.json"]


def test_schemas_formato_do_arquivo(raiz):
    rodar(raiz)
    texto = (raiz / "public/schemas/1.1.0/common.schema.json").read_text(encoding="utf-8")
    assert texto.endswith("}\n") and not texto.endswith("\n\n")
    assert "ção" in texto and "\\u00e7" not in texto
    assert texto == json.dumps(json.loads(texto), indent=2, ensure_ascii=False) + "\n"
    assert "urn:contexto" not in texto


def test_urn_que_sobra_na_saida_gera_erro(raiz):
    escrever(raiz / "schemas/kpi.schema.json", schema("1.1.0", "kpi", {"description": "urn:contexto:schemas:1.1.0:inexistente?x"}))
    relatorio, _ = rodar(raiz)
    assert any("urn:contexto" in e for e in relatorio.erros)
    assert not (raiz / "public/schemas").exists()


def test_registry_com_os_publicados_valida_um_exemplo(raiz):
    rodar(raiz)
    pasta = raiz / "public/schemas/1.1.0"
    recursos = []
    for arquivo in sorted(pasta.glob("*.schema.json")):
        conteudo = json.loads(arquivo.read_text(encoding="utf-8"))
        assert conteudo["$id"] == f"{SITE}/schemas/1.1.0/{arquivo.name}"
        recursos.append((conteudo["$id"], Resource.from_contents(conteudo)))
    registro = Registry().with_resources(recursos)
    kpi = json.loads((pasta / "kpi.schema.json").read_text(encoding="utf-8"))
    validador = jsonschema.Draft202012Validator(kpi, registry=registro)
    assert list(validador.iter_errors({"nome": "ok"})) == []
    assert list(validador.iter_errors({"nome": ""}))


# ---------- documentos ----------
def test_documento_yaml_tem_os_bytes_do_exemplo_gerado(raiz):
    rodar(raiz)
    texto = (raiz / "src/exemplos/exemplo-kpi-completo.md").read_text(encoding="utf-8").split("---\n")[1]
    assert (raiz / "public/documentos/KPI-AURORA-001@2.0.yaml").read_bytes() == texto.encode("utf-8")


def test_documento_md_tem_titulos_com_id_versao_e_vigencia(raiz):
    rodar(raiz)
    texto = (raiz / "public/documentos/KPI-AURORA-001@2.0.md").read_text(encoding="utf-8")
    quadro = "de 15/09/2026, sem fim previsto"
    assert texto.startswith("---\nid: KPI-AURORA-001\n")
    assert "\n---\n\n# Taxa de conversão (KPI-AURORA-001@2.0)\n\n" in texto
    assert "> **Estado:** Aprovado" in texto
    assert "> **Vigência:** de 15/09/2026, sem fim previsto" in texto
    assert "> **Domínio:** ecommerce" in texto
    assert f"> **Licença:** {enderecos.LICENCA_DO_CONTEUDO}" in texto
    assert f"> **Endereço:** {SITE}/documentos/KPI-AURORA-001@2.0.md" in texto
    assert f"## Pergunta que este documento responde (KPI-AURORA-001@2.0, {quadro})\n\nQual é a pergunta de KPI-AURORA-001?\n" in texto
    assert f"## Em poucas palavras (KPI-AURORA-001@2.0, {quadro})\n\nResumo de KPI-AURORA-001.\n" in texto
    assert f"## Comentário (KPI-AURORA-001@2.0, {quadro})\n\nComentário do documento.\n" in texto
    assert texto.endswith("Comentário do documento.\n")


@pytest.mark.parametrize("de,ate,esperado", [
    ("2026-09-15", "2026-10-20", "de 15/09/2026 até 20/10/2026"),
    ("2026-09-15", None, "de 15/09/2026, sem fim previsto"),
    (None, None, "sem vigência definida"),
])
def test_vigencia_curta(de, ate, esperado):
    assert g.vigencia_curta({"valid_from": de, "valid_to": ate}) == esperado


def test_vigencia_longa_diz_que_o_ultimo_dia_nao_conta():
    longa = g.vigencia({"valid_from": "2026-09-15", "valid_to": "2026-10-20"})
    assert longa == "de 15/09/2026 até 20/10/2026, sem contar o último dia"


def test_comentario_vazio_nao_gera_secao(raiz):
    escrever(raiz / "src/exemplos/exemplo-kpi-completo.md", doc("KPI-AURORA-001", "2.0", "kpi", "Taxa", corpo="\n"))
    rodar(raiz)
    assert "## Comentário" not in (raiz / "public/documentos/KPI-AURORA-001@2.0.md").read_text(encoding="utf-8")


def test_estados_em_portugues(raiz):
    rodar(raiz)
    assert "> **Estado:** Rascunho" in (raiz / "public/documentos/KPI-AURORA-001@0.1.md").read_text(encoding="utf-8")
    assert "> **Estado:** Substituído" in (raiz / "public/documentos/KPI-AURORA-001@1.0.md").read_text(encoding="utf-8")


def test_indice_ordenado_com_chaves_do_contrato(raiz):
    rodar(raiz)
    indice = json.loads((raiz / "public/documentos/indice.json").read_text(encoding="utf-8"))
    assert [(i["id"], i["version"]) for i in indice] == [
        ("EVENT-AURORA-GENERATE-LEAD", "1.1"), ("KPI-AURORA-001", "0.1"), ("KPI-AURORA-001", "1.0"),
        ("KPI-AURORA-001", "2.0"), ("QA-AURORA-001", "1.1")]
    assert indice[3] == {
        "id": "KPI-AURORA-001", "version": "2.0", "revision_id": "KPI-AURORA-001@2.0", "type": "kpi",
        "title": "Taxa de conversão", "status": "approved", "valid_from": "2026-09-15", "valid_to": None,
        "license": enderecos.LICENCA_DO_CONTEUDO, "md": "documentos/KPI-AURORA-001@2.0.md",
        "yaml": "documentos/KPI-AURORA-001@2.0.yaml"}
    texto = (raiz / "public/documentos/indice.json").read_text(encoding="utf-8")
    assert texto.endswith("]\n")


def test_versao_10_ordena_depois_de_9(raiz):
    escrever(raiz / "src/exemplos/exemplo-kpi-v9.md", doc("KPI-AURORA-001", "9.0", "kpi", "Nove"))
    escrever(raiz / "src/exemplos/exemplo-kpi-v10.md", doc("KPI-AURORA-001", "10.0", "kpi", "Dez"))
    rodar(raiz)
    indice = json.loads((raiz / "public/documentos/indice.json").read_text(encoding="utf-8"))
    assert [i["version"] for i in indice if i["id"] == "KPI-AURORA-001"][-2:] == ["9.0", "10.0"]


def test_id_e_versao_repetidos_geram_erro(raiz):
    escrever(raiz / "src/exemplos/exemplo-kpi-copia.md", doc("KPI-AURORA-001", "2.0", "kpi", "Cópia"))
    relatorio, _ = rodar(raiz)
    assert any("KPI-AURORA-001@2.0" in e and "repetido" in e for e in relatorio.erros)
    assert not (raiz / "public/documentos").exists()


@pytest.mark.parametrize("linha", ["id: KPI-AURORA-001\n", 'version: "2.0"\n'])
def test_falta_de_id_ou_versao_gera_erro(raiz, linha):
    caminho = raiz / "src/exemplos/exemplo-kpi-completo.md"
    escrever(caminho, caminho.read_text(encoding="utf-8").replace(linha, "", 1))
    relatorio, _ = rodar(raiz)
    assert any("exemplo-kpi-completo.md" in e for e in relatorio.erros)


# ---------- kit ----------
KIT = "public/downloads/kit/contexto-kit-agentes"


def test_kit_tem_a_estrutura_pedida_e_nenhum_rascunho(raiz):
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []
    arquivos = set(instantaneo(raiz / KIT))
    assert arquivos == {
        "AGENTS.md", "glossario.md", "contratos/KPI-AURORA-001@2.0.md", "contratos/EVENT-AURORA-GENERATE-LEAD@1.1.md",
        "contratos/historico/KPI-AURORA-001@1.0.md", "gabaritos/QA-AURORA-001@1.1.md", "dados/aurora-fixture.sql",
        "skills/auditar-coleta/SKILL.md", "skills/auditar-coleta/references/EVENT-AURORA-GENERATE-LEAD@1.1.md"}
    assert not any("@0.1" in a for a in arquivos)


def test_kit_md_dos_documentos_sao_os_mesmos_bytes_de_public_documentos(raiz):
    rodar(raiz)
    docs = raiz / "public/documentos"
    assert (raiz / KIT / "contratos/KPI-AURORA-001@2.0.md").read_bytes() == (docs / "KPI-AURORA-001@2.0.md").read_bytes()
    assert (raiz / KIT / "contratos/historico/KPI-AURORA-001@1.0.md").read_bytes() == (docs / "KPI-AURORA-001@1.0.md").read_bytes()
    assert (raiz / KIT / "gabaritos/QA-AURORA-001@1.1.md").read_bytes() == (docs / "QA-AURORA-001@1.1.md").read_bytes()


def test_agents_troca_o_marcador_por_lista_com_id_versao_e_titulo(raiz):
    rodar(raiz)
    texto = (raiz / KIT / "AGENTS.md").read_text(encoding="utf-8")
    assert "contexto:kit-indice" not in texto
    assert "- [Taxa de conversão (KPI-AURORA-001@2.0)](contratos/KPI-AURORA-001@2.0.md)" in texto
    assert "- [Perguntas da Aurora (QA-AURORA-001@1.1)](gabaritos/QA-AURORA-001@1.1.md)" in texto
    assert "(contratos/historico/KPI-AURORA-001@1.0.md)" in texto
    assert "- [Skill `auditar-coleta`](skills/auditar-coleta/SKILL.md)" in texto


@pytest.mark.parametrize("agents", ["# Kit sem marcador\n", AGENTS + "\n<!-- contexto:kit-indice -->\n"])
def test_marcador_ausente_ou_repetido_gera_erro(raiz, agents):
    escrever(raiz / "src/kit/AGENTS.md", agents)
    relatorio, _ = rodar(raiz)
    assert any("contexto:kit-indice" in e for e in relatorio.erros)


def test_link_quebrado_no_agents_gera_erro(raiz):
    escrever(raiz / "src/kit/AGENTS.md", AGENTS + "\n[some](contratos/NAO-EXISTE@1.0.md)\n")
    relatorio, _ = rodar(raiz)
    assert any("AGENTS.md" in e and "contratos/NAO-EXISTE@1.0.md" in e for e in relatorio.erros)


def test_link_quebrado_no_skill_gera_erro(raiz):
    escrever(raiz / "src/kit/skills/auditar-coleta/SKILL.md", SKILL + "\n[x](references/falta.md)\n")
    relatorio, _ = rodar(raiz)
    assert any("SKILL.md" in e and "references/falta.md" in e for e in relatorio.erros)


def test_links_externos_ancoras_e_codigo_nao_sao_conferidos(raiz):
    escrever(raiz / "src/kit/AGENTS.md", AGENTS + "\n[a](https://exemplo.org) [b](#topo)\n```\n[c](nao/existe.md)\n```\n")
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []


@pytest.mark.parametrize("cabecalho,trecho", [
    ("name: outra-coisa\ndescription: ok\n", "name"),
    ("name: Auditar_Coleta\ndescription: ok\n", "name"),
    ("name: auditar-coleta\n", "description"),
    ("name: auditar-coleta\ndescription: ''\n", "description"),
    ("name: auditar-coleta\ndescription: " + "x" * 1025 + "\n", "description"),
])
def test_skill_fora_da_especificacao_gera_erro(raiz, cabecalho, trecho):
    escrever(raiz / "src/kit/skills/auditar-coleta/SKILL.md", f"---\n{cabecalho}---\n# Corpo\n\n{RESSALVA}")
    relatorio, _ = rodar(raiz)
    assert any("SKILL.md" in e and trecho in e for e in relatorio.erros)


def test_skill_com_name_de_64_caracteres_passa_e_65_falha():
    assert kit.erros_do_frontmatter_da_skill({"name": "a" * 64, "description": "x"}, "a" * 64) == []
    assert kit.erros_do_frontmatter_da_skill({"name": "a" * 65, "description": "x"}, "a" * 65)


def test_skill_com_corpo_de_500_linhas_gera_erro(raiz):
    corpo = "linha\n" * 500
    escrever(raiz / "src/kit/skills/auditar-coleta/SKILL.md", "---\nname: auditar-coleta\ndescription: ok\n---\n" + RESSALVA + corpo)
    relatorio, _ = rodar(raiz)
    assert any("500" in e for e in relatorio.erros)


def test_referencia_de_skill_para_id_sem_documento_aprovado_gera_erro(raiz):
    escrever(raiz / "src/kit/kit.yaml", KIT_YAML.replace("EVENT-AURORA-GENERATE-LEAD", "EVENT-NAO-EXISTE"))
    relatorio, _ = rodar(raiz)
    assert any("EVENT-NAO-EXISTE" in e for e in relatorio.erros)


def test_referencia_usa_a_versao_aprovada_mais_alta(raiz):
    escrever(raiz / "src/exemplos/exemplo-evento-coleta-v2.md", doc("EVENT-AURORA-GENERATE-LEAD", "1.2", "evento-coleta", "Evento novo"))
    escrever(raiz / "src/kit/skills/auditar-coleta/SKILL.md", SKILL.replace("@1.1", "@1.2"))
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []
    assert (raiz / KIT / "skills/auditar-coleta/references/EVENT-AURORA-GENERATE-LEAD@1.2.md").is_file()


def test_arquivo_de_dados_ausente_gera_erro(raiz):
    (raiz / "public/downloads/aurora-fixture.sql").unlink()
    relatorio, _ = rodar(raiz)
    assert any("aurora-fixture.sql" in e for e in relatorio.erros)


def glossario_de(raiz: Path) -> str:
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []
    return (raiz / KIT / "glossario.md").read_text(encoding="utf-8")


def entrada_do(texto: str, termo: str) -> str:
    return texto.split(f"## {termo}\n")[1].split("\n## ")[0]


def termos_do(texto: str) -> list[str]:
    return [linha[3:] for linha in texto.splitlines() if linha.startswith("## ")]


def test_glossario_tem_conceitos_e_deixa_fora_gabaritos_rubricas_e_processos(raiz):
    ex = raiz / "src/exemplos"
    escrever(ex / "exemplo-rubrica-completo.md", doc("RUBRIC-A-001", "1.0", "rubrica", "Rubrica de campanha"))
    escrever(ex / "exemplo-processo-completo.md", doc("PROCESS-A-001", "1.0", "processo", "Solicitar campanha"))
    escrever(ex / "exemplo-dataset-completo.md", doc("DATASET-A-001", "1.0", "dataset", "Pedidos: Aurora"))
    texto = glossario_de(raiz)
    assert "documentos aprovados" in texto.split("##")[0]
    assert termos_do(texto) == ["Evento generate_lead", "Taxa de conversão"]
    for fora in ("Perguntas da Aurora", "Rubrica", "Solicitar", "Pedidos: Aurora", "Rascunho", "Conversão antiga"):
        assert fora not in texto


def test_glossario_entrada_do_indicador_traz_termo_sinonimos_nao_confundir_e_origem(raiz):
    escrever(raiz / "src/exemplos/exemplo-kpi-completo.md", doc(
        "KPI-AURORA-001", "2.0", "kpi", "Taxa de conversão: loja web",
        extra='synonyms: ["conversão web"]\nvocabulary:\n  altLabel: ["CR"]\n  not_synonyms: ["Pedidos por sessão"]\n'
              'business_definition:\n  concept: "Sessões com pedido sobre sessões elegíveis"\n'
              '  different_meanings_in_other_domains: ["Conversão de lead: outro indicador"]\n'))
    entrada = entrada_do(glossario_de(raiz), "Taxa de conversão")
    assert "Sessões com pedido sobre sessões elegíveis" in entrada
    assert "**Também chamado:** conversão web; CR" in entrada
    assert "**Não confundir com:** Pedidos por sessão; Conversão de lead: outro indicador" in entrada
    assert "**Fonte:** `KPI-AURORA-001@2.0`" in entrada


def test_glossario_entrada_do_conceito_usa_termo_preferido_e_definicao(raiz):
    escrever(raiz / "src/exemplos/exemplo-conceito-completo.md", doc(
        "CONCEPT-A-001", "2.0", "conceito", "Participante ativo: programa",
        extra='definition: "Pessoa inscrita com presença nos últimos 30 dias."\nvocabulary:\n  prefLabel: "Participante ativo"\n'
              '  not_synonyms: ["Participante inscrito"]\n  other_domain_meanings: ["Na folha, ativo é vínculo vigente."]\n'))
    entrada = entrada_do(glossario_de(raiz), "Participante ativo")
    assert "Pessoa inscrita com presença nos últimos 30 dias." in entrada
    assert "Resumo de CONCEPT-A-001." not in entrada
    assert "**Não confundir com:** Participante inscrito; Na folha, ativo é vínculo vigente." in entrada
    assert "**Fonte:** `CONCEPT-A-001@2.0`" in entrada


def test_glossario_evento_com_desambiguacao_vira_uma_entrada_por_termo(raiz):
    escrever(raiz / "src/exemplos/exemplo-evento-coleta-completo.md", doc(
        "EVENT-AURORA-GENERATE-LEAD", "1.1", "evento-coleta", "Evento generate_lead: Aurora",
        extra='disambiguation:\n  - term: generate_lead\n    means: "Cadastro de atacado enviado"\n'
              '    not_to_confuse_with: "sign_up da newsletter"\n'))
    texto = glossario_de(raiz)
    entrada = entrada_do(texto, "generate_lead")
    assert "Cadastro de atacado enviado" in entrada
    assert "**Não confundir com:** sign_up da newsletter" in entrada
    assert "**Fonte:** `EVENT-AURORA-GENERATE-LEAD@1.1`" in entrada
    assert "Evento generate_lead" not in termos_do(texto)


def test_glossario_omite_linhas_sem_sinonimos(raiz):
    entrada = entrada_do(glossario_de(raiz), "Evento generate_lead")
    assert "Também chamado" not in entrada and "Não confundir" not in entrada


TERMOS_YAML = """termos:
  - termo: linha de base
    documento: EVENT-AURORA-GENERATE-LEAD
    resumo: "Comportamento normal do evento numa operação."
    sinonimos: []
    nao_confundir: ["um dia isolado em zero"]
"""


def test_glossario_inclui_termos_do_kit_com_a_versao_aprovada_vigente(raiz):
    escrever(raiz / "src/kit/kit.yaml", KIT_YAML + TERMOS_YAML)
    texto = glossario_de(raiz)
    assert termos_do(texto) == ["Evento generate_lead", "linha de base", "Taxa de conversão"]
    entrada = entrada_do(texto, "linha de base")
    assert "Comportamento normal do evento numa operação." in entrada
    assert "**Não confundir com:** um dia isolado em zero" in entrada
    assert "**Fonte:** `EVENT-AURORA-GENERATE-LEAD@1.1`" in entrada


@pytest.mark.parametrize("troca, trecho", [
    ("documento: EVENT-AURORA-GENERATE-LEAD", "documento: EVENT-INEXISTENTE"),
    ("documento: EVENT-AURORA-GENERATE-LEAD", "documento: QA-AURORA-001"),
    ('resumo: "Comportamento normal do evento numa operação."', 'resumo: ""'),
    ("termo: linha de base", "termo: Taxa de conversão"),
])
def test_termo_do_kit_invalido_gera_erro(raiz, troca, trecho):
    escrever(raiz / "src/kit/kit.yaml", KIT_YAML + TERMOS_YAML.replace(troca, trecho))
    relatorio, _ = rodar(raiz)
    assert any("termo" in e for e in relatorio.erros)


# ---------- zip ----------
def entradas_do_zip(caminho: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(caminho) as z:
        return {n: z.read(n) for n in z.namelist()}


def test_zip_tem_os_mesmos_arquivos_do_kit_sob_o_prefixo(raiz):
    rodar(raiz)
    entradas = entradas_do_zip(raiz / "public/downloads/kit/contexto-kit-agentes.zip")
    esperado = {f"contexto-kit-agentes/{k}": v for k, v in instantaneo(raiz / KIT).items()}
    assert entradas == esperado
    assert list(entradas) == sorted(entradas)


def test_zip_com_metadados_fixos(raiz):
    rodar(raiz)
    with zipfile.ZipFile(raiz / "public/downloads/kit/contexto-kit-agentes.zip") as z:
        for info in z.infolist():
            assert info.date_time == (1980, 1, 1, 0, 0, 0)
            assert info.compress_type == zipfile.ZIP_STORED
            assert (info.external_attr >> 16) & 0o777 == 0o644


def test_zip_deterministico(tmp_path):
    a, b = montar(tmp_path / "a"), montar(tmp_path / "b")
    rodar(a)
    rodar(b)
    assert (a / "public/downloads/kit/contexto-kit-agentes.zip").read_bytes() == (b / "public/downloads/kit/contexto-kit-agentes.zip").read_bytes()


# ---------- executar: escrita, --check, órfãos ----------
def test_segunda_execucao_nao_reescreve_nada(raiz):
    rodar(raiz)
    antes = {p: p.stat().st_mtime_ns for p in publicado(raiz).rglob("*") if p.is_file()}
    for p in antes:
        os.utime(p, ns=(10**9, 10**9))
    rodar(raiz)
    assert {p: p.stat().st_mtime_ns for p in antes} == {p: 10**9 for p in antes}


def test_check_aprova_depois_de_gerar(raiz):
    rodar(raiz)
    relatorio, _ = rodar(raiz, check=True)
    assert relatorio.erros == []


def test_check_nao_escreve_nada(raiz):
    relatorio, _ = rodar(raiz, check=True)
    assert relatorio.erros
    assert not (raiz / "public/schemas").exists() and not (raiz / "public/documentos").exists()


def test_check_acusa_arquivo_desatualizado(raiz):
    rodar(raiz)
    (raiz / "public/documentos/KPI-AURORA-001@2.0.md").write_text("velho\n", encoding="utf-8")
    relatorio, _ = rodar(raiz, check=True)
    assert any("KPI-AURORA-001@2.0.md" in e and "desatualizado" in e for e in relatorio.erros)


def test_check_acusa_arquivo_ausente(raiz):
    rodar(raiz)
    (raiz / "public/schemas/1.1.0/kpi.schema.json").unlink()
    relatorio, _ = rodar(raiz, check=True)
    assert any("kpi.schema.json" in e and "ausente" in e for e in relatorio.erros)


@pytest.mark.parametrize("orfao", ["public/schemas/1.1.0/velho.schema.json", "public/documentos/X-Y@1.0.md",
                                   f"{KIT}/contratos/sobra.md"])
def test_check_acusa_orfao_e_gerar_remove(raiz, orfao):
    rodar(raiz)
    escrever(raiz / orfao, "sobra\n")
    relatorio, _ = rodar(raiz, check=True)
    assert any(Path(orfao).name in e and "órfão" in e for e in relatorio.erros)
    assert (raiz / orfao).exists()
    rodar(raiz)
    assert not (raiz / orfao).exists()


def test_orfao_de_versao_de_schema_removida_leva_a_pasta_vazia_junto(raiz):
    rodar(raiz)
    escrever(raiz / "public/schemas/0.9.0/kpi.schema.json", "{}\n")
    rodar(raiz)
    assert not (raiz / "public/schemas/0.9.0").exists()


def test_com_erro_nada_e_escrito_nem_removido(raiz):
    rodar(raiz)
    escrever(raiz / "public/documentos/sobra@1.0.md", "x\n")
    escrever(raiz / "src/kit/AGENTS.md", "sem marcador\n")
    relatorio, _ = rodar(raiz)
    assert relatorio.erros
    assert (raiz / "public/documentos/sobra@1.0.md").exists()


def test_downloads_fora_do_kit_nao_sao_tocados(raiz):
    rodar(raiz)
    assert (raiz / "public/downloads/aurora-fixture.sql").read_text(encoding="utf-8") == "select 1;\n"


def test_main_com_raiz_e_check(raiz, capsys):
    g.main(["--raiz", str(raiz)])
    g.main(["--raiz", str(raiz), "--check"])
    assert capsys.readouterr().out.count("OK") == 2


def test_main_check_termina_com_codigo_1_e_linha_erro(raiz, capsys):
    with pytest.raises(SystemExit) as saida:
        g.main(["--raiz", str(raiz), "--check"])
    assert saida.value.code == 1
    assert "ERRO:" in capsys.readouterr().out


# ---------- llms.txt ----------
CONFIG = """export default defineConfig({
  integrations: [
    starlight({
      title: 'Contexto',
      description: 'Promessa do portal.',
      sidebar: [
        { label: 'Comece aqui', items: ['fundamentos/comece'] },
        { label: 'Consultar', items: ['metodo/x', 'referencias', 'sobre/creditos'] }
      ]
    })
  ]
});
"""


def montar_portal(raiz: Path) -> None:
    escrever(raiz / "astro.config.mjs", CONFIG)
    docs = raiz / "src/content/docs"
    escrever(docs / "fundamentos/comece.mdx", "---\ntitle: Comece em 5 minutos\ndescription: Primeiro passo.\n---\nCorpo\n")
    escrever(docs / "metodo/x.md", "---\ntitle: Método X\n---\nCorpo\n")
    escrever(docs / "referencias/index.mdx", "---\ntitle: Referências\ndescription: Lista de consulta.\n---\nCorpo\n")
    escrever(docs / "sobre/creditos.mdx", "---\ntitle: Créditos\ndescription: Quem fez.\n---\nCorpo\n")


def test_llms_txt_segue_o_menu_e_aponta_para_as_saidas(raiz):
    montar_portal(raiz)
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []
    texto = (raiz / "public/llms.txt").read_text(encoding="utf-8")
    assert texto.startswith("# Contexto\n\n> Promessa do portal.\n\n")
    assert f"## Comece aqui\n\n- [Comece em 5 minutos]({SITE}/fundamentos/comece/): Primeiro passo.\n" in texto
    assert f"- [Método X]({SITE}/metodo/x/)\n" in texto
    para_agentes = texto.split("## Para agentes")[1].split("## Optional")[0]
    assert f"{SITE}/downloads/kit/contexto-kit-agentes.zip" in para_agentes
    assert f"{SITE}/documentos/indice.json" in para_agentes
    assert ("AGENTS.md, glossário, contratos, gabaritos e as Skills do kit (auditoria de coleta, descoberta, "
            "consulta e importação do plano de mensuração).") in para_agentes
    assert f"{SITE}/schemas/1.1.0/common.schema.json" in para_agentes
    opcional = texto.split("## Optional")[1]
    assert f"[Referências]({SITE}/referencias/): Lista de consulta." in opcional
    assert f"[Créditos]({SITE}/sobre/creditos/): Quem fez." in opcional
    assert "Créditos" not in texto.split("## Para agentes")[0]


def test_llms_txt_com_pagina_do_menu_inexistente_gera_erro(raiz):
    montar_portal(raiz)
    (raiz / "src/content/docs/metodo/x.md").unlink()
    relatorio, _ = rodar(raiz)
    assert any("metodo/x" in e for e in relatorio.erros)


def test_llms_txt_sem_astro_config_nao_e_gerado(raiz):
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []
    assert not (raiz / "public/llms.txt").exists()


def test_check_acusa_llms_txt_desatualizado(raiz):
    montar_portal(raiz)
    rodar(raiz)
    (raiz / "public/llms.txt").write_text("velho\n", encoding="utf-8")
    relatorio, _ = rodar(raiz, check=True)
    assert any("llms.txt" in e and "desatualizado" in e for e in relatorio.erros)


# ---------- arquivos estáticos, ressalva, versão alvo e Skill sem registro ----------
SKILLS_DIR = "src/kit/skills"


def test_arquivo_estatico_da_skill_vai_para_o_kit_e_para_o_zip(raiz):
    escrever(raiz / SKILLS_DIR / "auditar-coleta/references/x.md", "# Estático\n")
    escrever(raiz / SKILLS_DIR / "auditar-coleta/assets/modelo/y.txt", "y\n")
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []
    kit_ = instantaneo(raiz / KIT)
    assert kit_["skills/auditar-coleta/references/x.md"] == "# Estático\n".encode()
    assert kit_["skills/auditar-coleta/assets/modelo/y.txt"] == b"y\n"
    zip_ = entradas_do_zip(raiz / "public/downloads/kit/contexto-kit-agentes.zip")
    assert "contexto-kit-agentes/skills/auditar-coleta/references/x.md" in zip_
    assert "contexto-kit-agentes/skills/auditar-coleta/assets/modelo/y.txt" in zip_
    texto = (raiz / KIT / "AGENTS.md").read_text(encoding="utf-8")
    assert "- [Referência da Skill `auditar-coleta`: references/x.md](skills/auditar-coleta/references/x.md)" in texto


def test_arquivo_estatico_com_caminho_de_referencia_gerada_gera_erro(raiz):
    escrever(raiz / SKILLS_DIR / "auditar-coleta/references/EVENT-AURORA-GENERATE-LEAD@1.1.md", "# Outro\n")
    relatorio, _ = rodar(raiz)
    assert any("EVENT-AURORA-GENERATE-LEAD@1.1.md" in e and "mesmo caminho" in e for e in relatorio.erros)


def test_link_do_skill_para_arquivo_estatico_passa(raiz):
    escrever(raiz / SKILLS_DIR / "auditar-coleta/references/x.md", "# Estático\n")
    escrever(raiz / SKILLS_DIR / "auditar-coleta/SKILL.md", SKILL + "\n[x](references/x.md)\n")
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []


def test_link_do_skill_para_estatico_inexistente_gera_erro(raiz):
    escrever(raiz / SKILLS_DIR / "auditar-coleta/SKILL.md", SKILL + "\n[x](references/x.md)\n")
    relatorio, _ = rodar(raiz)
    assert any("references/x.md" in e for e in relatorio.erros)


def corpo_da_skill(extra: str) -> str:
    return f"---\nname: auditar-coleta\ndescription: ok\n---\n# Corpo\n\n{extra}"


@pytest.mark.parametrize("extra,trecho", [
    ("Versão alvo: x.\n", "ressalva"),
    (kit.FRASE_DA_RESSALVA + "\n", "Versão alvo:"),
    ("", "ressalva"),
])
def test_skill_sem_ressalva_ou_sem_versao_alvo_gera_erro(raiz, extra, trecho):
    escrever(raiz / SKILLS_DIR / "auditar-coleta/SKILL.md", corpo_da_skill(extra))
    relatorio, _ = rodar(raiz)
    assert any("SKILL.md" in e and trecho in e for e in relatorio.erros)


def test_skill_com_ressalva_e_versao_alvo_passa(raiz):
    escrever(raiz / SKILLS_DIR / "auditar-coleta/SKILL.md", corpo_da_skill(RESSALVA))
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []


def test_frase_da_ressalva_e_a_da_auditar_coleta_real():
    real = (g.ROOT if hasattr(g, "ROOT") else Path(__file__).resolve().parents[2]) / "src/kit/skills/auditar-coleta/SKILL.md"
    assert kit.FRASE_DA_RESSALVA in real.read_text(encoding="utf-8")


def test_skill_sem_entrada_no_kit_yaml_gera_erro(raiz):
    escrever(raiz / SKILLS_DIR / "nova-skill/SKILL.md", SKILL.replace("auditar-coleta", "nova-skill"))
    relatorio, _ = rodar(raiz)
    assert any("skill nova-skill sem entrada em src/kit/kit.yaml" in e for e in relatorio.erros)


def test_skill_com_lista_vazia_no_kit_yaml_e_aceita(raiz):
    escrever(raiz / "src/kit/kit.yaml", KIT_YAML + "  nova-skill: []\n")
    escrever(raiz / SKILLS_DIR / "nova-skill/SKILL.md", SKILL.replace("auditar-coleta", "nova-skill").replace("Leia [o evento](references/EVENT-AURORA-GENERATE-LEAD@1.1.md).", ""))
    relatorio, _ = rodar(raiz)
    assert relatorio.erros == []
    assert "skills/nova-skill/SKILL.md" in instantaneo(raiz / KIT)
