"""Testes de enderecos: funções puras que montam caminhos e URLs publicados (ADR 0011)."""
import pytest

import enderecos as e


def test_constantes_canonicas():
    assert e.URL_DO_SITE == "https://edoardolobl.github.io/contexto-framework"
    assert e.LICENCA_DO_CONTEUDO == "CC-BY-4.0"


def test_caminho_e_url_do_documento():
    assert e.caminho_do_documento("KPI-AURORA-001", "2.0") == "documentos/KPI-AURORA-001@2.0.md"
    assert e.caminho_do_documento("KPI-AURORA-001", "2.0", "json") == "documentos/KPI-AURORA-001@2.0.json"
    assert e.url_do_documento("KPI-AURORA-001", "2.0.1") == f"{e.URL_DO_SITE}/documentos/KPI-AURORA-001@2.0.1.md"


def test_caminho_e_url_do_schema():
    assert e.caminho_do_schema("1.1.0", "kpi") == "schemas/1.1.0/kpi.schema.json"
    assert e.url_do_schema("1.1.0", "kpi") == f"{e.URL_DO_SITE}/schemas/1.1.0/kpi.schema.json"


@pytest.mark.parametrize("id_", ["", "kpi-a-1", "KPI", "KPI-", "-KPI-1", "KPI A-1", "KPI-A/1", "KPI-A-1\n", "1KPI-A"])
def test_id_fora_do_padrao_gera_erro_claro(id_):
    with pytest.raises(ValueError, match="id"):
        e.caminho_do_documento(id_, "1.0")


@pytest.mark.parametrize("versao", ["", "1", "1.", "a.b", "1.0.0.0", "1.0 ", "1.0\n", "v1.0"])
def test_versao_fora_do_padrao_gera_erro_claro(versao):
    with pytest.raises(ValueError, match="versão"):
        e.caminho_do_documento("KPI-A-001", versao)
    with pytest.raises(ValueError, match="versão"):
        e.caminho_do_schema(versao, "kpi")


def test_tipos_invalidos_viram_value_error():
    with pytest.raises(ValueError):
        e.caminho_do_documento(None, "1.0")  # type: ignore[arg-type]
