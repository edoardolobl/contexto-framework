#!/usr/bin/env python3
"""Validações editoriais leves; não substituem o build nem a validação humana."""
from pathlib import Path
from posixpath import normpath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "src" / "content" / "docs"
PAGES = sorted([*DOCS.rglob("*.md"), *DOCS.rglob("*.mdx")])
errors = []

def route(path):
    rel = path.relative_to(DOCS)
    parts = list(rel.parts)
    parts[-1] = path.stem
    if parts[-1] == "index":
        parts.pop()
    return "/" + "/".join(parts) + ("/" if parts else "")

routes = {route(p): p for p in PAGES}

for path in PAGES:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n") or "\n---\n" not in content[4:]:
        errors.append(f"{path.relative_to(ROOT)}: frontmatter YAML ausente")
        continue
    front = content.split("---\n", 2)[1]
    for required in ("title", "description"):
        if not re.search(rf"^{required}:\s*\S+", front, re.M):
            errors.append(f"{path.relative_to(ROOT)}: campo {required} ausente")
    for url in re.findall(r"\]\(([^)]+)\)", content):
        if re.match(r"^(https?:|mailto:|#|/)", url):
            continue
        rel_url = url.split("#")[0].split("?")[0]
        if not rel_url:
            continue
        if rel_url.endswith((".yaml", ".md", ".pdf")) and "downloads" in rel_url:
            continue
        if "{" in rel_url or "}" in rel_url:
            continue
        target = normpath(route(path) + rel_url)
        target = "/" + target.strip("/") + "/" if target.strip("/") else "/"
        if target not in routes:
            errors.append(f"{path.relative_to(ROOT)}: link interno não encontrado {url} => {target}")

try:
    import yaml
    for path in sorted((ROOT / "public" / "downloads").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf8"))
        if not isinstance(data, dict) or not all(key in data for key in ("type", "status")):
            errors.append(f"{path.relative_to(ROOT)}: YAML sem type/status")
except ImportError:
    print("AVISO: PyYAML ausente; exemplos YAML não foram validados.")
except Exception as exc:
    errors.append(f"Falha ao validar YAML: {exc}")

if errors:
    print("\n".join("ERRO: " + error for error in errors))
    sys.exit(1)
print(f"OK: {len(PAGES)} páginas verificadas; metadados, links e exemplos YAML checados.")
