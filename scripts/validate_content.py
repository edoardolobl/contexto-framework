#!/usr/bin/env python3
"""Quality gates for the Contexto documentation, not certification of its business rules."""
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "src" / "content" / "docs"
DOWNLOADS = ROOT / "public" / "downloads"
TEMPLATE_COMPONENT = ROOT / "src" / "components" / "TemplateDownloads.astro"

PAGES = sorted([*DOCS.rglob("*.md"), *DOCS.rglob("*.mdx")])
REQUIRED_TYPES = ("kpi", "conceito", "processo", "decisao", "politica", "dataset", "relacionamento", "dashboard", "rubrica", "casos-teste")
VALID_STATUSES = {"draft", "pending_approval", "approved", "deprecated"}
errors: list[str] = []


def record(path: Path, msg: str):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def route(path: Path):
    rel = path.relative_to(DOCS)
    parts = list(rel.parts)
    parts[-1] = path.stem
    if parts[-1] == "index":
        parts.pop()
    return "/" + "/".join(parts) + ("/" if parts else "")


routes = {route(p): p for p in PAGES}

for path in PAGES:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
    if not match:
        record(path, "frontmatter YAML ausente")
        continue
    try:
        front = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        record(path, f"frontmatter YAML inválido: {exc}")
        continue
    if not isinstance(front, dict):
        record(path, "frontmatter não é um objeto")
        continue
    for required in ("title", "description"):
        if not isinstance(front.get(required), str) or not front[required].strip():
            record(path, f"campo obrigatório {required} ausente/vazio")

    # Simple Markdown link check: verify routes, not remote URLs.
    for url in re.findall(r"\]\(([^)]+)\)", content):
        if re.match(r"^(https?:|mailto:|#|/)", url):
            continue
        rel_url = url.split("#")[0].split("?")[0]
        if not rel_url or "{" in rel_url or "}" in rel_url:
            continue
        if "downloads" in rel_url and rel_url.endswith((".yaml", ".md", ".pdf")):
            file = DOWNLOADS / Path(rel_url).name
            if not file.exists():
                record(path, f"download inexistente: {url}")
            continue
        # Resolve o link como o navegador faria. Subir além da raiz do site é erro:
        # no GitHub Pages isso sai do subcaminho do projeto e resulta em 404.
        segments = [seg for seg in route(path).strip("/").split("/") if seg]
        escaped = False
        for seg in rel_url.split("/"):
            if seg in ("", "."):
                continue
            if seg == "..":
                if not segments:
                    escaped = True
                    break
                segments.pop()
            else:
                segments.append(seg)
        if escaped:
            record(path, f"link interno sobe além da raiz do site: {url}")
            continue
        target = "/" + "/".join(segments) + "/" if segments else "/"
        if target not in routes:
            record(path, f"link interno não encontrado: {url} => {target}")

seen_ids: dict[str, str] = {}
yaml_count = 0
for path in sorted(DOWNLOADS.glob("*.yaml")):
    yaml_count += 1
    try:
        data = yaml.safe_load(path.read_text(encoding="utf8"))
    except yaml.YAMLError as exc:
        record(path, f"YAML inválido: {exc}")
        continue
    if not isinstance(data, dict):
        record(path, "YAML deve ser mapa na raiz")
        continue
    if not data.get("type"):
        record(path, "campo type ausente")
    if data.get("status") not in VALID_STATUSES:
        record(path, f"status inválido: {data.get('status')}")
    if data.get("status") == "approved":
        for key in ("owner", "source_of_truth", "valid_from"):
            if data.get(key) in (None, "", []):
                record(path, f"documento approved sem {key}")
    if path.name.startswith("exemplo-"):
        if not data.get("id"):
            record(path, "exemplo sem identificador")
        elif data["id"] in seen_ids:
            record(path, f"identificador duplicado em {seen_ids[data['id']]}")
        else:
            seen_ids[data["id"]] = str(path.relative_to(ROOT))

markdown_count = 0
for path in sorted(DOWNLOADS.glob("*.md")):
    markdown_count += 1
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
    if not match:
        record(path, "template Markdown sem metadados")
        continue
    try:
        front = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        record(path, f"frontmatter inválido: {exc}")
        continue
    if not isinstance(front, dict) or not front.get("type") or front.get("status") not in VALID_STATUSES:
        record(path, "campos type ou status inválidos")

# Every download card must lead to an existing file.
component = TEMPLATE_COMPONENT.read_text(encoding="utf-8")
for filename in re.findall(r"href:\s*'([^']+)'", component):
    if not (DOWNLOADS / filename).is_file():
        record(TEMPLATE_COMPONENT, f"arquivo de download ausente: {filename}")

# Check the SQLite example links separately; they are not included in template cards.
analytics = ROOT / "src" / "components" / "AnalyticsLabDownloads.astro"
if analytics.exists():
    for filename in re.findall(r"file:\s*'([^']+)'", analytics.read_text(encoding="utf8")):
        if not (DOWNLOADS / filename).is_file():
            record(analytics, f"arquivo SQL não encontrado: {filename}")

for kind in REQUIRED_TYPES:
    for suffix in (".md", ".yaml"):
        expected = DOWNLOADS / f"template-{kind}{suffix}"
        if not expected.exists():
            record(TEMPLATE_COMPONENT, f"template anunciado não existe: {expected.name}")

if errors:
    print("\n".join("ERRO: " + error for error in errors))
    sys.exit(1)
print(f"OK: {len(PAGES)} páginas, {markdown_count} templates Markdown, "
      f"{yaml_count} arquivos YAML, rotas internas e downloads verificados.")
