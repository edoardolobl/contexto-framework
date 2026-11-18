"""Testes de unidade de check_revisions: datas de artefatos, ids e avisos de fim de semana."""
from datetime import date
from pathlib import Path

import pytest

import comum
import check_revisions as cr


def artefatos_de_exemplo(tmp_path: Path, corpo: str) -> tuple[list, comum.Relatorio]:
    arquivo = tmp_path / "artefatos.yaml"
    arquivo.write_text(corpo, encoding="utf-8")
    relatorio = comum.Relatorio()
    return cr.carregar_artefatos(arquivo, relatorio), relatorio


YAML_OK = """# cabeçalho
artefatos:
  - nome: 'consulta de referência'
    desde: 2026-09-15
    origem: 'implementa KPI-X-001@2.0'
    padroes: ['consulta-ref\\.sql']
"""


def doc(id_, version, data, texto="", approved_by=None, status="draft", extras=None):
    d = {"id": id_, "version": version, "version_date": data, "status": status,
         "revision_id": f"{id_}@{version}",
         "version_history": [{"version": version, "date": data, "change": texto, "approved_by": approved_by}],
         "texto": texto}
    d.update(extras or {})
    return d


def registro_de(docs, artefatos=()):
    return cr.montar_registro({Path(f"/x/d{i}.yaml"): d for i, d in enumerate(docs)}, list(artefatos))


def acusar(docs, artefatos=()):
    relatorio = comum.Relatorio()
    mapa = {Path(f"/x/d{i}.yaml"): d for i, d in enumerate(docs)}
    cr.checar_datas(mapa, cr.montar_registro(mapa, list(artefatos)), relatorio)
    return relatorio


def test_registro_usa_menor_data_de_cada_id_somando_arquivos():
    reg = registro_de([doc("A-1", "2.0", "2026-09-01"), doc("A-1", "1.0", "2026-08-01")])
    assert reg.ids["A-1"] == date(2026, 8, 1)
    assert reg.versoes["A-1@2.0"] == date(2026, 9, 1)


def test_id_posterior_e_acusado():
    r = acusar([doc("A-1", "1.0", "2026-08-01", "veja B-2"), doc("B-2", "1.0", "2026-09-01")])
    assert any("versão de 2026-08-01 cita B-2, que só existe a partir de 2026-09-01" in e for e in r.erros)


def test_versao_posterior_e_acusada():
    r = acusar([doc("A-1", "1.0", "2026-08-01", "veja A-1@2.0"), doc("A-1", "2.0", "2026-09-01")])
    assert any("cita A-1@2.0, que só existe a partir de 2026-09-01" in e for e in r.erros)


def test_data_igual_e_permitida():
    r = acusar([doc("A-1", "1.0", "2026-09-01", "veja B-2 e B-2@1.0"), doc("B-2", "1.0", "2026-09-01")])
    assert r.erros == []


def test_artefato_por_padrao_e_acusado(tmp_path: Path):
    arts, rel = artefatos_de_exemplo(tmp_path, YAML_OK)
    assert rel.erros == []
    r = acusar([doc("A-1", "1.0", "2026-08-01", "rode consulta-ref.sql")], arts)
    assert any("cita consulta de referência, que só existe a partir de 2026-09-15" in e for e in r.erros)


def test_comentarios_nao_contam_pois_so_o_yaml_interpretado_e_lido():
    r = acusar([doc("A-1", "1.0", "2026-08-01"), doc("B-2", "1.0", "2026-09-01")])
    assert r.erros == []


def test_archival_note_e_conferida_pela_propria_data():
    nota = {"date": "2026-10-05", "text": "veja B-2"}
    r = acusar([doc("A-1", "1.0", "2026-08-01", extras={"archival_note": nota}), doc("B-2", "1.0", "2026-09-01")])
    assert r.erros == []
    nota_antiga = {"date": "2026-08-15", "text": "veja B-2"}
    r = acusar([doc("A-1", "1.0", "2026-08-01", extras={"archival_note": nota_antiga}), doc("B-2", "1.0", "2026-09-01")])
    assert any("B-2" in e and "2026-09-01" in e for e in r.erros)


def test_archival_note_nao_vale_como_texto_do_documento():
    nota = {"date": "2026-10-05", "text": "veja B-2"}
    r = acusar([doc("A-1", "1.0", "2026-08-01", extras={"archival_note": nota}), doc("B-2", "1.0", "2026-09-01")])
    assert r.erros == []


def test_archival_note_com_data_anterior_a_version_date_e_acusada():
    nota = {"date": "2026-07-01", "text": "ok"}
    r = acusar([doc("A-1", "1.0", "2026-08-01", extras={"archival_note": nota})])
    assert any("archival_note" in e and "anterior" in e for e in r.erros)


