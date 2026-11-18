#!/usr/bin/env python3
"""Validador de navegação: nenhuma página órfã, nenhum passo do percurso sem próximo passo.

Lê astro.config.mjs (menu e redirecionamentos), src/data/*.yaml e as páginas de src/content/docs.
Funções puras no topo; `executar` junta tudo e `main` imprime o resultado.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (ROOT, Entrada, Modelo, Passo, Relatorio, carregar_entradas, carregar_modelos,  # noqa: E402
                   carregar_percurso, resolver_link, rota_da_pagina)

GRUPO_DO_PERCURSO = "Percurso"
ORDEM_DOS_NIVEIS = {"nucleo": 0, "segundo": 1, "complementar": 2}
PREFIXO_DO_SITE = "/contexto-framework"
_LINK_MARKDOWN = re.compile(r"\]\(([^)\s]+)")
_LINK_HREF = re.compile(r"""\bhref\s*=\s*["']([^"']+)["']""")
_CERCA = re.compile(r"^\s*```", re.M)
_CERCA_YAML = re.compile(r"^\s*```ya?ml\b", re.M | re.I)
_PAR_ORIGEM_DESTINO = re.compile(r"""['"]/([^'"]*?)/?['"]\s*:\s*[`'"](?:\$\{base\})?/?([^`'"]*?)/?[`'"]""")


def chave(rota: str) -> str:
    """Identificador de página: a rota sem barras nas pontas; a página inicial é '/'."""
    return rota.strip("/") or "/"


# ---------- leitura do astro.config.mjs ----------
def _fim_do_bloco(texto: str, inicio: int, abre: str, fecha: str) -> int:
    """Índice do fecho que casa com o `abre` anterior a `inicio`, ignorando strings e comentários."""
    nivel, i = 1, inicio
    while i < len(texto):
        c = texto[i]
        if texto.startswith("//", i):
            i = texto.find("\n", i)
            if i < 0:
                break
        elif c in "'\"`":
            i = _fim_da_string(texto, i)
        elif c == abre:
            nivel += 1
        elif c == fecha:
            nivel -= 1
            if nivel == 0:
                return i
        i += 1
    return -1


def _fim_da_string(texto: str, inicio: int) -> int:
    aspas, i = texto[inicio], inicio + 1
    while i < len(texto) and texto[i] != aspas:
        i += 2 if texto[i] == "\\" else 1
    return i


def _bloco(config: str, marcador: str, abre: str, fecha: str) -> str:
    achado = next((m for m in re.finditer(marcador, config)
                   if "//" not in config[config.rfind("\n", 0, m.start()) + 1:m.start()]), None)
    if not achado:
        return ""
    fim = _fim_do_bloco(config, achado.end(), abre, fecha)
    return config[achado.end():fim] if fim >= 0 else ""


def bloco_do_menu(config: str) -> str:
    """Texto entre os colchetes de `sidebar: [ ... ]`, ou '' se não houver o bloco."""
    return _bloco(config, r"\bsidebar\s*:\s*\[", "[", "]")


@dataclass(frozen=True)
class Grupo:
    rotulo: str
    paginas: tuple[str, ...]
    subgrupos: tuple[Grupo, ...] = ()


def _simbolos(bloco: str) -> list[str]:
    """Quebra o trecho de JavaScript em strings (com aspas), pontuação e palavras."""
    padrao = r"""'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|`[^`]*`|//[^\n]*|[\[\]{}:,]|[^\s\[\]{}:,'"`]+"""
    return [s for s in re.findall(padrao, bloco) if not s.startswith("//")]


def _sem_aspas(simbolo: str) -> str:
    return simbolo[1:-1] if simbolo[0] in "'\"`" else simbolo


def _ler_lista(simbolos: list[str], i: int) -> tuple[list[Any], int]:
    itens: list[Any] = []
    while i < len(simbolos) and simbolos[i] != "]":
        if simbolos[i] == ",":
            i += 1
            continue
        valor, i = _ler_valor(simbolos, i)
        itens.append(valor)
    return itens, i + 1


