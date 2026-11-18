#!/usr/bin/env python3
"""Gera as saídas para máquinas: schemas publicados, documentos por id@versão, kit para agentes e llms.txt.

Fontes: schemas/ e schemas/historico/, src/exemplos, src/kit, astro.config.mjs. Destinos: public/schemas,
public/documentos, public/downloads/kit e public/llms.txt. Sem flag, escreve só o que mudou e remove os
órfãos das pastas geridas. Com --check, não escreve nada e termina com código 1 se algo estiver fora de sincronia.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import re
import sys
from typing import Any

from check_navegacao import bloco_do_menu, chave, grupos_do_menu
from comum import ROOT, Relatorio, ler_frontmatter
from enderecos import (LICENCA_DO_CONTEUDO, URL_DO_SITE, caminho_do_documento, caminho_do_schema,
                       url_do_documento, url_do_schema)
from gerar_downloads import _data_br
import kit
from kit import Documento

PASTAS_GERIDAS = ("public/schemas", "public/documentos", "public/downloads/kit")
ESTADOS = {"draft": "Rascunho", "pending_approval": "Pendente de aprovação", "approved": "Aprovado",
           "superseded": "Substituído", "deprecated": "Obsoleto"}
CAMINHO_DO_KIT = "public/downloads/kit"
_URN = re.compile(r"^urn:contexto:schemas:(\d+\.\d+\.\d+):([a-z0-9-]+)(#.*)?$")
_SUFIXO_SCHEMA = ".schema.json"
OPCIONAIS = ("referencias", "sobre/creditos")
_DESCRICAO = re.compile(r"\bdescription\s*:\s*'((?:[^'\\]|\\.)*)'")


def _json(dados: Any) -> bytes:
    return (json.dumps(dados, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


# ---------- schemas ----------
def _reescrever(valor: Any) -> Any:
    if isinstance(valor, str):
        achado = _URN.match(valor)
        return url_do_schema(achado.group(1), achado.group(2)) + (achado.group(3) or "") if achado else valor
    if isinstance(valor, list):
        return [_reescrever(v) for v in valor]
    if isinstance(valor, dict):
        return {k: _reescrever(v) for k, v in valor.items()}
    return valor


def _pastas_de_schemas(raiz: Path) -> list[tuple[str, Path]]:
    """(versão, pasta de origem): as históricas em schemas/historico/<versão> e a vigente em schemas/."""
    pastas = [(p.name, p) for p in sorted((raiz / "schemas" / "historico").glob("*")) if p.is_dir()]
    atuais = sorted((raiz / "schemas").glob(f"*{_SUFIXO_SCHEMA}"))
    if atuais:
        try:
            achado = _URN.match(json.loads(atuais[0].read_text(encoding="utf-8")).get("$id", ""))
        except (ValueError, OSError):
            achado = None
        pastas.append((achado.group(1) if achado else "", raiz / "schemas"))
    return pastas


def montar_schemas(raiz: Path, relatorio: Relatorio) -> dict[Path, bytes]:
    saida: dict[Path, bytes] = {}
    for versao, pasta in _pastas_de_schemas(raiz):
        if not versao:
            relatorio.erro(pasta, "não consegui ler a versão no $id do schema (esperado urn:contexto:schemas:<versão>:<slug>)")
            continue
        for fonte in sorted(pasta.glob(f"*{_SUFIXO_SCHEMA}")):
            slug = fonte.name[: -len(_SUFIXO_SCHEMA)]
            try:
                conteudo = _json(_reescrever(json.loads(fonte.read_text(encoding="utf-8"))))
            except (ValueError, OSError) as exc:
                relatorio.erro(fonte, f"schema ilegível: {exc}")
                continue
            if b"urn:contexto" in conteudo:
                relatorio.erro(fonte, "sobrou 'urn:contexto' depois da reescrita; confira os $id e $ref do schema")
                continue
            saida[raiz / "public" / caminho_do_schema(versao, slug)] = conteudo
    return saida


# ---------- documentos ----------
def _iso(valor: Any) -> str | None:
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%Y-%m-%d")
    return None if valor is None else str(valor)


def vigencia(dados: dict[str, Any]) -> str:
    de, ate = _iso(dados.get("valid_from")), _iso(dados.get("valid_to"))
    if de and ate:
        return f"de {_data_br(de)} até {_data_br(ate)}, sem contar o último dia"
    if de:
        return f"de {_data_br(de)}, sem fim previsto"
    return f"até {_data_br(ate)}, sem contar o último dia" if ate else "sem vigência definida"


def vigencia_curta(dados: dict[str, Any]) -> str:
    return vigencia(dados).removesuffix(", sem contar o último dia")


def _texto(valor: Any) -> str:
    return " ".join(str(valor).split()) if valor is not None else ""


def documento_md(dados: dict[str, Any], texto: str, corpo: str, id_: str, versao: str) -> str:
    rev, curta = f"{id_}@{versao}", vigencia_curta(dados)
    quadro = [f"**Estado:** {ESTADOS[dados['status']]}", f"**Vigência:** {vigencia(dados)}"]
    if dados.get("domain"):
        quadro.append(f"**Domínio:** {_texto(dados['domain'])}")
    quadro += [f"**Licença:** {_texto(dados.get('license') or LICENCA_DO_CONTEUDO)}",
               f"**Endereço:** {_texto(dados.get('source_url') or url_do_documento(id_, versao))}"]
    partes = [f"---\n{texto}\n---", f"# {_texto(dados.get('title'))} ({rev})", "\n>\n".join(f"> {q}" for q in quadro)]
    for titulo, valor in (("Pergunta que este documento responde", (dados.get("intent") or {}).get("question")),
                          ("Em poucas palavras", dados.get("plain_summary")), ("Comentário", corpo.strip())):
        if valor and str(valor).strip():
            partes.append(f"## {titulo} ({rev}, {curta})\n\n{str(valor).strip()}")
    return "\n\n".join(partes) + "\n"


def _versao_ordenavel(versao: str) -> tuple[int, ...]:
    return tuple(int(p) if p.isdigit() else 0 for p in versao.split("."))


def _entrada_do_indice(d: Documento) -> dict[str, Any]:
    dados = d.dados
    return {"id": d.id, "version": d.version, "revision_id": dados.get("revision_id") or d.rev, "type": d.type,
            "title": d.title, "status": d.status, "valid_from": _iso(dados.get("valid_from")),
            "valid_to": _iso(dados.get("valid_to")), "license": dados.get("license") or LICENCA_DO_CONTEUDO,
            "md": caminho_do_documento(d.id, d.version), "yaml": caminho_do_documento(d.id, d.version, "yaml")}


def montar_documentos(raiz: Path, relatorio: Relatorio) -> tuple[dict[Path, bytes], list[Documento]]:
    saida: dict[Path, bytes] = {}
    documentos: dict[str, tuple[Documento, Path]] = {}
    for fonte in sorted((raiz / "src" / "exemplos").rglob("*.md")):
        lido = ler_frontmatter(fonte, relatorio)
        if lido is None:
            continue
        dados, texto, corpo = lido
        id_, versao = dados.get("id"), dados.get("version")
        if not isinstance(id_, str) or not isinstance(versao, str):
            relatorio.erro(fonte, "frontmatter sem id ou sem version (ambos devem ser texto)")
            continue
        if dados.get("status") not in ESTADOS:
            relatorio.erro(fonte, f"status desconhecido: {dados.get('status')!r}")
            continue
        try:
            md, yaml_ = caminho_do_documento(id_, versao), caminho_do_documento(id_, versao, "yaml")
        except ValueError as exc:
            relatorio.erro(fonte, str(exc))
            continue
        rev = f"{id_}@{versao}"
        if rev in documentos:
            relatorio.erro(fonte, f"{rev} repetido; já existe em {documentos[rev][1].name}")
            continue
        conteudo = documento_md(dados, texto, corpo, id_, versao).encode("utf-8")
        documentos[rev] = (Documento(id_, versao, _texto(dados.get("title")), str(dados.get("type")), dados["status"], dados, conteudo), fonte)
        saida[raiz / "public" / md], saida[raiz / "public" / yaml_] = conteudo, (texto + "\n").encode("utf-8")
    ordenados = sorted((d for d, _ in documentos.values()), key=lambda d: (d.id, _versao_ordenavel(d.version)))
    if ordenados:
        saida[raiz / "public" / "documentos" / "indice.json"] = _json([_entrada_do_indice(d) for d in ordenados])
    return saida, ordenados


# ---------- kit ----------
def montar_kit(raiz: Path, documentos: list[Documento], relatorio: Relatorio) -> dict[Path, bytes]:
    config = kit.carregar_config(raiz / "src" / "kit" / "kit.yaml", relatorio)
    arquivos = kit.montar_kit(raiz, config, documentos, relatorio) if config else None
    if config is None or arquivos is None:
        return {}
    base = raiz / CAMINHO_DO_KIT
    saida = {base / config.pasta / nome: dados for nome, dados in arquivos.items()}
    saida[base / f"{config.pasta}.zip"] = kit.montar_zip(config.pasta, arquivos)
    return saida


# ---------- llms.txt ----------
def _pagina(docs: Path, rota: str) -> Path | None:
    base = docs / rota
    achados = [base.with_suffix(s) if rota != "/" else docs / f"index{s}" for s in (".mdx", ".md")]
    achados += [base / f"index{s}" for s in (".mdx", ".md")]
    return next((a for a in achados if a.is_file()), None)


def _item(docs: Path, rota: str, relatorio: Relatorio) -> str | None:
    arquivo = _pagina(docs, rota)
    lido = ler_frontmatter(arquivo, relatorio) if arquivo else None
    if lido is None:
        relatorio.erro(None, f"llms.txt: a página do menu '{rota}' não tem arquivo em src/content/docs")
        return None
    url = URL_DO_SITE + ("/" if rota == "/" else f"/{rota}/")
    descricao = _texto(lido[0].get("description"))
    return f"- [{_texto(lido[0].get('title'))}]({url})" + (f": {descricao}" if descricao else "")


def montar_llms(raiz: Path, relatorio: Relatorio) -> dict[Path, bytes]:
    config_js = raiz / "astro.config.mjs"
    if not config_js.is_file():
        return {}
    config = config_js.read_text(encoding="utf-8")
    promessa = _DESCRICAO.search(config)
    if not promessa:
        relatorio.erro(config_js, "llms.txt: não achei description no astro.config.mjs")
        return {}
    docs = raiz / "src" / "content" / "docs"
    secoes = [f"# Contexto\n\n> {promessa.group(1).replace(chr(92) + chr(39), chr(39))}"]
    for grupo in grupos_do_menu(bloco_do_menu(config)):
        itens = [_item(docs, p, relatorio) for p in grupo.paginas if chave(p) not in OPCIONAIS]
        if grupo.rotulo and any(itens):
            secoes.append(f"## {grupo.rotulo}\n\n" + "\n".join(i for i in itens if i))
    versao = max((v for v, _ in _pastas_de_schemas(raiz) if v), key=_versao_ordenavel, default="")
    agentes = [("Kit para agentes (zip)", f"{URL_DO_SITE}/downloads/kit/contexto-kit-agentes.zip", "AGENTS.md, glossário, contratos, gabaritos e a skill de auditoria."),
               ("Índice dos documentos", f"{URL_DO_SITE}/documentos/indice.json", "Lista de todos os documentos por id e versão, com o endereço de cada um."),
               ("Schema comum", url_do_schema(versao, "common") if versao else "", "Campos que todo documento tem.")]
    secoes.append("## Para agentes\n\n" + "\n".join(f"- [{t}]({u}): {d}" for t, u, d in agentes if u))
    opcionais = [_item(docs, rota, relatorio) for rota in OPCIONAIS]
    secoes.append("## Optional\n\n" + "\n".join(o for o in opcionais if o))
    return {raiz / "public" / "llms.txt": ("\n\n".join(secoes) + "\n").encode("utf-8")}


# ---------- orquestração ----------
def montar_esperados(raiz: Path, relatorio: Relatorio) -> dict[Path, bytes]:
    """Cada arquivo que deve existir nas pastas geridas (caminho absoluto, bytes)."""
    documentos, lista = montar_documentos(raiz, relatorio)
    esperados = {**montar_schemas(raiz, relatorio), **documentos, **montar_kit(raiz, lista, relatorio)}
    esperados.update(montar_llms(raiz, relatorio))
    return esperados


def orfaos(raiz: Path, esperados: dict[Path, bytes]) -> list[Path]:
    achados = [p for pasta in PASTAS_GERIDAS if (raiz / pasta).is_dir() for p in (raiz / pasta).rglob("*") if p.is_file()]
    return sorted(p for p in achados if p not in esperados)


def _igual(caminho: Path, conteudo: bytes) -> bool:
    if not caminho.is_file():
        return False
    atual = caminho.read_bytes()
    if caminho.suffix == ".zip":  # compara as entradas, não os bytes, para não depender da versão do Python
        return kit.entradas_do_zip(atual) == kit.entradas_do_zip(conteudo) is not None
    return atual == conteudo


def _nome(raiz: Path, caminho: Path) -> str:
    try:
        return caminho.relative_to(raiz).as_posix()
    except ValueError:
        return str(caminho)


def _remover_pastas_vazias(raiz: Path) -> None:
    for pasta in PASTAS_GERIDAS:
        for p in sorted((raiz / pasta).rglob("*"), reverse=True) if (raiz / pasta).is_dir() else []:
            if p.is_dir() and not any(p.iterdir()):
                p.rmdir()


def executar(raiz: Path, check: bool = False) -> tuple[Relatorio, str]:
    """Devolve o relatório de erros e a mensagem de sucesso. Só escreve se check for falso e não houver erro."""
    relatorio = Relatorio()
    esperados = montar_esperados(raiz, relatorio)
    mensagem = f"OK: {len(esperados)} arquivos de saída em sincronia com as fontes"
    if relatorio.erros:
        return relatorio, mensagem
    sobras = orfaos(raiz, esperados)
    if check:
        for caminho, conteudo in esperados.items():
            if not caminho.is_file():
                relatorio.erro(None, f"{_nome(raiz, caminho)}: ausente; rode npm run gerar:saidas")
            elif not _igual(caminho, conteudo):
                relatorio.erro(None, f"{_nome(raiz, caminho)}: desatualizado em relação à fonte; rode npm run gerar:saidas")
        for caminho in sobras:
            relatorio.erro(None, f"{_nome(raiz, caminho)}: órfão, sem fonte; rode npm run gerar:saidas")
        return relatorio, mensagem
    for caminho, conteudo in esperados.items():
        if not _igual(caminho, conteudo):
            caminho.parent.mkdir(parents=True, exist_ok=True)
            caminho.write_bytes(conteudo)
    for caminho in sobras:
        caminho.unlink()
    _remover_pastas_vazias(raiz)
    return relatorio, mensagem


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