def test_archival_note_malformada_vira_erro():
    for nota in ("texto solto", {"text": "sem data"}, {"date": "2026-10-05"}, {"date": "ontem", "text": "x"}, {"date": "2026-10-05", "text": 3}):
        r = acusar([doc("A-1", "1.0", "2026-08-01", extras={"archival_note": nota})])
        assert any("archival_note" in e for e in r.erros), nota


def test_artefatos_com_regex_invalida_vira_erro(tmp_path: Path):
    _, rel = artefatos_de_exemplo(tmp_path, YAML_OK.replace("consulta-ref\\.sql", "(aberto"))
    assert any("padroes" in e and "inválida" in e for e in rel.erros)


def test_artefatos_sem_desde_vira_erro(tmp_path: Path):
    _, rel = artefatos_de_exemplo(tmp_path, YAML_OK.replace("    desde: 2026-09-15\n", ""))
    assert any("desde" in e for e in rel.erros)


def test_artefatos_vazio_ou_quebrado_vira_erro(tmp_path: Path):
    for corpo in ("", "artefatos: 3\n", "artefatos: [1]\n", "a: [\n"):
        arts, rel = artefatos_de_exemplo(tmp_path, corpo)
        assert rel.erros and arts == []


def test_aviso_para_aprovacao_em_fim_de_semana():
    rel = comum.Relatorio()
    d = doc("A-1", "1.0", "2026-08-15", approved_by="Gerência", status="approved")  # sábado
    cr.avisar_fim_de_semana(Path("/x/a.yaml"), d, rel)
    assert len(rel.avisos) == 2  # entrada do histórico e version_date
    assert all("sábado" in a for a in rel.avisos)
    assert rel.erros == []


def test_sem_aviso_em_dia_util_ou_sem_aprovacao():
    rel = comum.Relatorio()
    cr.avisar_fim_de_semana(Path("/x/a.yaml"), doc("A-1", "1.0", "2026-08-14", approved_by="G", status="approved"), rel)
    cr.avisar_fim_de_semana(Path("/x/b.yaml"), doc("A-1", "1.0", "2026-08-15"), rel)
    assert rel.avisos == []


def test_aviso_de_domingo():
    rel = comum.Relatorio()
    cr.avisar_fim_de_semana(Path("/x/a.yaml"), doc("A-1", "1.0", "2026-08-16", approved_by="G"), rel)
    assert any("domingo" in a for a in rel.avisos)


# ---------- estados ja aprovados e substituicao (F3) ----------

def revisoes_de(docs):
    mapa = {Path(f"/x/d{i}.yaml"): d for i, d in enumerate(docs)}
    relatorio = comum.Relatorio()
    revisions = cr.checar_documentos(mapa, relatorio)
    cr.checar_substituicao(revisions, relatorio)
    return mapa, revisions, relatorio


def par(**sucessor_extras):
    antigo = doc("A-1", "1.0", "2026-08-03", approved_by="G", status="superseded", extras={
        "valid_from": "2026-08-03", "valid_to": "2026-09-14", "recorded_at": "2026-09-14",
        "superseded_by_revision": "A-1@2.0"})
    novo = doc("A-1", "2.0", "2026-09-14", approved_by="G", status="approved", extras={
        "valid_from": "2026-09-14", "valid_to": None, "supersedes_revision": "A-1@1.0", **sucessor_extras})
    novo["version_history"].append({"version": "1.0", "date": "2026-08-03", "change": "x", "approved_by": "G"})
    return antigo, novo


def test_par_superseded_e_sucessor_coerentes_nao_da_erro():
    assert revisoes_de(par())[2].erros == []


def test_superseded_conta_como_ja_aprovado_nas_selecoes():
    antigo, novo = par()
    grouped = cr.agrupar_por_id({Path("/x/a.yaml"): antigo, Path("/x/b.yaml"): novo})
    rel = comum.Relatorio()
    assert cr.select(grouped, "A-1", "2026-08-20", rel) == ["A-1@1.0"]
    assert cr.select(grouped, "A-1", "2026-09-20", rel) == ["A-1@2.0"]
    assert rel.erros == []
    rel = comum.Relatorio()
    cr.checar_sobreposicao(grouped, rel)
    assert rel.erros == []


def test_sobreposicao_entre_superseded_e_sucessor_e_acusada():
    antigo, novo = par()
    antigo["valid_to"] = "2026-09-20"
    rel = comum.Relatorio()
    cr.checar_sobreposicao(cr.agrupar_por_id({Path("/x/a.yaml"): antigo, Path("/x/b.yaml"): novo}), rel)
    assert any("sobrepõe" in e for e in rel.erros)


