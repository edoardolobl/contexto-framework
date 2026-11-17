"""Testes do gerador da referência de campos, com schemas de mentira em tmp_path e a raiz como parâmetro."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

import gerar_referencias as r

MODELOS = """tipos:
  - slug: kpi
    pagina: kpi
    nome: Indicador (KPI)
    nivel: nucleo
    tarefa: Explicar um indicador
    resumo: Fórmula e período.
    quando: Quando há dúvida.
    resultado: Uma definição.
    preparar: O nome do indicador.
    rotulo_download: Modelo de KPI
  - slug: dataset
    pagina: dataset
    nome: Dataset
    nivel: nucleo
    tarefa: Explicar uma tabela
    resumo: Granularidade e chaves.
    quando: Quando colunas confundem.
    resultado: Um dicionário.
    preparar: O schema.
    rotulo_download: Modelo de dataset
"""
CAMPOS = """cabecalho:
  - chave: id
    rotulo: Identificador do assunto
    obrigatorio: true
    descricao: Código estável do assunto.
  - chave: intent.question
    rotulo: Pergunta de negócio
    obrigatorio: false
    descricao: A pergunta que o documento responde.
"""
COMUM = {
    "title": "Cabeçalho comum",
    "properties": {
        "context": {
            "title": "Contexto para agentes (para quem é técnico)",
            "description": "Bloco opcional para agentes.",
            "type": "object",
            "properties": {
                "instructions": {"title": "Instrução ao agente", "description": "Texto curto.", "type": ["string", "null"]},
            },
        },
        "authoritativeDefinitions": {
            "title": "Onde mora a regra executável",
            "description": "Lugares com a regra executável.",
            "type": "array",
            "items": {"$ref": "#/$defs/definicao_oficial"},
        },
    },
    "$defs": {
        "data_ou_nulo": {"title": "Data", "description": "AAAA-MM-DD.", "anyOf": [{"type": "null"}, {"type": "string", "format": "date"}]},
        "definicao_oficial": {
            "type": "object",
            "properties": {"url": {"title": "Endereço", "description": "Onde está a regra.", "type": "string"}},
        },
    },
}
KPI = {
    "title": "Indicador (KPI)",
    "type": "object",
    "properties": {
        "type": {"const": "kpi"},
        "domain": {"title": "Domínio", "description": "Área do negócio.", "type": ["string", "null"]},
        "synonyms": {"title": "Sinônimos", "description": "Nomes iguais.", "type": "array", "items": {"type": "string"}},
        "calculation": {
            "title": "Cálculo",
            "description": "Como calcular.",
            "type": "object",
            "properties": {
                "unit": {"title": "Unidade", "description": "O que se conta.", "type": ["string", "null"]},
            },
        },
        "history_recalculation": {
            "title": "Recálculo",
            "description": "O que fazer com a série.",
            "type": "object",
            "properties": {"policy": {"title": "Política", "description": "Como tratar.", "enum": [None, "recalculate", "method_break"]}},
        },
    },
}
DATASET = {
    "title": "Dataset",
    "type": "object",
    "properties": {
        "type": {"const": "dataset"},
        "columns": {
            "title": "Colunas",
            "description": "Uma entrada por coluna.",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"title": "Nome", "description": "Nome físico.", "type": "string"},
                    "required": {"title": "Obrigatória", "description": "Aceita vazio ou não.", "type": ["boolean", "null"]},
                    "checked_at": {"title": "Conferida em", "description": "Data da conferência.", "$ref": "urn:contexto:schemas:1.0.0:common#/$defs/data_ou_nulo"},
                },
            },
        },
    },
}


def escrever_json(caminho: Path, dados: dict) -> None:
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")


def montar(raiz: Path, kpi: dict = KPI, comum: dict = COMUM) -> Path:
    (raiz / "src" / "data").mkdir(parents=True)
    (raiz / "schemas").mkdir()
    (raiz / "src" / "content" / "docs" / "referencias" / "campos").mkdir(parents=True)
    (raiz / "src" / "data" / "modelos.yaml").write_text(MODELOS, encoding="utf-8")
    (raiz / "src" / "data" / "campos.yaml").write_text(CAMPOS, encoding="utf-8")
    escrever_json(raiz / "schemas" / "common.schema.json", comum)
    escrever_json(raiz / "schemas" / "kpi.schema.json", kpi)
    escrever_json(raiz / "schemas" / "dataset.schema.json", DATASET)
    return raiz


def pagina(raiz: Path, nome: str) -> str:
    return (raiz / "src" / "content" / "docs" / "referencias" / "campos" / nome).read_text(encoding="utf-8")


def instantaneo(pasta: Path) -> dict[str, bytes]:
    return {p.relative_to(pasta).as_posix(): p.read_bytes() for p in sorted(pasta.rglob("*")) if p.is_file()}


class TestValorDoCampo:
    DEFS = COMUM["$defs"]

    @pytest.mark.parametrize(
        ("no", "esperado"),
        [
            ({"type": "string"}, "texto"),
            ({"type": ["string", "null"]}, "texto"),
            ({"type": "array", "items": {"type": "string"}}, "lista de textos"),
            ({"type": "array", "items": {"type": "integer"}}, "lista de números"),
            ({"type": "array"}, "lista"),
            ({"type": "array", "items": {}}, "lista de valores livres"),
            ({"type": "boolean"}, "sim ou não (true ou false)"),
            ({"type": ["boolean", "null"]}, "sim ou não (true ou false)"),
            ({"type": ["integer", "null"]}, "número inteiro"),
            ({"type": ["integer", "number", "null"]}, "número"),
            ({"type": "number"}, "número"),
            ({"type": ["string", "number", "boolean", "null"]}, "texto, número ou sim ou não (true ou false)"),
            ({"enum": [None, "a", "b"]}, "um destes: a, b"),
            ({"type": ["string", "null"], "enum": ["x", "y", None]}, "um destes: x, y"),
            ({"type": "array", "items": {"enum": ["p", "q"]}}, "lista, cada item um destes: p, q"),
            ({"type": "string", "format": "date"}, "data (AAAA-MM-DD)"),
            ({"anyOf": [{"type": "null"}, {"type": "string", "format": "date"}]}, "data (AAAA-MM-DD)"),
            ({"$ref": "urn:contexto:schemas:1.0.0:common#/$defs/data_ou_nulo"}, "data (AAAA-MM-DD)"),
            ({"$ref": "#/$defs/data_ou_nulo"}, "data (AAAA-MM-DD)"),
            ({"type": "object", "properties": {"a": {"type": "string"}}}, "grupo de campos"),
            ({"type": "array", "items": {"type": "object", "properties": {}}}, "lista de grupos de campos"),
            ({"type": "object", "additionalProperties": {"type": "string"}}, "uma entrada por chave, cada uma com texto"),
            ({"type": "object"}, "grupo de chaves livres"),
        ],
    )
    def test_descreve_o_valor_aceito(self, no, esperado):
        assert r.valor_do_campo(no, self.DEFS) == esperado

    @pytest.mark.parametrize(
        "no",
        [
            {"type": "tuple"},
            {"anyOf": [{"type": "string"}, {"type": "integer"}]},
            {"$ref": "urn:outro:schema#/$defs/x"},
            {"$ref": "#/$defs/nao_existe"},
            {"title": "sem forma"},
            "texto solto",
        ],
    )
    def test_estrutura_desconhecida_vira_erro_do_gerador(self, no):
        with pytest.raises(r.ErroDeSchema):
            r.valor_do_campo(no, self.DEFS)


class TestLinhasDeCampos:
    def test_chaves_com_ponto_e_colchetes_em_listas_de_objetos(self):
        linhas = r.linhas_de_campos(DATASET["properties"], COMUM["$defs"])
        chaves = [linha[1].strip("`") for linha in linhas]
        assert chaves == ["columns", "columns[].name", "columns[].required", "columns[].checked_at"]

    def test_type_do_cabecalho_fica_de_fora_e_ordem_e_a_do_schema(self):
        linhas = r.linhas_de_campos(KPI["properties"], COMUM["$defs"])
        assert [linha[1].strip("`") for linha in linhas] == [
            "domain", "synonyms", "calculation", "calculation.unit", "history_recalculation", "history_recalculation.policy",
        ]

    def test_linha_tem_titulo_chave_valor_e_descricao(self):
        linhas = r.linhas_de_campos(KPI["properties"], COMUM["$defs"])
        assert linhas[0] == ["Domínio", "`domain`", "texto", "Área do negócio."]
        assert linhas[-1][2] == "um destes: recalculate, method_break"


def test_pagina_do_tipo_tem_frontmatter_aviso_e_secoes(tmp_path: Path):
    montar(tmp_path)
    relatorio, _ = r.executar(tmp_path)
    assert relatorio.erros == []
    texto = pagina(tmp_path, "kpi.md")
    assert texto.startswith('---\ntitle: "Campos: Indicador (KPI)"\ndescription: ')
    assert "<!--" in texto and "gerado" in texto and "à mão" in texto
    assert "(../../../templates/kpi/)" in texto and "(../../../fundamentos/como-ler-os-campos/)" in texto
    ordem = [texto.index(t) for t in ("## Cabeçalho comum", "## Campos do tipo", "## Para quem é técnico")]
    assert ordem == sorted(ordem)
    assert "| Campo | Chave | Obrigatório |" in texto
    assert "| Identificador do assunto | `id` | Sim |" in texto
    assert "| Pergunta de negócio | `intent.question` | Não |" in texto
    assert "| Campo | Chave | Valor | O que escrever |" in texto
    assert "| Cálculo | `calculation` | grupo de campos | Como calcular. |" in texto
    assert "| Unidade | `calculation.unit` | texto | O que se conta. |" in texto
    assert "`const`" not in texto and "`type`" not in texto.split("## Campos do tipo")[1].split("## Para quem")[0]


def test_secao_tecnica_vem_de_common_e_some_se_nao_houver(tmp_path: Path):
    montar(tmp_path)
    r.executar(tmp_path)
    texto = pagina(tmp_path, "kpi.md")
    assert "| Instrução ao agente | `context.instructions` | texto | Texto curto. |" in texto
    assert "| Endereço | `authoritativeDefinitions[].url` | texto | Onde está a regra. |" in texto

    sem = {"title": "Comum", "properties": {}, "$defs": COMUM["$defs"]}
    outra = tmp_path / "outra"
    outra.mkdir()
    montar(outra, comum=sem)
    r.executar(outra)
    assert "## Para quem é técnico" not in pagina(outra, "kpi.md")


def test_indice_tem_uma_linha_por_tipo_na_ordem_do_yaml(tmp_path: Path):
    montar(tmp_path)
    r.executar(tmp_path)
    texto = pagina(tmp_path, "index.md")
    assert texto.startswith("---\ntitle: Referência de campos\n")
    assert texto.index("[Indicador (KPI)](kpi/)") < texto.index("[Dataset](dataset/)")
    assert texto.count("](kpi/)") == 1 and texto.count("](dataset/)") == 1


def test_saida_deterministica_sem_travessao_nem_cr(tmp_path: Path):
    montar(tmp_path)
    r.executar(tmp_path)
    primeira = instantaneo(tmp_path / "src" / "content" / "docs" / "referencias" / "campos")
    r.executar(tmp_path)
    assert instantaneo(tmp_path / "src" / "content" / "docs" / "referencias" / "campos") == primeira
    for conteudo in primeira.values():
        texto = conteudo.decode("utf-8")
        assert chr(0x2014) not in texto and chr(0x2013) not in texto and "\r" not in texto and texto.endswith("\n")


def test_check_em_sincronia_nao_escreve_e_diz_ok(tmp_path: Path):
    montar(tmp_path)
    r.executar(tmp_path)
    pasta = tmp_path / "src" / "content" / "docs" / "referencias" / "campos"
    antes = instantaneo(pasta)
    mtimes = {p: p.stat().st_mtime_ns for p in pasta.rglob("*") if p.is_file()}
    relatorio, mensagem = r.executar(tmp_path, check=True)
    assert relatorio.erros == []
    assert mensagem.startswith("OK: 3 páginas")
    assert instantaneo(pasta) == antes
    assert {p: p.stat().st_mtime_ns for p in pasta.rglob("*") if p.is_file()} == mtimes


def test_check_acusa_desatualizado_ausente_e_orfao_sem_escrever(tmp_path: Path):
    montar(tmp_path)
    r.executar(tmp_path)
    pasta = tmp_path / "src" / "content" / "docs" / "referencias" / "campos"
    (pasta / "kpi.md").write_text("editado à mão\n", encoding="utf-8")
    (pasta / "dataset.md").unlink()
    (pasta / "velho.md").write_text("x\n", encoding="utf-8")
    antes = instantaneo(pasta)
    relatorio, _ = r.executar(tmp_path, check=True)
    assert any("kpi.md" in e and "desatualizado" in e for e in relatorio.erros)
    assert any("dataset.md" in e and "ausente" in e for e in relatorio.erros)
    assert any("velho.md" in e and "órfão" in e for e in relatorio.erros)
    assert instantaneo(pasta) == antes


def test_sem_flag_corrige_e_remove_orfaos(tmp_path: Path):
    montar(tmp_path)
    pasta = tmp_path / "src" / "content" / "docs" / "referencias" / "campos"
    (pasta / "velho.md").write_text("x\n", encoding="utf-8")
    relatorio, _ = r.executar(tmp_path)
    assert relatorio.erros == []
    assert not (pasta / "velho.md").exists()
    assert {p.name for p in pasta.iterdir()} == {"index.md", "kpi.md", "dataset.md"}


def test_schema_ausente_vira_erro_e_nada_e_escrito(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "schemas" / "dataset.schema.json").unlink()
    relatorio, _ = r.executar(tmp_path)
    assert any("dataset.schema.json" in e for e in relatorio.erros)
    assert not (tmp_path / "src/content/docs/referencias/campos/kpi.md").exists()


def test_json_quebrado_vira_erro(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "schemas" / "kpi.schema.json").write_text("{quebrado", encoding="utf-8")
    relatorio, _ = r.executar(tmp_path)
    assert any("kpi.schema.json" in e and "JSON" in e for e in relatorio.erros)


def test_estrutura_de_schema_desconhecida_vira_erro_com_o_campo(tmp_path: Path):
    ruim = {"title": "KPI", "properties": {"estranho": {"title": "Estranho", "description": "x", "type": "tuple"}}}
    montar(tmp_path, kpi=ruim)
    relatorio, _ = r.executar(tmp_path)
    assert any("kpi.schema.json" in e and "estranho" in e for e in relatorio.erros), relatorio.erros


def test_campo_sem_titulo_ou_descricao_vira_erro(tmp_path: Path):
    ruim = {"title": "KPI", "properties": {"sem_titulo": {"description": "x", "type": "string"}}}
    montar(tmp_path, kpi=ruim)
    relatorio, _ = r.executar(tmp_path)
    assert any("sem_titulo" in e and "title" in e for e in relatorio.erros), relatorio.erros


def test_cli_com_entrada_quebrada_sai_1_sem_traceback(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "schemas" / "kpi.schema.json").write_text("{quebrado", encoding="utf-8")
    resultado = subprocess.run([sys.executable, str(Path(r.__file__)), "--raiz", str(tmp_path), "--check"],
                               capture_output=True, text=True, timeout=60)
    assert resultado.returncode == 1
    assert "ERRO:" in resultado.stdout and "Traceback" not in resultado.stderr + resultado.stdout
