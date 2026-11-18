"""Testes de check_schemas, com schemas e fontes de mentira em tmp_path."""
import json
import re
from pathlib import Path

import pytest

import comum
import check_schemas as cs
from enderecos import url_do_documento

COMUM = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "urn:contexto:schemas:1.0.0:common",
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "schema_version": {"enum": ["1.0.0", "1.1.0"]},
        "license": {"type": ["string", "null"]},
        "source_url": {"type": ["string", "null"]},
        "type": {"type": "string"},
        "title": {"type": "string"},
        "status": {"enum": sorted(comum.ESTADOS_DO_DOCUMENTO)},
        "valid_from": {"type": ["string", "null"], "format": "date"},
        "recorded_at": {"type": "string", "format": "date"},
        "intent": {"type": "object", "properties": {"question": {"type": "string"}}},
    },
}
KPI = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "urn:contexto:schemas:1.0.0:kpi",
    "allOf": [{"$ref": "urn:contexto:schemas:1.0.0:common"}],
    "required": ["id", "type"],
}
MODELOS_YAML = "tipos:\n  - slug: kpi\n    pagina: kpi\n    nome: K\n    nivel: nucleo\n    tarefa: t\n    resumo: r\n    quando: q\n    resultado: r\n    preparar: p\n    rotulo_download: R\n"
CAMPOS = "cabecalho:\n  - {chave: id, rotulo: I, obrigatorio: true, descricao: d}\n  - {chave: type, rotulo: T, obrigatorio: true, descricao: d}\n  - {chave: intent.question, rotulo: P, obrigatorio: false, descricao: d}\n"
CABECALHO = [k for k in comum.HEADER_ORDER if k != "recorded_at"]


def fonte_do_modelo() -> str:
    valores = {"id": "KPI-MODELO", "schema_version": '"1.0.0"', "type": "kpi", "title": "Um", "status": "draft",
               "valid_from": "2026-01-02", "intent": "{question: Q}"}
    return "---\n" + "\n".join(f"{k}: {valores.get(k, 'null')}" for k in CABECALHO) + "\n---\ncorpo\n"


def montar(raiz: Path, comum_: dict = COMUM, kpi: dict = KPI) -> Path:
    for pasta in ("schemas", "src/modelos", "src/exemplos/historico", "src/data"):
        (raiz / pasta).mkdir(parents=True, exist_ok=True)
    (raiz / "schemas/common.schema.json").write_text(json.dumps(comum_), encoding="utf-8")
    (raiz / "schemas/kpi.schema.json").write_text(json.dumps(kpi), encoding="utf-8")
    (raiz / "src/data/modelos.yaml").write_text(MODELOS_YAML, encoding="utf-8")
    (raiz / "src/data/campos.yaml").write_text(CAMPOS, encoding="utf-8")
    (raiz / "src/modelos/kpi.md").write_text(fonte_do_modelo(), encoding="utf-8")
    (raiz / "src/exemplos/exemplo-kpi-completo.md").write_text(
        "---\n# aviso\nid: KPI-A-001\nschema_version: \"1.1.0\"\ntype: kpi\nversion: \"1.0\"\nvalid_from: 2026-09-15\n"
        f"license: CC-BY-4.0\nsource_url: {url_do_documento('KPI-A-001', '1.0')}\nintent:\n  question: Q?\n---\ncorpo\n", encoding="utf-8")
    (raiz / "src/exemplos/historico/exemplo-kpi-v1.0.md").write_text(
        "---\nid: KPI-A-001\nschema_version: \"1.1.0\"\ntype: kpi\nversion: \"1.0\"\nstatus: superseded\nrecorded_at: 2026-10-01\n"
        f"license: CC-BY-4.0\nsource_url: {url_do_documento('KPI-A-001', '1.0')}\n---\ncorpo\n", encoding="utf-8")
    return raiz


