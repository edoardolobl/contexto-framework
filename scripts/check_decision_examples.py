#!/usr/bin/env python3
"""Checks only the internal consistency of one fictional decision-table example.

This is NOT a test of a real policy, formal DMN compliance or agent accuracy.
"""
from itertools import product
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "public/downloads/exemplo-decisao-ficticia.yaml"
doc = yaml.safe_load(source.read_text(encoding="utf-8"))

errors = []
inputs = doc["required_inputs"]
columns = [entry["name"] for entry in inputs]
domains = [entry["allowed_values"] for entry in inputs]
rules = doc["decision_table"]
possible_outputs = set(doc["possible_outputs"])


def matches(rule, values):
    cond = rule["when"]
    return all(cond[k] == "any" or cond[k] == values[k] for k in columns)


def classify(values):
    matched = [rule for rule in rules if matches(rule, values)]
    if len(matched) != 1:
        errors.append(f"Condições {values}: esperado 1 caminho, encontrado {len(matched)}")
        return None
    outcome = matched[0]["then"]
    if outcome not in possible_outputs:
        errors.append(f"Resultado não declarado: {outcome}")
    return outcome


seen = 0
for combination in product(*domains):
    values = dict(zip(columns, combination))
    classify(values)
    seen += 1

for case in doc.get("tests", []):
    observed = classify(case["inputs"])
    expected = case["expected_outcome"]
    if observed != expected:
        errors.append(f"Teste {case['inputs']}: esperado {expected}, observado {observed}")

if doc.get("status") == "approved":
    errors.append("O exemplo fictício não deve declarar uma aprovação organizacional real.")

if errors:
    for error in errors:
        print("ERRO:", error)
    sys.exit(1)

print(f"OK: {seen} combinações de entrada cobertas por uma única regra cada; "
      f"{len(doc.get('tests', []))} casos explícitos validados.")
