#!/usr/bin/env python3
"""Reproduce a fictional SQLite fixture and cross-check reference documents.

Does not test RAG, LLM accuracy, policies or live analytics systems.
"""
from pathlib import Path
from collections import Counter
import sqlite3
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "public" / "downloads"
errors = []

def fail(msg):
    errors.append(msg)

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


def load(name):
    return yaml.safe_load((DL / name).read_text(encoding="utf8"))

for name in ("exemplo-rubrica-ficticia.yaml", "exemplo-rubrica-completo.yaml"):
    rubric = load(name)
    weights = [item["weight"] for item in rubric["criteria"]]
    if sum(weights) != 100 or rubric["scoring"]["weight_sum"] != 100:
        fail(f"{name}: os pesos devem somar 100 e a soma declarada deve conferir")
    for item in rubric["criteria"]:
        if set(item["anchors"].keys()) != {str(i) for i in range(5)}:
            fail(f"{name}: critério {item['id']} não descreve os níveis 0 a 4")
    if rubric["scoring"]["automatic_decision_allowed"] or not rubric["human_review_required"]:
        fail(f"{name}: a rubrica não pode autorizar decisão automática")
    if rubric["scoring"]["missing_evidence_behavior"] != "not_evaluable":
        fail(f"{name}: falta de evidência não pode virar nota zero em silêncio")
complete_rubric = load("exemplo-rubrica-completo.yaml")
if not complete_rubric["scoring"]["not_evaluable_rule"]:
    fail("A rubrica completa precisa dizer como calcular a nota com critério não avaliável")
if any(not c.get("not_in_scope") for c in complete_rubric["criteria"]):
    fail("A rubrica completa precisa delimitar o que cada critério não avalia")

expected = {"Q01": "answer", "Q02": "answer", "Q03": "clarify", "Q04": "abstain", "Q05": "abstain", "Q06": "abstain"}
for name in ("exemplo-casos-teste-ficticios.yaml", "exemplo-casos-teste-completo.yaml"):
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
pending_kpi = load("exemplo-kpi-ficticio.yaml")
pending_q01 = next(q for q in load("exemplo-casos-teste-ficticios.yaml")["questions"] if q["id"] == "Q01")
if pending_kpi["status"] != "approved" and "não foi aprovada" not in pending_q01["reference_answer"]:
    fail("Q01 do exemplo com lacunas responde a partir de KPI pendente sem ressalva")

# A fórmula publicada tem linguagem natural, mas não pode trocar de numerador.
# Este teste guarda os significados das revisões, enquanto o SQLite verifica o cálculo.
formulas_de_referencia = {
    "historico/exemplo-kpi-v1.0.yaml":
        "(Pedidos confirmados elegíveis / Sessões elegíveis) × 100",
    "exemplo-kpi-ficticio.yaml":
        "(Sessões únicas com pelo menos um pedido confirmado / Sessões elegíveis) × 100",
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

for name in ("exemplo-relacionamento-ficticio.yaml", "exemplo-relacionamento-completo.yaml"):
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

if errors:
    for e in errors:
        print("ERRO:", e)
    sys.exit(1)

print("OK: SQLite retorna 25.0% (1 de 4 sessões); pedidos por sessão dá 50% (2 de 4); "
      "rubricas com pesos, âncoras e regra de não avaliável; seis perguntas de referência nos dois gabaritos; "
      "dicionário de pedidos confere com as colunas e os códigos da amostra.")
