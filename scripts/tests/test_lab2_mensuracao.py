"""Testes do validador do Lab 2 (check_lab2_mensuracao.py): funções puras sobre SQLite em memória,
execução no repositório e mutações numa cópia (padrão de test_mutacoes.py)."""
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

import pytest
import yaml

import check_lab2_mensuracao as lab2
import comum

IGNORAR = shutil.ignore_patterns("node_modules", "dist", ".astro", ".git", ".codegraph", "auditoria", "__pycache__", ".pytest_cache")
FIXTURE = "aurora-lab2-fixture.sql"
GABARITO = "exemplo-perguntas-de-negocio-eventos-completo.yaml"

TABELA_YAML = """
required_inputs:
  - {name: active_in_scope}
  - {name: deviation_streak_reached}
decision_table:
  - when: {active_in_scope: false, deviation_streak_reached: any}
    then: not_active_in_scope
  - when: {active_in_scope: true, deviation_streak_reached: true}
    then: failure_candidate
  - when: {active_in_scope: true, deviation_streak_reached: false}
    then: within_expected
"""


def banco(carga: list[tuple[str, int]], eventos: list[tuple[str, int]] = ()) -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.executescript("""
        CREATE TABLE lab2_carga (event_date TEXT, operation TEXT, is_complete INTEGER);
        CREATE TABLE lab2_eventos_diarios (event_date TEXT, operation TEXT, event_name TEXT, event_count INTEGER);
        CREATE TABLE lab2_pedidos (order_id TEXT, order_date TEXT, operation TEXT, revenue INTEGER);
        CREATE TABLE lab2_itens (item_id TEXT, order_id TEXT, sku TEXT);
    """)
    db.executemany("INSERT INTO lab2_carga VALUES (?, 'BR', ?)", carga)
    db.executemany("INSERT INTO lab2_eventos_diarios VALUES (?, 'BR', 'x', ?)", eventos)
    return db


# ---------- dias completos (D+2) ----------
def test_dias_completos_param_dois_dias_antes_da_consulta():
    db = banco([("2026-11-13", 1), ("2026-11-14", 1), ("2026-11-15", 1), ("2026-11-16", 1)])
    assert lab2.dias_completos(db, "BR", "2026-11-17") == ["2026-11-13", "2026-11-14", "2026-11-15"]


def test_dia_marcado_incompleto_fica_de_fora_mesmo_antes_do_limite():
    db = banco([("2026-11-13", 1), ("2026-11-14", 0), ("2026-11-15", 1)])
    assert lab2.dias_completos(db, "BR", "2026-11-17") == ["2026-11-13", "2026-11-15"]


def test_dias_completos_de_operacao_sem_carga_e_vazio():
    assert lab2.dias_completos(banco([]), "MX", "2026-11-17") == []


def test_dias_completos_separa_por_operacao():
    db = banco([("2026-11-10", 1)])
    db.execute("INSERT INTO lab2_carga VALUES ('2026-11-11', 'MX', 1)")
    assert lab2.dias_completos(db, "MX", "2026-11-17") == ["2026-11-11"]


# ---------- sequências em zero ----------
DIAS = ["2026-11-10", "2026-11-11", "2026-11-12", "2026-11-13", "2026-11-14"]


def test_falta_de_linha_conta_como_zero_na_sequencia_atual():
    contagens = {"2026-11-10": 3, "2026-11-11": 1}
    assert lab2.sequencia_atual_zero(DIAS, contagens) == 3


def test_sequencia_atual_e_zero_quando_o_ultimo_dia_tem_disparo():
    assert lab2.sequencia_atual_zero(DIAS, {"2026-11-14": 2}) == 0


def test_sequencia_atual_sem_nenhum_disparo_e_a_janela_inteira():
    assert lab2.sequencia_atual_zero(DIAS, {}) == 5


def test_sequencia_atual_de_janela_vazia_e_zero():
    assert lab2.sequencia_atual_zero([], {}) == 0


