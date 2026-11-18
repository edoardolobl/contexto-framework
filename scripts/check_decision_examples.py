#!/usr/bin/env python3
"""Checks the campaign decision table and the rubric that feeds one of its inputs.

This is NOT a test of a real policy, formal DMN compliance or agent accuracy.
"""
from itertools import product

from comum import DOWNLOADS as DL, Relatorio, carregar_yaml

relatorio = Relatorio()
relatorio.instalar()
FILES = sorted(p.name for p in DL.glob("exemplo-decisao-*.yaml"))
FAILURE = "failure_candidate"
FAILURE_REQUIRED = {
    "active_in_scope": True,
    "ingestion_complete": True,
    "expected_in_window": True,
    "deviation_streak_reached": True,
    "known_exception_applies": False,
}
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


def conferir_linhas(name: str, rules: list, columns: list[str]) -> bool:
    """Cada linha precisa de when com todas as entradas e de then; falta vira ERRO legível."""
    ok = True
    for numero, rule in enumerate(rules, start=1):
        when = rule.get("when") if isinstance(rule, dict) else None
        if not isinstance(when, dict) or "then" not in rule:
            errors.append(f"{name}: linha {numero} da tabela precisa de when e then")
            ok = False
            continue
        for coluna in (c for c in columns if c not in when):
            errors.append(f"{name}: linha {numero} da tabela não traz a entrada {coluna} no when (use any se não importa)")
            ok = False
    return ok


def conferir_failure_candidate(name: str, rules: list, inputs: list) -> None:
    """Regra canônica de evento quebrado: só vira failure_candidate com as cinco condições e sem limiar."""
    candidatas = [r for r in rules if r["then"] == FAILURE]
    if not candidatas:
        errors.append(f"{name}: nenhuma combinação dá {FAILURE}")
    for rule in candidatas:
        for entrada, esperado in FAILURE_REQUIRED.items():
            if rule["when"].get(entrada) is not esperado:
                errors.append(f"{name}: {FAILURE} exige {entrada}={str(esperado).lower()}, mas a linha {rule['when']} aceita {rule['when'].get(entrada)!r}")
    for entry in inputs:
        if any(isinstance(v, (int, float)) and not isinstance(v, bool) for v in entry["allowed_values"]):
            errors.append(f"{name}: a entrada {entry['name']} tem número em allowed_values; limiar é escolha do time e mora no Evento de coleta")


def conferir_documento(name: str, doc: dict) -> None:
    if not conferir_campos(name, doc, "decisao", ("required_inputs", "decision_table", "possible_outputs")):
        return
    inputs = doc["required_inputs"]
    columns = [entry["name"] for entry in inputs]
    rules = doc["decision_table"]
    if not conferir_linhas(name, rules, columns):
        return
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
    for combination in product(*(entry["allowed_values"] for entry in inputs)):
        classify(dict(zip(columns, combination)))
        seen += 1
    for case in doc.get("tests", []):
        observed = classify(case["inputs"])
        if observed != case["expected_outcome"]:
            errors.append(f"{name}: teste {case['inputs']}: esperado {case['expected_outcome']}, observado {observed}")
    if FAILURE in possible_outputs:
        conferir_failure_candidate(name, rules, inputs)
    summary.append(f"{name}: {seen} combinações, {len(doc.get('tests', []))} casos")


for name in FILES:
    doc = carregar_yaml(DL / name, relatorio)
    if doc is not None:
        conferir_documento(name, doc)

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
