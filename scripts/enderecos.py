"""Endereços publicados do Contexto: caminhos e URLs de documentos e schemas (ADR 0011).

Funções puras, sem ler ambiente nem disco. A URL do site é a canônica; quem publica em outro
endereço troca esta constante num só lugar.
"""
from __future__ import annotations

import re

URL_DO_SITE = "https://edoardolobl.github.io/contexto-framework"
LICENCA_DO_CONTEUDO = "CC-BY-4.0"

_PADRAO_ID = re.compile(r"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+")
_PADRAO_VERSAO = re.compile(r"\d+\.\d+(\.\d+)?")


def _conferir(valor: object, padrao: re.Pattern[str], nome: str, exemplo: str) -> str:
    if not isinstance(valor, str) or not padrao.fullmatch(valor):
        raise ValueError(f"{nome} fora do padrão: {valor!r} (exemplo: {exemplo})")
    return valor


def caminho_do_documento(id_: str, versao: str, extensao: str = "md") -> str:
    """Caminho relativo ao site: documentos/<id>@<versao>.<extensao>."""
    _conferir(id_, _PADRAO_ID, "id", "KPI-AURORA-001")
    _conferir(versao, _PADRAO_VERSAO, "versão", "2.0")
    return f"documentos/{id_}@{versao}.{extensao}"


def url_do_documento(id_: str, versao: str, extensao: str = "md") -> str:
    return f"{URL_DO_SITE}/{caminho_do_documento(id_, versao, extensao)}"


def caminho_do_schema(versao: str, slug: str) -> str:
    """Caminho relativo ao site: schemas/<versao>/<slug>.schema.json."""
    _conferir(versao, _PADRAO_VERSAO, "versão", "1.1.0")
    return f"schemas/{versao}/{slug}.schema.json"


def url_do_schema(versao: str, slug: str) -> str:
    return f"{URL_DO_SITE}/{caminho_do_schema(versao, slug)}"
