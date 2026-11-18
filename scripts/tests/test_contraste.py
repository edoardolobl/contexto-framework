"""Testes de unidade de check_contraste, com CSS e YAML de exemplo em tmp_path."""
from pathlib import Path

import pytest

import comum
import check_contraste as cc

CSS = """
:root { --fundo: #000; --texto: #fff; --ouro: var(--base); --base: #ffd700; }
:root { --extra: #123456; }
:root[data-theme='light'] { --fundo: #ffffff; --texto: #000000; --base: #fdd; }
"""


def test_converte_hex_curto_e_longo():
    assert cc.hex_para_rgb("#fff") == (255, 255, 255)
    assert cc.hex_para_rgb("#0a0B0c") == (10, 11, 12)


@pytest.mark.parametrize("ruim", ["fff", "#ffff", "#ggg", "red", ""])
def test_hex_invalido_levanta_valueerror(ruim):
    with pytest.raises(ValueError):
        cc.hex_para_rgb(ruim)


def test_luminancia_e_razao_da_wcag():
    assert cc.luminancia((255, 255, 255)) == pytest.approx(1.0)
    assert cc.luminancia((0, 0, 0)) == 0.0
    assert cc.razao_de_contraste((0, 0, 0), (255, 255, 255)) == pytest.approx(21.0)
    assert cc.razao_de_contraste((255, 255, 255), (255, 255, 255)) == pytest.approx(1.0)
    assert cc.razao_de_contraste((119, 119, 119), (255, 255, 255)) == pytest.approx(4.48, abs=0.01)


def test_tema_escuro_junta_blocos_root_e_claro_sobrepoe():
    escuro = cc.tokens_do_tema(CSS, "escuro")
    claro = cc.tokens_do_tema(CSS, "claro")
    assert escuro["--extra"] == "#123456" and escuro["--fundo"] == "#000"
    assert claro["--fundo"] == "#ffffff" and claro["--extra"] == "#123456"


def test_aceita_aspas_duplas_no_seletor_claro():
    css = ':root { --a: #000; }\n:root[data-theme="light"] { --a: #fff; }'
    assert cc.tokens_do_tema(css, "claro")["--a"] == "#fff"


def test_resolve_var_e_respeita_o_tema():
    assert cc.resolver("--ouro", cc.tokens_do_tema(CSS, "escuro")) == "#ffd700"
    assert cc.resolver("--ouro", cc.tokens_do_tema(CSS, "claro")) == "#fdd"


def test_valor_rgb_nao_e_suportado_vira_erro():
    with pytest.raises(cc.TokenInvalido):
        cc.resolver("--a", {"--a": "rgb(1,2,3)"})


def test_ciclo_e_detectado():
    with pytest.raises(cc.TokenInvalido, match="ciclo"):
        cc.resolver("--a", {"--a": "var(--b)", "--b": "var(--a)"})


def test_token_ausente_e_acusado():
    with pytest.raises(cc.TokenInvalido, match="--nada"):
        cc.resolver("--nada", {})


def test_token_que_nao_termina_em_hex_e_acusado():
    with pytest.raises(cc.TokenInvalido, match="hex"):
        cc.resolver("--a", {"--a": "red"})


def par(**extra):
    base = {"nome": "texto", "frente": "--texto", "fundos": ["--fundo"], "minimo": 4.5}
    base.update(extra)
    return base


def test_verificar_par_formata_mensagem_com_virgula_decimal():
    css = ":root { --f: #ffffff; --t: #cccccc; } :root[data-theme='light'] { --f: #ffffff; }"
    erros = cc.verificar_pares([par(frente="--t", fundos=["--f"])], css)
    assert erros and erros[0].startswith("tema escuro: --t sobre --f dá ") and "," in erros[0]
    assert erros[0].endswith("mínimo 4,5:1")


def test_verificar_par_respeita_temas_e_passa_quando_contraste_basta():
    assert cc.verificar_pares([par()], CSS) == []
    css = ":root { --fundo: #000; --texto: #fff; } :root[data-theme='light'] { --fundo: #fff; --texto: #eee; }"
    erros = cc.verificar_pares([par()], css)
    assert len(erros) == 1 and erros[0].startswith("tema claro:")
    assert cc.verificar_pares([par(temas=["escuro"])], css) == []


def escrever(tmp_path: Path, css: str, pares: str) -> tuple[Path, Path]:
    (tmp_path / "c.css").write_text(css, encoding="utf-8")
    (tmp_path / "c.yaml").write_text(pares, encoding="utf-8")
    return tmp_path / "c.css", tmp_path / "c.yaml"


def pares_yaml(n: int, minimo: str = "4.5") -> str:
    item = "  - nome: p{i}\n    frente: --texto\n    fundos: [--fundo]\n    minimo: " + minimo + "\n"
    return "pares:\n" + "".join(item.format(i=i) for i in range(n))


def test_carregar_exige_pelo_menos_5_pares(tmp_path: Path):
    css, yml = escrever(tmp_path, CSS, pares_yaml(4))
    rel = comum.Relatorio()
    cc.conferir(css, yml, rel)
    assert any("pelo menos 5" in e for e in rel.erros)


def test_conferir_passa_com_5_pares_bons(tmp_path: Path):
    css, yml = escrever(tmp_path, CSS, pares_yaml(5))
    rel = comum.Relatorio()
    assert cc.conferir(css, yml, rel) == 5
    assert rel.erros == []


@pytest.mark.parametrize("corpo", ["", "pares: 3\n", "a: [\n", "pares: [1,2,3,4,5]\n",
                                    "pares:\n  - nome: x\n"] )
def test_yaml_vazio_quebrado_ou_sem_campo_vira_erro(tmp_path: Path, corpo):
    css, yml = escrever(tmp_path, CSS, corpo)
    rel = comum.Relatorio()
    cc.conferir(css, yml, rel)
    assert rel.erros


def test_minimo_nao_numerico_ou_tema_desconhecido_vira_erro(tmp_path: Path):
    css, yml = escrever(tmp_path, CSS, pares_yaml(5, "alto"))
    rel = comum.Relatorio()
    cc.conferir(css, yml, rel)
    assert any("minimo" in e for e in rel.erros)
    css, yml = escrever(tmp_path, CSS, pares_yaml(5) + "    temas: [roxo]\n")
    rel = comum.Relatorio()
    cc.conferir(css, yml, rel)
    assert any("tema" in e for e in rel.erros)


def test_css_ausente_vira_erro(tmp_path: Path):
    _, yml = escrever(tmp_path, CSS, pares_yaml(5))
    rel = comum.Relatorio()
    cc.conferir(tmp_path / "nao.css", yml, rel)
    assert any("nao.css" in e for e in rel.erros)
