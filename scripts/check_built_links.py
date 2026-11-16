#!/usr/bin/env python3
"""Confere os links internos do site já gerado em dist/.

Roda depois de `npm run build`. Verifica o HTML final, incluindo links criados
por componentes, e falha se algum link interno sair do subcaminho publicado ou
apontar para um arquivo que não existe. Não confere URLs externas.
"""
from pathlib import Path
from posixpath import join, normpath
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BASE = "/" + os.environ.get("BASE_PATH", "/contexto-framework").strip("/")
BASE = "" if BASE == "/" else BASE

if not DIST.is_dir():
    print("ERRO: dist/ não existe. Rode `npm run build` antes.")
    sys.exit(1)

errors = []
checked = 0
for page in sorted(DIST.rglob("*.html")):
    html = page.read_text(encoding="utf-8")
    rel = page.relative_to(DIST).as_posix()
    page_url = BASE + "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
    for href in re.findall(r'<a\s[^>]*?href="([^"]+)"', html):
        if re.match(r"^(https?:|mailto:|#)", href):
            continue
        checked += 1
        target = href.split("#")[0].split("?")[0]
        resolved = target if target.startswith("/") else normpath(join(page_url, target))
        if BASE and not (resolved == BASE or resolved.startswith(BASE + "/")):
            errors.append(f"{rel}: link fora do subcaminho {BASE}: {href}")
            continue
        local = DIST / resolved[len(BASE):].lstrip("/")
        if not (local.is_file() or (local / "index.html").is_file()):
            errors.append(f"{rel}: destino inexistente: {href}")

if errors:
    print("\n".join("ERRO: " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK: {checked} links internos conferidos no HTML gerado.")
