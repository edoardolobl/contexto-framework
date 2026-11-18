"""Testes do módulo comum dos validadores."""
from pathlib import Path

import pytest

import comum


def test_carregar_yaml_devolve_o_mapa(tmp_path: Path):
    arquivo = tmp_path / "ok.yaml"
    arquivo.write_text("id: KPI-1\nstatus: draft\n", encoding="utf-8")
    relatorio = comum.Relatorio()
    assert comum.carregar_yaml(arquivo, relatorio) == {"id": "KPI-1", "status": "draft"}
    assert relatorio.erros == []


@pytest.mark.parametrize(
    ("conteudo", "trecho_do_erro"),
    [("", "mapa na raiz"), ("- a\n- b\n", "mapa na raiz"), ("id: [sem fim\n", "YAML inválido")],
)
def test_carregar_yaml_registra_erro_em_vez_de_quebrar(tmp_path: Path, conteudo: str, trecho_do_erro: str):
    arquivo = tmp_path / "ruim.yaml"
    arquivo.write_text(conteudo, encoding="utf-8")
    relatorio = comum.Relatorio()
    assert comum.carregar_yaml(arquivo, relatorio) is None
    assert len(relatorio.erros) == 1 and trecho_do_erro in relatorio.erros[0]


def test_carregar_yaml_arquivo_inexistente(tmp_path: Path):
    relatorio = comum.Relatorio()
    assert comum.carregar_yaml(tmp_path / "nao-existe.yaml", relatorio) is None
    assert "não encontrado" in relatorio.erros[0]


def test_exigir_minimo_acusa_busca_vazia():
    relatorio = comum.Relatorio()
    assert comum.exigir_minimo([], 1, "arquivos YAML", relatorio) == []
    assert relatorio.erros == ["esperado pelo menos 1 arquivos YAML, encontrado 0"]


def test_exigir_minimo_devolve_lista_ordenada(tmp_path: Path):
    b, a = tmp_path / "b", tmp_path / "a"
    relatorio = comum.Relatorio()
    assert comum.exigir_minimo([b, a], 2, "itens", relatorio) == [a, b]
    assert relatorio.erros == []


def test_encerrar_com_erro_sai_com_codigo_1(capsys):
    relatorio = comum.Relatorio()
    relatorio.erro(None, "algo errado")
    with pytest.raises(SystemExit) as saida:
        relatorio.encerrar("OK")
    assert saida.value.code == 1
    assert "ERRO: algo errado" in capsys.readouterr().out


def test_encerrar_sem_erro_imprime_ok(capsys):
    comum.Relatorio().encerrar("OK: tudo certo")
    assert capsys.readouterr().out.strip() == "OK: tudo certo"


def test_gancho_troca_traceback_por_linha_de_erro(capsys, monkeypatch):
    relatorio = comum.Relatorio(arquivo_atual=comum.ROOT / "public" / "downloads" / "x.yaml")
    monkeypatch.setattr("sys.excepthook", None)
    relatorio.instalar()
    import sys

    try:
        raise KeyError("calculation")
    except KeyError as exc:
        tb = exc.__traceback__
    with pytest.raises(SystemExit) as saida:
        sys.excepthook(KeyError, KeyError("calculation"), tb)
    assert saida.value.code == 1
    saida_texto = capsys.readouterr().out
    assert "ERRO: falha inesperada (último arquivo lido: public/downloads/x.yaml; em scripts/tests/test_comum.py:" in saida_texto
    assert "KeyError 'calculation'" in saida_texto


def test_relativo_fora_do_repositorio_devolve_caminho_inteiro(tmp_path: Path):
    assert comum.relativo(tmp_path) == str(tmp_path)


def test_carregar_yaml_data_impossivel_vira_erro(tmp_path: Path):
    arquivo = tmp_path / "data.yaml"
    arquivo.write_text("valid_from: 2026-99-99\n", encoding="utf-8")
    relatorio = comum.Relatorio()
    assert comum.carregar_yaml(arquivo, relatorio) is None
    assert "data.yaml" in relatorio.erros[0]


def test_carregar_yaml_bytes_que_nao_sao_utf8_viram_erro(tmp_path: Path):
    arquivo = tmp_path / "latin.yaml"
    arquivo.write_bytes("título: ação".encode("latin-1"))
    relatorio = comum.Relatorio()
    assert comum.carregar_yaml(arquivo, relatorio) is None
    assert "UTF-8" in relatorio.erros[0]


def test_mesmo_erro_nao_se_repete():
    relatorio = comum.Relatorio()
    relatorio.erro(None, "data inválida")
    relatorio.erro(None, "data inválida")
    assert relatorio.erros == ["data inválida"]


def test_gancho_diz_ultimo_arquivo_e_onde_o_script_falhou(capsys, monkeypatch):
    relatorio = comum.Relatorio(arquivo_atual=comum.ROOT / "README.md")
    monkeypatch.setattr("sys.excepthook", None)
    relatorio.instalar()
    import sys

    try:
        raise AttributeError("x")
    except AttributeError as exc:
        tb = exc.__traceback__
    with pytest.raises(SystemExit):
        sys.excepthook(AttributeError, AttributeError("x"), tb)
    saida = capsys.readouterr().out
    assert "último arquivo lido: README.md" in saida
    assert "test_comum.py:" in saida


def test_aviso_sai_em_linha_aviso_e_nao_muda_o_codigo_de_saida(capsys):
    relatorio = comum.Relatorio()
    relatorio.aviso(comum.ROOT / "README.md", "data em sábado")
    relatorio.encerrar("OK: tudo certo")
    saida = capsys.readouterr().out
    assert "AVISO: README.md: data em sábado" in saida
    assert "OK: tudo certo" in saida
    assert relatorio.erros == []


def test_aviso_aparece_junto_dos_erros_e_o_codigo_continua_1(capsys):
    relatorio = comum.Relatorio()
    relatorio.aviso(None, "cuidado")
    relatorio.erro(None, "quebrou")
    with pytest.raises(SystemExit) as saida:
        relatorio.encerrar("OK")
    assert saida.value.code == 1
    texto = capsys.readouterr().out
    assert "AVISO: cuidado" in texto and "ERRO: quebrou" in texto


def test_mesmo_aviso_nao_se_repete():
    relatorio = comum.Relatorio()
    relatorio.aviso(None, "x")
    relatorio.aviso(None, "x")
    assert relatorio.avisos == ["x"]


def test_links_do_repositorio_ausentes_acusa_arquivo_que_nao_existe(tmp_path: Path):
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs" / "adr" / "0001-existe.md").write_text("# ok\n", encoding="utf-8")
    base = "https://github.com/edoardolobl/contexto-framework/blob/main/"
    texto = (
        f"[ok]({base}docs/adr/0001-existe.md) e [falta]({base}docs/adr/0099-falta.md#contexto) "
        '<a href="https://github.com/edoardolobl/contexto-framework/tree/main/docs/nada">pasta</a>'
    )
    assert comum.links_do_repositorio_ausentes(texto, tmp_path) == ["docs/adr/0099-falta.md", "docs/nada"]


def test_links_do_repositorio_ausentes_ignora_outros_enderecos(tmp_path: Path):
    texto = (
        "[repo](https://github.com/edoardolobl/contexto-framework) "
        "[outro](https://github.com/outra/coisa/blob/main/x.md) "
        "[pasta](https://github.com/edoardolobl/contexto-framework/tree/main/docs)"
    )
    (tmp_path / "docs").mkdir()
    assert comum.links_do_repositorio_ausentes(texto, tmp_path) == []
