#!/usr/bin/env python3
"""Reproduce a fictional SQLite fixture and cross-check reference documents.

Does not test RAG, LLM accuracy, policies or live analytics systems.
"""
import sqlite3
from typing import Any

from comum import DOWNLOADS as DL, ROOT, Relatorio, carregar_yaml

relatorio = Relatorio()
relatorio.instalar()
errors = relatorio.erros


def fail(msg: str) -> None:
    relatorio.erro(None, msg)

with sqlite3.connect(":memory:") as db:
    db.executescript((DL / "aurora-fixture.sql").read_text(encoding="utf8"))
    query = (DL / "aurora-reference-query.sql").read_text(encoding="utf8")
    result = db.execute(query).fetchone()
    if not result or result[0] != 25.0:
        fail(f"Expected 25.0% of converted sessions, observed {result}")

    eligible = db.execute("""
        SELECT COUNT(*) FROM demo_sessions
        WHERE channel='web' AND is_internal=0 AND session_date='2026-10-01'
    """).fetchone()[0]
    if eligible != 4:
        fail(f"Expected four eligible sessions, got {eligible}")

    converted = db.execute("""
        SELECT COUNT(DISTINCT s.session_id)
        FROM demo_sessions AS s
        JOIN demo_orders AS o ON o.session_id=s.session_id
        WHERE s.channel='web' AND s.is_internal=0
          AND s.session_date='2026-10-01' AND o.status_code='CONFIRMED'
    """).fetchone()[0]
    if converted != 1:
        fail(f"Expected one distinct converted session, got {converted}")

    orders = db.execute("""
        SELECT COUNT(*)
        FROM demo_orders AS o JOIN demo_sessions AS s ON o.session_id=s.session_id
        WHERE s.channel='web' AND s.is_internal=0 AND o.status_code='CONFIRMED'
    """).fetchone()[0]
    if orders != 2:
        fail(f"Expected two confirmed orders in eligible sessions, got {orders}")

    # Sem o filtro de sessões internas, S3 (interna, com O4 confirmado) entra na conta.
    with_internal = db.execute("""
        SELECT 100.0 * COUNT(DISTINCT CASE WHEN o.status_code='CONFIRMED' THEN s.session_id END)
               / COUNT(DISTINCT s.session_id)
        FROM demo_sessions AS s LEFT JOIN demo_orders AS o ON o.session_id=s.session_id
        WHERE s.channel='web' AND s.session_date='2026-10-01'
    """).fetchone()[0]


def load(name: str) -> dict[str, Any]:
    """Carrega um download; um arquivo ausente ou quebrado vira ERRO com o nome, não traceback."""
    data = carregar_yaml(DL / name, relatorio)
    if data is None:
        relatorio.encerrar("")  # há erro registrado: encerra com código 1 e lista os erros
        raise SystemExit(1)
    return data

base = {"Q01": "answer", "Q02": "answer", "Q03": "clarify", "Q04": "abstain", "Q05": "abstain", "Q06": "abstain"}
for name, expected in (("exemplo-perguntas-de-negocio-lacunas.yaml", base), ("exemplo-perguntas-de-negocio-completo.yaml", {**base, "Q07": "answer"})):
    questions = load(name)["questions"]
    behaviors = {q["id"]: q["expected_behavior"] for q in questions}
    if behaviors != expected:
        fail(f"{name}: comportamentos documentados diferentes do esperado: {behaviors}")
    q01 = next(q for q in questions if q["id"] == "Q01")
    if "25%" not in q01["reference_answer"]:
        fail(f"{name}: Q01 não corresponde ao resultado testado de 25%")
    for q in questions:
        if q["expected_behavior"] == "abstain" and (q["reference_answer"] is not None or not q["reason_if_abstain"]):
            fail(f"{name}: {q['id']} é abstenção e precisa de motivo, sem resposta numérica")
        if q["expected_behavior"] == "clarify" and not q["ambiguity"]:
            fail(f"{name}: {q['id']} pede esclarecimento e precisa dizer o que falta")
# Uma resposta apoiada em definição ainda não aprovada precisa dizer isso.
# Em 01/10 o KPI 2.0 já valia; o que faltava no gabarito com lacunas era a conferência da resposta.
pending_qa = load("exemplo-perguntas-de-negocio-lacunas.yaml")
pending_q01 = next(q for q in pending_qa["questions"] if q["id"] == "Q01")
if pending_qa["status"] != "approved" and "ainda não foi conferida" not in pending_q01["reference_answer"]:
    fail("Q01 do gabarito com lacunas responde sem a ressalva de que ninguém conferiu a resposta")

