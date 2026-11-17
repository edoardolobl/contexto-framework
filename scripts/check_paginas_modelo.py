#!/usr/bin/env python3
"""Confere a sequência didática das páginas de modelo (I-24, I-25, ADR 0017).

Para cada tipo de src/data/modelos.yaml, lê src/content/docs/templates/<pagina>.mdx, ignora os blocos
cercados por ``` e confere a ordem: resumo, '## O problema' com par contrastante, o bloco <Steps> com as
cinco etapas de estudo, e '## Baixe o modelo' como último h2, com os downloads só ali.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from comum import ROOT, Relatorio, carregar_modelos

H2_PROBLEMA = "## O problema"
H2_BAIXE = "## Baixe o modelo"
ETAPAS = ("comentado", "diagnostico", "complete", "caso-novo", "teste")
MINIMO_DE_EXERCICIOS = {"complete": 1, "teste": 2}
MINIMO_DE_DETAILS_OU_EXERCICIOS_NO_COMENTADO = 2
_H2 = re.compile(r"^## ")
_STEPS_ABRE = re.compile(r"^\s*<Steps\b")
_STEPS_FECHA = re.compile(r"^\s*</Steps>")
_ETAPA = re.compile(r"<EtapaDeEstudo\b")
_TIPO = re.compile(r"""\btipo=["']([^"']*)["']""")
_EXERCICIO = re.compile(r"<Exercicio\b")
_DETAILS = re.compile(r"<details\b")
Linha = tuple[int, str]


def linhas_fora_de_cerca(texto: str) -> list[Linha]:
    """(número da linha, texto) de cada linha fora de bloco ```; o número conta as linhas cercadas."""
    saida: list[Linha] = []
    cercado = False
    for numero, linha in enumerate(texto.replace("\r\n", "\n").split("\n"), start=1):
        if linha.lstrip().startswith("```"):
            cercado = not cercado
            continue
        if not cercado:
            saida.append((numero, linha))
    return saida


def _primeira(linhas: list[Linha], padrao: str | re.Pattern[str], depois_de: int = 0) -> int | None:
    for numero, texto in linhas:
        if numero > depois_de and (padrao.search(texto) if isinstance(padrao, re.Pattern) else padrao in texto):
            return numero
    return None


def _proximo_h2(linhas: list[Linha], depois_de: int) -> int | None:
    return next((n for n, t in linhas if n > depois_de and _H2.match(t)), None)


def _contar(linhas: list[Linha], padrao: re.Pattern[str]) -> int:
    return sum(len(padrao.findall(t)) for _, t in linhas)


def _entre(linhas: list[Linha], inicio: int, fim: int | None) -> list[Linha]:
    return [(n, t) for n, t in linhas if n >= inicio and (fim is None or n < fim)]


def _resumo_antes_do_problema(linhas: list[Linha], slug: str, problema: int | None) -> list[tuple[int, str]]:
    alvo = f'<TemplateStart kind="{slug}"'
    achado = _primeira(linhas, alvo)
    if achado is None:
        return [(problema or 1, f'falta {alvo} antes de "{H2_PROBLEMA}"')]
    if problema is not None and achado > problema:
        return [(achado, f'{alvo} deve vir antes de "{H2_PROBLEMA}"')]
    return []


def _problema_e_par(linhas: list[Linha]) -> tuple[int | None, list[tuple[int, str]]]:
    h2s = [n for n, t in linhas if t.rstrip() == H2_PROBLEMA]
    if len(h2s) != 1:
        onde = h2s[1] if len(h2s) > 1 else 1
        return (h2s[0] if h2s else None), [(onde, f'a página precisa de exatamente um "{H2_PROBLEMA}", achados {len(h2s)}')]
    inicio = h2s[0]
    fim = _proximo_h2(linhas, inicio)
    if _primeira(_entre(linhas, inicio, fim), "<ParContrastante") is None:
        return inicio, [(inicio, f'falta <ParContrastante antes do próximo h2 depois de "{H2_PROBLEMA}"')]
    return inicio, []


