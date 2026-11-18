"""Testes do conversor de planilha para rascunho de Evento de coleta (I-31)."""
from pathlib import Path

import pytest
import yaml

import check_schemas
import comum
import planilha_para_evento as ppe

RAIZ = comum.ROOT
MODELO = RAIZ / "public" / "downloads" / "plano-de-mensuracao-modelo.csv"
COLUNAS_MD = RAIZ / "src" / "kit" / "skills" / "importar-plano-de-mensuracao" / "references" / "colunas.md"
EXEMPLO = RAIZ / "src" / "exemplos" / "exemplo-evento-coleta-completo.md"
DATA = "2026-11-17"

AURORA = {
    "Evento": "generate_lead", "Identificador": "EVENT-AURORA-GENERATE-LEAD",
    "Pergunta de negócio": "Quando um dia sem generate_lead deve ser tratado como falha de coleta?",
    "Responsável": "Analytics de E-commerce (Aurora)",
    "Gatilho": "Envio com sucesso do formulário de cadastro de atacado",
    "Frequência esperada": "Poucos envios por dia", "Prazo para os dados chegarem": "D+2 às 06h",
    "Data de lançamento": "03/08/2026", "Consentimento exigido": "analytics_storage concedido",
    "Indicadores que dependem do evento": "Taxa de cadastro, Receita",
    "Operação": "BR", "País": "Brasil", "Marca": "Aurora", "Ativo na operação": "sim",
    "Ativo desde": "03/08/2026", "Motivo": "Formulário publicado", "Tolerância ao silêncio": "4 dias",
    "Ferramenta de destino": "GA4", "Onde dentro da ferramenta": "Propriedade Aurora BR",
    "Fuso horário": "America/Sao_Paulo",
}


def csv_texto(linhas: list[dict], sep: str = ";", colunas=ppe.COLUNAS) -> str:
    out = [sep.join(colunas)]
    for linha in linhas:
        out.append(sep.join(linha.get(c, "") for c in colunas))
    return "\n".join(out) + "\n"


def planilha(tmp_path: Path, linhas: list[dict], **kw) -> Path:
    caminho = tmp_path / "plano.csv"
    caminho.write_text(csv_texto(linhas, **kw), encoding="utf-8-sig")
    return caminho


def converter(tmp_path: Path, linhas: list[dict], **kw):
    relatorio = comum.Relatorio()
    docs = ppe.ler_e_montar(planilha(tmp_path, linhas, **kw), DATA, RAIZ, relatorio)
    return docs, relatorio


def rascunho(tmp_path: Path, linhas: list[dict]) -> dict:
    docs, relatorio = converter(tmp_path, linhas)
    assert relatorio.erros == []
    assert len(docs) == 1
    return docs[0]


def aurora_mx() -> dict:
    return {**AURORA, "Operação": "MX", "País": "México", "Ativo na operação": "não", "Ativo desde": "",
            "Motivo": "Sem formulário", "Tolerância ao silêncio": "Não se aplica"}


# ---------- modelo e referência ----------

def test_cabecalho_do_modelo_e_igual_a_colunas_com_bom_e_ponto_e_virgula():
    bruto = MODELO.read_bytes()
    assert bruto.startswith(b"\xef\xbb\xbf")
    assert bruto.decode("utf-8-sig").splitlines()[0] == ";".join(ppe.COLUNAS)
    assert len(ppe.COLUNAS) == 20


def test_converter_o_modelo_gera_um_rascunho_valido_e_na_ordem(tmp_path: Path):
    relatorio = comum.Relatorio()
    docs = ppe.ler_e_montar(MODELO, DATA, RAIZ, relatorio)
    assert relatorio.erros == []
    assert len(docs) == 1
    assert check_schemas.erros_de_ordem(list(docs[0]), exigir_todas=False) == []
    assert ppe.erros_no_schema(docs[0], RAIZ) == []