def test_superseded_com_valid_to_antes_de_valid_from_e_acusado():
    antigo, novo = par()
    antigo["valid_to"] = "2026-08-01"
    assert any("valid_to deve ser posterior" in e for e in revisoes_de([antigo, novo])[2].erros)


def test_superseded_sem_vigencia_e_acusado():
    antigo, novo = par()
    antigo["valid_from"] = None
    assert any("precisa de valid_from" in e for e in revisoes_de([antigo, novo])[2].erros)


def test_superseded_sem_superseded_by_revision():
    antigo, novo = par()
    del antigo["superseded_by_revision"]
    assert any("superseded exige superseded_by_revision" in e for e in revisoes_de([antigo, novo])[2].erros)


def test_superseded_by_revision_de_outro_id():
    antigo, novo = par()
    antigo["superseded_by_revision"] = "B-9@2.0"
    assert any("superseded exige superseded_by_revision com o mesmo id" in e for e in revisoes_de([antigo, novo])[2].erros)


def test_superseded_by_revision_ausente_do_registro():
    antigo, _ = par()
    assert any("A-1@2.0" in e and "registro" in e for e in revisoes_de([antigo])[2].erros)


def test_sucessor_precisa_ser_reciproco():
    antigo, novo = par()
    novo["supersedes_revision"] = None
    novo["version_history"].pop()
    assert any("reciproc" in e or "recíproc" in e for e in revisoes_de([antigo, novo])[2].erros)


def test_valid_to_da_substituida_igual_a_valid_from_do_sucessor():
    antigo, novo = par()
    antigo["valid_to"] = "2026-09-10"
    assert any("valid_to da revisão substituída" in e for e in revisoes_de([antigo, novo])[2].erros)


def test_recorded_at_invalido_e_anterior_a_version_date():
    antigo, novo = par()
    antigo["recorded_at"] = "ontem"
    assert any("recorded_at: data inválida" in e for e in revisoes_de([antigo, novo])[2].erros)
    antigo, novo = par()
    antigo["recorded_at"] = "2026-08-01"
    assert any("recorded_at" in e and "anterior a version_date" in e for e in revisoes_de([antigo, novo])[2].erros)


def test_rascunho_com_vigencia_continua_acusado():
    d = doc("A-1", "1.0", "2026-08-03", extras={"valid_from": "2026-08-03"})
    assert any("rascunho pendente" in e for e in revisoes_de([d])[2].erros)


def test_checar_datas_ignora_superseded_by_revision_e_recorded_at():
    antigo, novo = par()
    antigo["version_date"] = "2026-08-03"
    antigo["version_history"][0]["date"] = "2026-08-03"
    rel = acusar([antigo, novo])
    assert rel.erros == []


# ---------- vigência retroativa declarada (KPI-AURORA-002, F8, contrato 0.13) ----------

DECLARACAO = {"reason": "Documenta uma regra em uso desde 01/10/2026", "confirmed_by": "Gerência de Analytics (Aurora)"}


def _primeira_revisao(valid_from, retroatividade=None):
    extras = {"valid_from": valid_from, "valid_to": None, "supersedes_revision": None}
    if retroatividade is not None:
        extras["retroactive_validity"] = retroatividade
    return doc("A-2", "1.0", "2026-11-17", approved_by="G", status="approved", extras=extras)


def _erros(docs):
    return revisoes_de(docs)[2].erros


def test_primeira_revisao_com_retroatividade_declarada_pode_valer_desde_antes_da_emissao():
    assert _erros([_primeira_revisao("2026-10-01", DECLARACAO)]) == []


def test_primeira_revisao_sem_declaracao_nao_pode_valer_desde_antes_da_emissao():
    assert any("retroactive_validity" in e for e in _erros([_primeira_revisao("2026-10-01")]))


@pytest.mark.parametrize("declaracao", [
    {"reason": "", "confirmed_by": "G"},
    {"reason": "x"},
    {"confirmed_by": "G"},
    "sim",
])
def test_declaracao_incompleta_e_acusada(declaracao):
    assert any("retroactive_validity" in e for e in _erros([_primeira_revisao("2026-10-01", declaracao)]))


def test_declaracao_sem_vigencia_retroativa_e_acusada():
    assert any("retroactive_validity" in e for e in _erros([_primeira_revisao("2026-11-17", DECLARACAO)]))


def test_revisao_que_substitui_outra_nao_pode_valer_desde_antes_da_emissao_mesmo_declarada():
    antigo, novo = par()
    novo["valid_from"] = "2026-09-01"
    novo["retroactive_validity"] = DECLARACAO
    assert any("valid_from anterior à emissão" in e for e in _erros([antigo, novo]))