def _bloco_steps(linhas: list[Linha], problema: int) -> tuple[tuple[int, int] | None, list[tuple[int, str]]]:
    abre = next((n for n, t in linhas if n > problema and _STEPS_ABRE.match(t)), None)
    if abre is None:
        return None, [(problema, f'falta o bloco <Steps> depois de "{H2_PROBLEMA}"')]
    fecha = next((n for n, t in linhas if n > abre and _STEPS_FECHA.match(t)), None)
    if fecha is None:
        return None, [(abre, "o bloco <Steps> não tem o fechamento </Steps>")]
    return (abre, fecha), []


def _etapas_do_bloco(linhas: list[Linha], abre: int, fecha: int) -> tuple[dict[str, list[Linha]], list[tuple[int, str]]]:
    """Linhas de cada etapa (da abertura até a próxima etapa ou </Steps>) e os erros de tipo, contagem e ordem."""
    bloco = _entre(linhas, abre, fecha + 1)
    inicios = [(n, t) for n, t in bloco if _ETAPA.search(t)]
    erros: list[tuple[int, str]] = []
    achadas: list[tuple[int, str]] = []
    for n, t in inicios:
        tipo = _TIPO.search(t)
        if tipo is None or tipo.group(1) not in ETAPAS:
            erros.append((n, f'<EtapaDeEstudo sem tipo conhecido; use um de {", ".join(ETAPAS)}'))
        else:
            achadas.append((n, tipo.group(1)))
    conteudo: dict[str, list[Linha]] = {}
    for i, (n, tipo) in enumerate(achadas):
        proximo = inicios[i + 1][0] if i + 1 < len(inicios) else fecha
        conteudo.setdefault(tipo, _entre(linhas, n, proximo))
    for tipo in ETAPAS:
        vezes = [n for n, t in achadas if t == tipo]
        if not vezes:
            erros.append((abre, f'falta <EtapaDeEstudo tipo="{tipo}"> dentro de <Steps>'))
        elif len(vezes) > 1:
            erros.append((vezes[1], f'<EtapaDeEstudo tipo="{tipo}"> deve aparecer uma vez, achadas {len(vezes)}'))
    presentes = [t for _, t in achadas if t in ETAPAS]
    unicas = [t for t in dict.fromkeys(presentes)]
    if not erros and unicas != [t for t in ETAPAS if t in unicas]:
        erros.append((achadas[0][0], f'as etapas estão fora de ordem; a ordem é {", ".join(ETAPAS)}'))
    return conteudo, erros


def _conteudo_das_etapas(conteudo: dict[str, list[Linha]], slug: str) -> list[tuple[int, str]]:
    erros: list[tuple[int, str]] = []

    def inicio(tipo: str) -> int:
        return conteudo[tipo][0][0] if conteudo.get(tipo) else 1

    for tipo, sufixo in (("comentado", "completo"), ("diagnostico", "lacunas")):
        alvo = f'<ExampleDoc file="exemplo-{slug}-{sufixo}.yaml"'
        if tipo in conteudo and _primeira(conteudo[tipo], alvo) is None:
            erros.append((inicio(tipo), f'a etapa {tipo} precisa de {alvo}'))
    if "comentado" in conteudo:
        total = _contar(conteudo["comentado"], _DETAILS) + _contar(conteudo["comentado"], _EXERCICIO)
        if total < MINIMO_DE_DETAILS_OU_EXERCICIOS_NO_COMENTADO:
            erros.append((inicio("comentado"), f"a etapa comentado precisa de pelo menos {MINIMO_DE_DETAILS_OU_EXERCICIOS_NO_COMENTADO} "
                                               f"<details ou <Exercicio somados, achados {total}"))
    for tipo, minimo in MINIMO_DE_EXERCICIOS.items():
        if tipo in conteudo and (total := _contar(conteudo[tipo], _EXERCICIO)) < minimo:
            erros.append((inicio(tipo), f"a etapa {tipo} precisa de pelo menos {minimo} <Exercicio, achados {total}"))
    return erros