def test_colunas_md_cita_todas_as_colunas():
    texto = COLUNAS_MD.read_text(encoding="utf-8")
    assert [c for c in ppe.COLUNAS if c not in texto] == []


def test_linha_da_aurora_concorda_com_o_evento_aprovado():
    doc = ppe.ler_e_montar(MODELO, DATA, RAIZ, comum.Relatorio())[0]
    aprovado = yaml.safe_load(EXEMPLO.read_text(encoding="utf-8").split("---")[1])
    assert doc["trigger"] == aprovado["trigger"]
    assert doc["owner"] == aprovado["owner"]
    assert doc["id"] == aprovado["id"]
    assert doc["launch_date"] == aprovado["launch_date"]
    assert doc["late_arrival_window"] == aprovado["late_arrival_window"]
    br = lambda itens: next(i for i in itens if i["operation"] == "BR")
    assert br(doc["active_scopes"]) == br(aprovado["active_scopes"])
    assert br(doc["expected_behavior"]["silence_tolerance"]) == br(aprovado["expected_behavior"]["silence_tolerance"])


# ---------- montagem ----------

def test_rascunho_tem_estado_e_campos_de_aprovacao_nulos(tmp_path: Path):
    doc = rascunho(tmp_path, [AURORA])
    assert doc["status"] == "draft" and doc["type"] == "evento-coleta"
    assert doc["schema_version"] == "1.1.0" and doc["version"] == "0.1"
    for chave in ("approver", "valid_from", "valid_to", "last_reviewed", "review_interval", "source_of_truth",
                  "supersedes_revision", "superseded_by_revision", "license", "source_url"):
        assert doc[chave] is None, chave
    assert doc["version_history"][0]["approved_by"] is None
    assert doc["title"] == "Evento generate_lead"
    assert doc["revision_id"] == "EVENT-AURORA-GENERATE-LEAD@0.1"
    assert doc["version_date"] == DATA
    assert "context" not in doc


def test_historico_cita_arquivo_e_linhas(tmp_path: Path):
    docs, _ = converter(tmp_path, [AURORA, aurora_mx()])
    mudanca = docs[0]["version_history"][0]
    assert mudanca["version"] == "0.1" and mudanca["date"] == DATA
    assert mudanca["change"] == "Rascunho gerado da planilha plano.csv, linhas 2 e 3, por scripts/planilha_para_evento.py"


def test_chaves_do_tipo_sempre_presentes(tmp_path: Path):
    doc = rascunho(tmp_path, [AURORA])
    for chave in ("trigger", "destination", "active_scopes", "parameters",
                  "retirement_date", "renamed_from", "deduplication_key", "known_exceptions", "validation_query",
                  "missing_days_policy", "grain_note", "data_incidents", "disambiguation", "related_documents"):
        assert chave in doc
    assert doc["expected_behavior"]["baseline_by_scope"] == []
    assert doc["expected_behavior"]["seasonality"] is None
    assert doc["expected_behavior"]["expected_zero_conditions"] == []
    assert doc["intent"] == {"question": AURORA["Pergunta de negócio"], "audience": [], "purpose": None, "decisions": []}
    assert doc["plain_summary"] is None
    assert doc["downstream_kpis"] == ["Taxa de cadastro", "Receita"]


def test_duas_operacoes_formam_um_documento(tmp_path: Path):
    doc = rascunho(tmp_path, [AURORA, aurora_mx()])
    assert [s["operation"] for s in doc["active_scopes"]] == ["BR", "MX"]
    assert [s["active"] for s in doc["active_scopes"]] == [True, False]
    assert len(doc["destination"]) == 2
    assert doc["destination"][0] == {"platform": "GA4", "object": "Propriedade Aurora BR",
                                     "timezone": "America/Sao_Paulo", "note": None}
    assert doc["expected_behavior"]["silence_tolerance"][1] == {"operation": "MX", "rule": "Não se aplica"}