def _ler_mapa(simbolos: list[str], i: int) -> tuple[dict[str, Any], int]:
    mapa: dict[str, Any] = {}
    while i < len(simbolos) and simbolos[i] != "}":
        if i + 1 < len(simbolos) and simbolos[i + 1] == ":":
            nome = _sem_aspas(simbolos[i])
            mapa[nome], i = _ler_valor(simbolos, i + 2)
        else:
            i += 1
    return mapa, i + 1


def _ler_valor(simbolos: list[str], i: int) -> tuple[Any, int]:
    """Lê um valor (lista, mapa ou texto) a partir de `i`; devolve o valor e o próximo índice."""
    if i >= len(simbolos):
        return "", i
    if simbolos[i] == "[":
        return _ler_lista(simbolos, i + 1)
    if simbolos[i] == "{":
        return _ler_mapa(simbolos, i + 1)
    return _sem_aspas(simbolos[i]), i + 1


def _grupo_de(item: Any) -> Grupo:
    if isinstance(item, str):
        return Grupo("", (chave(item),))
    if not isinstance(item, dict):
        return Grupo("", ())
    paginas: list[str] = []
    subgrupos: list[Grupo] = []
    if isinstance(item.get("link"), str):
        paginas.append(chave(item["link"]))
    for filho in item.get("items", []) if isinstance(item.get("items"), list) else []:
        if isinstance(filho, str):
            paginas.append(chave(filho))
        else:
            sub = _grupo_de(filho)
            subgrupos.append(sub)
            paginas.extend(sub.paginas)
    rotulo = item.get("label")
    return Grupo(rotulo if isinstance(rotulo, str) else "", tuple(paginas), tuple(subgrupos))


def grupos_do_menu(bloco: str) -> list[Grupo]:
    """Grupos de topo do menu, com rótulo, páginas em ordem (inclui as dos subgrupos) e subgrupos."""
    simbolos = _simbolos(bloco)
    itens, i = [], 0
    while i < len(simbolos):
        if simbolos[i] == ",":
            i += 1
            continue
        valor, i = _ler_valor(simbolos, i)
        itens.append(valor)
    return [_grupo_de(item) for item in itens]


def redirecionamentos(config: str) -> dict[str, str]:
    """Mapa origem -> destino do bloco `redirects`, ambos como chaves de página (sem barras nas pontas)."""
    bloco = _bloco(config, r"\bredirects\s*:\s*\{", "{", "}")
    pares = {}
    for origem, destino in _PAR_ORIGEM_DESTINO.findall(bloco):
        pares[chave(origem)] = chave(destino.removeprefix(PREFIXO_DO_SITE))
    return pares


# ---------- links das páginas ----------
def _sem_codigo(texto: str) -> str:
    """Remove os blocos cercados por ``` (exemplos de código não são links da página)."""
    partes = _CERCA.split(texto)
    return "\n".join(partes[::2])


def _rota_absoluta(caminho: str) -> str:
    partes = [p for p in caminho.split("/") if p]
    return "/" + "/".join(partes) + ("/" if partes else "")


def links_internos(texto_mdx: str, rota: str) -> set[str]:
    """Rotas internas (com barras nas pontas) citadas por links markdown e atributos href."""
    destinos: set[str] = set()
    texto = _sem_codigo(texto_mdx)
    for url in [*_LINK_MARKDOWN.findall(texto), *_LINK_HREF.findall(texto)]:
        if url.startswith(PREFIXO_DO_SITE + "/"):
            url = url[len(PREFIXO_DO_SITE):]
        if url.startswith("/") and not url.startswith("//"):
            absoluta = _rota_absoluta(url.split("#")[0].split("?")[0])
            if "." not in absoluta.rsplit("/", 2)[-2]:
                destinos.add(absoluta)
            continue
        destino, _ = resolver_link(rota, url)
        if destino:
            destinos.add(destino)
    return destinos