def _baixe_o_modelo(linhas: list[Linha], slug: str, fecha_steps: int | None, problema: int | None) -> tuple[int | None, list[tuple[int, str]]]:
    baixes = [n for n, t in linhas if t.rstrip() == H2_BAIXE]
    if len(baixes) != 1:
        return None, [(baixes[1] if len(baixes) > 1 else 1, f'a página precisa de exatamente um "{H2_BAIXE}", achados {len(baixes)}')]
    baixe = baixes[0]
    erros: list[tuple[int, str]] = []
    h2s = [n for n, t in linhas if _H2.match(t)]
    if h2s[-1] != baixe:
        erros.append((h2s[-1], f'"{H2_BAIXE}" deve ser o último h2 da página'))
    if fecha_steps is not None:
        if baixe < fecha_steps:
            erros.append((baixe, f'"{H2_BAIXE}" deve vir depois de </Steps>'))
        elif len([n for n in h2s if fecha_steps < n < baixe]) > 1:
            erros.append((baixe, f'entre </Steps> e "{H2_BAIXE}" cabe no máximo um h2 de triagem'))
    secao = _entre(linhas, baixe, None)
    alvo = f'<TemplateDownloads kind="{slug}"'
    if _primeira(secao, alvo) is None:
        erros.append((baixe, f'"{H2_BAIXE}" precisa de {alvo}'))
    if _primeira(secao, f"referencias/campos/{slug}/") is None:
        erros.append((baixe, f'"{H2_BAIXE}" precisa de um link para referencias/campos/{slug}/'))
    return baixe, erros


def _downloads_cedo(linhas: list[Linha], baixe: int | None) -> list[tuple[int, str]]:
    antes = [(n, t) for n, t in linhas if baixe is None or n < baixe]
    erros: list[tuple[int, str]] = []
    for n, t in antes:
        for trecho in ("<TemplateDownloads", "downloads/template-"):
            if trecho in t:
                erros.append((n, f'{trecho} antes de {H2_BAIXE}; o download fica só nessa seção'))
    return erros


def verificar_pagina(texto: str, slug: str, arquivo: str, campos_existe: bool = True) -> list[str]:
    """Mensagens 'arquivo:linha: problema' de uma página de modelo; lista vazia quando a página segue a sequência."""
    linhas = linhas_fora_de_cerca(texto)
    problema, achados = _problema_e_par(linhas)
    achados = _resumo_antes_do_problema(linhas, slug, problema) + achados
    fecha_steps = None
    if problema is not None:
        bloco, erros = _bloco_steps(linhas, problema)
        achados += erros
        if bloco is not None:
            fecha_steps = bloco[1]
            conteudo, erros_etapas = _etapas_do_bloco(linhas, *bloco)
            achados += erros_etapas + _conteudo_das_etapas(conteudo, slug)
    baixe, erros = _baixe_o_modelo(linhas, slug, fecha_steps, problema)
    achados += erros + _downloads_cedo(linhas, baixe)
    if not campos_existe:
        achados.append((1, f"falta src/content/docs/referencias/campos/{slug}.md; rode python3 scripts/gerar_referencias.py"))
    return [f"{arquivo}:{numero}: {mensagem}" for numero, mensagem in sorted(achados, key=lambda a: a[0])]


def executar(raiz: Path) -> tuple[Relatorio, str]:
    relatorio = Relatorio()
    modelos = carregar_modelos(raiz / "src" / "data" / "modelos.yaml", relatorio)
    docs = raiz / "src" / "content" / "docs"
    conferidas = 0
    for modelo in modelos:
        caminho = docs / "templates" / f"{modelo.pagina}.mdx"
        relativo = caminho.relative_to(raiz).as_posix()
        relatorio.arquivo_atual = caminho
        try:
            texto = caminho.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            relatorio.erro(None, f"{relativo}:1: não foi possível ler a página do modelo: {exc}")
            continue
        conferidas += 1
        existe = (docs / "referencias" / "campos" / f"{modelo.slug}.md").is_file()
        for mensagem in verificar_pagina(texto, modelo.slug, relativo, campos_existe=existe):
            relatorio.erro(None, mensagem)
    return relatorio, f"OK: {conferidas} páginas de modelo seguem a sequência didática"


def main(argv: list[str] | None = None) -> None:
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("--raiz", type=Path, default=ROOT, help="raiz do repositório (para testes)")
    opcoes = argumentos.parse_args(argv)
    relatorio, mensagem = executar(opcoes.raiz)
    relatorio.instalar()
    relatorio.encerrar(mensagem)


if __name__ == "__main__":
    main(sys.argv[1:])