def test_celula_vazia_em_um_evento_e_preenchida_em_outra_linha_nao_e_conflito(tmp_path: Path):
    mx = {**aurora_mx(), "Gatilho": ""}
    doc = rascunho(tmp_path, [mx, AURORA])
    assert doc["trigger"] == AURORA["Gatilho"]


def test_linhas_com_eventos_diferentes_geram_dois_documentos(tmp_path: Path):
    outro = {**AURORA, "Evento": "sign_up", "Identificador": "EVENT-AURORA-SIGN-UP"}
    docs, relatorio = converter(tmp_path, [AURORA, outro])
    assert relatorio.erros == [] and len(docs) == 2


# ---------- perguntas em aberto ----------

def aprova(evento: str = "generate_lead") -> str:
    return f"Quem aprova o documento do evento {evento}?"


def test_linha_toda_preenchida_so_gera_a_pergunta_de_quem_aprova(tmp_path: Path):
    doc = rascunho(tmp_path, [AURORA])
    assert [q["question"] for q in doc["open_questions"]] == [aprova()]
    assert doc["open_questions"][0]["status"] == "unresolved"
    assert doc["open_questions"][0]["resolution"] is None
    assert doc["open_questions"][0]["owner_to_resolve"] == AURORA["Responsável"]


@pytest.mark.parametrize("coluna", [c for c in ppe.COLUNAS if c not in ("Evento", "Motivo")])
def test_cada_celula_vazia_vira_uma_pergunta_em_aberto(tmp_path: Path, coluna: str):
    doc = rascunho(tmp_path, [{**AURORA, coluna: ""}])
    perguntas = doc["open_questions"]
    assert len(perguntas) == 2
    assert perguntas[-1]["question"] == aprova()
    assert all(q["status"] == "unresolved" and q["resolution"] is None for q in perguntas)
    assert all(q["question"] and q["impact"] for q in perguntas)


def test_pergunta_de_coluna_de_operacao_cita_a_operacao(tmp_path: Path):
    doc = rascunho(tmp_path, [{**AURORA, "Fuso horário": ""}])
    assert "BR" in doc["open_questions"][0]["question"]


def test_responsavel_vazio_deixa_owner_e_quem_resolve_nulos(tmp_path: Path):
    doc = rascunho(tmp_path, [{**AURORA, "Responsável": ""}])
    assert doc["owner"] is None
    assert all(q["owner_to_resolve"] is None for q in doc["open_questions"])


def test_motivo_vazio_com_ativo_sim_nao_gera_pergunta(tmp_path: Path):
    doc = rascunho(tmp_path, [{**AURORA, "Motivo": ""}])
    assert len(doc["open_questions"]) == 1


def test_motivo_vazio_com_ativo_nao_gera_pergunta(tmp_path: Path):
    doc = rascunho(tmp_path, [{**aurora_mx(), "Motivo": ""}])
    assert len(doc["open_questions"]) == 3  # Ativo desde vazio no MX, Motivo vazio e quem aprova


def test_celula_vazia_nunca_e_preenchida(tmp_path: Path):
    doc = rascunho(tmp_path, [{**AURORA, "Gatilho": "", "Data de lançamento": ""}])
    assert doc["trigger"] is None and doc["launch_date"] is None


def test_ativo_aceita_true_false_e_datas_iso(tmp_path: Path):
    doc = rascunho(tmp_path, [{**AURORA, "Ativo na operação": "TRUE", "Ativo desde": "2026-08-03"},
                              {**aurora_mx(), "Ativo na operação": "false"}])
    assert [s["active"] for s in doc["active_scopes"]] == [True, False]
    assert doc["active_scopes"][0]["since"] == "2026-08-03"
    assert doc["launch_date"] == "2026-08-03"


# ---------- erros ----------

def erros_de(tmp_path: Path, linhas: list[dict], **kw) -> list[str]:
    docs, relatorio = converter(tmp_path, linhas, **kw)
    return relatorio.erros


def test_evento_vazio_e_erro_com_linha(tmp_path: Path):
    erros = erros_de(tmp_path, [{**AURORA, "Evento": ""}])
    assert any("plano.csv" in e and "linha 2" in e and "Evento" in e for e in erros)


