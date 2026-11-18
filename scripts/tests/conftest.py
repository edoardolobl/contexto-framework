"""Deixa os testes importarem os módulos de scripts/ sem instalar pacote."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
