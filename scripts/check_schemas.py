#!/usr/bin/env python3
"""Confere as fontes de src/modelos e src/exemplos contra os JSON Schemas de schemas/ (ADR 0006).

Valida o frontmatter de cada fonte, a ordem do cabeçalho comum, o vínculo entre type, nome de arquivo e
slug de src/data/modelos.yaml e a ordem de src/data/campos.yaml.
"""
from __future__ import annotations

from datetime import date, datetime
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from enderecos import LICENCA_DO_CONTEUDO, url_do_documento
from comum import HEADER_ORDER, ROOT, Relatorio, carregar_modelos, carregar_yaml, ler_frontmatter

MAX_OBRIGATORIOS_NO_NUCLEO = 8
CHAVES_DE_MODELO = tuple(k for k in HEADER_ORDER if k != "recorded_at")
SCHEMA_CONGELADO = "1.0.0"
CAMPOS_DE_PUBLICACAO = ("license", "source_url")


def mensagem_ok(modelos: int, exemplos: int) -> str:
    return f"OK: {modelos} modelos e {exemplos} exemplos válidos no JSON Schema 1.1.0, cabeçalho na ordem"


def para_json(valor: Any) -> Any:
    """Troca datas do YAML por texto ISO, para o JSON Schema enxergar o que um arquivo JSON teria."""
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, dict):
        return {k: para_json(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [para_json(v) for v in valor]
    return valor


def erros_de_ordem(chaves: list[str], exigir_todas: bool) -> list[str]:
    """As chaves do cabeçalho presentes seguem HEADER_ORDER e vêm antes de qualquer outra."""
    erros = []
    presentes = [k for k in chaves if k in HEADER_ORDER]
    esperado = [k for k in HEADER_ORDER if k in presentes]
    if presentes != esperado:
        erros.append(f"ordem do cabeçalho errada: encontrado {', '.join(presentes)}; esperado {', '.join(esperado)}")
    ultimo_do_cabecalho = max((i for i, k in enumerate(chaves) if k in HEADER_ORDER), default=-1)
    for i, chave in enumerate(chaves):
        if chave not in HEADER_ORDER and i < ultimo_do_cabecalho:
            depois = next(k for k in chaves[i + 1:] if k in HEADER_ORDER)
            erros.append(f"a chave {chave} aparece antes de {depois}: as chaves do cabeçalho vêm primeiro, na ordem")
            break
    if exigir_todas:
        erros += [f"falta a chave {k} do cabeçalho no modelo" for k in CHAVES_DE_MODELO if k not in chaves]
    return erros


def _esperado_do_exemplo(dados: dict[str, Any]) -> dict[str, Any]:
    """Valores que um exemplo publicado deve ter; source_url some se id ou version não formam endereço."""
    esperado: dict[str, Any] = {"schema_version": "1.1.0", "license": LICENCA_DO_CONTEUDO}
    try:
        esperado["source_url"] = url_do_documento(dados.get("id"), dados.get("version"))  # type: ignore[arg-type]
    except ValueError:
        esperado["source_url"] = None
    return esperado


def e_copia_historica_1_0_0(dados: dict[str, Any]) -> bool:
    """Cópia histórica (superseded, com recorded_at) que declara o schema 1.0.0 com que foi aprovada."""
    return (dados.get("schema_version") == SCHEMA_CONGELADO and dados.get("status") == "superseded"
            and dados.get("recorded_at") is not None)


def erros_de_publicacao(dados: dict[str, Any], modelo: bool) -> list[str]:
    """Modelo: license e source_url presentes e null. Exemplo: schema 1.1.0, licença do conteúdo e URL do documento.

    A cópia histórica guarda o texto como foi aprovado (contrato editorial): se declara 1.0.0, fica sem os dois campos.
    """
    if not modelo and e_copia_historica_1_0_0(dados):
        return [f"{k} não existe no schema {SCHEMA_CONGELADO}: a cópia histórica fica como foi aprovada"
                for k in CAMPOS_DE_PUBLICACAO if k in dados]
    if modelo:
        esperado: dict[str, Any] = {"license": None, "source_url": None}
        presentes = [k for k in esperado if k in dados]
        erros = [f"falta a chave {k}: o modelo traz {k}: null" for k in esperado if k not in presentes]
        return erros + [f"{k} deve ser null no modelo em branco (cada time define o seu), encontrado {dados[k]!r}"
                        for k in presentes if dados[k] is not None]
    esperado = _esperado_do_exemplo(dados)
    erros = [f"{k} deve ser {valor!r}, encontrado {dados.get(k)!r}" for k, valor in esperado.items()
             if valor is not None and dados.get(k) != valor]
    if esperado["source_url"] is None:
        erros.append("source_url não pôde ser calculado: id (como KPI-AURORA-001) ou version (como 2.0) fora do padrão")
    return erros


def erros_de_perguntas(dados: dict[str, Any]) -> list[str]:
    """also_accepted não pode repetir o expected_behavior da mesma pergunta (o esperado já vale)."""
    perguntas = dados.get("questions")
    if not isinstance(perguntas, list):
        return []
    erros: list[str] = []
    for pergunta in (q for q in perguntas if isinstance(q, dict) and isinstance(q.get("also_accepted"), list)):
        for aceita in (a for a in pergunta["also_accepted"] if isinstance(a, dict)):
            if aceita.get("behavior") == pergunta.get("expected_behavior"):
                erros.append(f"questions.{pergunta.get('id')}.also_accepted: behavior {aceita.get('behavior')!r} "
                             "repete o expected_behavior da mesma pergunta")
    return erros


def erros_de_campos(itens: list[dict[str, Any]], chaves_do_comum: set[str]) -> list[str]:
    """Regras de src/data/campos.yaml: ordem do cabeçalho, chaves no comum e núcleo curto (ADR 0006)."""
    erros = []
    bases = [str(i.get("chave", "")).split(".")[0] for i in itens]
    # intent.question, intent.audience... seguidas contam como um só bloco; separadas, ficam fora da ordem
    conhecidas = [b for i, b in enumerate(bases) if b in HEADER_ORDER and (i == 0 or bases[i - 1] != b)]
    if conhecidas != [k for k in HEADER_ORDER if k in conhecidas]:
        erros.append(f"a ordem do cabecalho deve seguir HEADER_ORDER: encontrado {', '.join(conhecidas)}")
    for item, base in zip(itens, bases):
        if base not in chaves_do_comum:
            erros.append(f"a chave {item.get('chave')} não existe em common.schema.json")
    obrigatorios = sum(1 for i in itens if i.get("obrigatorio") is True)
    if obrigatorios > MAX_OBRIGATORIOS_NO_NUCLEO:
        erros.append(f"{obrigatorios} campos obrigatórios; o núcleo curto aceita no máximo {MAX_OBRIGATORIOS_NO_NUCLEO} (ADR 0006)")
    return erros


def titulo_do_campo(schema: dict[str, Any], chave: str) -> str | None:
    """Título de um campo do tipo pelo caminho com pontos ("dataset.physicalName", "columns[].physicalType")."""
    no: Any = schema
    for parte in chave.split("."):
        lista = parte.endswith("[]")
        nome = parte[:-2] if lista else parte
        no = (no.get("properties") or {}).get(nome) if isinstance(no, dict) else None
        if not isinstance(no, dict):
            return None
        if lista:
            no = no.get("items") if no.get("type") == "array" else None
    titulo = no.get("title") if isinstance(no, dict) else None
    return titulo if isinstance(titulo, str) else None


def erros_de_rotulos_do_tipo(itens: list[dict[str, Any]], schemas: dict[str, dict[str, Any]]) -> list[str]:
    """Seção campos_do_tipo de src/data/campos.yaml: cada rótulo repete o title do campo no schema do tipo."""
    erros = []
    for item in itens:
        tipo, chave, rotulo = item.get("tipo"), str(item.get("chave", "")), item.get("rotulo")
        if tipo not in schemas:
            erros.append(f"campos_do_tipo: o tipo {tipo} não tem schema")
            continue
        titulo = titulo_do_campo(schemas[tipo], chave)
        if titulo is None:
            erros.append(f"campos_do_tipo: a chave {chave} não existe no schema {tipo}")
        elif titulo != rotulo:
            erros.append(f"campos_do_tipo: o rótulo de {tipo} {chave} é \"{rotulo}\", mas o schema diz \"{titulo}\"")
    return erros


def _carregar_schemas(pasta: Path, relatorio: Relatorio) -> dict[str, dict[str, Any]]:
    """Schemas por slug (nome do arquivo sem .schema.json). Inválidos viram erro e saem."""
    schemas: dict[str, dict[str, Any]] = {}
    for caminho in sorted(pasta.glob("*.schema.json")):
        relatorio.arquivo_atual = caminho
        try:
            schema = json.loads(caminho.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            relatorio.erro(caminho, f"JSON inválido: {exc}")
            continue
        except (OSError, UnicodeDecodeError) as exc:
            relatorio.erro(caminho, f"não foi possível ler o arquivo: {exc}")
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            relatorio.erro(caminho, f"schema inválido: {exc.message}")
            continue
        if not isinstance(schema, dict) or not isinstance(schema.get("$id"), str):
            relatorio.erro(caminho, "schema sem $id (use urn:contexto:schemas:1.1.0:<slug>)")
            continue
        schemas[caminho.name.removesuffix(".schema.json")] = schema
    return schemas


def _registro(schemas: dict[str, dict[str, Any]]) -> Registry:
    recursos = [(s["$id"], Resource(contents=s, specification=DRAFT202012)) for s in schemas.values()]
    return Registry().with_resources(recursos)


def _validar(caminho: Path, dados: dict[str, Any], validador: Draft202012Validator, relatorio: Relatorio) -> None:
    try:
        achados = sorted(validador.iter_errors(para_json(dados)), key=lambda e: [str(p) for p in e.absolute_path])
    except Exception as exc:  # referência não resolvida e similares: erro legível, sem traceback
        relatorio.erro(caminho, f"não foi possível validar no schema: {type(exc).__name__}: {exc}")
        return
    for erro in achados:
        onde = ".".join(str(p) for p in erro.absolute_path) or "(raiz)"
        relatorio.erro(caminho, f"{onde}: {erro.message}")


def _checar_fonte(caminho: Path, modelo: bool, schemas: dict[str, dict[str, Any]],
                  registro: Registry, relatorio: Relatorio) -> None:
    lido = ler_frontmatter(caminho, relatorio)
    if lido is None:
        return
    dados = lido[0]
    tipo = dados.get("type")
    for erro in erros_de_ordem(list(dados), exigir_todas=modelo):
        relatorio.erro(caminho, erro)
    if not isinstance(tipo, str):
        relatorio.erro(caminho, "type ausente ou que não é texto")
        return
    if modelo and tipo != caminho.stem:
        relatorio.erro(caminho, f"type {tipo!r} deve ser igual ao nome do arquivo ({caminho.stem})")
    if not modelo and not caminho.name.startswith(f"exemplo-{tipo}-"):
        relatorio.erro(caminho, f"o nome do exemplo deve começar com exemplo-{tipo}-")
    if tipo not in schemas:
        relatorio.erro(caminho, f"sem schemas/{tipo}.schema.json para validar type {tipo!r}")
        return
    for erro in erros_de_publicacao(dados, modelo):
        relatorio.erro(caminho, erro)
    validador = Draft202012Validator(schemas[tipo], registry=registro, format_checker=FormatChecker())
    _validar(caminho, dados, validador, relatorio)
    if tipo == "perguntas-de-negocio":
        for erro in erros_de_perguntas(dados):
            relatorio.erro(caminho, erro)


def _checar_vinculos(raiz: Path, slugs: list[str], schemas: dict[str, dict[str, Any]], relatorio: Relatorio) -> None:
    for slug in slugs:
        if slug not in schemas:
            relatorio.erro(raiz / "src/data/modelos.yaml", f"tipo {slug} sem schemas/{slug}.schema.json")
        if not (raiz / "src" / "modelos" / f"{slug}.md").is_file():
            relatorio.erro(raiz / "src/data/modelos.yaml", f"tipo {slug} sem src/modelos/{slug}.md")
    for slug in schemas:
        if slug != "common" and slug not in slugs:
            relatorio.erro(raiz / "schemas" / f"{slug}.schema.json", "schema sem tipo correspondente em src/data/modelos.yaml")
    for fonte in sorted((raiz / "src" / "modelos").glob("*.md")):
        if fonte.stem not in slugs:
            relatorio.erro(fonte, "modelo sem tipo correspondente em src/data/modelos.yaml")


def _checar_campos(raiz: Path, schemas: dict[str, dict[str, Any]], relatorio: Relatorio) -> None:
    comum_schema = schemas.get("common")
    caminho = raiz / "src" / "data" / "campos.yaml"
    dados = carregar_yaml(caminho, relatorio)
    if dados is None:
        return
    itens = dados.get("cabecalho")
    if not isinstance(itens, list) or not all(isinstance(i, dict) for i in itens):
        relatorio.erro(caminho, "falta a lista 'cabecalho' de mapas")
        return
    propriedades = set((comum_schema or {}).get("properties", {}))
    for erro in erros_de_campos(itens, propriedades):
        relatorio.erro(caminho, erro)
    do_tipo = dados.get("campos_do_tipo", [])
    if not isinstance(do_tipo, list) or not all(isinstance(i, dict) for i in do_tipo):
        relatorio.erro(caminho, "campos_do_tipo deve ser uma lista de mapas")
        return
    for erro in erros_de_rotulos_do_tipo(do_tipo, schemas):
        relatorio.erro(caminho, erro)


def executar(raiz: Path) -> tuple[Relatorio, int, int]:
    """Roda todas as conferências sobre `raiz`. Devolve o relatório e as contagens de modelos e exemplos."""
    relatorio = Relatorio()
    schemas = _carregar_schemas(raiz / "schemas", relatorio)
    if not schemas:
        relatorio.erro(None, "nenhum schemas/*.schema.json válido encontrado")
    if "common" not in schemas:
        relatorio.erro(raiz / "schemas" / "common.schema.json", "schema comum ausente ou inválido")
    registro = _registro(schemas)
    modelos = sorted((raiz / "src" / "modelos").glob("*.md"))
    exemplos = sorted((raiz / "src" / "exemplos").rglob("*.md"))
    for fonte in modelos:
        _checar_fonte(fonte, True, schemas, registro, relatorio)
    for fonte in exemplos:
        _checar_fonte(fonte, False, schemas, registro, relatorio)
    slugs = [m.slug for m in carregar_modelos(raiz / "src" / "data" / "modelos.yaml", relatorio)]
    _checar_vinculos(raiz, slugs, schemas, relatorio)
    _checar_campos(raiz, schemas, relatorio)
    return relatorio, len(modelos), len(exemplos)


def main() -> None:
    relatorio, modelos, exemplos = executar(ROOT)
    relatorio.instalar()
    relatorio.encerrar(mensagem_ok(modelos, exemplos))


if __name__ == "__main__":
    main()