def test_data_invalida_e_erro_com_linha(tmp_path: Path):
    erros = erros_de(tmp_path, [AURORA, {**aurora_mx(), "Ativo desde": "31/02/2026"}])
    assert any("linha 3" in e and "Ativo desde" in e for e in erros)


def test_data_de_lancamento_invalida_e_erro(tmp_path: Path):
    assert any("Data de lançamento" in e for e in erros_de(tmp_path, [{**AURORA, "Data de lançamento": "ontem"}]))


def test_talvez_em_ativo_e_erro(tmp_path: Path):
    erros = erros_de(tmp_path, [{**AURORA, "Ativo na operação": "talvez"}])
    assert any("linha 2" in e and "Ativo na operação" in e for e in erros)


def test_conflito_entre_linhas_cita_as_duas(tmp_path: Path):
    erros = erros_de(tmp_path, [AURORA, {**aurora_mx(), "Gatilho": "Outro gatilho"}])
    assert any("linhas 2 e 3" in e and "Gatilho" in e for e in erros)


def test_par_evento_e_operacao_repetido_e_erro(tmp_path: Path):
    erros = erros_de(tmp_path, [AURORA, AURORA])
    assert any("linhas 2 e 3" in e and "BR" in e for e in erros)


def test_coluna_que_falta_e_erro(tmp_path: Path):
    colunas = tuple(c for c in ppe.COLUNAS if c != "Marca")
    erros = erros_de(tmp_path, [AURORA], colunas=colunas)
    assert any("Marca" in e and "plano.csv" in e for e in erros)


def test_coluna_desconhecida_gera_aviso_e_e_ignorada(tmp_path: Path):
    colunas = ppe.COLUNAS + ("Extra",)
    docs, relatorio = converter(tmp_path, [{**AURORA, "Extra": "x"}], colunas=colunas)
    assert relatorio.erros == [] and len(docs) == 1
    assert any("Extra" in a for a in relatorio.avisos)
    assert "Extra" not in yaml.safe_dump(docs[0])


def test_separador_virgula_e_cabecalho_sem_diferenca_de_caixa(tmp_path: Path):
    colunas = tuple(f"  {c.upper()} " for c in ppe.COLUNAS)
    caminho = tmp_path / "v.csv"
    caminho.write_text(",".join(colunas) + "\n" + ",".join(AURORA.get(c, "") for c in ppe.COLUNAS).replace(
        "Taxa de cadastro, Receita", '"Taxa de cadastro, Receita"') + "\n", encoding="utf-8-sig")
    relatorio = comum.Relatorio()
    docs = ppe.ler_e_montar(caminho, DATA, RAIZ, relatorio)
    assert relatorio.erros == [] and len(docs) == 1
    assert docs[0]["downstream_kpis"] == ["Taxa de cadastro", "Receita"]


def _csv_com_celula_multilinha(tmp_path: Path, linhas: list[dict], fim: str = "\n") -> Path:
    """Escreve a planilha com a célula multilinha entre aspas, como o Excel faz com Alt+Enter."""
    def celula(valor: str) -> str:
        return f'"{valor}"' if "\n" in valor else valor
    corpo = [";".join(ppe.COLUNAS)] + [";".join(celula(linha.get(c, "")) for c in ppe.COLUNAS) for linha in linhas]
    caminho = tmp_path / "plano.csv"
    caminho.write_bytes(("\n".join(corpo) + "\n").replace("\n", fim).encode("utf-8-sig"))
    return caminho


@pytest.mark.parametrize("fim", ["\n", "\r\n"])
def test_celula_com_quebra_de_linha_mantem_o_texto(tmp_path: Path, fim: str):
    gatilho = "Envio com sucesso\ndo formulário de atacado"
    relatorio = comum.Relatorio()
    caminho = _csv_com_celula_multilinha(tmp_path, [{**AURORA, "Gatilho": gatilho}], fim)
    docs = ppe.ler_e_montar(caminho, DATA, RAIZ, relatorio)
    assert relatorio.erros == [] and len(docs) == 1
    assert docs[0]["trigger"] == gatilho


