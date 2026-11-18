"""Transforma os erros de um experimento em perguntas em aberto propostas (revisão humana).

Lê um docs/experimentos/*-resultados.json, liga cada pergunta do experimento a uma pergunta de um
gabarito (documento perguntas-de-negocio aprovado em src/exemplos) e escreve um relatório Markdown
com uma entrada de open_questions por pergunta errada e por documento-alvo. Não altera nenhum
documento: o responsável revisa a proposta e só uma versão nova do documento a incorpora.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

import yaml

from comum import ROOT, Relatorio, ler_frontmatter, relativo

PADRAO_ID = re.compile(r"^[A-Z][A-Z0-9]*(-[A-Z0-9]+)+$")  # igual ao id de schemas/common.schema.json
TIPO_GABARITO = "perguntas-de-negocio"
SEM_VERSAO = "(sem versão aprovada)"
CAMPOS_DE_ACERTO = ("categoria_certa", "conclusao_certa", "conclusao_igual_q01")  # citacao_certa fica de fora
COMPORTAMENTOS = {"answer": "responder", "clarify": "pedir esclarecimento", "abstain": "abster-se"}
AVISO_FIXO = (
    "Relatório para revisão humana. Este script não altera nenhum documento. Uma proposta só entra num "
    "documento depois que o responsável por ele a revisa, e um documento aprovado só muda numa versão nova."
)


@dataclass(frozen=True)
class Versao:
    id: str
    numero: tuple[int, ...]
    texto: str
    tipo: str | None
    owner: str | None
    dados: dict[str, Any]

    @property
    def rotulo(self) -> str:
        return f"{self.id}@{self.texto}"


@dataclass(frozen=True)
class Alvo:
    rotulo: str
    owner: str | None


def _numero_da_versao(texto: str) -> tuple[int, ...] | None:
    partes = texto.split(".")
    return tuple(int(p) for p in partes) if all(p.isdigit() for p in partes) else None


def indexar_aprovados(raiz: Path) -> dict[str, list[Versao]]:
    """Versões approved de src/exemplos por id, da mais alta para a mais baixa. Arquivo ilegível é ignorado."""
    indice: dict[str, list[Versao]] = {}
    for caminho in sorted((raiz / "src" / "exemplos").glob("*.md")):
        lido = ler_frontmatter(caminho, Relatorio())
        if lido is None:
            continue
        dados = lido[0]
        id_, versao = dados.get("id"), str(dados.get("version", ""))
        numero = _numero_da_versao(versao)
        if dados.get("status") != "approved" or not isinstance(id_, str) or numero is None:
            continue
        owner = dados.get("owner")
        indice.setdefault(id_, []).append(
            Versao(id_, numero, versao, dados.get("type"), owner if isinstance(owner, str) else None, dados))
    return {id_: sorted(v, key=lambda x: x.numero, reverse=True) for id_, v in indice.items()}


def ler_mapas(brutos: list[str], relatorio: Relatorio) -> tuple[dict[str, tuple[str, str | None]], dict[str, tuple[str, str | None]]]:
    """Devolve (por prefixo, por nome inteiro). PREFIXO=ID ou NOME=ID:Qnn."""
    prefixos: dict[str, tuple[str, str | None]] = {}
    nomes: dict[str, tuple[str, str | None]] = {}
    for bruto in brutos:
        chave, igual, valor = bruto.partition("=")
        gabarito, doispontos, qnn = valor.partition(":")
        if not igual or not chave or not gabarito or (doispontos and not qnn):
            relatorio.erro(None, f"--mapa inválido: {bruto!r} (use PREFIXO=ID ou NOME=ID:Qnn)")
        elif doispontos:
            nomes[chave] = (gabarito, qnn)
        else:
            prefixos[chave] = (gabarito, None)
    return prefixos, nomes


def ler_resultados(caminho: Path, relatorio: Relatorio) -> list[dict[str, Any]]:
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except FileNotFoundError:
        relatorio.erro(caminho, "arquivo não encontrado")
        return []
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        relatorio.erro(caminho, f"não foi possível ler o JSON: {exc}")
        return []
    if not isinstance(dados, list):
        relatorio.erro(caminho, "o JSON deve ser uma lista de execuções")
        return []
    itens: list[dict[str, Any]] = []
    for numero, item in enumerate(dados, start=1):
        if not isinstance(item, dict):
            relatorio.erro(caminho, f"item {numero} não é um mapa")
        elif not isinstance(item.get("pergunta"), str) or not item["pergunta"]:
            relatorio.erro(caminho, f"item {numero} sem 'pergunta'")
        elif not isinstance(item.get("cond"), str):
            relatorio.erro(caminho, f"item {numero} sem 'cond'")
        else:
            itens.append(item)
    return itens


def errou(item: dict[str, Any]) -> bool:
    return any(item.get(campo) is False for campo in CAMPOS_DE_ACERTO)


def ligar(pergunta: str, prefixos: dict[str, tuple[str, str | None]],
          nomes: dict[str, tuple[str, str | None]]) -> tuple[str, str] | None:
    """(id do gabarito, Qnn) da pergunta do experimento, ou None se não houver mapa."""
    if pergunta in nomes:
        gabarito, qnn = nomes[pergunta]
        return gabarito, qnn or ""
    prefixo, traco, resto = pergunta.partition("-")
    if traco and prefixo in prefixos and resto:
        return prefixos[prefixo][0], resto
    return None


def resolver_gabarito(id_: str, indice: dict[str, list[Versao]], relatorio: Relatorio) -> Versao | None:
    versoes = [v for v in indice.get(id_, []) if v.tipo == TIPO_GABARITO]
    if not versoes:
        relatorio.erro(None, f"gabarito {id_} sem versão aprovada do tipo {TIPO_GABARITO} em src/exemplos")
        return None
    return versoes[0]


def achar_pergunta(gabarito: Versao, qnn: str, relatorio: Relatorio) -> dict[str, Any] | None:
    perguntas = gabarito.dados.get("questions")
    for pergunta in perguntas if isinstance(perguntas, list) else []:
        if isinstance(pergunta, dict) and pergunta.get("id") == qnn:
            return pergunta
    relatorio.erro(None, f"{gabarito.rotulo} não tem a pergunta {qnn}")
    return None


def alvos_da_pergunta(gabarito: Versao, pergunta: dict[str, Any], indice: dict[str, list[Versao]]) -> list[Alvo]:
    fontes = pergunta.get("required_sources")
    ids = sorted({f for f in (fontes if isinstance(fontes, list) else [])
                  if isinstance(f, str) and not f.endswith(".sql") and PADRAO_ID.match(f)})
    if not ids:
        return [Alvo(gabarito.rotulo, gabarito.owner)]
    alvos = []
    for id_ in ids:
        vigente = indice.get(id_, [None])[0]
        alvos.append(Alvo(vigente.rotulo, vigente.owner) if vigente else Alvo(f"{id_} {SEM_VERSAO}", None))
    return alvos


def _resposta_esperada(pergunta: dict[str, Any]) -> str:
    comportamento = pergunta.get("expected_behavior")
    campos = {"answer": ("reference_answer",), "abstain": ("reason_if_abstain",),
              "clarify": ("ambiguity", "reference_answer")}.get(str(comportamento), ("reference_answer",))
    return next((str(pergunta[c]) for c in campos if pergunta.get(c)), "não registrada no gabarito")


def _categoria(item: dict[str, Any]) -> str:
    return str(item.get("categoria_observada") or item.get("categoria") or "sem categoria")


def _modelo(item: dict[str, Any]) -> str:
    return str(item.get("modelo_nome") or item.get("modelo") or "modelo não informado")


def _bloco_yaml(entrada: dict[str, Any]) -> str:
    corpo = yaml.safe_dump({"open_questions": [entrada]}, allow_unicode=True, sort_keys=False, width=10_000)
    return f"```yaml\n{corpo}```"


def _proposta(gabarito: Versao, qnn: str, nome: str, pergunta: dict[str, Any], erros: list[dict[str, Any]],
              total: int, alvo: Alvo) -> dict[str, Any]:
    categorias = ", ".join(f"{c} ({n})" for c, n in sorted(Counter(_categoria(i) for i in erros).items()))
    return {
        "question": (f'A IA errou a {qnn} do {gabarito.rotulo} ("{nome}") em {len(erros)} de {total} execuções. '
                     f"O que falta em {alvo.rotulo} para a resposta esperada sair, ou o gabarito precisa mudar?"),
        "impact": f"Resposta esperada: {_resposta_esperada(pergunta)}. Categorias observadas: {categorias}.",
        "owner_to_resolve": alvo.owner,
        "status": "unresolved",
        "resolution": None,
    }


def _secao_da_pergunta(gabarito: Versao, qnn: str, pergunta: dict[str, Any], execucoes: list[dict[str, Any]],
                       indice: dict[str, list[Versao]]) -> list[str]:
    erros = [i for i in execucoes if errou(i)]
    nome = sorted({i["pergunta"] for i in erros})[0]
    comportamento = COMPORTAMENTOS.get(str(pergunta.get("expected_behavior")), str(pergunta.get("expected_behavior")))
    por_categoria = ", ".join(f"{c}: {n}" for c, n in sorted(Counter(_categoria(i) for i in erros).items()))
    por_modelo = ", ".join(f"{m}: {n}" for m, n in sorted(Counter(_modelo(i) for i in erros).items()))
    linhas = [f"### {gabarito.rotulo} {qnn}", "",
              f"- Pergunta: {pergunta.get('question')}",
              f"- Comportamento esperado: {comportamento}",
              f"- Errou em {len(erros)} de {len(execucoes)} execuções",
              f"- Categorias observadas: {por_categoria}",
              f"- Modelos: {por_modelo}", ""]
    for alvo in sorted(alvos_da_pergunta(gabarito, pergunta, indice), key=lambda a: a.rotulo):
        linhas += [f"Alvo: {alvo.rotulo}", "",
                   _bloco_yaml(_proposta(gabarito, qnn, nome, pergunta, erros, len(execucoes), alvo)), ""]
    return linhas


def comando_do_relatorio(caminho: Path, mapas: list[str], condicoes: list[str]) -> str:
    """Comando que gera de novo o relatório, com os mapas e as condições em ordem fixa."""
    partes = ["python3 scripts/erros_para_perguntas.py", relativo(caminho)]
    partes += [f"--mapa {m}" for m in sorted(mapas)] + [f"--condicao {c}" for c in sorted(condicoes)]
    return " ".join(partes)


def montar_relatorio(caminho: Path, selecionadas: list[dict[str, Any]], condicoes: list[str], raiz: Path,
                     prefixos: dict[str, tuple[str, str | None]], nomes: dict[str, tuple[str, str | None]],
                     relatorio: Relatorio, mapas: list[str] | None = None) -> str:
    indice = indexar_aprovados(raiz)
    ligadas: dict[tuple[str, str], list[dict[str, Any]]] = {}
    sem_mapa: dict[str, list[dict[str, Any]]] = {}
    for item in selecionadas:
        ligacao = ligar(item["pergunta"], prefixos, nomes)
        if ligacao is None:
            sem_mapa.setdefault(item["pergunta"], []).append(item)
        else:
            ligadas.setdefault(ligacao, []).append(item)
    for pergunta in sorted(sem_mapa):
        relatorio.aviso(None, f"pergunta {pergunta!r} sem --mapa: fora das propostas")
    secoes: list[str] = []
    for (id_gabarito, qnn), execucoes in sorted(ligadas.items()):
        gabarito = resolver_gabarito(id_gabarito, indice, relatorio)
        pergunta = achar_pergunta(gabarito, qnn, relatorio) if gabarito else None
        if gabarito and pergunta and any(errou(i) for i in execucoes):
            secoes += _secao_da_pergunta(gabarito, qnn, pergunta, execucoes, indice)
    total_erros = sum(errou(i) for i in selecionadas)
    linhas = ["# Perguntas em aberto propostas a partir dos erros do experimento", "", AVISO_FIXO, "",
              f"- Resultados: {relativo(caminho)}", f"- Condições: {', '.join(condicoes)}",
              f"- Comando: `{comando_do_relatorio(caminho, mapas or [], condicoes)}`",
              f"- Execuções: {len(selecionadas)}", f"- Erros: {total_erros}", ""]
    linhas += ["## Propostas", ""] + (secoes if secoes else ["Nenhuma pergunta errada nas condições escolhidas.", ""])
    if sem_mapa:
        linhas += ["## Sem gabarito ligado", ""]
        linhas += [f"- {p}: {len(v)} execuções, {sum(errou(i) for i in v)} erros" for p, v in sorted(sem_mapa.items())]
        linhas.append("")
    return "\n".join(linhas).rstrip("\n") + "\n"


def main(argv: list[str] | None = None) -> None:
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument("resultados", type=Path, help="docs/experimentos/*-resultados.json")
    analisador.add_argument("--mapa", action="append", default=[], metavar="PREFIXO=ID[:Qnn]",
                            help="liga PREFIXO-Qnn (ou NOME=ID:Qnn) ao id de um gabarito; repetível")
    analisador.add_argument("--condicao", action="append", default=None, help="condição a analisar (padrão: B); repetível")
    analisador.add_argument("--saida", type=Path, help="escreve o relatório neste arquivo em vez de imprimir")
    analisador.add_argument("--raiz", type=Path, default=ROOT, help="raiz com src/exemplos (padrão: o repositório)")
    argumentos = analisador.parse_args(argv)

    relatorio = Relatorio()
    relatorio.instalar()
    condicoes = sorted(set(argumentos.condicao or ["B"]))
    prefixos, nomes = ler_mapas(argumentos.mapa, relatorio)
    itens = ler_resultados(argumentos.resultados, relatorio)
    selecionadas = [i for i in itens if i["cond"] in condicoes]
    texto = montar_relatorio(argumentos.resultados, selecionadas, condicoes, argumentos.raiz,
                             prefixos, nomes, relatorio, argumentos.mapa)
    if relatorio.erros:
        relatorio.encerrar("")
    if argumentos.saida:
        argumentos.saida.write_text(texto, encoding="utf-8")
        relatorio.encerrar(f"OK: relatório escrito em {relativo(argumentos.saida)}")
    else:
        print(texto, end="")
        relatorio.encerrar("")


if __name__ == "__main__":
    main()