def test_maior_sequencia_historica_em_zero():
    contagens = {"2026-11-10": 1, "2026-11-13": 1, "2026-11-14": 1}
    assert lab2.maior_sequencia_zero(DIAS, contagens) == 2


def test_maior_sequencia_sem_dias_em_zero_e_zero():
    assert lab2.maior_sequencia_zero(DIAS, {d: 1 for d in DIAS}) == 0


def test_media_e_dias_em_zero_na_janela():
    media, zeros = lab2.resumo_da_janela(DIAS, {"2026-11-10": 3, "2026-11-12": 2})
    assert (media, zeros) == (1.0, 3)


def test_resumo_de_janela_vazia_nao_divide_por_zero():
    assert lab2.resumo_da_janela([], {}) == (0.0, 0)


def test_contagens_do_par_le_so_o_evento_e_a_operacao():
    db = banco([], [("2026-11-10", 4)])
    db.execute("INSERT INTO lab2_eventos_diarios VALUES ('2026-11-10', 'MX', 'x', 9)")
    db.execute("INSERT INTO lab2_eventos_diarios VALUES ('2026-11-10', 'BR', 'y', 7)")
    assert lab2.contagens_do_par(db, "x", "BR") == {"2026-11-10": 4}


# ---------- tabela de decisão ----------
@pytest.fixture
def tabela() -> list[dict]:
    return yaml.safe_load(TABELA_YAML)["decision_table"]


@pytest.mark.parametrize("entradas, esperado", [
    ({"active_in_scope": False, "deviation_streak_reached": True}, "not_active_in_scope"),
    ({"active_in_scope": True, "deviation_streak_reached": True}, "failure_candidate"),
    ({"active_in_scope": True, "deviation_streak_reached": False}, "within_expected"),
])
def test_classificar_usa_a_tabela_lida_do_yaml(tabela, entradas, esperado):
    assert lab2.classificar(entradas, tabela) == esperado


def test_classificar_sem_linha_que_valha_devolve_none(tabela):
    assert lab2.classificar({"active_in_scope": "unknown", "deviation_streak_reached": True}, tabela) is None


def test_classificar_com_duas_linhas_valendo_devolve_none():
    tabela = [{"when": {"a": "any"}, "then": "x"}, {"when": {"a": True}, "then": "y"}]
    assert lab2.classificar({"a": True}, tabela) is None


def test_classificar_entrada_ausente_devolve_none(tabela):
    assert lab2.classificar({"active_in_scope": True}, tabela) is None


# ---------- fan-out (I-23) ----------
def test_receita_certa_e_receita_duplicada_depois_da_juncao():
    db = banco([])
    db.executemany("INSERT INTO lab2_pedidos VALUES (?, '2026-11-02', 'BR', ?)", [("P1", 100), ("P2", 300)])
    db.executemany("INSERT INTO lab2_itens VALUES (?, ?, 's')", [("I1", "P1"), ("I2", "P2"), ("I3", "P2"), ("I4", "P2")])
    assert lab2.receita_certa(db, "BR", "2026-11-02") == 400
    assert lab2.receita_apos_juncao(db, "BR", "2026-11-02") == 1000


def test_receita_de_dia_sem_pedido_e_zero():
    assert lab2.receita_certa(banco([]), "BR", "2026-11-02") == 0
    assert lab2.receita_apos_juncao(banco([]), "BR", "2026-11-02") == 0


# ---------- integração ----------
@pytest.fixture
def copia(tmp_path: Path) -> Path:
    destino = tmp_path / "repo"
    shutil.copytree(comum.ROOT, destino, ignore=IGNORAR)
    return destino


def downloads(raiz: Path) -> Path:
    return raiz / "public" / "downloads"


def trocar(arquivo: Path, antigo: str, novo: str, todas: bool = False) -> None:
    texto = arquivo.read_text(encoding="utf-8")
    assert antigo in texto, antigo
    arquivo.write_text(texto.replace(antigo, novo, -1 if todas else 1), encoding="utf-8")