# ---------- regras ----------
def paginas_orfas(paginas: set[str], menu: set[str], links: dict[str, set[str]]) -> list[str]:
    """Páginas fora do menu e sem link vindo de outra página (link para si mesma não conta)."""
    recebem = {destino for origem, alvos in links.items() for destino in alvos if destino != origem}
    return sorted(p for p in paginas if p not in menu and p not in recebem)


def passos_sem_saida(passos: tuple[Passo, ...] | list[Passo], textos: dict[str, str]) -> list[str]:
    """Páginas do percurso que existem mas não trazem o componente <NextStep."""
    return [chave(p.pagina) for p in passos if chave(p.pagina) in textos and "<NextStep" not in textos[chave(p.pagina)]]


def yaml_no_percurso(texto: str) -> list[int]:
    """Linhas (a partir de 1) com cerca ```yaml, ```yml ou <ExampleDoc: YAML não entra no percurso."""
    return [n for n, linha in enumerate(texto.splitlines(), start=1)
            if _CERCA_YAML.match(linha) or "<ExampleDoc" in linha]


def ordem_dos_modelos(paginas_do_grupo: list[str] | tuple[str, ...], modelos: list[Modelo]) -> list[str]:
    """Erros se um modelo aparece depois de outro de nível mais distante (núcleo, segundo, complementar)."""
    nivel_de = {f"templates/{m.pagina}": m for m in modelos}
    erros: list[str] = []
    maior: Modelo | None = None
    for pagina in paginas_do_grupo:
        atual = nivel_de.get(pagina)
        if atual is None:
            continue
        if maior and ORDEM_DOS_NIVEIS[atual.nivel] < ORDEM_DOS_NIVEIS[maior.nivel]:
            erros.append(f"ordem dos modelos: {atual.slug} ({atual.nivel}) vem depois de {maior.slug} ({maior.nivel})")
        elif maior is None or ORDEM_DOS_NIVEIS[atual.nivel] > ORDEM_DOS_NIVEIS[maior.nivel]:
            maior = atual
    return erros


def percurso_no_menu(grupos: list[Grupo], passos: tuple[Passo, ...] | list[Passo]) -> list[str]:
    """O grupo Percurso do menu tem exatamente as páginas de percurso.yaml, na mesma ordem."""
    esperado = tuple(chave(p.pagina) for p in passos)
    grupo = next((g for g in grupos if g.rotulo == GRUPO_DO_PERCURSO), None)
    if grupo is None:
        return [f"o menu não tem o grupo {GRUPO_DO_PERCURSO}"]
    if grupo.paginas != esperado:
        return [f"o grupo {GRUPO_DO_PERCURSO} do menu ({', '.join(grupo.paginas)}) difere de percurso.yaml ({', '.join(esperado)})"]
    return []


def titulos_do_percurso(passos: tuple[Passo, ...] | list[Passo], titulos: dict[str, str]) -> list[str]:
    """O titulo de cada passo em percurso.yaml é igual ao title da página."""
    erros: list[str] = []
    for passo in passos:
        pagina = chave(passo.pagina)
        if pagina not in titulos:
            erros.append(f"o passo {passo.numero} aponta para a página {pagina}, que não existe")
        elif titulos[pagina] != passo.titulo:
            erros.append(f"passo {passo.numero}: titulo \"{passo.titulo}\" difere do title da página {pagina} (\"{titulos[pagina]}\")")
    return erros


def destinos(entradas: list[Entrada], depois_do_ultimo: str, redirects: dict[str, str], paginas: set[str]) -> list[str]:
    """Destinos de entradas.yaml, de depois_do_ultimo e dos redirecionamentos precisam existir."""
    erros = [f"entrada \"{e.sintoma}\" aponta para a página {chave(e.pagina)}, que não existe"
             for e in entradas if chave(e.pagina) not in paginas]
    if depois_do_ultimo and chave(depois_do_ultimo) not in paginas:
        erros.append(f"depois_do_ultimo aponta para a página {chave(depois_do_ultimo)}, que não existe")
    for origem, alvo in redirects.items():
        if alvo not in paginas:
            erros.append(f"redirecionamento de {origem} para a página {alvo}, que não existe")
        if origem in paginas:
            erros.append(f"redirecionamento com origem {origem}, que ainda é uma página")
    return erros


