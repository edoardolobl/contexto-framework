#!/usr/bin/env python3
"""Gera a referência de campos (src/content/docs/referencias/campos) a partir dos schemas (ADR 0017).

Lê src/data/modelos.yaml, src/data/campos.yaml, schemas/common.schema.json e schemas/<slug>.schema.json.
Sem flag, escreve as páginas e remove as órfãs. Com --check, não escreve nada: confere que as páginas
estão em sincronia e termina com código 1 se não estiverem.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from comum import ROOT, Modelo, Relatorio, carregar_modelos, carregar_yaml
from gerar_downloads import tabela_markdown

PASTA_RELATIVA = Path("src") / "content" / "docs" / "referencias" / "campos"
AVISO_DE_GERADO = ("<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. "
                   "Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->")
CABECALHO_COMUM = ("Campo", "Chave", "Obrigatório")
CABECALHO_DO_TIPO = ("Campo", "Chave", "Valor", "O que escrever")
CAMPOS_TECNICOS = ("context", "authoritativeDefinitions")
NOMES_DE_TIPO = {"string": "texto", "integer": "número inteiro", "number": "número", "boolean": "sim ou não (true ou false)"}
NOMES_NO_PLURAL = {"string": "textos", "integer": "números", "number": "números"}


class ErroDeSchema(ValueError):
    """Estrutura de schema que o gerador não reconhece; a mensagem diz qual."""


def _como_mapa(no: Any) -> dict[str, Any]:
    if not isinstance(no, dict):
        raise ErroDeSchema(f"esperado um mapa, achado {type(no).__name__}")
    return no


def resolver(no: Any, defs: dict[str, Any]) -> dict[str, Any]:
    """Segue `$ref` (só para $defs do cabeçalho comum) e escolhe o ramo não nulo de `anyOf`."""
    no = _como_mapa(no)
    if "$ref" in no:
        alvo = no["$ref"]
        prefixo, _, nome = str(alvo).partition("#/$defs/")
        if not nome or (prefixo and not prefixo.endswith(":common")) or nome not in defs:
            raise ErroDeSchema(f"referência desconhecida: {alvo}")
        local = {k: v for k, v in no.items() if k != "$ref"}
        return resolver({**_como_mapa(defs[nome]), **local}, defs)
    if "anyOf" in no:
        ramos = [r for r in no["anyOf"] if r != {"type": "null"}]
        if len(ramos) != 1:
            raise ErroDeSchema("anyOf com mais de um ramo não nulo")
        local = {k: v for k, v in no.items() if k != "anyOf"}
        return resolver({**_como_mapa(ramos[0]), **local}, defs)
    return no


def _enum(valores: Any) -> str:
    return ", ".join(str(v) for v in valores if v is not None)


def _tipos(no: dict[str, Any]) -> list[str]:
    bruto = no.get("type")
    tipos = [bruto] if isinstance(bruto, str) else list(bruto) if isinstance(bruto, list) else []
    return [t for t in tipos if t != "null"]


def _valor_de_lista(no: dict[str, Any], defs: dict[str, Any]) -> str:
    if "items" not in no:
        return "lista"
    itens = resolver(no["items"], defs)
    if not itens:
        return "lista de valores livres"
    if "enum" in itens:
        return f"lista, cada item um destes: {_enum(itens['enum'])}"
    if itens.get("format") == "date":
        return "lista de datas"
    tipos = _tipos(itens)
    if tipos == ["object"]:
        return "lista de grupos de campos"
    if len(tipos) == 1 and tipos[0] in NOMES_NO_PLURAL:
        return f"lista de {NOMES_NO_PLURAL[tipos[0]]}"
    raise ErroDeSchema(f"itens de lista não reconhecidos: {json.dumps(itens, ensure_ascii=False)[:80]}")


def _valor_de_mapa(no: dict[str, Any], defs: dict[str, Any]) -> str:
    if no.get("properties"):
        return "grupo de campos"
    adicional = no.get("additionalProperties")
    if isinstance(adicional, dict):
        return f"uma entrada por chave, cada uma com {valor_do_campo(adicional, defs)}"
    return "grupo de chaves livres"


def valor_do_campo(no: Any, defs: dict[str, Any]) -> str:
    """Texto do que o campo aceita: texto, lista de textos, data, 'um destes: ...' e assim por diante."""
    no = resolver(no, defs)
    if "enum" in no:
        return f"um destes: {_enum(no['enum'])}"
    if "const" in no:
        return f"sempre {no['const']}"
    if no.get("format") == "date":
        return "data (AAAA-MM-DD)"
    tipos = _tipos(no)
    if tipos == ["array"]:
        return _valor_de_lista(no, defs)
    if tipos == ["object"]:
        return _valor_de_mapa(no, defs)
    desconhecidos = [t for t in tipos if t not in NOMES_DE_TIPO]
    if not tipos or desconhecidos:
        raise ErroDeSchema(f"tipo não reconhecido: {desconhecidos or json.dumps(no, ensure_ascii=False)[:80]}")
    if "number" in tipos and "integer" in tipos:
        tipos.remove("integer")
    nomes = [NOMES_DE_TIPO[t] for t in tipos]
    return nomes[0] if len(nomes) == 1 else ", ".join(nomes[:-1]) + " ou " + nomes[-1]


def _texto_obrigatorio(no: dict[str, Any], campo: str, chave: str) -> str:
    valor = no.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise ErroDeSchema(f"campo `{chave}` sem {campo}")
    return valor


def _filhos(no: dict[str, Any], defs: dict[str, Any], chave: str) -> tuple[dict[str, Any], str]:
    """Propriedades de um grupo ou dos itens de uma lista de grupos, com o prefixo da chave dos filhos."""
    if no.get("properties"):
        return no["properties"], chave + "."
    if "items" in no:
        itens = resolver(no["items"], defs)
        if itens.get("properties"):
            return itens["properties"], chave + "[]."
    return {}, ""


def linhas_de_campos(propriedades: dict[str, Any], defs: dict[str, Any], prefixo: str = "") -> list[list[str]]:
    """Uma linha [Campo, Chave, Valor, O que escrever] por campo, em ordem do schema, com os filhos logo depois."""
    linhas: list[list[str]] = []
    for nome, bruto in propriedades.items():
        chave = prefixo + nome
        if not prefixo and nome == "type":
            continue
        try:
            no = resolver(bruto, defs)
            titulo = _texto_obrigatorio(no, "title", chave)
            descricao = _texto_obrigatorio(no, "description", chave)
            valor = valor_do_campo(no, defs)
            filhos, prefixo_filhos = _filhos(no, defs, chave)
        except ErroDeSchema as erro:
            raise ErroDeSchema(str(erro) if str(erro).startswith(f"campo `{chave}`") else f"campo `{chave}`: {erro}") from None
        linhas.append([titulo, f"`{chave}`", valor, descricao])
        linhas += linhas_de_campos(filhos, defs, prefixo_filhos)
    return linhas


def _frontmatter(titulo: str, descricao: str, titulo_entre_aspas: bool = True) -> str:
    titulo_yaml = json.dumps(titulo, ensure_ascii=False) if titulo_entre_aspas else titulo
    return f"---\ntitle: {titulo_yaml}\ndescription: {json.dumps(descricao, ensure_ascii=False)}\n---"


def pagina_do_tipo(modelo: Modelo, cabecalho: list[dict[str, Any]], schema: dict[str, Any], comum: dict[str, Any]) -> str:
    defs = comum.get("$defs") if isinstance(comum.get("$defs"), dict) else {}
    props_comuns = comum.get("properties") if isinstance(comum.get("properties"), dict) else {}
    do_cabecalho = [[c.get("rotulo"), f"`{c.get('chave')}`", "Sim" if c.get("obrigatorio") is True else "Não"] for c in cabecalho]
    do_tipo = linhas_de_campos(schema["properties"], defs)
    partes = [
        _frontmatter(f"Campos: {modelo.nome}",
                     f"Chave, valor aceito e o que escrever em cada campo do modelo {modelo.nome}."),
        AVISO_DE_GERADO,
        f"Esta página lista, campo a campo, o modelo [{modelo.nome}](../../../templates/{modelo.pagina}/). "
        f"Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja "
        f"[como ler os campos](../../../fundamentos/como-ler-os-campos/).",
        "## Cabeçalho comum\n\nTodo documento começa com estes campos, na mesma ordem.\n\n"
        + tabela_markdown(CABECALHO_COMUM, do_cabecalho),
        f"## Campos do tipo\n\nDepois do cabeçalho, o modelo {modelo.nome} tem estes campos.\n\n"
        + tabela_markdown(CABECALHO_DO_TIPO, do_tipo),
    ]
    tecnicos = {nome: props_comuns[nome] for nome in CAMPOS_TECNICOS if nome in props_comuns}
    if tecnicos:
        partes.append("## Para quem é técnico\n\nBlocos opcionais, iguais em todos os modelos.\n\n"
                      + tabela_markdown(CABECALHO_DO_TIPO, linhas_de_campos(tecnicos, defs)))
    return "\n\n".join(partes) + "\n"


def pagina_indice(modelos: list[Modelo]) -> str:
    itens = [f"- [{m.nome}]({m.slug}/): {m.resumo}" for m in modelos]
    return "\n\n".join([
        _frontmatter("Referência de campos", "Tabela dos campos de cada modelo do Contexto, gerada dos schemas.",
                     titulo_entre_aspas=False),
        AVISO_DE_GERADO,
        "Uma página por modelo, com a chave de cada campo, o valor aceito e o que escrever. Para aprender a "
        "preencher, comece pela página do modelo; para entender as colunas, veja "
        "[como ler os campos](../../fundamentos/como-ler-os-campos/).",
        "\n".join(itens),
    ]) + "\n"


def _ler_schema(caminho: Path, relatorio: Relatorio) -> dict[str, Any] | None:
    relatorio.arquivo_atual = caminho
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except FileNotFoundError:
        relatorio.erro(caminho, "arquivo não encontrado")
        return None
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        relatorio.erro(caminho, f"JSON ilegível: {exc}")
        return None
    if not isinstance(dados, dict) or not isinstance(dados.get("properties"), dict):
        relatorio.erro(caminho, "schema sem o mapa 'properties'")
        return None
    return dados


def _cabecalho(raiz: Path, relatorio: Relatorio) -> list[dict[str, Any]]:
    caminho = raiz / "src" / "data" / "campos.yaml"
    dados = carregar_yaml(caminho, relatorio)
    itens = dados.get("cabecalho") if dados else None
    if dados is not None and (not isinstance(itens, list) or not all(isinstance(i, dict) for i in itens)):
        relatorio.erro(caminho, "falta a lista 'cabecalho' de mapas")
        return []
    return itens or []


def montar_esperados(raiz: Path, relatorio: Relatorio) -> tuple[dict[Path, str], int]:
    """Cada página que deve existir (caminho absoluto, conteúdo) e o total de schemas lidos."""
    pasta = raiz / PASTA_RELATIVA
    modelos = carregar_modelos(raiz / "src" / "data" / "modelos.yaml", relatorio)
    cabecalho = _cabecalho(raiz, relatorio)
    comum = _ler_schema(raiz / "schemas" / "common.schema.json", relatorio)
    esperados: dict[Path, str] = {}
    for modelo in modelos:
        schema = _ler_schema(raiz / "schemas" / f"{modelo.slug}.schema.json", relatorio)
        if schema is None or comum is None:
            continue
        caminho = raiz / "schemas" / f"{modelo.slug}.schema.json"
        try:
            esperados[pasta / f"{modelo.slug}.md"] = pagina_do_tipo(modelo, cabecalho, schema, comum)
        except ErroDeSchema as erro:
            relatorio.erro(caminho, str(erro))
    if modelos and len(esperados) == len(modelos) and not relatorio.erros:
        esperados[pasta / "index.md"] = pagina_indice(modelos)
    return esperados, len(modelos)


def orfaos(raiz: Path, esperados: dict[Path, str]) -> list[Path]:
    pasta = raiz / PASTA_RELATIVA
    return sorted(p for p in pasta.glob("*.md") if p not in esperados) if pasta.is_dir() else []


def _nome(raiz: Path, caminho: Path) -> str:
    try:
        return caminho.relative_to(raiz).as_posix()
    except ValueError:
        return str(caminho)


def executar(raiz: Path, check: bool = False) -> tuple[Relatorio, str]:
    """Devolve o relatório de erros e a mensagem de sucesso. Só escreve se check for falso e não houver erro."""
    relatorio = Relatorio()
    esperados, tipos = montar_esperados(raiz, relatorio)
    sobras = orfaos(raiz, esperados) if not relatorio.erros else []
    if check and not relatorio.erros:
        for caminho, conteudo in esperados.items():
            nome = _nome(raiz, caminho)
            if not caminho.is_file():
                relatorio.erro(None, f"{nome}: ausente; rode python3 scripts/gerar_referencias.py")
            elif caminho.read_bytes() != conteudo.encode("utf-8"):
                relatorio.erro(None, f"{nome}: desatualizado em relação aos schemas; rode python3 scripts/gerar_referencias.py")
        for caminho in sobras:
            relatorio.erro(None, f"{_nome(raiz, caminho)}: órfão, sem tipo em src/data/modelos.yaml; rode python3 scripts/gerar_referencias.py")
    elif not check and not relatorio.erros:
        for caminho, conteudo in esperados.items():
            dados = conteudo.encode("utf-8")
            if not caminho.is_file() or caminho.read_bytes() != dados:
                caminho.parent.mkdir(parents=True, exist_ok=True)
                caminho.write_bytes(dados)
        for caminho in sobras:
            caminho.unlink()
    return relatorio, f"OK: {len(esperados)} páginas de referência em sincronia com {tipos} schemas"


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
