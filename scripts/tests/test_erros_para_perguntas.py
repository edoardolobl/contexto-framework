"""Testes do erros_para_perguntas: erros do experimento viram perguntas em aberto propostas."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import pytest
import yaml

import comum
import erros_para_perguntas as epp

SCHEMA_COMUM = comum.ROOT / "schemas" / "common.schema.json"
TRAVESSOES = ("—", "–")


def _doc(id_: str, versao: str, status: str, tipo: str, owner: str | None, extra: str = "") -> str:
    dono = "null" if owner is None else f'"{owner}"'
    return (f'---\nid: {id_}\ntype: {tipo}\nversion: "{versao}"\nstatus: {status}\nowner: {dono}\n{extra}---\n\nCorpo.\n')


def _gabarito(id_: str, versao: str, perguntas: str, status: str = "approved") -> str:
    return _doc(id_, versao, status, "perguntas-de-negocio", "Dono do gabarito", f"questions:\n{perguntas}")


PERGUNTAS_A = """  - id: Q01
    question: "Qual a taxa?"
    expected_behavior: answer
    reference_answer: "25%"
    required_sources: [KPI-X-001, consulta.sql]
    ambiguity: null
    reason_if_abstain: null
  - id: Q03
    question: "Qual a conversão?"
    expected_behavior: clarify
    reference_answer: "Perguntar o canal"
    required_sources: [KPI-X-001]
    ambiguity: "Falta o canal"
    reason_if_abstain: null
  - id: Q04
    question: "E no app?"
    expected_behavior: abstain
    reference_answer: null
    required_sources: [KPI-X-001]
    ambiguity: null
    reason_if_abstain: "Fora do escopo"
  - id: Q06
    question: "Só consulta?"
    expected_behavior: answer
    reference_answer: "ver SQL"
    required_sources: [amostra.sql]
    ambiguity: null
    reason_if_abstain: null
