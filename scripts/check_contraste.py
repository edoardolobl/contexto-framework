#!/usr/bin/env python3
"""Confere o contraste (WCAG 2.x) dos pares de tokens de src/data/contraste.yaml em src/styles/custom.css.

O tema escuro é o padrão (todos os blocos ':root { }' juntos). O tema claro aplica por cima
':root[data-theme="light"]'. Valores com var(--x) são resolvidos; só se aceita cor em hex no fim.
"""
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from comum import DADOS, ROOT, Relatorio, carregar_yaml

CSS = ROOT / "src" / "styles" / "custom.css"
PARES = DADOS / "contraste.yaml"
MINIMO_DE_PARES = 5
TEMAS = ("escuro", "claro")
ROTULO_DO_TEMA = {"escuro": "tema escuro", "claro": "tema claro"}

BLOCO_ESCURO = re.compile(r":root\s*\{([^{}]*)\}")
BLOCO_CLARO = re.compile(r""":root\[data-theme=(['"])light\1\]\s*\{([^{}]*)\}""")
DECLARACAO = re.compile(r"(--[\w-]+)\s*:\s*([^;]+?)\s*(?:;|$)")
VAR = re.compile(r"^var\(\s*(--[\w-]+)\s*\)$")
HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


class TokenInvalido(ValueError):
    """Token ausente, em ciclo ou que não termina em cor hex."""


def hex_para_rgb(valor: str) -> tuple[int, int, int]:
    if not HEX.match(valor):
        raise ValueError(f"cor hex inválida: {valor!r}")
    corpo = valor[1:]
    if len(corpo) == 3:
        corpo = "".join(c * 2 for c in corpo)
    return int(corpo[0:2], 16), int(corpo[2:4], 16), int(corpo[4:6], 16)


def luminancia(rgb: tuple[int, int, int]) -> float:
    def canal(c: int) -> float:
        s = c / 255
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = (canal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def razao_de_contraste(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    claro, escuro = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (claro + 0.05) / (escuro + 0.05)


def _declaracoes(corpo: str) -> dict[str, str]:
    sem_comentarios = re.sub(r"/\*.*?\*/", "", corpo, flags=re.S)
    return {nome: valor.strip() for nome, valor in DECLARACAO.findall(sem_comentarios)}


def tokens_do_tema(css: str, tema: str) -> dict[str, str]:
    tokens: dict[str, str] = {}
    for corpo in BLOCO_ESCURO.findall(css):
        tokens.update(_declaracoes(corpo))
    if tema == "claro":
        for _aspas, corpo in BLOCO_CLARO.findall(css):
            tokens.update(_declaracoes(corpo))
    return tokens


def resolver(token: str, tokens: dict[str, str]) -> str:
    """Segue var(--x) até uma cor hex. Acusa token ausente, ciclo ou valor que não é hex."""
    visto: list[str] = []
    atual = token
    while True:
        if atual in visto:
            raise TokenInvalido(f"ciclo entre tokens: {' -> '.join(visto + [atual])}")
        visto.append(atual)
        if atual not in tokens:
            raise TokenInvalido(f"token {atual} ausente no CSS")
        valor = tokens[atual]
        referencia = VAR.match(valor)
        if referencia:
            atual = referencia.group(1)
            continue
        if not HEX.match(valor):
            raise TokenInvalido(f"token {atual} não termina em cor hex: {valor!r}")
        return valor


def _formatar(numero: float, casas: int = 2) -> str:
    return f"{numero:.{casas}f}".replace(".", ",").rstrip("0").rstrip(",") if casas else str(numero)


def verificar_pares(pares: list[dict[str, Any]], css: str) -> list[str]:
    erros: list[str] = []
    for par in pares:
        for tema in par.get("temas") or TEMAS:
            tokens = tokens_do_tema(css, tema)
            for fundo in par["fundos"]:
                erro = _verificar(par, fundo, tema, tokens)
                if erro:
                    erros.append(erro)
    return erros


def _verificar(par: dict[str, Any], fundo: str, tema: str, tokens: dict[str, str]) -> str | None:
    rotulo = ROTULO_DO_TEMA[tema]
    try:
        frente_rgb = hex_para_rgb(resolver(par["frente"], tokens))
        fundo_rgb = hex_para_rgb(resolver(fundo, tokens))
    except TokenInvalido as exc:
        return f"{rotulo}: par '{par['nome']}': {exc}"
    razao = razao_de_contraste(frente_rgb, fundo_rgb)
    minimo = float(par["minimo"])
    if razao + 1e-9 < minimo:
        # trunca (não arredonda) para nunca mostrar um valor que pareça passar
        mostrado = int(razao * 100) / 100
        return f"{rotulo}: {par['frente']} sobre {fundo} dá {_formatar(mostrado)}:1; mínimo {_formatar(minimo)}:1"
    return None


def _par_valido(item: Any, numero: int, caminho: Path, relatorio: Relatorio) -> dict[str, Any] | None:
    def falha(motivo: str) -> None:
        relatorio.erro(caminho, f"par {numero} {motivo}")

    if not isinstance(item, dict):
        falha("não é um mapa")
        return None
    if not isinstance(item.get("nome"), str) or not item["nome"]:
        falha("sem nome")
        return None
    if not isinstance(item.get("frente"), str) or not item["frente"].startswith("--"):
        falha("sem frente (um token, como --cor)")
        return None
    fundos = item.get("fundos")
    if not isinstance(fundos, list) or not fundos or not all(isinstance(f, str) for f in fundos):
        falha("sem fundos (lista de tokens)")
        return None
    minimo = item.get("minimo")
    if isinstance(minimo, bool) or not isinstance(minimo, (int, float)) or minimo <= 0:
        falha("tem minimo que deve ser um número positivo")
        return None
    temas = item.get("temas")
    if temas is not None and (not isinstance(temas, list) or not temas or any(t not in TEMAS for t in temas)):
        falha("tem temas que deve ser uma lista com escuro e/ou claro (tema desconhecido)")
        return None
    return item


def conferir(css_caminho: Path, pares_caminho: Path, relatorio: Relatorio) -> int:
    """Devolve quantos pares foram conferidos."""
    dados = carregar_yaml(pares_caminho, relatorio)
    try:
        css = css_caminho.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        relatorio.erro(css_caminho, f"não foi possível ler o CSS: {exc}")
        return 0
    if dados is None:
        return 0
    brutos = dados.get("pares")
    if not isinstance(brutos, list):
        relatorio.erro(pares_caminho, "'pares' deve ser uma lista")
        return 0
    pares = [p for n, item in enumerate(brutos, start=1) if (p := _par_valido(item, n, pares_caminho, relatorio))]
    if len(brutos) < MINIMO_DE_PARES:
        relatorio.erro(pares_caminho, f"esperado pelo menos {MINIMO_DE_PARES} pares, encontrado {len(brutos)}")
    for erro in verificar_pares(pares, css):
        relatorio.erro(css_caminho, erro)
    return len(pares)


def main() -> None:
    relatorio = Relatorio()
    relatorio.instalar()
    total = conferir(CSS, PARES, relatorio)
    relatorio.encerrar(f"OK: {total} pares de contraste conferidos nos temas escuro e claro.")


if __name__ == "__main__":
    main()
