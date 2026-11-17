"""Integração com mutações: copia o repositório para uma pasta temporária, estraga um arquivo e
confere que o validador acusa o problema com uma linha ERRO, sem traceback."""
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest

import comum

IGNORAR = shutil.ignore_patterns("node_modules", "dist", ".astro", ".git", ".codegraph", "auditoria", "__pycache__", ".pytest_cache")


@pytest.fixture
def copia(tmp_path: Path) -> Path:
    destino = tmp_path / "repo"
    shutil.copytree(comum.ROOT, destino, ignore=IGNORAR)
    return destino


def rodar(raiz: Path, script: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(raiz / "scripts" / script)], capture_output=True, text=True, timeout=120)


def test_version_history_com_item_que_nao_e_mapa(copia: Path):
    arquivo = copia / "public" / "downloads" / "exemplo-kpi-lacunas.yaml"
    texto = arquivo.read_text(encoding="utf-8")
    arquivo.write_text(texto.replace("version_history:\n", "version_history:\n  - texto solto\n", 1), encoding="utf-8")
    resultado = rodar(copia, "check_revisions.py")
    assert resultado.returncode == 1
    assert "version_history deve conter só mapas" in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_menu_com_aspas_duplas_continua_valido(copia: Path):
    config = copia / "astro.config.mjs"
    config.write_text(config.read_text(encoding="utf-8").replace("'templates/kpi'", '"templates/kpi"'), encoding="utf-8")
    resultado = rodar(copia, "validate_content.py")
    assert resultado.returncode == 0, resultado.stdout


def test_menu_sem_um_tipo_e_acusado(copia: Path):
    config = copia / "astro.config.mjs"
    config.write_text(config.read_text(encoding="utf-8").replace("'templates/kpi', ", ""), encoding="utf-8")
    resultado = rodar(copia, "validate_content.py")
    assert resultado.returncode == 1
    assert "o menu não lista templates/kpi" in resultado.stdout


def test_sem_bloco_de_menu_e_acusado(copia: Path):
    config = copia / "astro.config.mjs"
    config.write_text(config.read_text(encoding="utf-8").replace("sidebar: [", "barra: ["), encoding="utf-8")
    resultado = rodar(copia, "validate_content.py")
    assert resultado.returncode == 1
    assert "bloco 'sidebar: [' não encontrado" in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_regra_de_vocabulario_com_erro_de_digitacao_falha(copia: Path):
    vocab = copia / "src" / "data" / "vocabulario.yaml"
    vocab.write_text(vocab.read_text(encoding="utf-8").replace("padrao: '\\bdonos?\\b'", "padroa: '\\bdonos?\\b'"), encoding="utf-8")
    resultado = rodar(copia, "validate_content.py")
    assert resultado.returncode == 1
    assert "sem padrao" in resultado.stdout


def test_carregar_yaml_em_pasta_vira_erro(tmp_path: Path):
    relatorio = comum.Relatorio()
    assert comum.carregar_yaml(tmp_path, relatorio) is None
    assert relatorio.erros and "não foi possível ler" in relatorio.erros[0]


def test_artefato_citado_antes_de_existir_e_acusado(copia: Path):
    arquivo = copia / "public" / "downloads" / "exemplo-kpi-lacunas.yaml"
    texto = arquivo.read_text(encoding="utf-8")
    arquivo.write_text(texto.replace('concept: "', 'concept: "aurora-reference-query.sql ', 1), encoding="utf-8")
    resultado = rodar(copia, "check_revisions.py")
    assert resultado.returncode == 1
    assert "versão de 2026-07-20 cita aurora-reference-query.sql, que só existe a partir de 2026-09-15" in resultado.stdout
    assert "Traceback" not in resultado.stdout + resultado.stderr


def test_link_para_adr_inexistente_e_acusado(copia: Path):
    (copia / "docs" / "adr" / "0021-responder-esclarecer-ou-abster-se.md").unlink()
    resultado = rodar(copia, "validate_content.py")
    assert resultado.returncode == 1
    assert "link para arquivo do repositório que não existe: docs/adr/0021-responder-esclarecer-ou-abster-se.md" in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_percurso_sem_nextstep_e_acusado(copia: Path):
    pagina = copia / "src" / "content" / "docs" / "percurso" / "delimite-o-acervo.mdx"
    pagina.write_text(pagina.read_text(encoding="utf-8").replace("<NextStep", "<Removido"), encoding="utf-8")
    resultado = rodar(copia, "check_navegacao.py")
    assert resultado.returncode == 1
    assert "próximo passo ausente: percurso/delimite-o-acervo" in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_pagina_fora_do_menu_e_sem_link_e_orfa(copia: Path):
    config = copia / "astro.config.mjs"
    texto = config.read_text(encoding="utf-8")
    assert "'metodo/limites'" in texto
    config.write_text(re.sub(r"'metodo/limites',?\s*", "", texto), encoding="utf-8")
    for pagina in (copia / "src" / "content" / "docs").rglob("*.mdx"):
        conteudo = pagina.read_text(encoding="utf-8")
        pagina.write_text(re.sub(r"\]\([^)]*metodo/limites[^)]*\)|\]\([^)]*/limites/?[^)]*\)", "](#)", conteudo), encoding="utf-8")
    resultado = rodar(copia, "check_navegacao.py")
    assert resultado.returncode == 1
    assert "página órfã: metodo/limites" in resultado.stdout
    assert "Traceback" not in resultado.stderr
