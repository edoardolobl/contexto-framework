#!/usr/bin/env python3
"""Verifica exemplos DIDÁTICOS de revisões e vigência sem simular um sistema RAG.

Uma versão citada no changelog não equivale a um snapshot histórico recuperável.
"""
from collections import defaultdict
from datetime import date
from pathlib import Path
import re

from comum import DOWNLOADS as DL, Relatorio, carregar_yaml, exigir_minimo

relatorio = Relatorio()
relatorio.instalar()
FILES = (exigir_minimo(DL.glob("exemplo-*.yaml"), 20, "exemplos YAML", relatorio)
         + exigir_minimo((DL / "historico").glob("*.yaml"), 2, "versões históricas em historico/", relatorio))

errors = relatorio.erros
revisions = {}
grouped = defaultdict(list)
documents: dict[Path, dict] = {}
for _path in FILES:
    _data = carregar_yaml(_path, relatorio)
    if _data is not None:
        documents[_path] = _data


def err(path: Path, reason: str) -> None:
    relatorio.erro(path, reason)


def day(path, value, field):
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        err(path, f"{field}: data inválida, esperado AAAA-MM-DD")
        return None


for path, data in documents.items():
    relatorio.arquivo_atual = path
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

    raw_history = data.get("version_history") or []
    if not all(isinstance(h, dict) for h in raw_history):
        err(path, "version_history deve conter só mapas")
    history = [h for h in raw_history if isinstance(h, dict)]
    if not history or str(history[0].get("version")) != version:
        err(path, "histórico deve começar pela versão representada no arquivo")
    elif day(path, history[0].get("date"), "version_history[0].date") != created:
        err(path, "data do histórico atual difere de version_date")

    previous = data.get("supersedes_revision")
    if previous and (previous == rev or not str(previous).startswith(f"{stable}@")):
        err(path, "supersedes_revision deve apontar uma revisão anterior do mesmo assunto")
    if previous and not any(f"{stable}@{x.get('version')}" == previous for x in history[1:]):
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
        start = day(path, data.get("valid_from"), "valid_from")
        if data.get("status") == "approved" and start:
            approved.append((start, day(path, data.get("valid_to"), "valid_to"), path, data))
    approved.sort(key=lambda x: x[0])
    for earlier, later in zip(approved, approved[1:]):
        if earlier[1] is None or earlier[1] > later[0]:
            err(later[2], f"vigência se sobrepõe à revisão {earlier[3]['revision_id']}")


def select(stable, as_of):
    """Consulta documental ilustrativa; não simula recuperação ou controle de acesso."""
    target = date.fromisoformat(as_of)
    found = []
    for path, data in grouped[stable]:
        start = day(path, data.get("valid_from"), "valid_from")
        if data.get("status") != "approved" or not start:
            continue
        end = day(path, data.get("valid_to"), "valid_to")
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


# Documento datado antes de 01/10 não pode citar a amostra de 01/10 nem o gabarito, que nasceram nesse dia.
LAB_DAY = date(2026, 10, 1)
for path, data in documents.items():
    created = day(path, data.get("version_date"), "version_date")
    if created and created < LAB_DAY:
        body = "\n".join(l for l in path.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#"))
        for marker in ("2026-10-01", "01/10", "QA-AURORA-001"):
            if marker in body:
                err(path, f"versão de {created.isoformat()} cita {marker}, que só existe a partir de 01/10")

# Uma resposta calculada sobre dados de 01/10 não deveria ter sido aprovada em setembro.
qa = next((r for k, r in revisions.items() if k.startswith("QA-AURORA-001@") and r["data"].get("status") == "approved"), None)
if not qa:
    errors.append("Gabarito QA-AURORA-001 aprovado não encontrado")
else:
    path, data = qa["path"], qa["data"]
    sample_date = date(2026, 10, 1)
    for q in data.get("questions", []):
        reviewed = day(path, q.get("reviewed_at"), f"{q.get('id')}.reviewed_at")
        if reviewed and reviewed < sample_date:
            err(path, f"{q.get('id')}: revisão anterior aos dados sintéticos referenciados")
    qa_date = day(path, data.get("version_date"), "version_date")
    if qa_date and qa_date < sample_date:
        err(path, "gabarito aprovado antes da data da amostra usada na avaliação")


# A revisão histórica e a atual do conceito devem diferir APENAS na
# janela temporal, sem alterar silenciosamente exclusões ou elegibilidade.
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


relatorio.encerrar(f"OK: {len(documents)} registros, IDs de revisão únicos, intervalos não sobrepostos, "
                   f"duas revisões históricas integrais e {len(expectations)} seleções temporais verificadas.")
