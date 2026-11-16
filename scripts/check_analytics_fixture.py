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

rubric = load("exemplo-rubrica-ficticia.yaml")
weights = [item["weight"] for item in rubric["criteria"]]
if sum(weights) != 100 or rubric["scoring"]["weight_sum"] != 100:
    fail("Rubric weights must sum to 100, with an accurate declared sum")
for item in rubric["criteria"]:
    if set(item["anchors"].keys()) != {str(i) for i in range(5)}:
        fail(f"Rubric {item['id']} does not describe levels 0..4")
if rubric["scoring"]["automatic_hiring_decision"] or not rubric["human_review_required"]:
    fail("Fictitious candidate rubric must not authorize automatic hiring decisions")
if rubric["scoring"]["missing_evidence_behavior"] != "not_evaluable":
    fail("A lack of evidence must not silently become a zero score")

questions = load("exemplo-casos-teste-ficticios.yaml")["questions"]
if len(questions) != 5:
    fail("Expected five reference questions in the demonstration")
ids = [q["id"] for q in questions]
if len(ids) != len(set(ids)):
    fail("Duplicate reference question IDs")
expected = {"Q01": "answer", "Q02": "answer", "Q03": "clarify", "Q04": "abstain", "Q05": "abstain"}
for q in questions:
    if expected.get(q["id"]) != q["expected_behavior"]:
        fail(f"Unexpected documented behavior for question {q['id']}")
q01 = next(q for q in questions if q["id"] == "Q01")
if "25%" not in q01["reference_answer"]:
    fail("Q01 does not match the tested fixture answer 25%")

kpi = load("exemplo-kpi-ficticio.yaml")
formula = kpi["calculation"]["formula_description"]
if "sessoes_unicas" not in formula or "pedidos_confirmados /" in formula:
    fail("KPI numerator must be distinct converted sessions, not count of orders")

relation = load("exemplo-relacionamento-ficticio.yaml")
if relation["cardinality"] != "one_to_many":
    fail("Dataset relation must record sessions -> orders as one-to-many")

if errors:
    for e in errors:
        print("ERRO:", e)
    sys.exit(1)

print("OK: SQLite produced 25.0% (1/4 sessions); naive orders-per-session is 50% "
      "(2/4); rubric weights and anchors; five reference questions; semantic links checked.")
