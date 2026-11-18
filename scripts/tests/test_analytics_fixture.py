"""Testes do validador da amostra SQLite do Laboratório Aurora (ADR 0022)."""
from pathlib import Path
import re
import subprocess
import sys

import pytest

import check_analytics_fixture as f

SCRIPTS = Path(__file__).resolve().parents[1]
CHECAGENS_ANTES_DA_F8 = 23


class TestTabelaDaAmostra:
    @pytest.mark.parametrize(
        ("nome_fisico", "esperado"),
        [
            ("aurora-analytics.web.sessoes_web", "sessoes_web"),
            ("aurora-analytics.vendas.pedidos", "pedidos"),
            ("pedidos", "pedidos"),
        ],
    )
    def test_a_tabela_e_o_ultimo_trecho_do_nome_completo(self, nome_fisico, esperado):
        assert f.tabela_da_amostra(nome_fisico) == esperado

    @pytest.mark.parametrize("invalido", [None, "", "   ", "aurora-analytics.web.", 42])
    def test_nome_fisico_ausente_ou_incompleto_e_recusado(self, invalido):
        with pytest.raises(ValueError):
            f.tabela_da_amostra(invalido)


class TestColunasDocumentadas:
    def test_indexa_as_colunas_pelo_physical_name_em_camel_case(self):
        doc = {"columns": [{"physicalName": "order_id"}, {"physicalName": "status_code"}]}
        assert set(f.colunas_documentadas(doc)) == {"order_id", "status_code"}

    def test_chave_antiga_em_snake_case_nao_vale_mais(self):
        with pytest.raises(ValueError):
            f.colunas_documentadas({"columns": [{"physical_name": "order_id"}]})


class TestValidadorCompleto:
    def test_passa_e_nao_perde_nenhuma_checagem(self):
        fonte = (SCRIPTS / "check_analytics_fixture.py").read_text(encoding="utf-8")
        checagens = len(re.findall(r"(?<!def )\bfail\(", fonte))
        assert checagens >= CHECAGENS_ANTES_DA_F8
        saida = subprocess.run([sys.executable, str(SCRIPTS / "check_analytics_fixture.py")],
                               capture_output=True, text=True, check=False)
        assert saida.returncode == 0, saida.stdout + saida.stderr

    def test_a_amostra_usa_os_nomes_de_producao(self):
        fixture = (SCRIPTS.parent / "public" / "downloads" / "aurora-fixture.sql").read_text(encoding="utf-8")
        assert "CREATE TABLE sessoes_web" in fixture
        assert "CREATE TABLE pedidos" in fixture
        assert "demo_" not in fixture
