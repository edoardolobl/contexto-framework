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
