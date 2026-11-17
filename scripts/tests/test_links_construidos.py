"""Testes de check_built_links: caminhos e âncoras (#) no HTML gerado, com um dist/ de exemplo."""
from pathlib import Path

import pytest

import check_built_links as cbl

BASE = "/contexto-framework"


def escrever(dist: Path, relativo: str, corpo: str) -> None:
    arquivo = dist / relativo
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(f"<html><body>{corpo}</body></html>", encoding="utf-8")


@pytest.fixture
def dist(tmp_path: Path) -> Path:
    escrever(tmp_path, "a/index.html", '<h2 id="ficha-de-reconciliação-entre-fontes">x</h2><h1 id="_top">a</h1>')
    return tmp_path


def erros(dist: Path, corpo: str) -> list[str]:
    escrever(dist, "b/index.html", corpo)
    return cbl.conferir(dist, BASE)[0]


def test_ancora_que_existe_na_mesma_pagina_passa(dist: Path):
    assert erros(dist, '<h1 id="_top">b</h1><h2 id="ok">t</h2><a href="#ok">x</a><a href="#_top">topo</a>') == []


def test_ancora_sem_acento_quando_o_id_tem_acento_falha(dist: Path):
    texto = erros(dist, '<a href="#ficha-de-reconciliacao-entre-fontes">x</a>')
    assert any("âncora inexistente" in e and "ficha-de-reconciliacao" in e for e in texto)


def test_ancora_codificada_em_porcentagem_e_decodificada(dist: Path):
    assert erros(dist, '<h2 id="versões">t</h2><a href="#vers%C3%B5es">x</a>') == []


def test_ancora_em_outra_pagina_e_conferida(dist: Path):
    assert erros(dist, '<a href="../a/#ficha-de-reconciliação-entre-fontes">x</a>') == []
    assert any("âncora inexistente" in e for e in erros(dist, '<a href="../a/#nao-tem">x</a>'))


def test_cerquilha_sozinha_e_ignorada(dist: Path):
    assert erros(dist, '<a href="#">x</a>') == []


def test_destino_inexistente_continua_falhando(dist: Path):
    assert any("destino inexistente" in e for e in erros(dist, '<a href="../c/">x</a>'))


def test_link_fora_do_subcaminho_falha(dist: Path):
    assert any("fora do subcaminho" in e for e in erros(dist, '<a href="/outro/">x</a>'))


def test_conta_os_links_conferidos(dist: Path):
    escrever(dist, "b/index.html", '<h1 id="_top">b</h1><a href="#_top">x</a><a href="../a/">y</a><a href="https://e.x/">z</a>')
    assert cbl.conferir(dist, BASE)[1] == 2