# Os números citados no dicionário e nas páginas saem da amostra, não de digitação.
rate_with_internal = f"{with_internal:.0f}%"
if rate_with_internal != "40%":
    fail(f"Sem o filtro de sessões internas, esperado 40%, observado {rate_with_internal}")
caveats = " ".join(load("exemplo-dataset-completo.yaml")["usage"]["known_caveats"])
if rate_with_internal not in caveats or "25%" not in caveats:
    fail("O dicionário de sessões precisa citar a taxa com e sem sessões internas calculadas na amostra")
pages = {
    "templates/dataset.mdx": [rate_with_internal, "25%"],
    "templates/relacionamento.mdx": ["50%", "25%"],
}
for page, numbers in pages.items():
    text = (ROOT / "src/content/docs" / page).read_text(encoding="utf8")
    for number in numbers:
        if number not in text:
            fail(f"{page}: falta o número {number} calculado na amostra")

# A fórmula publicada tem linguagem natural, mas não pode trocar de numerador.
# Este teste guarda os significados das revisões, enquanto o SQLite verifica o cálculo.
formulas_de_referencia = {
    "historico/exemplo-kpi-v1.0.yaml":
        "(Pedidos confirmados elegíveis / Sessões elegíveis) × 100",
    "exemplo-kpi-completo.yaml":
        "(Sessões únicas com pelo menos um pedido confirmado / Sessões elegíveis) × 100",
}
for name, formula_esperada in formulas_de_referencia.items():
    doc = load(name)
    atual = doc["calculation"]["formula_description"]
    if atual != formula_esperada:
        fail(f"{name}: fórmula descritiva divergente da definição: {atual!r}")
    if "_" in atual:
        fail(f"{name}: fórmula da aba de leitura contém identificadores técnicos")
    numerador = doc["calculation"]["numerator"].lower()
    if name.startswith("historico/"):
        if "quantidade de pedidos" not in numerador:
            fail(f"{name}: fórmula histórica não pode contar sessões únicas")
    elif "quantidade de sessões" not in numerador:
        fail(f"{name}: a fórmula atual precisa contar sessões únicas convertidas")

# O rascunho 0.1 ainda não sabia se conversão era pedido ou sessão: o numerador fica em aberto,
# e a pergunta aparece entre as perguntas em aberto. Assim a 1.0, que contou pedidos, não "volta atrás".
draft = load("exemplo-kpi-lacunas.yaml")
if draft["calculation"]["numerator"] is not None:
    fail("exemplo-kpi-lacunas.yaml: o rascunho não pode já trazer o numerador que só foi decidido depois")
if not any("pedidos confirmados ou sessões" in q["question"] for q in draft["open_questions"]):
    fail("exemplo-kpi-lacunas.yaml: falta a pergunta em aberto sobre contar pedidos ou sessões")

# I-14: o KPI atual declara que o histórico não se recalcula, o que sustenta a resposta "Não" de Q07.
kpi_atual = load("exemplo-kpi-completo.yaml")
politica = (kpi_atual.get("history_recalculation") or {}).get("policy")
if politica != "method_break":
    fail(f"exemplo-kpi-completo.yaml: history_recalculation.policy deve ser method_break, encontrado {politica!r}")
q07 = next((q for q in load("exemplo-perguntas-de-negocio-completo.yaml")["questions"] if q["id"] == "Q07"), None)
if not q07 or not str(q07["reference_answer"]).startswith("Não"):
    fail("Q07 do gabarito completo deve responder Não, coerente com method_break")

for name in ("exemplo-relacionamento-lacunas.yaml", "exemplo-relacionamento-completo.yaml"):
    if load(name)["cardinality"] != "one_to_many":
        fail(f"{name}: a relação sessões para pedidos deve ser um para muitos")

orders_doc = load("exemplo-dataset-pedidos-completo.yaml")
documented = {c["physical_name"]: c for c in orders_doc["columns"]}
with sqlite3.connect(":memory:") as db:
    db.executescript((DL / "aurora-fixture.sql").read_text(encoding="utf8"))
    real_columns = {row[1] for row in db.execute("PRAGMA table_info(demo_orders)")}
    real_codes = {row[0] for row in db.execute("SELECT DISTINCT status_code FROM demo_orders")}
if set(documented) != real_columns:
    fail(f"Dicionário de pedidos não cobre as colunas reais: {sorted(real_columns ^ set(documented))}")
if not real_codes <= set(documented["status_code"]["allowed_values"]):
    fail("Há código de estado na amostra que o dicionário de pedidos não documenta")

relatorio.encerrar("OK: SQLite retorna 25.0% (1 de 4 sessões); pedidos por sessão dá 50% (2 de 4); "
      "taxa sem filtro de sessões internas dá 40%; sete perguntas de negócio no gabarito aprovado; "
      "dicionário de pedidos confere com as colunas e os códigos da amostra.")