def acrescentar(arquivo: Path, texto: str) -> None:
    arquivo.write_text(arquivo.read_text(encoding="utf-8") + "\n" + texto + "\n", encoding="utf-8")


def erros(raiz: Path) -> str:
    return "\n".join(lab2.executar(raiz).erros)


def test_repositorio_passa_sem_erros():
    relatorio = lab2.executar(comum.ROOT)
    assert relatorio.erros == []


def test_arquivo_ausente_vira_erro_legivel(tmp_path: Path):
    texto = erros(tmp_path)
    assert FIXTURE in texto
    assert "Traceback" not in texto


def test_sql_quebrado_vira_erro_legivel(tmp_path: Path):
    destino = downloads(tmp_path)
    destino.mkdir(parents=True)
    (destino / FIXTURE).write_text("CREATE TABLE ((;", encoding="utf-8")
    (destino / "aurora-lab2-reference-query.sql").write_text("SELECT 1;", encoding="utf-8")
    texto = erros(tmp_path)
    assert "SQL inválido" in texto and FIXTURE in texto


def test_script_termina_com_ok_e_resume_o_limite(copia: Path):
    resultado = subprocess.run([sys.executable, str(copia / "scripts" / "check_lab2_mensuracao.py")],
                               capture_output=True, text=True, timeout=120)
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
    assert resultado.stdout.startswith("OK:")
    for trecho in ("2 operações", "3 eventos", "28 dias", "1 dia incompleto", "add_to_cart MX"):
        assert trecho in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_gabarito_com_numero_trocado_falha(copia: Path):
    trocar(downloads(copia) / GABARITO, "9 de 27", "8 de 27", todas=True)
    assert "9 de 27" in erros(copia)


def test_terceira_operacao_na_amostra_falha_pelo_limite(copia: Path):
    acrescentar(downloads(copia) / FIXTURE, "INSERT INTO lab2_plano VALUES ('add_to_cart', 'PT', 1, '2026-10-01', 1);")
    texto = erros(copia)
    assert "limite fixo" in texto and "operações" in texto


def test_quarto_evento_na_amostra_falha_pelo_limite(copia: Path):
    acrescentar(downloads(copia) / FIXTURE, "INSERT INTO lab2_plano VALUES ('page_view', 'BR', 1, '2026-10-01', 1);")
    texto = erros(copia)
    assert "limite fixo" in texto and "eventos" in texto


def test_linha_de_generate_lead_no_mexico_falha(copia: Path):
    acrescentar(downloads(copia) / FIXTURE, "INSERT INTO lab2_eventos_diarios VALUES ('2026-11-10', 'MX', 'generate_lead', 1);")
    assert "generate_lead" in erros(copia)


def test_comportamento_trocado_no_gabarito_falha(copia: Path):
    trocar(downloads(copia) / GABARITO, "expected_behavior: clarify", "expected_behavior: answer")
    assert "comportamentos" in erros(copia)


# ---------- frases recalculadas (F4-02) ----------
def test_periodo_da_maior_sequencia_devolve_primeiro_e_ultimo_dia():
    contagens = {"2026-11-10": 1, "2026-11-14": 1}
    assert lab2.periodo_da_maior_sequencia(DIAS, contagens) == ("2026-11-11", "2026-11-13")


def test_periodo_da_maior_sequencia_sem_zero_e_none():
    assert lab2.periodo_da_maior_sequencia(DIAS, {d: 1 for d in DIAS}) is None


def test_periodo_da_maior_sequencia_empatada_fica_com_a_primeira():
    contagens = {"2026-11-11": 1, "2026-11-13": 1}
    assert lab2.periodo_da_maior_sequencia(DIAS, contagens) == ("2026-11-10", "2026-11-10")


@pytest.mark.parametrize("inicio, fim, esperado", [
    ("2026-10-27", "2026-10-29", "27 a 29/10"),
    ("2026-11-14", "2026-11-15", "14 e 15/11"),
    ("2026-10-30", "2026-11-02", "30/10 a 02/11"),
    ("2026-10-31", "2026-11-01", "31/10 e 01/11"),
    ("2026-11-11", "2026-11-11", "11/11"),
])
def test_formatar_periodo(inicio, fim, esperado):
    assert lab2.formatar_periodo(inicio, fim) == esperado


