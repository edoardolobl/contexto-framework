#!/usr/bin/env python3
"""Confere o HTML gerado em dist/: um h1, títulos sem salto, og:image e theme-color.

Páginas sem <main> (como as de redirecionamento) são ignoradas.
"""
from __future__ import annotations

from html.parser import HTMLParser
import os
from pathlib import Path
import sys
from urllib.parse import urlparse

from comum import ROOT, Relatorio

DIST = ROOT / "dist"
TITULOS = {f"h{n}": n for n in range(1, 7)}


def base_path() -> str:
    """Mesma regra de BASE_PATH de check_built_links.py."""
    base = "/" + os.environ.get("BASE_PATH", "/contexto-framework").strip("/")
    return "" if base == "/" else base


class Leitor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tem_main = False
        self.dentro_do_main = 0
        self.titulos: list[int] = []
        self.og_image: list[str] = []
        self.theme_color = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        atributos = dict(attrs)
        if tag == "main":
            self.tem_main = True
            self.dentro_do_main += 1
        elif tag in TITULOS and self.dentro_do_main:
            self.titulos.append(TITULOS[tag])
        elif tag == "meta":
            if atributos.get("property") == "og:image":
                self.og_image.append(atributos.get("content") or "")
            if atributos.get("name") == "theme-color":
                self.theme_color += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "main" and self.dentro_do_main:
            self.dentro_do_main -= 1


def _erros_de_titulos(titulos: list[int]) -> list[str]:
    erros = []
    if titulos.count(1) != 1:
        erros.append(f"dentro de <main> deve haver exatamente um h1, encontrado {titulos.count(1)}")
    for anterior, atual in zip(titulos, titulos[1:]):
        if atual > anterior + 1:
            erros.append(f"título h{atual} logo depois de h{anterior}: não pule níveis")
    return erros


def _erros_de_og_image(imagens: list[str], dist: Path, base: str) -> list[str]:
    if len(imagens) != 1:
        return [f"deve haver exatamente um meta og:image, encontrado {len(imagens)}"]
    url = urlparse(imagens[0])
    caminho = url.path
    proprio_site = (not url.netloc) or (base and (caminho == base or caminho.startswith(base + "/")))
    if not proprio_site or not caminho:
        return []
    if base and (caminho == base or caminho.startswith(base + "/")):
        caminho = caminho[len(base):]
    elif url.netloc:
        return []
    alvo = dist / caminho.lstrip("/")
    return [] if alvo.is_file() else [f"og:image aponta para {imagens[0]}, mas o arquivo não existe em dist/"]


def checar_pagina(html: str, dist: Path, base: str) -> list[str]:
    leitor = Leitor()
    leitor.feed(html)
    if not leitor.tem_main:
        return []
    erros = _erros_de_titulos(leitor.titulos)
    erros += _erros_de_og_image(leitor.og_image, dist, base)
    if leitor.theme_color < 1:
        erros.append("falta meta theme-color")
    return erros


def conferir(dist: Path) -> list[str]:
    if not dist.is_dir():
        return ["dist/ não existe. Rode npm run build antes."]
    erros = []
    base = base_path()
    for pagina in sorted(dist.rglob("*.html")):
        try:
            html = pagina.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            erros.append(f"{pagina.relative_to(dist).as_posix()}: não foi possível ler: {exc}")
            continue
        rel = pagina.relative_to(dist).as_posix()
        erros += [f"{rel}: {e}" for e in checar_pagina(html, dist, base)]
    return erros


def main() -> None:
    erros = conferir(DIST)
    if erros:
        print("\n".join("ERRO: " + e for e in erros))
        sys.exit(1)
    print("OK: HTML gerado conferido (um h1, títulos em ordem, og:image e theme-color).")


if __name__ == "__main__":
    main()