def erros(raiz: Path) -> list[str]:
    return cs.executar(raiz)[0].erros


def test_fontes_validas_passam(tmp_path: Path):
    montar(tmp_path)
    relatorio, modelos, exemplos = cs.executar(tmp_path)
    assert relatorio.erros == []
    assert (modelos, exemplos) == (1, 2)


def test_mensagem_final(tmp_path: Path):
    montar(tmp_path)
    assert cs.mensagem_ok(1, 2) == "OK: 1 modelos e 2 exemplos válidos no JSON Schema 1.1.0, cabeçalho na ordem"


def test_erro_de_schema_sai_com_arquivo_caminho_e_mensagem(tmp_path: Path):
    montar(tmp_path)
    arq = tmp_path / "src/exemplos/exemplo-kpi-completo.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace("id: KPI-A-001", "id: 7"), encoding="utf-8")
    achados = erros(tmp_path)
    assert any("exemplo-kpi-completo.md: id: " in e and "string" in e for e in achados), achados


def test_caminho_aninhado_usa_pontos(tmp_path: Path):
    montar(tmp_path)
    arq = tmp_path / "src/exemplos/exemplo-kpi-completo.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace("question: Q?", "question: 3"), encoding="utf-8")
    assert any(": intent.question: " in e for e in erros(tmp_path))


def test_data_do_yaml_e_convertida_e_validada_como_format_date(tmp_path: Path):
    montar(tmp_path)  # valid_from: 2026-09-15 é datetime.date no YAML e deve passar
    assert erros(tmp_path) == []
    arq = tmp_path / "src/exemplos/exemplo-kpi-completo.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace("valid_from: 2026-09-15", 'valid_from: "15/09/2026"'), encoding="utf-8")
    assert any("valid_from" in e for e in erros(tmp_path))


def test_schema_invalido_vira_erro_sem_traceback(tmp_path: Path):
    montar(tmp_path, kpi={**KPI, "type": 12})
    assert any("kpi.schema.json" in e and "schema inválido" in e for e in erros(tmp_path))


def test_json_quebrado_vira_erro(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "schemas/kpi.schema.json").write_text("{quebrado", encoding="utf-8")
    assert any("kpi.schema.json" in e and "JSON inválido" in e for e in erros(tmp_path))


def test_ref_nao_resolvida_vira_erro(tmp_path: Path):
    montar(tmp_path, kpi={**KPI, "allOf": [{"$ref": "urn:contexto:schemas:1.0.0:nao-existe"}]})
    assert any("kpi.schema.json" in e or "exemplo" in e for e in erros(tmp_path))


def test_frontmatter_ausente_vira_erro(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "src/exemplos/exemplo-kpi-completo.md").write_text("sem\n", encoding="utf-8")
    assert any("frontmatter ausente" in e for e in erros(tmp_path))


# ---------- ordem ----------

def test_ordem_certa_nao_acusa():
    assert cs.erros_de_ordem(["id", "type", "title", "intent", "kpi_campo"], exigir_todas=False) == []


def test_chave_do_cabecalho_fora_de_ordem_e_acusada():
    achados = cs.erros_de_ordem(["type", "id", "title"], exigir_todas=False)
    assert achados and "id" in achados[0] and "type" in achados[0]


def test_chave_de_outro_tipo_antes_do_cabecalho_e_acusada():
    achados = cs.erros_de_ordem(["id", "formula", "title"], exigir_todas=False)
    assert any("formula" in a and "title" in a for a in achados)


def test_modelo_precisa_de_todas_as_chaves_menos_recorded_at():
    achados = cs.erros_de_ordem([k for k in CABECALHO if k != "intent"], exigir_todas=True)
    assert any("intent" in a and "falta" in a for a in achados)
    assert cs.erros_de_ordem(CABECALHO, exigir_todas=True) == []


