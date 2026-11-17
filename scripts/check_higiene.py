#!/usr/bin/env python3
"""Checagens de higiene do repositório, independentes de LLM.

1. Caracteres Unicode invisíveis: podem esconder instruções em arquivos que agentes de IA leem
   (o ataque conhecido como "Rules File Backdoor"). Nenhum arquivo de texto do projeto precisa deles.
2. Descrições que só repetem o nome do campo: não ensinam nada a quem lê nem à IA.
3. Uma versão do produto: package.json, README, página inicial e CHANGELOG dizem a mesma versão.
4. Vocabulário: todo termo de src/data/vocabulario.yaml aparece na tabela do contrato editorial.

Política dos caracteres invisíveis: são acusados a categoria Cf (inclui ZWJ, ZWNJ e marcas de direção),
Cc (exceto tab, \\n e \\r), Zl, Zp, os seletores de variação (U+FE00 a U+FE0F e U+E0100 a U+E01EF) e os
preenchedores que renderizam em branco (U+3164, U+115F, U+1160, U+2800, U+FFA0). O projeto não usa emoji,
então ZWJ e seletores de variação não têm uso legítimo e também são acusados.
"""
from __future__ import annotations

from collections.abc import Iterator
import json
from pathlib import Path
import re
import unicodedata
from typing import Any

from comum import DADOS, DOWNLOADS, ROOT, Relatorio, carregar_vocabulario, carregar_yaml, exigir_minimo

