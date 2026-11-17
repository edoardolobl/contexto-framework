#!/usr/bin/env python3
"""Gera public/downloads a partir das fontes em src/modelos e src/exemplos (ADR 0006).

Sem flag, escreve os arquivos e remove os órfãos. Com --check, não escreve nada: confere que os
arquivos publicados estão em sincronia com as fontes e termina com código 1 se não estiverem.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import re
import sys
from typing import Any

from comum import ROOT, Relatorio, carregar_yaml, ler_frontmatter

MARCADOR_IDENTIFICACAO = "<!-- contexto:identificacao -->"
MARCADOR_HISTORICO = "<!-- contexto:historico -->"
FRASE_IDENTIFICACAO = "Preencha estes campos no topo do arquivo antes de escrever o resto."
CABECALHO_IDENTIFICACAO = ("Campo", "Chave no topo do arquivo", "Obrigatório", "O que escrever")
CABECALHO_HISTORICO = ("Versão", "Data", "O que mudou e por quê", "Aprovado por (cargo ou área)")
_DATA_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_MARCADOR_EXEMPLO = re.compile(r"^<!-- contexto:exemplo (\S+) -->[ \t]*$", re.MULTILINE)
PREFIXO_EXEMPLO = "Exemplo Aurora"
CHAVE_OBRIGATORIA_NO_EXEMPLO = "intent.question"
MINIMO_DE_MARCADORES_DE_EXEMPLO = 4


class ErroDeExemplo(ValueError):
    """Chave de marcador que não pode virar uma linha de exemplo; a mensagem diz o motivo."""


def _celula(valor: Any) -> str:
    texto = "" if valor is None else str(valor)
    return " ".join(texto.split()).replace("|", "\\|")


def tabela_markdown(cabecalho: tuple[str, ...], linhas: list[list[Any]]) -> str:
    partes = ["| " + " | ".join(cabecalho) + " |", "|" + "|".join("---" for _ in cabecalho) + "|"]
    partes += ["| " + " | ".join(_celula(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(partes)


def _data_br(valor: Any) -> str:
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, str) and (achado := _DATA_ISO.match(valor)):
        return f"{achado.group(3)}/{achado.group(2)}/{achado.group(1)}"
    return "" if valor is None else str(valor)


def secao_identificacao(campos: list[dict[str, Any]]) -> str:
    linhas = [[c.get("rotulo"), f"`{c.get('chave')}`", "Sim" if c.get("obrigatorio") is True else "", c.get("descricao")]
              for c in campos]
    return f"## Identificação\n\n{FRASE_IDENTIFICACAO}\n\n{tabela_markdown(CABECALHO_IDENTIFICACAO, linhas)}"


def secao_historico(historico: Any) -> str:
    itens = [h for h in historico if isinstance(h, dict)] if isinstance(historico, list) else []
    linhas = [[h.get("version"), _data_br(h.get("date")), h.get("change"), h.get("approved_by")] for h in itens]
    return f"## Histórico de versões\n\n{tabela_markdown(CABECALHO_HISTORICO, linhas)}"


def chaves_de_exemplo(corpo: str) -> list[str]:
    """Chaves dos marcadores `<!-- contexto:exemplo CHAVE -->` (cada um em linha própria), na ordem do texto."""
    return _MARCADOR_EXEMPLO.findall(corpo)


def _formatar_valor(valor: Any, chave: str) -> str:
    if isinstance(valor, (dict, list)):
        itens = list(valor.values()) if isinstance(valor, dict) else valor
        if isinstance(valor, dict) or any(isinstance(i, (dict, list)) for i in itens):
            raise ErroDeExemplo(f"a chave `{chave}` é um mapa ou lista de mapas no exemplo completo; aponte uma chave mais funda")
    if isinstance(valor, list):
        return "; ".join(_formatar_valor(item, chave) for item in valor)
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%Y-%m-%d")
    return " ".join(str(valor).split())


def valor_do_exemplo(dados: dict[str, Any], chave: str) -> str:
    """Texto de uma chave com pontos (índice numérico entra em listas) do frontmatter do exemplo completo."""
    atual: Any = dados
    for parte in chave.split("."):
        if isinstance(atual, dict) and parte in atual:
            atual = atual[parte]
        elif isinstance(atual, list) and parte.isdigit() and int(parte) < len(atual):
            atual = atual[int(parte)]
        else:
            raise ErroDeExemplo(f"a chave `{chave}` está ausente no exemplo completo")
    if atual is None or atual == [] or (isinstance(atual, str) and not atual.strip()):
        raise ErroDeExemplo(f"o valor de `{chave}` está vazio no exemplo completo (null, texto em branco ou lista vazia)")
    return _formatar_valor(atual, chave)


def _linhas_de_exemplo(caminho: Path, corpo: str, exemplo: dict[str, Any] | None, relatorio: Relatorio) -> dict[str, str] | None:
    """Chave de marcador para a linha publicada; None (com erros registrados) se algum marcador falhar."""
    chaves = chaves_de_exemplo(corpo)
    ok = True
    if corpo.count("contexto:exemplo") != len(chaves):
        relatorio.erro(caminho, "marcador contexto:exemplo mal formado; use `<!-- contexto:exemplo CHAVE -->` em linha própria")
        ok = False
    if CHAVE_OBRIGATORIA_NO_EXEMPLO not in chaves:
        relatorio.erro(caminho, f"modelo sem o marcador de exemplo de {CHAVE_OBRIGATORIA_NO_EXEMPLO}")
        ok = False
    if len(set(chaves)) < MINIMO_DE_MARCADORES_DE_EXEMPLO:
        relatorio.erro(caminho, f"modelo com {len(set(chaves))} marcadores de exemplo; use pelo menos {MINIMO_DE_MARCADORES_DE_EXEMPLO} chaves diferentes")
        ok = False
    if exemplo is None:
        return None
    linhas: dict[str, str] = {}
    for chave in dict.fromkeys(chaves):
        try:
            linhas[chave] = f"{PREFIXO_EXEMPLO}: `{chave}`: {valor_do_exemplo(exemplo, chave)}"
        except ErroDeExemplo as erro:
            relatorio.erro(caminho, str(erro))
            ok = False
    return linhas if ok else None


def _corpo_do_modelo(caminho: Path, corpo: str, dados: dict[str, Any], campos: list[dict[str, Any]],
                     exemplo: dict[str, Any] | None, relatorio: Relatorio) -> str | None:
    ok = True
    for marcador in (MARCADOR_IDENTIFICACAO, MARCADOR_HISTORICO):
        vezes = corpo.count(marcador)
        if vezes == 0:
            relatorio.erro(caminho, f"modelo sem o marcador {marcador}")
            ok = False
        elif vezes > 1:
            relatorio.erro(caminho, f"marcador {marcador} repetido ({vezes} vezes)")
            ok = False
    linhas = _linhas_de_exemplo(caminho, corpo, exemplo, relatorio)
    if not ok or linhas is None:
        return None
    corpo = _MARCADOR_EXEMPLO.sub(lambda achado: linhas[achado.group(1)], corpo)
    return (corpo.replace(MARCADOR_IDENTIFICACAO, secao_identificacao(campos))
                 .replace(MARCADOR_HISTORICO, secao_historico(dados.get("version_history"))))


def _campos_do_cabecalho(raiz: Path, relatorio: Relatorio) -> list[dict[str, Any]]:
    caminho = raiz / "src" / "data" / "campos.yaml"
    dados = carregar_yaml(caminho, relatorio)
    itens = dados.get("cabecalho") if dados else None
    if dados is not None and (not isinstance(itens, list) or not all(isinstance(i, dict) for i in itens)):
        relatorio.erro(caminho, "falta a lista 'cabecalho' de mapas")
        return []
    return itens or []


def _exemplo_completo(raiz: Path, modelo: Path, relatorio: Relatorio) -> dict[str, Any] | None:
    """Frontmatter de src/exemplos/exemplo-<slug>-completo.md, ou None com o erro registrado no modelo."""
    exemplo = raiz / "src" / "exemplos" / f"exemplo-{modelo.stem}-completo.md"
    if not exemplo.is_file():
        relatorio.erro(modelo, f"os marcadores de exemplo pedem src/exemplos/{exemplo.name}, que não existe")
        return None
    lido = ler_frontmatter(exemplo, relatorio)
    return lido[0] if lido else None


def montar_esperados(raiz: Path, relatorio: Relatorio) -> tuple[dict[Path, str], int]:
    """Cada arquivo que deve existir em public/downloads (caminho absoluto, conteúdo) e o total de fontes."""
    downloads = raiz / "public" / "downloads"
    modelos = sorted((raiz / "src" / "modelos").glob("*.md"))
    exemplos = sorted((raiz / "src" / "exemplos").rglob("*.md"))
    campos = _campos_do_cabecalho(raiz, relatorio) if modelos else []
    esperados: dict[Path, str] = {}
    for fonte in modelos:
        lido = ler_frontmatter(fonte, relatorio)
        if lido is None:
            continue
        dados, texto, corpo = lido
        novo = _corpo_do_modelo(fonte, corpo, dados, campos, _exemplo_completo(raiz, fonte, relatorio), relatorio)
        if novo is None:
            continue
        esperados[downloads / f"template-{fonte.stem}.yaml"] = texto + "\n"
        esperados[downloads / f"template-{fonte.stem}.md"] = f"---\n{texto}\n---\n{novo.rstrip(chr(10))}\n"
    for fonte in exemplos:
        lido = ler_frontmatter(fonte, relatorio)
        if lido is None:
            continue
        relativo = fonte.relative_to(raiz / "src" / "exemplos").with_suffix(".yaml")
        esperados[downloads / relativo] = lido[1] + "\n"
    return esperados, len(modelos) + len(exemplos)


def orfaos(raiz: Path, esperados: dict[Path, str]) -> list[Path]:
    """Arquivos gerados na raiz de downloads (e exemplos em historico/) que não têm mais fonte."""
    downloads = raiz / "public" / "downloads"
    achados: list[Path] = []
    if downloads.is_dir():
        achados += [*downloads.glob("template-*.md"), *downloads.glob("template-*.yaml"), *downloads.glob("exemplo-*.yaml")]
    if (downloads / "historico").is_dir():
        achados += (downloads / "historico").glob("exemplo-*.yaml")
    return sorted(p for p in achados if p.is_file() and p not in esperados)


def _nome(raiz: Path, caminho: Path) -> str:
    try:
        return caminho.relative_to(raiz).as_posix()
    except ValueError:
        return str(caminho)


def executar(raiz: Path, check: bool = False) -> tuple[Relatorio, str]:
    """Devolve o relatório de erros e a mensagem de sucesso. Só escreve se check for falso e não houver erro."""
    relatorio = Relatorio()
    esperados, fontes = montar_esperados(raiz, relatorio)
    sobras = orfaos(raiz, esperados)
    if check:
        for caminho, conteudo in esperados.items():
            nome = _nome(raiz, caminho)
            if not caminho.is_file():
                relatorio.erro(None, f"{nome}: ausente; rode npm run gerar:downloads")
            elif caminho.read_bytes() != conteudo.encode("utf-8"):
                relatorio.erro(None, f"{nome}: desatualizado em relação à fonte; rode npm run gerar:downloads")
        for caminho in sobras:
            relatorio.erro(None, f"{_nome(raiz, caminho)}: órfão, sem fonte em src/modelos ou src/exemplos; rode npm run gerar:downloads")
    elif not relatorio.erros:
        for caminho, conteudo in esperados.items():
            dados = conteudo.encode("utf-8")
            if not caminho.is_file() or caminho.read_bytes() != dados:
                caminho.parent.mkdir(parents=True, exist_ok=True)
                caminho.write_bytes(dados)
        for caminho in sobras:
            caminho.unlink()
    return relatorio, f"OK: {len(esperados)} arquivos gerados em sincronia com {fontes} fontes"


def main(argv: list[str] | None = None) -> None:
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("--check", action="store_true", help="só confere, não escreve")
    argumentos.add_argument("--raiz", type=Path, default=ROOT, help="raiz do repositório (para testes)")
    opcoes = argumentos.parse_args(argv)
    relatorio, mensagem = executar(opcoes.raiz, check=opcoes.check)
    relatorio.instalar()
    relatorio.encerrar(mensagem)


if __name__ == "__main__":
    main(sys.argv[1:])
