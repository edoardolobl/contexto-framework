"""Testes de unidade de check_html_gerado, com HTML de exemplo em texto."""
from pathlib import Path

import check_html_gerado as hg

CABECA = '<head><meta property="og:image" content="https://outro.site/x.png"><meta name="theme-color" content="#000"></head>'


def pagina(corpo: str, cabeca: str = CABECA) -> str:
    return f"<html>{cabeca}<body><main>{corpo}</main></body></html>"


def erros(html: str, dist: Path | None = None) -> list[str]:
    return hg.checar_pagina(html, dist or Path("/nao-existe"), "/contexto-framework")


def test_pagina_correta_nao_tem_erro():
    assert erros(pagina("<h1>a</h1><h2>b</h2><h3>c</h3><h2>d</h2>")) == []


def test_pagina_sem_main_e_ignorada():
    assert erros('<html><head><meta http-equiv="refresh" content="0"></head><body></body></html>') == []


def test_sem_h1_ou_com_dois_h1_e_erro():
    assert any("exatamente um h1" in e for e in erros(pagina("<h2>a</h2>")))
    assert any("exatamente um h1" in e for e in erros(pagina("<h1>a</h1><h1>b</h1>")))


def test_pulo_de_nivel_e_erro():
    assert any("h2" in e and "h4" in e for e in erros(pagina("<h1>a</h1><h2>b</h2><h4>c</h4>")))
    assert any("h1" in e and "h3" in e for e in erros(pagina("<h1>a</h1><h3>b</h3>")))


def test_descer_varios_niveis_de_volta_e_permitido():
    assert erros(pagina("<h1>a</h1><h2>b</h2><h3>c</h3><h4>d</h4><h2>e</h2>")) == []


def test_titulos_fora_do_main_nao_contam():
    html = f"<html>{CABECA}<body><h3>menu</h3><main><h1>a</h1></main><h5>rodapé</h5></body></html>"
    assert erros(html) == []


def test_og_image_ausente_ou_repetida_e_erro():
    sem = '<head><meta name="theme-color" content="#000"></head>'
    assert any("og:image" in e for e in erros(pagina("<h1>a</h1>", sem)))
    dupla = '<head><meta property="og:image" content="a"><meta property="og:image" content="b"><meta name="theme-color" content="#000"></head>'
    assert any("og:image" in e for e in erros(pagina("<h1>a</h1>", dupla)))


def test_theme_color_ausente_e_erro():
    sem = '<head><meta property="og:image" content="https://outro.site/x.png"></head>'
    assert any("theme-color" in e for e in erros(pagina("<h1>a</h1>", sem)))


def test_og_image_do_proprio_site_precisa_existir_em_dist(tmp_path: Path):
    cabeca = '<head><meta property="og:image" content="https://exemplo.dev/contexto-framework/og.png"><meta name="theme-color" content="#000"></head>'
    assert any("og.png" in e for e in erros(pagina("<h1>a</h1>", cabeca), tmp_path))
    (tmp_path / "og.png").write_bytes(b"x")
    assert erros(pagina("<h1>a</h1>", cabeca), tmp_path) == []


def test_og_image_com_caminho_absoluto_do_site(tmp_path: Path):
    cabeca = '<head><meta property="og:image" content="/contexto-framework/og.png"><meta name="theme-color" content="#000"></head>'
    assert any("og.png" in e for e in erros(pagina("<h1>a</h1>", cabeca), tmp_path))


def test_conferir_sem_dist_diz_para_rodar_o_build(tmp_path: Path):
    assert hg.conferir(tmp_path / "dist") == ["dist/ não existe. Rode npm run build antes."]


def test_conferir_le_as_paginas(tmp_path: Path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "index.html").write_text(pagina("<h1>a</h1><h3>b</h3>"), encoding="utf-8")
    (tmp_path / "r.html").write_text("<html></html>", encoding="utf-8")
    resultado = hg.conferir(tmp_path)
    assert len(resultado) == 1 and resultado[0].startswith("a/index.html:")
