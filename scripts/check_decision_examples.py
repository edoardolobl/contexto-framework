#!/usr/bin/env python3
"""Checks only the internal consistency of one fictional decision-table example.

This is NOT a test of a real policy, formal DMN compliance or agent accuracy.
"""
from itertools import product
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
FILES = ["exemplo-decisao-ficticia.yaml", "exemplo-decisao-completo.yaml"]
errors = []
summary = []

for name in FILES:
    doc = yaml.safe_load((ROOT / "public/downloads" / name).read_text(encoding="utf-8"))
    inputs = doc["required_inputs"]
    columns = [entry["name"] for entry in inputs]
    domains = [entry["allowed_values"] for entry in inputs]
    rules = doc["decision_table"]
    possible_outputs = set(doc["possible_outputs"])

    def classify(values):
        matched = [r for r in rules if all(r["when"][k] == "any" or r["when"][k] == values[k] for k in columns)]
        if len(matched) != 1:
            errors.append(f"{name}: condições {values}: esperado 1 caminho, encontrado {len(matched)}")
            return None
        outcome = matched[0]["then"]
        if outcome not in possible_outputs:
            errors.append(f"{name}: resultado não declarado: {outcome}")
        return outcome

    seen = 0
    for combination in product(*domains):
        classify(dict(zip(columns, combination)))
        seen += 1
    for case in doc.get("tests", []):
        observed = classify(case["inputs"])
        if observed != case["expected_outcome"]:
            errors.append(f"{name}: teste {case['inputs']}: esperado {case['expected_outcome']}, observado {observed}")
    summary.append(f"{name}: {seen} combinações, {len(doc.get('tests', []))} casos")

if errors:
    for error in errors:
        print("ERRO:", error)
    sys.exit(1)

print("OK: cada combinação casa com uma única regra. " + "; ".join(summary) + ".")