EXTENSOES_DE_TEXTO = {".md", ".mdx", ".yaml", ".yml", ".astro", ".py", ".mjs", ".js", ".ts", ".json", ".sql", ".css", ".txt", ".svg", ".html", ".toml"}
ARQUIVOS_SEM_EXTENSAO = {"LICENSE", "LICENSE-CONTENT"}
CATEGORIAS_INVISIVEIS = {"Cf", "Cc", "Zl", "Zp"}
PERMITIDOS = {"\t", "\n", "\r"}
FAIXAS_INVISIVEIS = ((0xFE00, 0xFE0F), (0xE0100, 0xE01EF))
PREENCHEDORES = {0x3164, 0x115F, 0x1160, 0x2800, 0xFFA0}
PASTAS_IGNORADAS = {".git", "node_modules", "dist", ".astro", ".codegraph", ".taste-skill", "__pycache__", ".pytest_cache"}
CHAVES_DE_NOME = ("name", "physical_name", "business_name", "term", "field", "prefLabel", "rotulo")
CHAVES_DE_DESCRICAO = ("meaning", "description", "definition", "descricao")
PALAVRAS_VAZIAS = {"a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "no", "na", "the", "of"}


def _invisivel(caractere: str) -> bool:
    if caractere in PERMITIDOS:
        return False
    codigo = ord(caractere)
    return (
        unicodedata.category(caractere) in CATEGORIAS_INVISIVEIS
        or codigo in PREENCHEDORES
        or any(inicio <= codigo <= fim for inicio, fim in FAIXAS_INVISIVEIS)
    )


def caracteres_invisiveis(texto: str) -> list[tuple[int, int, str]]:
    """Devolve (linha, coluna, código e nome) de cada caractere de formatação invisível."""
    achados = []
    for numero, linha in enumerate(texto.split("\n"), start=1):
        for coluna, caractere in enumerate(linha, start=1):
            if _invisivel(caractere):
                nome = unicodedata.name(caractere, "SEM NOME")
                achados.append((numero, coluna, f"U+{ord(caractere):04X} {nome}"))
    return achados


def _palavras(texto: str) -> list[str]:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    palavras = [p for p in re.split(r"[^a-z0-9]+", sem_acento.lower()) if p and p not in PALAVRAS_VAZIAS]
    return [_singular(p) for p in palavras]


def _singular(palavra: str) -> str:
    """Plural simples: 'canais' vira 'canal', 'papeis' vira 'papel', 'canais' e 'dados' perdem o s."""
    if palavra.endswith("ais") and len(palavra) > 4:
        return palavra[:-3] + "al"
    if palavra.endswith("eis") and len(palavra) > 4:
        return palavra[:-3] + "el"
    if palavra.endswith("s") and len(palavra) > 3:
        return palavra[:-1]
    return palavra


def descricao_tautologica(nome: str | None, descricao: str | None) -> bool:
    """Verdadeiro quando a descrição não tem nenhuma palavra que o nome já não tenha."""
    if not nome or not descricao:
        return False
    palavras_descricao = _palavras(str(descricao))
    return bool(palavras_descricao) and set(palavras_descricao) <= set(_palavras(str(nome)))


def pares_nome_descricao(dados: Any) -> Iterator[tuple[str, str]]:
    """Percorre o YAML e devolve cada (nome, descrição) que aparece no mesmo mapa."""
    if isinstance(dados, dict):
        descricoes = [dados[c] for c in CHAVES_DE_DESCRICAO if isinstance(dados.get(c), str)]
        nomes = [dados[c] for c in CHAVES_DE_NOME if isinstance(dados.get(c), str)]
        for nome in nomes:
            for descricao in descricoes:
                yield nome, descricao
        for valor in dados.values():
            yield from pares_nome_descricao(valor)
    elif isinstance(dados, list):
        for item in dados:
            yield from pares_nome_descricao(item)


def pares_de_schema(dados: Any) -> Iterator[tuple[str, str]]:
    """Cada objeto de um JSON Schema que tem 'title' e 'description' em texto (I-02)."""
    if isinstance(dados, dict):
        titulo, descricao = dados.get("title"), dados.get("description")
        if isinstance(titulo, str) and isinstance(descricao, str):
            yield titulo, descricao
        for valor in dados.values():
            yield from pares_de_schema(valor)
    elif isinstance(dados, list):
        for item in dados:
            yield from pares_de_schema(item)


def maior_menor(versao: str) -> str | None:
    """Reduz '0.4.0', 'v0.4' ou '1.12.3-rc1' a 'maior.menor'."""
    achado = re.search(r"(\d+)\.(\d+)", versao or "")
    return f"{achado.group(1)}.{achado.group(2)}" if achado else None


def _ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8") if caminho.is_file() else ""


def versoes_do_produto(raiz: Path) -> dict[str, str | None]:
    """Lê a versão do produto nas quatro fontes que o leitor ou a ferramenta enxergam."""
    try:
        pacote = json.loads(_ler(raiz / "package.json") or "{}").get("version", "")
    except json.JSONDecodeError:
        pacote = ""
    readme = re.search(r"^## O que existe na (v[\d.]+)", _ler(raiz / "README.md"), re.M)
    inicio = re.search(r"Versão (\d+\.\d+)", _ler(raiz / "src" / "content" / "docs" / "index.mdx"))
    lancada = re.search(r"^## \[(\d+\.\d+\.\d+)\]", _ler(raiz / "CHANGELOG.md"), re.M)
    return {
        "package.json": maior_menor(pacote),
        "README.md": maior_menor(readme.group(1)) if readme else None,
        "src/content/docs/index.mdx": maior_menor(inicio.group(1)) if inicio else None,
        "CHANGELOG.md": maior_menor(lancada.group(1)) if lancada else None,
    }


def _normalizar_termo(texto: str) -> str:
    return re.sub(r"[“”‘’\"'\s]+", "", texto).casefold()


def termos_fora_do_contrato(regras: list[dict[str, Any]], contrato: str) -> list[str]:
    """Termos do vocabulário que não são uma célula inteira da coluna "Termo" da seção Vocabulário."""
    inicio = contrato.find("## Vocabulário")
    secao = contrato[inicio:].split("\n## ", 1)[0] if inicio >= 0 else contrato
    celulas: set[str] = set()
    for linha in secao.splitlines():
        if not linha.startswith("| ") or linha.count("|") < 4:
            continue
        for parte in re.split(r"[;,]", linha.split("|")[2]):
            celulas.add(_normalizar_termo(parte))
    return sorted({r["termo"] for r in regras if r.get("termo") and _normalizar_termo(r["termo"]) not in celulas})


def arquivos_de_texto(raiz: Path) -> Iterator[Path]:
    for caminho in sorted(raiz.rglob("*")):
        if PASTAS_IGNORADAS.intersection(caminho.relative_to(raiz).parts):
            continue
        if caminho.is_file() and (
            caminho.suffix in EXTENSOES_DE_TEXTO
            or (caminho.parent == raiz and caminho.name in ARQUIVOS_SEM_EXTENSAO)
        ):
            yield caminho


def main() -> None:
    relatorio = Relatorio()
    relatorio.instalar()

    arquivos = exigir_minimo(arquivos_de_texto(ROOT), 50, "arquivos de texto no repositório", relatorio)
    for caminho in arquivos:
        relatorio.arquivo_atual = caminho
        for linha, coluna, codigo in caracteres_invisiveis(caminho.read_text(encoding="utf-8", errors="replace")):
            relatorio.erro(caminho, f"linha {linha}, coluna {coluna}: caractere invisível {codigo}")

    yamls = exigir_minimo(DOWNLOADS.rglob("*.yaml"), 20, "YAML em public/downloads", relatorio)
    for caminho in yamls:
        dados = carregar_yaml(caminho, relatorio)
        for nome, descricao in pares_nome_descricao(dados or {}):
            if descricao_tautologica(nome, descricao):
                relatorio.erro(caminho, f"a descrição \"{descricao}\" só repete o nome \"{nome}\"; diga como interpretar o valor")

    campos = carregar_yaml(DADOS / "campos.yaml", relatorio) if (DADOS / "campos.yaml").is_file() else None
    for nome, descricao in pares_nome_descricao(campos or {}):
        if descricao_tautologica(nome, descricao):
            relatorio.erro(DADOS / "campos.yaml", f"a descrição \"{descricao}\" só repete o rótulo \"{nome}\"; diga o que escrever")
    esquemas = sorted((ROOT / "schemas").glob("*.json"))
    for caminho in esquemas:
        relatorio.arquivo_atual = caminho
        try:
            conteudo = json.loads(caminho.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
            relatorio.erro(caminho, f"JSON ilegível: {exc}")
            continue
        for titulo, descricao in pares_de_schema(conteudo):
            if descricao_tautologica(titulo, descricao):
                relatorio.erro(caminho, f"a descrição \"{descricao}\" só repete o título \"{titulo}\"; diga como interpretar o valor")

    versoes = versoes_do_produto(ROOT)
    lidas = {fonte: v for fonte, v in versoes.items() if v}
    for fonte, valor in versoes.items():
        if valor is None:
            relatorio.erro(None, f"{fonte}: versão do produto não encontrada")
    if len(set(lidas.values())) > 1:
        relatorio.erro(None, "versões do produto divergem: " + ", ".join(f"{f} {v}" for f, v in lidas.items()))

    regras = carregar_vocabulario(DADOS / "vocabulario.yaml", relatorio)
    if not regras:
        relatorio.erro(DADOS / "vocabulario.yaml", "vocabulário vazio; nada para conferir no contrato")
    bruto = carregar_yaml(DADOS / "vocabulario.yaml", relatorio) or {}
    contrato = _ler(ROOT / "docs" / "CONTRATO_EDITORIAL.md")
    for termo in termos_fora_do_contrato(bruto.get("regras") or [], contrato):
        relatorio.erro(ROOT / "docs" / "CONTRATO_EDITORIAL.md", f"termo \"{termo}\" do vocabulário falta na tabela Vocabulário")

    versao = next(iter(lidas.values()), "?")
    relatorio.encerrar(
        f"OK: {len(arquivos)} arquivos sem caracteres invisíveis, {len(yamls)} YAML sem descrição que só repete o nome, "
        f"versão {versao} igual em {len(lidas)} fontes, vocabulário presente no contrato."
    )


if __name__ == "__main__":
    main()
