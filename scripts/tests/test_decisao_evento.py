"""Regra canônica de evento quebrado: check_decision_examples confere o exemplo por glob."""
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import comum

IGNORAR = shutil.ignore_patterns("node_modules", "dist", ".astro", ".git", ".codegraph", "auditoria", "__pycache__", ".pytest_cache")
ARQUIVO = "exemplo-decisao-evento-quebrado-completo.yaml"


@pytest.fixture
def copia(tmp_path: Path) -> Path:
    destino = tmp_path / "repo"
    shutil.copytree(comum.ROOT, destino, ignore=IGNORAR)
    return destino


def rodar(raiz: Path, script: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(raiz / "scripts" / script)], capture_output=True, text=True, timeout=120)


def downloads(raiz: Path) -> Path:
    return raiz / "public" / "downloads"


def trocar(arquivo: Path, antigo: str, novo: str) -> None:
    texto = arquivo.read_text(encoding="utf-8")
    assert antigo in texto, antigo
    arquivo.write_text(texto.replace(antigo, novo, 1), encoding="utf-8")


def test_repositorio_passa_e_cita_o_exemplo(copia: Path):
    resultado = rodar(copia, "check_decision_examples.py")
    assert resultado.returncode == 0, resultado.stdout
    assert f"{ARQUIVO}: 243 combinações, 6 casos" in resultado.stdout


def test_arquivo_extra_lido_por_glob_e_acusado(copia: Path):
    original = downloads(copia) / ARQUIVO
    extra = downloads(copia) / "exemplo-decisao-extra.yaml"
    texto = original.read_text(encoding="utf-8")
    linhas = texto.split("\n")
    # remove a última linha da tabela (expected=true e streak=unknown): sobra combinação sem linha
    indice = max(i for i, l in enumerate(linhas) if l.strip().startswith("- when:"))
    del linhas[indice:indice + 2]
    extra.write_text("\n".join(linhas), encoding="utf-8")
    resultado = rodar(copia, "check_decision_examples.py")
    assert resultado.returncode == 1
    assert "exemplo-decisao-extra.yaml" in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_failure_candidate_com_entrada_violada(copia: Path):
    arquivo = downloads(copia) / ARQUIVO
    texto = arquivo.read_text(encoding="utf-8")
    assert "active_in_scope: false" in texto
    import re
    novo = re.sub(r"(active_in_scope: false[^\n]*\n\s*then: )\w+", r"\1failure_candidate", texto, count=1)
    assert novo != texto
    arquivo.write_text(novo, encoding="utf-8")
    resultado = rodar(copia, "check_decision_examples.py")
    assert resultado.returncode == 1
    assert "failure_candidate" in resultado.stdout
    assert "active_in_scope" in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_linha_sem_entrada_no_when_vira_erro_legivel(copia: Path):
    arquivo = downloads(copia) / ARQUIVO
    trocar(arquivo, "known_exception_applies: any, ", "")
    resultado = rodar(copia, "check_decision_examples.py")
    assert resultado.returncode == 1
    assert "ERRO" in resultado.stdout
    assert "known_exception_applies" in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_limiar_numerico_em_allowed_values_e_acusado(copia: Path):
    arquivo = downloads(copia) / ARQUIVO
    trocar(arquivo, "allowed_values: [true, false, unknown]", "allowed_values: [true, false, unknown, 4]")
    resultado = rodar(copia, "check_decision_examples.py")
    assert resultado.returncode == 1
    assert "limiar é escolha do time e mora no Evento de coleta" in resultado.stdout
    assert "Traceback" not in resultado.stderr


def test_referencia_a_evento_inexistente_e_acusada(copia: Path):
    fonte = copia / "src" / "exemplos" / "exemplo-decisao-evento-quebrado-completo.md"
    for arquivo in (fonte, downloads(copia) / ARQUIVO):
        trocar(arquivo, "EVENT-AURORA-GENERATE-LEAD", "EVENT-AURORA-INEXISTENTE")
    resultado = rodar(copia, "validate_content.py")
    assert resultado.returncode == 1
    assert "referência a documento inexistente: EVENT-AURORA-INEXISTENTE" in resultado.stdout
