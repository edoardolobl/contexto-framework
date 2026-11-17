#!/usr/bin/env python3
"""Confere os links internos do site já gerado em dist/.

Roda depois de `npm run build`. Verifica o HTML final, incluindo links criados
por componentes, e falha se algum link interno sair do subcaminho publicado,
apontar para um arquivo que não existe ou para uma âncora (#) que não existe
na página de destino. Não confere URLs externas.
"""
from __future__ import annotations

from pathlib import Path
from posixpath import join, normpath
import os
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
LINK = re.compile(r'<a\s[^>]*?href="([^"]+)"')
ID = re.compile(r'\sid="([^"]+)"')
EXTERNO = re.compile(r"^(https?:|mailto:)")


def base_path() -> str:
    base = "/" + os.environ.get("BASE_PATH", "/contexto-framework").strip("/")
    return "" if base == "/" else base


def _arquivo_de_destino(dist: Path, resolvido: str, base: str) -> Path | None:
    local = dist / resolvido[len(base):].lstrip("/")
    if local.is_file():
        return local
    indice = local / "index.html"
    return indice if indice.is_file() else None


class _Ids:
    """Ids de cada página, lidos uma vez só."""

    def __init__(self) -> None:
        self._cache: dict[Path, set[str]] = {}

    def de(self, pagina: Path) -> set[str]:
        if pagina not in self._cache:
            self._cache[pagina] = set(ID.findall(pagina.read_text(encoding="utf-8")))
        return self._cache[pagina]


def _erros_do_link(href: str, pagina: Path, page_url: str, dist: Path, base: str, ids: _Ids) -> list[str]:
    caminho, _, fragmento = href.partition("#")
    caminho = caminho.split("?")[0]
    if caminho:
        resolvido = caminho if caminho.startswith("/") else normpath(join(page_url, caminho))
        if base and not (resolvido == base or resolvido.startswith(base + "/")):
            return [f"link fora do subcaminho {base}: {href}"]
        destino = _arquivo_de_destino(dist, resolvido, base)
        if destino is None:
            return [f"destino inexistente: {href}"]
    else:
        destino = pagina
    if fragmento and unquote(fragmento) not in ids.de(destino):
        return [f"âncora inexistente: {href}"]
    return []


def conferir(dist: Path, base: str) -> tuple[list[str], int]:
    """Erros encontrados e quantidade de links internos conferidos."""
    erros: list[str] = []
    conferidos = 0
    ids = _Ids()
    for pagina in sorted(dist.rglob("*.html")):
        html = pagina.read_text(encoding="utf-8")
        rel = pagina.relative_to(dist).as_posix()
        page_url = base + "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
        for href in LINK.findall(html):
            if EXTERNO.match(href) or href == "#":
                continue
            conferidos += 1
            erros += [f"{rel}: {erro}" for erro in _erros_do_link(href, pagina, page_url, dist, base, ids)]
    return sorted(set(erros)), conferidos


def main() -> None:
    if not DIST.is_dir():
        print("ERRO: dist/ não existe. Rode `npm run build` antes.")
        sys.exit(1)
    erros, conferidos = conferir(DIST, base_path())
    if erros:
        print("\n".join("ERRO: " + e for e in erros))
        sys.exit(1)
    print(f"OK: {conferidos} links internos conferidos no HTML gerado, com as âncoras.")


if __name__ == "__main__":
    main()
