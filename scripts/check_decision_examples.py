#!/usr/bin/env python3
"""Checks the campaign decision table and the rubric that feeds one of its inputs.

This is NOT a test of a real policy, formal DMN compliance or agent accuracy.
"""
from itertools import product

from comum import DOWNLOADS as DL, Relatorio, carregar_yaml

relatorio = Relatorio()
relatorio.instalar()
FILES = ["exemplo-decisao-lacunas.yaml", "exemplo-decisao-completo.yaml"]
errors = relatorio.erros
summary = []


def conferir_campos(name: str, doc: dict, tipo: str, campos: tuple[str, ...]) -> bool:
    """Confere type e a presença dos campos lidos; falta vira ERRO legível, não KeyError."""
    ok = True
    if doc.get("type") != tipo:
        errors.append(f"{name}: type deve ser {tipo!r}, encontrado {doc.get('type')!r}")
        ok = False
    for campo in campos:
        if doc.get(campo) in (None, ""):
            errors.append(f"{name}: falta o campo {campo}, que a conferência precisa ler")
            ok = False
    return ok


for name in FILES:
    doc = carregar_yaml(DL / name, relatorio)
    if doc is None:
        continue
    if not conferir_campos(name, doc, "decisao", ("required_inputs", "decision_table", "possible_outputs")):
        continue
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

# Rubrica de material de campanha: pesos, âncoras, nota recalculada e encaminhamento pela tabela aprovada.
decision = carregar_yaml(DL / "exemplo-decisao-completo.yaml", relatorio) or {"decision_table": []}


def route(brief_complete: bool, evidence_sufficient: bool) -> str | None:
    values = {"brief_complete": brief_complete, "evidence_sufficient": evidence_sufficient}
    hits = [r["then"] for r in decision["decision_table"]
            if all(r["when"][k] == "any" or r["when"][k] == v for k, v in values.items())]
    return hits[0] if len(hits) == 1 else None


calibrated = 0
for name in ("exemplo-rubrica-lacunas.yaml", "exemplo-rubrica-completo.yaml"):
    rubric = carregar_yaml(DL / name, relatorio)
    if rubric is None or not conferir_campos(name, rubric, "rubrica", ("criteria", "scoring", "human_review_required")):
        continue
    weights = {c["id"]: c["weight"] for c in rubric["criteria"]}
    if sum(weights.values()) != 100 or rubric["scoring"]["weight_sum"] != 100:
        errors.append(f"{name}: os pesos devem somar 100 e a soma declarada deve conferir")
    for c in rubric["criteria"]:
        if set(c["anchors"]) != {str(i) for i in range(5)}:
            errors.append(f"{name}: critério {c['id']} não descreve os níveis 0 a 4")
    if rubric["scoring"]["automatic_decision_allowed"] or not rubric["human_review_required"]:
        errors.append(f"{name}: a rubrica não pode autorizar decisão automática")
    if rubric["scoring"]["missing_evidence_behavior"] != "not_evaluable":
        errors.append(f"{name}: falta de evidência não pode virar nota zero em silêncio")
    if rubric["status"] != "approved":
        continue
    if not rubric["scoring"]["not_evaluable_rule"] or any(not c.get("not_in_scope") for c in rubric["criteria"]):
        errors.append(f"{name}: a rubrica aprovada precisa da regra de não avaliável e do que cada critério não avalia")
    for case in rubric.get("calibration_examples") or []:
        levels = case["levels"]
        if set(levels) != set(weights):
            errors.append(f"{name}: calibração sem nível para todos os critérios")
            continue
        score = round(sum(levels[k] / 4 * weights[k] for k in weights), 2)
        if score != case["score"]:
            errors.append(f"{name}: nota declarada {case['score']}, recalculada {score}")
        sufficient = levels["claims_with_proof"] >= 3
        if sufficient != case["evidence_sufficient"]:
            errors.append(f"{name}: alegações com prova em nível {levels['claims_with_proof']} não dá evidence_sufficient={case['evidence_sufficient']}")
        if route(True, sufficient) != case["routing"]:
            errors.append(f"{name}: a tabela de decisão encaminha para {route(True, sufficient)}, não {case['routing']}")
        calibrated += 1
summary.append(f"rubrica de campanha: {calibrated} materiais com nota e encaminhamento recalculados")

relatorio.encerrar("OK: cada combinação casa com uma única regra. " + "; ".join(summary) + ".")
