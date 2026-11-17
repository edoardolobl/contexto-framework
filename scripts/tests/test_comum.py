"""Testes do módulo comum dos validadores."""
from pathlib import Path
import shutil
import subprocess

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


# ---------- ler_frontmatter ----------

def _fonte(tmp_path: Path, conteudo: str) -> Path:
    arquivo = tmp_path / "fonte.md"
    arquivo.write_text(conteudo, encoding="utf-8")
    return arquivo


def test_ler_frontmatter_devolve_dados_texto_e_corpo(tmp_path: Path):
    arquivo = _fonte(tmp_path, "---\n# nota\nid: KPI-1\ntitle: Um\n---\n## Corpo\n\ntexto\n")
    relatorio = comum.Relatorio()
    dados, texto, corpo = comum.ler_frontmatter(arquivo, relatorio)
    assert dados == {"id": "KPI-1", "title": "Um"}
    assert texto == "# nota\nid: KPI-1\ntitle: Um"
    assert corpo == "## Corpo\n\ntexto\n"
    assert relatorio.erros == []


@pytest.mark.parametrize(
    ("conteudo", "trecho"),
    [
        ("id: x\n", "frontmatter ausente"),
        ("", "frontmatter ausente"),
        ("---\nid: x\n", "não fechado"),
        ("---\nid: [sem fim\n---\ncorpo\n", "YAML inválido"),
        ("---\n- a\n- b\n---\ncorpo\n", "mapa"),
        ("---\n---\ncorpo\n", "mapa"),
    ],
)
def test_ler_frontmatter_registra_erro_legivel(tmp_path: Path, conteudo: str, trecho: str):
    relatorio = comum.Relatorio()
    assert comum.ler_frontmatter(_fonte(tmp_path, conteudo), relatorio) is None
    assert len(relatorio.erros) == 1 and trecho in relatorio.erros[0] and "fonte.md" in relatorio.erros[0]


def test_ler_frontmatter_arquivo_inexistente(tmp_path: Path):
    relatorio = comum.Relatorio()
    assert comum.ler_frontmatter(tmp_path / "nada.md", relatorio) is None
    assert "não encontrado" in relatorio.erros[0]


def test_ler_frontmatter_aceita_crlf(tmp_path: Path):
    arquivo = tmp_path / "w.md"
    arquivo.write_bytes(b"---\r\nid: A\r\n---\r\ncorpo\r\n")
    dados, texto, corpo = comum.ler_frontmatter(arquivo, comum.Relatorio())
    assert (dados, texto, corpo) == ({"id": "A"}, "id: A", "corpo\n")


# ---------- constantes ----------

def test_estados_e_ordem_do_cabecalho():
    assert comum.ESTADOS_DO_DOCUMENTO == {"draft", "pending_approval", "approved", "superseded", "deprecated"}
    assert comum.ESTADOS_JA_APROVADOS == {"approved", "superseded"}
    assert comum.HEADER_ORDER[0] == "id" and comum.HEADER_ORDER[-1] == "version_history"
    assert len(comum.HEADER_ORDER) == 22 and len(set(comum.HEADER_ORDER)) == 22
    assert comum.HEADER_ORDER.index("recorded_at") == comum.HEADER_ORDER.index("valid_to") + 1


# ---------- arquivo_de_download ----------

@pytest.mark.parametrize(
    ("url", "esperado"),
    [
        ("../../downloads/template-kpi.yaml", "template-kpi.yaml"),
        ("../downloads/historico/0.x/template-casos-teste.yaml", "historico/0.x/template-casos-teste.yaml"),
        ("downloads/historico/exemplo-kpi-v1.0.yaml#x", "historico/exemplo-kpi-v1.0.yaml"),
        ("https://exemplo.org/downloads/a.yaml", None),
        ("../metodo/limites/", None),
    ],
)
def test_arquivo_de_download_devolve_caminho_relativo(url: str, esperado: str | None):
    assert comum.arquivo_de_download(url) == esperado


# ---------- regras puras de validate_content ----------

def test_ids_citados_inclui_chaves_de_depends_on_versions():
    dados = {"depends_on_versions": {"KPI-A-001": "2.0", "DATASET-B-001": "1.0"}, "related_documents": ["REL-1"]}
    assert set(comum.ids_citados(dados)) == {"KPI-A-001", "DATASET-B-001", "REL-1"}


def test_ids_citados_ignora_depends_on_versions_que_nao_e_mapa():
    assert list(comum.ids_citados({"depends_on_versions": None})) == []
    assert list(comum.ids_citados({"depends_on_versions": ["x"]})) == []


def test_ids_citados_le_fontes_e_perguntas():
    dados = {"data_sources": {"authoritative_dataset": "DATASET-1", "valid_join_paths": ["REL-1"]},
             "questions": [{"required_sources": ["KPI-1"]}]}
    assert set(comum.ids_citados(dados)) == {"DATASET-1", "REL-1", "KPI-1"}


def test_exemplo_completo_exige_pergunta_e_resumo():
    assert comum.faltas_de_leitura({"intent": {"question": "Q?"}, "plain_summary": "R"}) == []
    faltas = comum.faltas_de_leitura({"intent": {"question": " "}, "plain_summary": ""})
    assert faltas == ["intent.question", "plain_summary"]
    assert comum.faltas_de_leitura({}) == ["intent.question", "plain_summary"]
    assert comum.faltas_de_leitura({"intent": "texto", "plain_summary": "R"}) == ["intent.question"]


def test_markdown_de_download_modelo_exige_frontmatter():
    ok = "---\nid: x\n---\n## Identificação\n\n## Histórico de versões\n"
    assert comum.erros_do_markdown_de_download("template-kpi.md", ok) == []
    erros = comum.erros_do_markdown_de_download("template-kpi.md", "## Identificação\n\n## Histórico de versões\n")
    assert erros == ["modelo Markdown deve começar com frontmatter (ADR 0006)"]


def test_markdown_de_download_roteiro_nao_exige_frontmatter_mas_exige_secoes():
    erros = comum.erros_do_markdown_de_download("roteiro-revisao-documental.md", "texto\n")
    assert erros == ["template Markdown sem a seção ## Identificação", "template Markdown sem a seção ## Histórico de versões"]


@pytest.mark.skipif(shutil.which("node") is None, reason="node não está instalado")
def test_regras_do_checklist_visual_passam_no_node_test():
    """Leva visual.test.mjs (node --test) para dentro de `npm run test:scripts`, que só roda pytest."""
    resultado = subprocess.run(["node", "--test", str(comum.ROOT / "scripts" / "tests" / "visual.test.mjs")],
                               capture_output=True, text=True, timeout=120)
    assert resultado.returncode == 0, resultado.stdout[-2000:] + resultado.stderr[-1000:]
