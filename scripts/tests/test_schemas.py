"""Testes de check_schemas, com schemas e fontes de mentira em tmp_path."""
import json
import re
from pathlib import Path

import pytest

import comum
import check_schemas as cs

COMUM = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "urn:contexto:schemas:1.0.0:common",
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "schema_version": {"const": "1.0.0"},
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
        "---\n# aviso\nid: KPI-A\ntype: kpi\nvalid_from: 2026-09-15\nintent:\n  question: Q?\n---\ncorpo\n", encoding="utf-8")
    (raiz / "src/exemplos/historico/exemplo-kpi-v1.0.md").write_text(
        "---\nid: KPI-A\ntype: kpi\nstatus: superseded\nrecorded_at: 2026-10-01\n---\ncorpo\n", encoding="utf-8")
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
    assert cs.mensagem_ok(1, 2) == "OK: 1 modelos e 2 exemplos válidos no JSON Schema 1.0.0, cabeçalho na ordem"


def test_erro_de_schema_sai_com_arquivo_caminho_e_mensagem(tmp_path: Path):
    montar(tmp_path)
    arq = tmp_path / "src/exemplos/exemplo-kpi-completo.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace("id: KPI-A", "id: 7"), encoding="utf-8")
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
