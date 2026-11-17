"""Integração: cada validador roda no repositório real e termina com OK."""
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "script",
    ["validate_content.py", "check_higiene.py", "check_decision_examples.py", "check_analytics_fixture.py", "check_revisions.py", "check_contraste.py"],
)
def test_validador_passa_no_repositorio(script: str):
    resultado = subprocess.run([sys.executable, str(SCRIPTS / script)], capture_output=True, text=True, timeout=120)
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
    assert any(linha.startswith("OK:") for linha in resultado.stdout.splitlines()), resultado.stdout
    assert "Traceback" not in resultado.stderr