def test_linha_do_erro_e_a_linha_da_planilha_mesmo_com_celula_multilinha(tmp_path: Path):
    primeira = {**AURORA, "Gatilho": "Envio com sucesso\ndo formulário"}
    segunda = {**aurora_mx(), "Ativo desde": "31/02/2026"}
    relatorio = comum.Relatorio()
    ppe.ler_e_montar(_csv_com_celula_multilinha(tmp_path, [primeira, segunda]), DATA, RAIZ, relatorio)
    assert any("linha 3" in e and "Ativo desde" in e for e in relatorio.erros)


def test_arquivo_inexistente_e_erro(tmp_path: Path):
    relatorio = comum.Relatorio()
    assert ppe.ler_e_montar(tmp_path / "nao.csv", DATA, RAIZ, relatorio) == []
    assert relatorio.erros


def test_erro_do_schema_vira_erro_do_relatorio(tmp_path: Path):
    erros = erros_de(tmp_path, [{**AURORA, "Identificador": "minusculo"}])
    assert any("id" in e for e in erros)


# ---------- escrita e CLI ----------

def test_nome_do_arquivo_normaliza_o_evento():
    assert ppe.nome_do_arquivo("Generate Lead/BR") == "rascunho-generate-lead-br.md"


def test_main_escreve_um_rascunho_valido(tmp_path: Path, capsys):
    saida = tmp_path / "saida"
    ppe.main([str(MODELO), "--saida", str(saida), "--data", DATA, "--raiz", str(RAIZ)])
    arquivos = list(saida.iterdir())
    assert [a.name for a in arquivos] == ["rascunho-generate_lead.md"]
    texto = arquivos[0].read_text(encoding="utf-8")
    assert texto.startswith("---\n")
    frontmatter = yaml.safe_load(texto.split("---\n")[1])
    assert frontmatter["status"] == "draft" and frontmatter["version_date"] == DATA
    assert frontmatter["approver"] is None and frontmatter["valid_from"] is None
    assert frontmatter["version_history"][0]["approved_by"] is None
    corpo = texto.lower()
    assert "rascunho gerado da planilha" in corpo and "nada foi aprovado" in corpo
    assert "pergunta em aberto" in corpo and "quem responde pelo evento" in corpo
    assert "—" not in texto and "–" not in texto
    assert ppe.erros_no_schema(frontmatter, RAIZ) == []


def test_main_nao_sobrescreve_sem_substituir(tmp_path: Path):
    saida = tmp_path / "saida"
    args = [str(MODELO), "--saida", str(saida), "--data", DATA]
    ppe.main(args)
    arquivo = saida / "rascunho-generate_lead.md"
    arquivo.write_text("meu texto", encoding="utf-8")
    with pytest.raises(SystemExit):
        ppe.main(args)
    assert arquivo.read_text(encoding="utf-8") == "meu texto"
    ppe.main(args + ["--substituir"])
    assert arquivo.read_text(encoding="utf-8").startswith("---\n")


def test_com_erro_nada_e_escrito(tmp_path: Path):
    bom = {**AURORA, "Evento": "sign_up", "Identificador": "EVENT-AURORA-SIGN-UP"}
    ruim = {**AURORA, "Ativo na operação": "talvez"}
    entrada = planilha(tmp_path, [bom, ruim])
    saida = tmp_path / "saida"
    with pytest.raises(SystemExit):
        ppe.main([str(entrada), "--saida", str(saida), "--data", DATA])
    assert not saida.exists() or list(saida.iterdir()) == []


def test_main_com_data_invalida_falha(tmp_path: Path):
    with pytest.raises(SystemExit):
        ppe.main([str(MODELO), "--saida", str(tmp_path / "s"), "--data", "17/11/2026"])