# ---------- execução ----------
def _titulo(texto: str) -> str | None:
    cabecalho = re.match(r"\A---\r?\n(.*?)\r?\n---", texto, re.S)
    try:
        front = yaml.safe_load(cabecalho.group(1)) if cabecalho else None
    except yaml.YAMLError:
        return None
    titulo = front.get("title") if isinstance(front, dict) else None
    return titulo if isinstance(titulo, str) else None


def _grupo_dos_modelos(grupos: list[Grupo], modelos: list[Modelo]) -> tuple[str, ...]:
    """Páginas do grupo de topo com mais modelos (é onde a ordem núcleo, segundo, complementar vale)."""
    alvo = {f"templates/{m.pagina}" for m in modelos}
    melhor = max(grupos, key=lambda g: sum(p in alvo for p in g.paginas), default=None)
    return melhor.paginas if melhor else ()


def executar(raiz: Path, relatorio: Relatorio) -> tuple[int, int, int]:
    """Roda todas as regras sobre a árvore em `raiz`. Devolve (páginas, no menu, passos do percurso)."""
    docs, dados = raiz / "src" / "content" / "docs", raiz / "src" / "data"
    arquivos = sorted([*docs.rglob("*.md"), *docs.rglob("*.mdx")])
    textos = {chave(rota_da_pagina(a, docs)): a.read_text(encoding="utf-8") for a in arquivos}
    modelos = carregar_modelos(dados / "modelos.yaml", relatorio)
    percurso = carregar_percurso(dados / "percurso.yaml", relatorio)
    entradas = carregar_entradas(dados / "entradas.yaml", relatorio)
    config = (raiz / "astro.config.mjs").read_text(encoding="utf-8")
    bloco = bloco_do_menu(config)
    if not bloco:
        relatorio.erro(raiz / "astro.config.mjs", "bloco 'sidebar: [' não encontrado; a navegação não foi verificada")
    grupos = grupos_do_menu(bloco)
    menu = {p for g in grupos for p in g.paginas}
    paginas = set(textos)
    links = {k: {chave(r) for r in links_internos(t, "/" + k + "/" if k != "/" else "/")} for k, t in textos.items()}
    avisos_e_erros = [
        *(f"página órfã: {p} (fora do menu e sem link de outra página)" for p in paginas_orfas(paginas, menu, links)),
        *(f"próximo passo ausente: {p} não tem <NextStep" for p in passos_sem_saida(percurso.passos, textos)),
        *(f"YAML no percurso: {chave(p.pagina)} linha {n}" for p in percurso.passos
          for n in yaml_no_percurso(textos.get(chave(p.pagina), ""))),
        *ordem_dos_modelos(_grupo_dos_modelos(grupos, modelos), modelos),
        *percurso_no_menu(grupos, percurso.passos),
        *titulos_do_percurso(percurso.passos, {k: _titulo(t) or "" for k, t in textos.items()}),
        *destinos(entradas, percurso.depois_do_ultimo, redirecionamentos(config), paginas),
    ]
    for mensagem in avisos_e_erros:
        relatorio.erro(None, mensagem)
    no_percurso = {chave(p.pagina) for p in percurso.passos}
    for pagina in sorted(paginas - no_percurso):
        if not {d for d in links[pagina] if d != pagina}:
            relatorio.aviso(None, f"página sem link interno de saída: {pagina}")
    return len(paginas), len(menu & paginas), len(percurso.passos)


def main() -> None:
    relatorio = Relatorio()
    relatorio.instalar()
    paginas, no_menu, passos = executar(ROOT, relatorio)
    relatorio.encerrar(f"OK: {paginas} páginas, {no_menu} no menu, {passos} passos do percurso, 0 órfãs.")


if __name__ == "__main__":
    main()