"""


@pytest.fixture
def raiz(tmp_path: Path) -> Path:
    ex = tmp_path / "src" / "exemplos"
    ex.mkdir(parents=True)
    (ex / "qa-a-1-0.md").write_text(_gabarito("QA-X-001", "1.0", PERGUNTAS_A.replace("25%", "30%")), encoding="utf-8")
    (ex / "qa-a-1-1.md").write_text(_gabarito("QA-X-001", "1.1", PERGUNTAS_A), encoding="utf-8")
    (ex / "qa-a-2-0.md").write_text(_gabarito("QA-X-001", "2.0", PERGUNTAS_A, "draft"), encoding="utf-8")
    (ex / "kpi-1.md").write_text(_doc("KPI-X-001", "1.0", "superseded", "kpi", "Dono antigo"), encoding="utf-8")
    (ex / "kpi-2.md").write_text(_doc("KPI-X-001", "2.0", "approved", "kpi", "Dono do KPI"), encoding="utf-8")
    return tmp_path


def _item_onboarding(pergunta: str, cond: str = "B", certo: bool = True, modelo: str = "Modelo M",
                     cat: str = "responder", **extra: Any) -> dict[str, Any]:
    base = {"cond": cond, "modelo": "m", "modelo_nome": modelo, "rodada": 1, "pergunta": pergunta,
            "resposta": "texto livre", "categoria_observada": cat, "categoria_certa": certo,
            "conclusao_certa": certo, "citacao_certa": True, "observacao": "free text"}
    return {**base, **extra}


def _escrever(tmp_path: Path, dados: Any, nome: str = "res.json") -> Path:
    caminho = tmp_path / nome
    caminho.write_text(json.dumps(dados), encoding="utf-8")
    return caminho


def _rodar(raiz: Path, resultados: Path, *args: str, capsys: pytest.CaptureFixture[str]) -> tuple[int, str, str]:
    try:
        epp.main([str(resultados), "--raiz", str(raiz), *args])
        codigo = 0
    except SystemExit as saida:
        codigo = int(saida.code or 0)
    captura = capsys.readouterr()
    return codigo, captura.out, captura.err


def _blocos(texto: str) -> list[dict[str, Any]]:
    achados = re.findall(r"```yaml\n(.*?)```", texto, flags=re.S)
    return [yaml.safe_load(a)["open_questions"][0] for a in achados]


def _validador() -> Draft202012Validator:
    schema = json.loads(SCHEMA_COMUM.read_text(encoding="utf-8"))
    registro = Registry().with_resources([(schema["$id"], Resource(contents=schema, specification=DRAFT202012))])
    return Draft202012Validator({"$ref": schema["$id"] + "#/$defs/pergunta_em_aberto"},
                                registry=registro, format_checker=FormatChecker())


def _hash_pasta(pasta: Path) -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(pasta.glob("*.md"))}


def test_erro_em_um_item_gera_proposta_valida_no_schema_comum(raiz: Path, tmp_path: Path, capsys):
    itens = [_item_onboarding("QA1-Q03", certo=False), _item_onboarding("QA1-Q03"), _item_onboarding("QA1-Q03")]
    codigo, saida, _ = _rodar(raiz, _escrever(tmp_path, itens), "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert codigo == 0
    blocos = _blocos(saida)
    assert len(blocos) == 1
    assert list(_validador().iter_errors(blocos[0])) == []
    assert blocos[0]["question"] == (
        'A IA errou a Q03 do QA-X-001@1.1 ("QA1-Q03") em 1 de 3 execuções. '
        "O que falta em KPI-X-001@2.0 para a resposta esperada sair, ou o gabarito precisa mudar?")
    assert blocos[0]["owner_to_resolve"] == "Dono do KPI"
    assert blocos[0]["status"] == "unresolved" and blocos[0]["resolution"] is None
    assert "Falta o canal" in blocos[0]["impact"] and "responder" in blocos[0]["impact"]
    assert "texto livre" not in saida and "free text" not in saida


def test_cada_tipo_de_erro_conta_sozinho(raiz: Path, tmp_path: Path, capsys):
    itens = [_item_onboarding("QA1-Q03", categoria_certa=False), _item_onboarding("QA1-Q03", conclusao_certa=False),
             _item_onboarding("QA1-Q03", conclusao_certa=None, conclusao_igual_q01=False)]
    itens[2].pop("conclusao_certa")
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, itens), "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert "em 3 de 3 execuções" in saida


def test_citacao_certa_falso_sozinha_nao_conta(raiz: Path, tmp_path: Path, capsys):
    itens = [_item_onboarding("QA1-Q03", citacao_certa=False)]
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, itens), "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert "Nenhuma pergunta errada nas condições escolhidas." in saida
    assert _blocos(saida) == []


def test_filtro_de_condicao_padrao_e_repetivel(raiz: Path, tmp_path: Path, capsys):
    itens = [_item_onboarding("QA1-Q03", cond="controle", certo=False), _item_onboarding("QA1-Q03", cond="B")]
    arquivo = _escrever(tmp_path, itens)
    _, padrao, _ = _rodar(raiz, arquivo, "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert "Nenhuma pergunta errada" in padrao and "Execuções: 1\n" in padrao
    _, ambas, _ = _rodar(raiz, arquivo, "--mapa", "QA1=QA-X-001", "--condicao", "B", "--condicao", "controle",
                         capsys=capsys)
    assert "em 1 de 2 execuções" in ambas and "Execuções: 2\n" in ambas


def test_formato_caso_1_com_mapa_por_nome(raiz: Path, tmp_path: Path, capsys):
    itens = [{"cond": "B", "modelo": "opus", "pergunta": "boa", "i": 1, "categoria": "answer",
              "categoria_certa": True, "conclusao_igual_q01": False, "observacao": "english text"},
             {"cond": "B", "modelo": "opus", "pergunta": "boa", "i": 2, "categoria": "answer",
              "categoria_certa": True, "conclusao_igual_q01": True, "observacao": "english text"}]
    codigo, saida, _ = _rodar(raiz, _escrever(tmp_path, itens), "--mapa", "boa=QA-X-001:Q01", capsys=capsys)
    assert codigo == 0
    blocos = _blocos(saida)
    assert len(blocos) == 1 and "Q01 do QA-X-001@1.1" in blocos[0]["question"]
    assert "em 1 de 2 execuções" in blocos[0]["question"]
    assert "english text" not in saida
    assert "opus" in saida and "answer" in saida


def test_required_sources_so_com_sql_aponta_para_o_gabarito(raiz: Path, tmp_path: Path, capsys):
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, [_item_onboarding("QA1-Q06", certo=False)]),
                         "--mapa", "QA1=QA-X-001", capsys=capsys)
    bloco = _blocos(saida)[0]
    assert "O que falta em QA-X-001@1.1 para" in bloco["question"]
    assert bloco["owner_to_resolve"] == "Dono do gabarito"


def test_kpi_superseded_e_approved_resolve_para_a_vigente(raiz: Path, tmp_path: Path, capsys):
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, [_item_onboarding("QA1-Q01", certo=False)]),
                         "--mapa", "QA1=QA-X-001", capsys=capsys)
    bloco = _blocos(saida)[0]
    assert "KPI-X-001@2.0" in bloco["question"] and "KPI-X-001@1.0" not in saida
    assert bloco["owner_to_resolve"] == "Dono do KPI"


def test_gabarito_usa_a_versao_aprovada_mais_alta(raiz: Path, tmp_path: Path, capsys):
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, [_item_onboarding("QA1-Q01", certo=False)]),
                         "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert "QA-X-001@1.1" in saida and "QA-X-001@2.0" not in saida and "QA-X-001@1.0" not in saida


def test_alvo_sem_versao_aprovada(raiz: Path, tmp_path: Path, capsys):
    (raiz / "src" / "exemplos" / "kpi-2.md").unlink()
    (raiz / "src" / "exemplos" / "kpi-1.md").unlink()
    (raiz / "src" / "exemplos" / "kpi-r.md").write_text(_doc("KPI-X-001", "0.1", "draft", "kpi", "Rascunho"), encoding="utf-8")
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, [_item_onboarding("QA1-Q01", certo=False)]),
                         "--mapa", "QA1=QA-X-001", capsys=capsys)
    bloco = _blocos(saida)[0]
    assert "(sem versão aprovada)" in bloco["question"]
    assert bloco["owner_to_resolve"] is None
    assert list(_validador().iter_errors(bloco)) == []


@pytest.mark.parametrize("comportamento", ["Q01", "Q03", "Q04"])
def test_comportamento_esperado_em_portugues(raiz: Path, tmp_path: Path, capsys, comportamento: str):
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, [_item_onboarding(f"QA1-{comportamento}", certo=False)]),
                         "--mapa", "QA1=QA-X-001", capsys=capsys)
    esperado = {"Q01": "responder", "Q03": "pedir esclarecimento", "Q04": "abster-se"}[comportamento]
    assert esperado in saida


@pytest.mark.parametrize("dados", [{"a": 1}, [1, 2], [{"cond": "B"}], "texto"])
def test_entrada_malformada_termina_com_erro(raiz: Path, tmp_path: Path, capsys, dados: Any):
    codigo, saida, _ = _rodar(raiz, _escrever(tmp_path, dados), "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert codigo == 1 and "ERRO:" in saida


def test_json_invalido_e_arquivo_inexistente_terminam_com_erro(raiz: Path, tmp_path: Path, capsys):
    ruim = tmp_path / "ruim.json"
    ruim.write_text("{nao e json", encoding="utf-8")
    assert _rodar(raiz, ruim, "--mapa", "QA1=QA-X-001", capsys=capsys)[0] == 1
    assert _rodar(raiz, tmp_path / "nada.json", "--mapa", "QA1=QA-X-001", capsys=capsys)[0] == 1


def test_gabarito_inexistente_ou_sem_versao_aprovada_da_erro(raiz: Path, tmp_path: Path, capsys):
    arquivo = _escrever(tmp_path, [_item_onboarding("QA1-Q03", certo=False)])
    codigo, saida, _ = _rodar(raiz, arquivo, "--mapa", "QA1=QA-NAO-EXISTE", capsys=capsys)
    assert codigo == 1 and "ERRO:" in saida and "QA-NAO-EXISTE" in saida
    (raiz / "src" / "exemplos" / "so-rascunho.md").write_text(
        _gabarito("QA-Y-001", "0.1", PERGUNTAS_A, "draft"), encoding="utf-8")
    assert _rodar(raiz, arquivo, "--mapa", "QA1=QA-Y-001", capsys=capsys)[0] == 1


def test_qnn_inexistente_no_gabarito_da_erro(raiz: Path, tmp_path: Path, capsys):
    codigo, saida, _ = _rodar(raiz, _escrever(tmp_path, [_item_onboarding("QA1-Q99", certo=False)]),
                              "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert codigo == 1 and "Q99" in saida


def test_mapa_malformado_da_erro(raiz: Path, tmp_path: Path, capsys):
    assert _rodar(raiz, _escrever(tmp_path, [_item_onboarding("QA1-Q03")]), "--mapa", "semigual", capsys=capsys)[0] == 1


def test_prefixo_sem_mapa_gera_aviso_e_secao(raiz: Path, tmp_path: Path, capsys):
    itens = [_item_onboarding("QA1-Q03", certo=False), _item_onboarding("QA9-Q01", certo=False)]
    codigo, saida, erro = _rodar(raiz, _escrever(tmp_path, itens), "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert codigo == 0
    assert "AVISO:" in saida + erro and "QA9-Q01" in erro + saida
    assert "Sem gabarito ligado" in saida
    assert len(_blocos(saida)) == 1


def test_saida_em_arquivo_escreve_so_esse_arquivo(raiz: Path, tmp_path: Path, capsys):
    destino = tmp_path / "saida" / "rel.md"
    destino.parent.mkdir()
    antes = _hash_pasta(raiz / "src" / "exemplos")
    codigo, saida, _ = _rodar(raiz, _escrever(tmp_path, [_item_onboarding("QA1-Q03", certo=False)]),
                              "--mapa", "QA1=QA-X-001", "--saida", str(destino), capsys=capsys)
    assert codigo == 0 and "Relatório para revisão humana" not in saida
    assert "Relatório para revisão humana" in destino.read_text(encoding="utf-8")
    assert _hash_pasta(raiz / "src" / "exemplos") == antes


def test_erro_nao_escreve_o_arquivo_de_saida(raiz: Path, tmp_path: Path, capsys):
    destino = tmp_path / "rel.md"
    codigo, _, _ = _rodar(raiz, _escrever(tmp_path, [{"cond": "B"}]), "--mapa", "QA1=QA-X-001",
                          "--saida", str(destino), capsys=capsys)
    assert codigo == 1 and not destino.exists()


def test_saida_igual_em_duas_execucoes_e_ordenada(raiz: Path, tmp_path: Path, capsys):
    itens = [_item_onboarding("QA1-Q06", certo=False), _item_onboarding("QA1-Q03", certo=False, modelo="Zeta"),
             _item_onboarding("QA1-Q03", certo=False, modelo="Alfa")]
    arquivo = _escrever(tmp_path, itens)
    primeira = _rodar(raiz, arquivo, "--mapa", "QA1=QA-X-001", capsys=capsys)[1]
    segunda = _rodar(raiz, arquivo, "--mapa", "QA1=QA-X-001", capsys=capsys)[1]
    assert primeira == segunda
    assert primeira.index("Q03") < primeira.index("Q06")
    assert primeira.index("Alfa") < primeira.index("Zeta")
    assert not any(t in primeira for t in TRAVESSOES)


def test_cabecalho_e_aviso_fixo(raiz: Path, tmp_path: Path, capsys):
    itens = [_item_onboarding("QA1-Q03", certo=False), _item_onboarding("QA1-Q03")]
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, itens), "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert "Relatório para revisão humana. Este script não altera nenhum documento. Uma proposta só entra num " \
           "documento depois que o responsável por ele a revisa, e um documento aprovado só muda numa versão nova." in saida
    assert "res.json" in saida and "Execuções: 2" in saida and "Erros: 1" in saida and "B" in saida


def test_cabecalho_registra_o_comando_que_reproduz_o_relatorio(raiz: Path, tmp_path: Path, capsys):
    itens = [_item_onboarding("QA1-Q03", certo=False), _item_onboarding("QA2-Q01", cond="A")]
    _, saida, _ = _rodar(raiz, _escrever(tmp_path, itens), "--mapa", "QA2=QA-X-001", "--mapa", "QA1=QA-X-001",
                         "--condicao", "B", "--condicao", "A", capsys=capsys)
    linha = next(l for l in saida.splitlines() if l.startswith("- Comando:"))
    assert linha.startswith("- Comando: `python3 scripts/erros_para_perguntas.py ")
    assert "res.json" in linha
    assert "--mapa QA1=QA-X-001 --mapa QA2=QA-X-001" in linha
    assert "--condicao A --condicao B" in linha
    assert "--raiz" not in linha and "--saida" not in linha


def test_arquivos_de_exemplos_nao_mudam(raiz: Path, tmp_path: Path, capsys):
    antes = _hash_pasta(raiz / "src" / "exemplos")
    _rodar(raiz, _escrever(tmp_path, [_item_onboarding("QA1-Q03", certo=False)]), "--mapa", "QA1=QA-X-001", capsys=capsys)
    assert _hash_pasta(raiz / "src" / "exemplos") == antes