def test_arquivo_com_ordem_errada_sai_no_relatorio(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "src/exemplos/exemplo-kpi-completo.md").write_text(
        "---\ntype: kpi\nid: KPI-A\n---\ncorpo\n", encoding="utf-8")
    assert any("exemplo-kpi-completo.md" in e and "ordem" in e for e in erros(tmp_path))


# ---------- type e arquivos ----------

def test_type_diferente_do_nome_do_modelo_e_acusado(tmp_path: Path):
    montar(tmp_path)
    arq = tmp_path / "src/modelos/kpi.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace("type: kpi", "type: dataset"), encoding="utf-8")
    assert any("kpi.md" in e and "type" in e for e in erros(tmp_path))


def test_exemplo_com_nome_de_outro_tipo_e_acusado(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "src/exemplos/exemplo-dataset-completo.md").write_text(
        "---\nid: X\ntype: kpi\n---\ncorpo\n", encoding="utf-8")
    assert any("exemplo-dataset-completo.md" in e and "exemplo-kpi-" in e for e in erros(tmp_path))


def test_slug_sem_schema_ou_modelo_e_acusado(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "schemas/kpi.schema.json").unlink()
    (tmp_path / "src/modelos/kpi.md").unlink()
    achados = erros(tmp_path)
    assert any("schemas/kpi.schema.json" in e and "kpi" in e for e in achados)
    assert any("src/modelos/kpi.md" in e for e in achados)


def test_schema_e_modelo_sem_slug_sao_acusados(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "schemas/sobra.schema.json").write_text(json.dumps({"$id": "urn:contexto:schemas:1.0.0:sobra"}), encoding="utf-8")
    (tmp_path / "src/modelos/sobra.md").write_text("---\nid: x\ntype: sobra\n---\n", encoding="utf-8")
    achados = erros(tmp_path)
    assert any("sobra.schema.json" in e and "modelos.yaml" in e for e in achados)
    assert any("src/modelos/sobra.md" in e and "modelos.yaml" in e for e in achados)


# ---------- campos.yaml ----------

def test_campos_fora_da_ordem_do_cabecalho(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "src/data/campos.yaml").write_text(
        "cabecalho:\n  - {chave: type, rotulo: T, obrigatorio: true, descricao: d}\n  - {chave: id, rotulo: I, obrigatorio: true, descricao: d}\n", encoding="utf-8")
    assert any("campos.yaml" in e and "ordem" in e for e in erros(tmp_path))


def test_campos_com_chave_inexistente_no_comum(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "src/data/campos.yaml").write_text(
        "cabecalho:\n  - {chave: id, rotulo: I, obrigatorio: true, descricao: d}\n  - {chave: version, rotulo: V, obrigatorio: false, descricao: d}\n", encoding="utf-8")
    assert any("campos.yaml" in e and "version" in e and "common.schema.json" in e for e in erros(tmp_path))


def test_campos_chave_com_ponto_usa_a_parte_antes_do_ponto():
    assert cs.erros_de_campos([{"chave": "id", "obrigatorio": True}, {"chave": "intent.question", "obrigatorio": False}],
                              {"id", "intent"}) == []


def test_campos_varias_chaves_do_mesmo_bloco_seguidas_mantem_a_ordem():
    itens = [{"chave": c, "obrigatorio": False} for c in
             ("id", "intent.question", "intent.audience", "intent.purpose", "plain_summary")]
    assert cs.erros_de_campos(itens, {"id", "intent", "plain_summary"}) == []


def test_campos_mesmo_bloco_separado_por_outra_chave_fica_fora_da_ordem():
    itens = [{"chave": c, "obrigatorio": False} for c in
             ("id", "intent.question", "plain_summary", "intent.purpose")]
    assert any("ordem" in e for e in cs.erros_de_campos(itens, {"id", "intent", "plain_summary"}))


