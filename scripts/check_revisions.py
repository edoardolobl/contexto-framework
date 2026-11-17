#!/usr/bin/env python3
"""Verifica exemplos DIDÁTICOS de revisões e vigência sem simular um sistema RAG.

Uma versão citada no changelog não equivale a um snapshot histórico recuperável.
"""
from collections import defaultdict
from datetime import date
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "public" / "downloads"
FILES = sorted(DL.glob("exemplo-*.yaml")) + sorted((DL / "historico").glob("*.yaml"))

errors = []
revisions = {}
grouped = defaultdict(list)


def err(path, reason):
    errors.append(f"{path.relative_to(ROOT)}: {reason}")


def day(path, value, field):
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        err(path, f"{field}: data inválida, esperado AAAA-MM-DD")
        return None


for path in FILES:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    stable = data.get("id")
    version = str(data.get("version"))
    rev = data.get("revision_id")
    if rev != f"{stable}@{version}":
        err(path, "revision_id deve ser formado por id@version")
    if rev in revisions:
        err(path, f"revision_id repetido no arquivo {revisions[rev]['path'].name}")
    else:
        revisions[rev] = {"path": path, "data": data}
    grouped[stable].append((path, data))

    created = day(path, data.get("version_date"), "version_date")
    start = day(path, data.get("valid_from"), "valid_from")
    end = day(path, data.get("valid_to"), "valid_to")

    history = data.get("version_history") or []
    if not history or str(history[0].get("version")) != version:
        err(path, "histórico deve começar pela versão representada no arquivo")
    elif day(path, history[0].get("date"), "version_history[0].date") != created:
        err(path, "data do histórico atual difere de version_date")

    previous = data.get("supersedes_revision")
    if previous and (previous == rev or not previous.startswith(stable + "@")):
        err(path, "supersedes_revision deve apontar uma revisão anterior do mesmo assunto")
    if previous and not any(stable + "@" + str(x.get("version")) == previous for x in history[1:]):
        err(path, "revisão substituída precisa constar no histórico")

    approved = data.get("status") == "approved"
    if approved:
        if not start:
            err(path, "revisão aprovada precisa de valid_from")
        if created and start and start < created:
            err(path, "valid_from anterior à emissão; declarar retroatividade em registro próprio se existir")
        if end and start and end <= start:
            err(path, "valid_to deve ser posterior a valid_from")
    elif start or end:
        err(path, "rascunho pendente não deve se passar por regra vigente")
    if data.get("status") != "approved" and previous:
        err(path, "rascunho inicial não deve afirmar que substitui uma revisão aprovada")


for stable, items in grouped.items():
    approved = []
    for path, data in items:
        if data.get("status") == "approved":
            approved.append((date.fromisoformat(data["valid_from"]),
                             date.fromisoformat(data["valid_to"]) if data.get("valid_to") else None,
                             path, data))
    approved.sort(key=lambda x: x[0])
    for earlier, later in zip(approved, approved[1:]):
        if earlier[1] is None or earlier[1] > later[0]:
            err(later[2], f"vigência se sobrepõe à revisão {earlier[3]['revision_id']}")


def select(stable, as_of):
    """Consulta documental ilustrativa; não simula recuperação ou controle de acesso."""
    target = date.fromisoformat(as_of)
    found = []
    for path, data in grouped[stable]:
        if data.get("status") != "approved" or not data.get("valid_from"):
            continue
        start = date.fromisoformat(data["valid_from"])
        end = date.fromisoformat(data["valid_to"]) if data.get("valid_to") else None
        if start <= target and (end is None or target < end):
            found.append(data["revision_id"])
    return found


expectations = [
    ("CONCEPT-ONBOARDING-001", "2026-07-25", []),
    ("CONCEPT-ONBOARDING-001", "2026-08-20", ["CONCEPT-ONBOARDING-001@1.0"]),
    ("CONCEPT-ONBOARDING-001", "2026-09-01", ["CONCEPT-ONBOARDING-001@2.0"]),
    ("KPI-AURORA-001", "2026-08-20", ["KPI-AURORA-001@1.0"]),
    ("KPI-AURORA-001", "2026-09-15", ["KPI-AURORA-001@2.0"]),
]
for stable, as_of, expected in expectations:
    actual = select(stable, as_of)
    if actual != expected:
        errors.append(f"Seleção histórica {stable} em {as_of}: esperado {expected}, obtido {actual}")


# Uma resposta calculada sobre dados de 01/10 não deveria ter sido aprovada em setembro.
qa = revisions.get("QA-AURORA-001@1.1")
if qa:
    path, data = qa["path"], qa["data"]
    sample_date = date(2026, 10, 1)
    for q in data.get("questions", []):
        reviewed = day(path, q.get("reviewed_at"), f"{q.get('id')}.reviewed_at")
        if reviewed and reviewed < sample_date:
            err(path, f"{q.get('id')}: revisão anterior aos dados sintéticos referenciados")
    if date.fromisoformat(data["version_date"]) < sample_date:
        err(path, "gabarito aprovado antes da data da amostra usada na avaliação")


# A revisão histórica e a atual do conceito devem diferir APENAS na
# janela temporal, sem alterar silenciosamente exclusões ou elegibilidade.
import re

historico_conceito = revisions.get("CONCEPT-ONBOARDING-001@1.0", {}).get("data")
atual_conceito = revisions.get("CONCEPT-ONBOARDING-001@2.0", {}).get("data")

def normalizar_janela(value):
    if isinstance(value, str):
        return re.sub(r"\b(?:30|60) dias\b", "N dias", value)
    if isinstance(value, list):
        return [normalizar_janela(item) for item in value]
    return value

if not historico_conceito or not atual_conceito:
    errors.append("Faltam revisões 1.0 e 2.0 do conceito fictício para comparar")
else:
    campos = (
        ("definition", historico_conceito["definition"], atual_conceito["definition"]),
        ("inclusion_criteria", historico_conceito["inclusion_criteria"], atual_conceito["inclusion_criteria"]),
        ("exclusion_criteria", historico_conceito["exclusion_criteria"], atual_conceito["exclusion_criteria"]),
        ("not_synonyms", historico_conceito["vocabulary"]["not_synonyms"], atual_conceito["vocabulary"]["not_synonyms"]),
    )
    for campo, antigo, novo in campos:
        if normalizar_janela(antigo) != normalizar_janela(novo):
            errors.append(f"Conceito Aurora: {campo} diverge além da janela de atividade")
    if "60 dias" not in historico_conceito["definition"] or "30 dias" not in atual_conceito["definition"]:
        errors.append("Conceito Aurora: revisão 1.0 deve ter 60 dias e revisão 2.0, 30")
    if historico_conceito["valid_to"] != atual_conceito["valid_from"]:
        errors.append("Conceito Aurora: períodos de validade não se conectam corretamente")


if errors:
    for error in errors:
        print("ERRO:", error)
    sys.exit(1)

print(f"OK: {len(FILES)} registros, IDs de revisão únicos, intervalos não sobrepostos, "
      "duas revisões históricas integrais e cinco seleções temporais verificadas.")