@pytest.mark.parametrize("valor, esperado", [(30.0, "30"), (1.111, "1,1"), (72.93, "72,9")])
def test_formatar_decimal_curto_tira_a_casa_zero(valor, esperado):
    assert lab2.formatar_decimal_curto(valor) == esperado


def _par(**mudancas) -> "lab2.Par":
    base = dict(evento="generate_lead", operacao="BR", ativo=True, dias=27, dias_em_zero=9, media=30 / 27, total=30,
                maior_sequencia=3, sequencia_atual=2, ultimo_disparo="2026-11-13", entradas={})
    return lab2.Par(**{**base, **mudancas})


@pytest.mark.parametrize("mudancas, esperado", [
    ({}, "| BR | generate_lead | 9 de 27 | 1,1 | 2 dias |"),
    ({"evento": "add_to_cart", "dias_em_zero": 0, "media": 72.93, "sequencia_atual": 0}, "| BR | add_to_cart | 0 de 27 | 72,9 | 0 |"),
    ({"sequencia_atual": 1}, "| BR | generate_lead | 9 de 27 | 1,1 | 1 dia |"),
])
def test_linha_da_tabela_da_pagina(mudancas, esperado):
    assert lab2.linha_da_tabela(_par(**mudancas)) == esperado


@pytest.fixture
def pares_da_amostra() -> dict:
    db = sqlite3.connect(":memory:")
    db.executescript((comum.ROOT / "public" / "downloads" / FIXTURE).read_text(encoding="utf-8"))
    return lab2.calcular_pares(db), db


def test_frases_esperadas_saem_da_amostra(pares_da_amostra):
    pares, db = pares_da_amostra
    frases = lab2.frases_esperadas(pares, db)
    assert "| MX | add_to_cart | 5 de 27 | 30,0 | 5 dias |" in frases["pagina"]
    assert not any("| MX | generate_lead |" in f for f in frases["pagina"])
    assert {"média de 1,1 por dia", "zero em 9 de 27 dias completos", "maior sequência em zero: 3 dias",
            "27 a 29/10"} <= set(frases["evento"])
    assert {"média de 30 por dia", "desde 11/11", "Em 14 e 15/11", "3 dias (27 a 29/10)"} <= set(frases["gabarito"])


PAGINA_LAB2 = Path("src/content/docs/exemplos/laboratorio-eventos.mdx")
EVENTO = "exemplo-evento-coleta-completo.yaml"


@pytest.mark.parametrize("onde, antigo, novo, esperado", [
    ("pagina", "| BR | add_to_cart | 0 de 27 | 72,9 | 0 |", "| BR | add_to_cart | 3 de 27 | 99,9 | 0 |", "72,9"),
    ("pagina", "(27 a 29/10)", "(1 a 3/11)", "27 a 29/10"),
    ("pagina", "desde 11/11", "desde 12/11", "desde 11/11"),
    ("evento", "média de 1,1 por dia", "média de 1,1 por semana", "média de 1,1 por dia"),
    ("evento", "maior sequência em zero: 3 dias", "maior sequência em zero: 7 dias (3 dias úteis)", "maior sequência em zero: 3 dias"),
    ("evento", "zero em 9 de 27 dias completos", "zero em 9 de 27 dias", "zero em 9 de 27 dias completos"),
    ("gabarito", "média de 30 por dia", "média de 80 por dia", "média de 30 por dia"),
    ("gabarito", "desde 11/11", "desde 10/11", "desde 11/11"),
])
def test_frase_trocada_falha(copia: Path, onde: str, antigo: str, novo: str, esperado: str):
    arquivos = {"pagina": copia / PAGINA_LAB2, "evento": downloads(copia) / EVENTO, "gabarito": downloads(copia) / GABARITO}
    trocar(arquivos[onde], antigo, novo)
    assert esperado in erros(copia)