def test_campos_com_mais_de_oito_obrigatorios(tmp_path: Path):
    itens = [{"chave": k, "obrigatorio": True} for k in comum.HEADER_ORDER[:9]]
    achados = cs.erros_de_campos(itens, set(comum.HEADER_ORDER))
    assert any("8" in a and "obrigat" in a for a in achados)
    assert cs.erros_de_campos(itens[:8], set(comum.HEADER_ORDER)) == []


def test_campos_ausente_vira_erro(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "src/data/campos.yaml").write_text("x: 1\n", encoding="utf-8")
    assert any("campos.yaml" in e and "cabecalho" in e for e in erros(tmp_path))


def _validador_do_context_real():
    from jsonschema import Draft202012Validator
    real = json.loads((comum.ROOT / "schemas" / "common.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(real["properties"]["context"])


def test_context_real_aceita_itens_no_formato_do_odcs():
    validador = _validador_do_context_real()
    context = {
        "instructions": "Use só pedidos pagos.",
        "verifiedStatements": [{"question": "Qual a conversão de setembro?", "answer": "2,1%"}, {"question": "Só a pergunta?"}],
        "constraints": [{"constraint": "Não compare períodos de regras diferentes."}],
    }
    assert list(validador.iter_errors(context)) == []


@pytest.mark.parametrize("context", [
    {"verifiedStatements": ["frase solta"]},
    {"verifiedStatements": [{"answer": "sem pergunta"}]},
    {"constraints": ["limite em texto solto"]},
    {"constraints": [{"texto": "chave errada"}]},
])
def test_context_real_recusa_itens_fora_do_formato_do_odcs(context: dict):
    assert list(_validador_do_context_real().iter_errors(context)) != []


def test_exemplo_yaml_do_contrato_segue_a_ordem_do_cabecalho():
    import yaml
    contrato = (comum.ROOT / "docs" / "CONTRATO_EDITORIAL.md").read_text(encoding="utf-8")
    blocos = [b for b in re.findall(r"```yaml\n(.*?)```", contrato, re.S) if "schema_version" in b]
    assert blocos, "o contrato perdeu o exemplo YAML do cabeçalho"
    for bloco in blocos:
        assert cs.erros_de_ordem(list(yaml.safe_load(bloco)), exigir_todas=False) == []


# ---------- schema 1.1.0 (aditivo) com os schemas reais ----------

def _kpi_completo() -> dict:
    lido = comum.ler_frontmatter(comum.ROOT / "src/exemplos/exemplo-kpi-completo.md", comum.Relatorio())
    assert lido is not None
    return lido[0]


def _erros_reais(dados: dict) -> list[str]:
    relatorio = comum.Relatorio()
    schemas = cs._carregar_schemas(comum.ROOT / "schemas", relatorio)
    validador = cs.Draft202012Validator(schemas["kpi"], registry=cs._registro(schemas), format_checker=cs.FormatChecker())
    return [e.message for e in validador.iter_errors(cs.para_json(dados))]


def test_documento_1_0_0_sem_license_nem_source_url_continua_valido():
    dados = {k: v for k, v in _kpi_completo().items() if k not in ("license", "source_url")}
    assert _erros_reais({**dados, "schema_version": "1.0.0"}) == []


def test_documento_1_1_0_completo_e_valido_e_versao_desconhecida_falha():
    dados = _kpi_completo()
    assert _erros_reais(dados) == []
    assert _erros_reais({**dados, "schema_version": "2.0.0"}) != []


def test_kpi_com_license_valida_passa_apesar_de_unevaluated_properties_false():
    assert _erros_reais({**_kpi_completo(), "license": "CC-BY-4.0"}) == []


@pytest.mark.parametrize("campo, valor", [("license", "CC BY 4.0"), ("license", ""), ("source_url", "http://x.org/a.md"),
                                          ("source_url", "x.org/a.md"), ("license", 3)])
def test_license_com_espaco_ou_source_url_sem_https_falham(campo: str, valor):
    assert _erros_reais({**_kpi_completo(), campo: valor}) != []


def test_schemas_so_lidos_no_nivel_de_schemas():
    """O 1.0.0 congelado fica em schemas/historico e não entra no glob dos validadores."""
    relatorio = comum.Relatorio()
    achados = cs._carregar_schemas(comum.ROOT / "schemas", relatorio)
    assert relatorio.erros == [] and "common" in achados and len(achados) == 12
    assert all(s["$id"].startswith("urn:contexto:schemas:1.1.0:") for s in achados.values())


# ---------- erros_de_publicacao ----------

def test_publicacao_modelo_exige_license_e_source_url_nulos():
    assert cs.erros_de_publicacao({"license": None, "source_url": None}, modelo=True) == []
    achados = cs.erros_de_publicacao({"license": "CC-BY-4.0", "source_url": "https://x.org/a.md"}, modelo=True)
    assert len(achados) == 2 and "license" in achados[0] and "source_url" in achados[1]
    assert len(cs.erros_de_publicacao({}, modelo=True)) == 2


def test_publicacao_exemplo_confere_versao_license_e_url():
    dados = {"id": "KPI-AURORA-001", "version": "2.0", "schema_version": "1.1.0", "license": "CC-BY-4.0",
             "source_url": "https://edoardolobl.github.io/contexto-framework/documentos/KPI-AURORA-001@2.0.md"}
    assert cs.erros_de_publicacao(dados, modelo=False) == []
    achados = cs.erros_de_publicacao({**dados, "source_url": "https://outro.org/x.md", "license": None,
                                      "schema_version": "1.0.0"}, modelo=False)
    assert len(achados) == 3
    assert any("documentos/KPI-AURORA-001@2.0.md" in a and "source_url" in a for a in achados)
    assert any("license" in a and "CC-BY-4.0" in a for a in achados)
    assert any("schema_version" in a and "1.1.0" in a for a in achados)


def test_publicacao_exemplo_sem_id_valido_vira_erro_e_nao_excecao():
    achados = cs.erros_de_publicacao({"id": "x", "version": "2.0", "schema_version": "1.1.0",
                                      "license": "CC-BY-4.0", "source_url": None}, modelo=False)
    assert achados and any("source_url" in a for a in achados)


HISTORICA_1_0_0 = {"id": "KPI-AURORA-001", "version": "1.0", "schema_version": "1.0.0", "status": "superseded",
                   "recorded_at": "2026-10-01"}


def test_publicacao_copia_historica_1_0_0_fica_como_foi_aprovada():
    assert cs.erros_de_publicacao(HISTORICA_1_0_0, modelo=False) == []


def test_publicacao_copia_historica_1_0_0_nao_ganha_license_nem_source_url():
    achados = cs.erros_de_publicacao({**HISTORICA_1_0_0, "license": "CC-BY-4.0",
                                      "source_url": url_do_documento("KPI-AURORA-001", "1.0")}, modelo=False)
    assert len(achados) == 2
    assert all("1.0.0" in a for a in achados)


def test_publicacao_1_0_0_so_vale_para_copia_historica():
    sem_recorded_at = {k: v for k, v in HISTORICA_1_0_0.items() if k != "recorded_at"}
    assert any("schema_version" in a for a in cs.erros_de_publicacao(sem_recorded_at, modelo=False))
    vigente = {**HISTORICA_1_0_0, "status": "approved"}
    assert any("schema_version" in a for a in cs.erros_de_publicacao(vigente, modelo=False))


def test_executar_aceita_copia_historica_intacta_na_1_0_0(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "src/exemplos/historico/exemplo-kpi-v1.0.md").write_text(
        "---\nid: KPI-A-001\nschema_version: \"1.0.0\"\ntype: kpi\nversion: \"1.0\"\nstatus: superseded\n"
        "recorded_at: 2026-10-01\n---\ncorpo\n", encoding="utf-8")
    assert erros(tmp_path) == []


def test_executar_acusa_source_url_errado_no_exemplo(tmp_path: Path):
    montar(tmp_path)
    arq = tmp_path / "src/exemplos/exemplo-kpi-completo.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace(url_do_documento("KPI-A-001", "1.0"), "https://x.org/a.md"),
                   encoding="utf-8")
    assert any("source_url" in e and "documentos/KPI-A-001@1.0.md" in e for e in erros(tmp_path))


# ---------- also_accepted nas perguntas de negócio (ADR 0021, QA-AURORA-002@1.1) ----------

def _perguntas_reais() -> dict:
    import copy
    lido = comum.ler_frontmatter(comum.ROOT / "src/exemplos/exemplo-perguntas-de-negocio-eventos-completo.md", comum.Relatorio())
    assert lido is not None
    return copy.deepcopy(lido[0])


def _erros_do_schema_de_perguntas(dados: dict) -> list[str]:
    relatorio = comum.Relatorio()
    schemas = cs._carregar_schemas(comum.ROOT / "schemas", relatorio)
    validador = cs.Draft202012Validator(schemas["perguntas-de-negocio"], registry=cs._registro(schemas),
                                        format_checker=cs.FormatChecker())
    return [e.message for e in validador.iter_errors(cs.para_json(dados))]


def _com_also_accepted(valor) -> dict:
    dados = _perguntas_reais()
    pergunta = next(q for q in dados["questions"] if q["id"] == "Q03")
    pergunta["also_accepted"] = valor
    return dados


def test_also_accepted_valido_passa_no_schema():
    valor = [{"behavior": "answer", "condition": "avalia Brasil e México"}]
    assert _erros_do_schema_de_perguntas(_com_also_accepted(valor)) == []


def test_pergunta_sem_also_accepted_continua_valida():
    assert _erros_do_schema_de_perguntas(_perguntas_reais()) == []


@pytest.mark.parametrize("valor", [
    [{"behavior": "guess", "condition": "x"}],
    [{"behavior": None, "condition": "x"}],
    [{"behavior": "answer", "condition": ""}],
    [{"behavior": "answer", "condition": None}],
    [{"behavior": "answer"}],
    [{"condition": "x"}],
    [{"behavior": "answer", "condition": "x", "extra": 1}],
    {"behavior": "answer", "condition": "x"},
    ["answer"],
])
def test_also_accepted_invalido_falha_no_schema(valor):
    assert _erros_do_schema_de_perguntas(_com_also_accepted(valor)) != []


def test_also_accepted_com_comportamento_diferente_do_esperado_passa_na_checagem_semantica():
    dados = _com_also_accepted([{"behavior": "answer", "condition": "x"}])
    assert cs.erros_de_perguntas(dados) == []


def test_also_accepted_repetindo_o_expected_behavior_e_acusado():
    dados = _com_also_accepted([{"behavior": "clarify", "condition": "x"}])
    erros_ = cs.erros_de_perguntas(dados)
    assert len(erros_) == 1 and "Q03" in erros_[0] and "clarify" in erros_[0]


def test_checagem_semantica_ignora_perguntas_sem_also_accepted_e_listas_malformadas():
    assert cs.erros_de_perguntas({"questions": [{"id": "Q1", "expected_behavior": "answer"}]}) == []
    assert cs.erros_de_perguntas({"questions": "x"}) == []
    assert cs.erros_de_perguntas({}) == []
    assert cs.erros_de_perguntas({"questions": [{"id": "Q1", "expected_behavior": "answer", "also_accepted": "x"}]}) == []


def test_executar_acusa_also_accepted_repetido_no_exemplo(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "schemas/perguntas-de-negocio.schema.json").write_text(json.dumps(
        {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "urn:contexto:schemas:1.0.0:perguntas-de-negocio",
         "allOf": [{"$ref": "urn:contexto:schemas:1.0.0:common"}]}), encoding="utf-8")
    (tmp_path / "src/data/modelos.yaml").write_text(
        MODELOS_YAML + MODELOS_YAML.split("tipos:\n")[1].replace("kpi", "perguntas-de-negocio"), encoding="utf-8")
    (tmp_path / "src/modelos/perguntas-de-negocio.md").write_text(
        fonte_do_modelo().replace("type: kpi", "type: perguntas-de-negocio"), encoding="utf-8")
    (tmp_path / "src/exemplos/exemplo-perguntas-de-negocio-completo.md").write_text(
        "---\nid: QA-A-001\nschema_version: \"1.1.0\"\ntype: perguntas-de-negocio\nversion: \"1.0\"\nvalid_from: 2026-09-15\n"
        f"license: CC-BY-4.0\nsource_url: {url_do_documento('QA-A-001', '1.0')}\nintent:\n  question: Q?\n"
        "questions:\n  - id: Q01\n    expected_behavior: clarify\n    also_accepted:\n      - {behavior: clarify, condition: x}\n---\ncorpo\n",
        encoding="utf-8")
    assert any("Q01" in e and "also_accepted" in e for e in erros(tmp_path))


# ---------- rótulos de campos do tipo em src/data/campos.yaml (ADR 0015, ADR 0030) ----------

SCHEMA_DE_TIPO = {
    "properties": {
        "dataset": {"type": "object", "properties": {"physicalName": {"title": "Nome físico"}}},
        "columns": {"type": "array", "items": {"type": "object", "properties": {"businessName": {"title": "Nome de negócio"}}}},
    }
}


def test_titulo_do_campo_segue_pontos_e_colchetes():
    assert cs.titulo_do_campo(SCHEMA_DE_TIPO, "dataset.physicalName") == "Nome físico"
    assert cs.titulo_do_campo(SCHEMA_DE_TIPO, "columns[].businessName") == "Nome de negócio"


def test_titulo_do_campo_inexistente_e_none():
    assert cs.titulo_do_campo(SCHEMA_DE_TIPO, "columns[].physical_name") is None
    assert cs.titulo_do_campo(SCHEMA_DE_TIPO, "dataset[].physicalName") is None


def test_rotulo_igual_ao_titulo_do_schema_passa():
    itens = [{"tipo": "dataset", "chave": "dataset.physicalName", "rotulo": "Nome físico", "descricao": "x"}]
    assert cs.erros_de_rotulos_do_tipo(itens, {"dataset": SCHEMA_DE_TIPO}) == []


def test_rotulo_diferente_do_titulo_do_schema_e_acusado():
    itens = [{"tipo": "dataset", "chave": "dataset.physicalName", "rotulo": "Tabela", "descricao": "x"}]
    assert any("Nome físico" in e for e in cs.erros_de_rotulos_do_tipo(itens, {"dataset": SCHEMA_DE_TIPO}))


def test_chave_ou_tipo_desconhecido_e_acusado():
    itens = [{"tipo": "dataset", "chave": "columns[].physical_name", "rotulo": "Nome físico", "descricao": "x"},
             {"tipo": "kpi", "chave": "domain", "rotulo": "Domínio", "descricao": "x"}]
    erros = cs.erros_de_rotulos_do_tipo(itens, {"dataset": SCHEMA_DE_TIPO})
    assert any("columns[].physical_name" in e for e in erros)
    assert any("kpi" in e for e in erros)


def test_campos_yaml_real_tem_rotulos_de_also_accepted_e_das_chaves_do_odcs():
    dados = comum.carregar_yaml(comum.ROOT / "src/data/campos.yaml", comum.Relatorio())
    chaves = {(i["tipo"], i["chave"]) for i in dados["campos_do_tipo"]}
    assert ("perguntas-de-negocio", "questions[].also_accepted") in chaves
    assert ("dataset", "columns[].physicalType") in chaves
