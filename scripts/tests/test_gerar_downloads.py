"""Testes do gerador de downloads, com fontes de mentira em tmp_path e a raiz como parâmetro."""
from datetime import date, datetime
from pathlib import Path
import subprocess
import sys

import pytest

import gerar_downloads as g

MODELO = """---
id: KPI-MODELO
type: kpi
title: Indicador
version_history:
  - version: "0.1"
    date: 2026-10-01
    change: "Primeira | versão"
    approved_by: null
  - version: "0.0"
    date: null
    change: "x"
    approved_by: "Gerência"
---
# Título do modelo

<!-- contexto:identificacao -->

Corpo do meio.

<!-- contexto:exemplo intent.question -->
<!-- contexto:exemplo plain_summary -->
<!-- contexto:exemplo owner -->
<!-- contexto:exemplo version_date -->

<!-- contexto:historico -->

Fim.
"""
EXEMPLO = (
    "---\n# Exemplo do Contexto, organização inventada\nid: KPI-X\ntype: kpi\nowner: Área  de\n  Vendas\n"
    "version_date: 2026-09-15\nintent:\n  question: Quanto vendemos?\n  audience: [Gerência, Operação]\n"
    "plain_summary: Resumo simples.\n---\n## Corpo que não vai\n"
)
CAMPOS = """cabecalho:
  - chave: id
    rotulo: Identificador
    obrigatorio: true
    descricao: "Código único | estável"
  - chave: intent.question
    rotulo: Pergunta
    obrigatorio: false
    descricao: Pergunta que o documento responde.
"""


def montar(raiz: Path, modelo: str = MODELO, exemplo: str = EXEMPLO) -> Path:
    (raiz / "src" / "modelos").mkdir(parents=True)
    (raiz / "src" / "exemplos" / "historico").mkdir(parents=True)
    (raiz / "src" / "data").mkdir(parents=True)
    (raiz / "public" / "downloads" / "historico" / "0.x").mkdir(parents=True)
    (raiz / "src" / "modelos" / "kpi.md").write_text(modelo, encoding="utf-8")
    (raiz / "src" / "exemplos" / "exemplo-kpi-completo.md").write_text(exemplo, encoding="utf-8")
    (raiz / "src" / "exemplos" / "historico" / "exemplo-kpi-v1.0.md").write_text(exemplo, encoding="utf-8")
    (raiz / "src" / "data" / "campos.yaml").write_text(CAMPOS, encoding="utf-8")
    return raiz


def instantaneo(pasta: Path) -> dict[str, bytes]:
    return {p.relative_to(pasta).as_posix(): p.read_bytes() for p in sorted(pasta.rglob("*")) if p.is_file()}


def rodar(raiz: Path, check: bool = False):
    return g.executar(raiz, check=check)


def test_gera_yaml_do_modelo_igual_ao_frontmatter(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    saida = (tmp_path / "public/downloads/template-kpi.yaml").read_text(encoding="utf-8")
    texto = MODELO.split("---\n", 2)[1]
    assert saida == texto
    assert saida.endswith("\n") and not saida.endswith("\n\n")


def test_gera_markdown_do_modelo_com_secoes(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    md = (tmp_path / "public/downloads/template-kpi.md").read_text(encoding="utf-8")
    assert md.startswith("---\nid: KPI-MODELO\n")
    assert "\n---\n# Título do modelo\n" in md
    assert "contexto:" not in md
    assert "## Identificação\n" in md and "## Histórico de versões\n" in md
    assert md.index("## Identificação") < md.index("Corpo do meio.") < md.index("## Histórico de versões") < md.index("Fim.")
    assert md.endswith("Fim.\n")


def test_tabela_de_identificacao(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    md = (tmp_path / "public/downloads/template-kpi.md").read_text(encoding="utf-8")
    assert "| Campo | Chave no topo do arquivo | Obrigatório | O que escrever |" in md
    assert "| Identificador | `id` | Sim | Código único \\| estável |" in md
    assert "| Pergunta | `intent.question` |  | Pergunta que o documento responde. |" in md


def test_tabela_de_historico(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    md = (tmp_path / "public/downloads/template-kpi.md").read_text(encoding="utf-8")
    assert "| Versão | Data | O que mudou e por quê | Aprovado por (cargo ou área) |" in md
    assert "| 0.1 | 01/10/2026 | Primeira \\| versão |  |" in md
    assert "| 0.0 |  | x | Gerência |" in md


def test_exemplos_geram_so_o_frontmatter_mantendo_o_caminho(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    esperado = EXEMPLO.split("---\n", 2)[1]
    assert (tmp_path / "public/downloads/exemplo-kpi-completo.yaml").read_text(encoding="utf-8") == esperado
    assert (tmp_path / "public/downloads/historico/exemplo-kpi-v1.0.yaml").read_text(encoding="utf-8") == esperado


def test_saida_sem_texto_proibido_e_deterministica(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    primeira = instantaneo(tmp_path / "public")
    rodar(tmp_path)
    assert instantaneo(tmp_path / "public") == primeira
    gerado = (tmp_path / "public/downloads/template-kpi.md").read_text(encoding="utf-8")
    secoes = gerado[gerado.index("## Identificação"):]
    for proibido in ("—", "–", "template", "fictício", "demonstrativo", "\r"):
        assert proibido not in secoes.replace("Corpo do meio.", "")


def test_check_em_sincronia_nao_escreve_e_imprime_ok(tmp_path: Path, capsys):
    montar(tmp_path)
    rodar(tmp_path)
    antes = instantaneo(tmp_path / "public")
    mtimes = {p: p.stat().st_mtime_ns for p in (tmp_path / "public").rglob("*") if p.is_file()}
    relatorio, mensagem = rodar(tmp_path, check=True)
    assert relatorio.erros == []
    assert mensagem == "OK: 4 arquivos gerados em sincronia com 3 fontes"
    assert instantaneo(tmp_path / "public") == antes
    assert {p: p.stat().st_mtime_ns for p in (tmp_path / "public").rglob("*") if p.is_file()} == mtimes


def test_check_acusa_desatualizado_ausente_e_nao_escreve(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    (tmp_path / "public/downloads/template-kpi.yaml").write_text("velho\n", encoding="utf-8")
    (tmp_path / "public/downloads/exemplo-kpi-completo.yaml").unlink()
    antes = instantaneo(tmp_path / "public")
    relatorio, _ = rodar(tmp_path, check=True)
    assert any("template-kpi.yaml" in e and "desatualizado" in e for e in relatorio.erros)
    assert any("exemplo-kpi-completo.yaml" in e and "ausente" in e for e in relatorio.erros)
    assert instantaneo(tmp_path / "public") == antes


def test_check_acusa_orfaos_e_ignora_arquivos_protegidos(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    dl = tmp_path / "public/downloads"
    for nome in ("template-velho.md", "template-velho.yaml", "exemplo-velho-completo.yaml", "historico/exemplo-velho-v1.0.yaml"):
        (dl / nome).write_text("x\n", encoding="utf-8")
    for nome in ("historico/0.x/template-kpi.yaml", "aurora-fixture.sql", "roteiro-revisao-documental.md"):
        (dl / nome).write_text("x\n", encoding="utf-8")
    relatorio, _ = rodar(tmp_path, check=True)
    orfaos = [e for e in relatorio.erros if "órfão" in e]
    assert len(orfaos) == 4
    assert not any("0.x" in e or "aurora" in e or "roteiro" in e for e in relatorio.erros)


def test_sem_flag_remove_orfaos_e_preserva_protegidos(tmp_path: Path):
    montar(tmp_path)
    dl = tmp_path / "public/downloads"
    (dl / "template-velho.md").write_text("x\n", encoding="utf-8")
    (dl / "historico/exemplo-velho-v1.0.yaml").write_text("x\n", encoding="utf-8")
    (dl / "historico/0.x/template-kpi.yaml").write_text("x\n", encoding="utf-8")
    (dl / "aurora-fixture.sql").write_text("x\n", encoding="utf-8")
    (dl / "roteiro-revisao-documental.md").write_text("x\n", encoding="utf-8")
    relatorio, _ = rodar(tmp_path)
    assert relatorio.erros == []
    assert not (dl / "template-velho.md").exists() and not (dl / "historico/exemplo-velho-v1.0.yaml").exists()
    for nome in ("historico/0.x/template-kpi.yaml", "aurora-fixture.sql", "roteiro-revisao-documental.md"):
        assert (dl / nome).exists()
    assert (dl / "template-kpi.md").exists()


@pytest.mark.parametrize(
    ("modelo", "trecho"),
    [
        (MODELO.replace("<!-- contexto:identificacao -->", ""), "contexto:identificacao"),
        (MODELO.replace("<!-- contexto:historico -->", ""), "contexto:historico"),
        (MODELO.replace("Fim.", "<!-- contexto:historico -->"), "repetido"),
        (MODELO.replace("Fim.", "<!-- contexto:identificacao -->"), "repetido"),
        ("sem frontmatter\n", "frontmatter ausente"),
    ],
)
def test_modelo_malformado_vira_erro(tmp_path: Path, modelo: str, trecho: str):
    montar(tmp_path, modelo=modelo)
    relatorio, _ = rodar(tmp_path)
    assert any("kpi.md" in e and trecho in e for e in relatorio.erros), relatorio.erros


def test_exemplo_sem_frontmatter_vira_erro_e_nada_e_escrito(tmp_path: Path):
    montar(tmp_path, exemplo="so texto\n")
    relatorio, _ = rodar(tmp_path)
    assert any("exemplo-kpi-completo.md" in e and "frontmatter ausente" in e for e in relatorio.erros)
    assert not (tmp_path / "public/downloads/template-kpi.yaml").exists()


def test_cli_com_entrada_quebrada_sai_1_sem_traceback(tmp_path: Path):
    montar(tmp_path, modelo=MODELO.replace("<!-- contexto:historico -->", ""))
    resultado = subprocess.run([sys.executable, str(Path(g.__file__)), "--raiz", str(tmp_path), "--check"],
                               capture_output=True, text=True, timeout=60)
    assert resultado.returncode == 1
    assert "ERRO:" in resultado.stdout and "Traceback" not in resultado.stderr + resultado.stdout


def test_secao_de_historico_aceita_data_em_texto_e_lista_vazia():
    assert "| 1.0 | 02/03/2026 | m | a |" in g.secao_historico([{"version": "1.0", "date": "2026-03-02", "change": "m", "approved_by": "a"}])
    assert g.secao_historico([]).count("\n") == 3 or "## Histórico de versões" in g.secao_historico([])


# ---------------------------------------------------------------- Exemplo Aurora nos moldes (AUR-13, MOD-03)
def marcador(chave: str) -> str:
    return f"<!-- contexto:exemplo {chave} -->"


MARCADORES_BASE = "\n".join(marcador(c) for c in ("intent.question", "plain_summary", "owner", "version_date"))


def modelo_com(marcadores: str) -> str:
    return MODELO.replace(MARCADORES_BASE, marcadores)


def exemplo_com(extra: str) -> str:
    return EXEMPLO.replace("plain_summary: Resumo simples.\n", "plain_summary: Resumo simples.\n" + extra)


class TestValorDoExemplo:
    DADOS = {
        "texto": "  um   texto\n em  linhas ",
        "data": date(2026, 9, 15),
        "datahora": datetime(2026, 9, 15, 10, 30),
        "ligado": True,
        "desligado": False,
        "numero": 25,
        "lista": ["a", " b  c", 3, True],
        "aninhado": {"filho": {"neto": "x"}},
        "lista_de_mapas": [{"baseline": "10%"}, {"baseline": "20%"}],
        "vazio": "",
        "branco": "   ",
        "nulo": None,
        "lista_vazia": [],
    }

    @pytest.mark.parametrize(
        ("chave", "esperado"),
        [
            ("texto", "um texto em linhas"),
            ("data", "2026-09-15"),
            ("datahora", "2026-09-15"),
            ("ligado", "true"),
            ("desligado", "false"),
            ("numero", "25"),
            ("lista", "a; b c; 3; true"),
            ("aninhado.filho.neto", "x"),
            ("lista_de_mapas.1.baseline", "20%"),
            ("lista.0", "a"),
        ],
    )
    def test_formata_cada_tipo_de_valor(self, chave: str, esperado: str):
        assert g.valor_do_exemplo(self.DADOS, chave) == esperado

    @pytest.mark.parametrize(
        ("chave", "trecho"),
        [
            ("nao_existe", "ausente"),
            ("aninhado.outro", "ausente"),
            ("lista.9", "ausente"),
            ("texto.filho", "ausente"),
            ("nulo", "vazio"),
            ("vazio", "vazio"),
            ("branco", "vazio"),
            ("lista_vazia", "vazio"),
            ("aninhado", "aponte uma chave mais funda"),
            ("aninhado.filho", "aponte uma chave mais funda"),
            ("lista_de_mapas", "aponte uma chave mais funda"),
            ("lista_de_mapas.0", "aponte uma chave mais funda"),
        ],
    )
    def test_erros_dizem_o_motivo(self, chave: str, trecho: str):
        with pytest.raises(g.ErroDeExemplo) as erro:
            g.valor_do_exemplo(self.DADOS, chave)
        assert trecho in str(erro.value) and chave in str(erro.value)


def test_marcadores_de_exemplo_lista_chaves_na_ordem():
    corpo = f"a\n{marcador('x.y')}\ntexto\n{marcador('z.0.w')}\n"
    assert g.chaves_de_exemplo(corpo) == ["x.y", "z.0.w"]


def test_substitui_marcadores_pela_linha_exemplo_aurora(tmp_path: Path):
    montar(tmp_path, exemplo=exemplo_com("tags: [a, b]\n"))
    relatorio, _ = rodar(tmp_path)
    assert relatorio.erros == []
    md = (tmp_path / "public/downloads/template-kpi.md").read_text(encoding="utf-8")
    assert "Exemplo Aurora: `intent.question`: Quanto vendemos?\n" in md
    assert "Exemplo Aurora: `plain_summary`: Resumo simples.\n" in md
    assert "Exemplo Aurora: `owner`: Área de Vendas\n" in md
    assert "Exemplo Aurora: `version_date`: 2026-09-15\n" in md
    assert "contexto:" not in md


def test_marcador_com_lista_usa_ponto_e_virgula(tmp_path: Path):
    modelo = modelo_com(MARCADORES_BASE.replace(marcador("owner"), marcador("intent.audience")))
    montar(tmp_path, modelo=modelo)
    rodar(tmp_path)
    md = (tmp_path / "public/downloads/template-kpi.md").read_text(encoding="utf-8")
    assert "Exemplo Aurora: `intent.audience`: Gerência; Operação\n" in md


def test_yaml_do_modelo_continua_identico_ao_frontmatter_com_marcadores(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    assert (tmp_path / "public/downloads/template-kpi.yaml").read_text(encoding="utf-8") == MODELO.split("---\n", 2)[1]


@pytest.mark.parametrize(
    ("exemplo", "trecho"),
    [
        (EXEMPLO.replace("owner: Área  de\n  Vendas\n", ""), "owner"),
        (EXEMPLO.replace("owner: Área  de\n  Vendas\n", "owner: null\n"), "vazio"),
        (EXEMPLO.replace("owner: Área  de\n  Vendas\n", "owner: []\n"), "vazio"),
        (EXEMPLO.replace("owner: Área  de\n  Vendas\n", "owner:\n  area: Vendas\n"), "aponte uma chave mais funda"),
        (EXEMPLO.replace("owner: Área  de\n  Vendas\n", "owner:\n  - area: Vendas\n"), "aponte uma chave mais funda"),
    ],
)
def test_erro_de_valor_do_exemplo_cita_modelo_e_exemplo(tmp_path: Path, exemplo: str, trecho: str):
    montar(tmp_path, exemplo=exemplo)
    relatorio, _ = rodar(tmp_path)
    assert any("kpi.md" in e and "owner" in e and trecho in e for e in relatorio.erros), relatorio.erros
    assert not (tmp_path / "public/downloads/template-kpi.md").exists()


def test_marcador_sem_exemplo_completo_do_mesmo_slug_vira_erro(tmp_path: Path):
    montar(tmp_path)
    (tmp_path / "src/exemplos/exemplo-kpi-completo.md").unlink()
    relatorio, _ = rodar(tmp_path)
    assert any("kpi.md" in e and "exemplo-kpi-completo.md" in e for e in relatorio.erros), relatorio.erros


def test_modelo_sem_marcador_de_intent_question_vira_erro(tmp_path: Path):
    montar(tmp_path, modelo=modelo_com(MARCADORES_BASE.replace(marcador("intent.question"), marcador("title"))))
    relatorio, _ = rodar(tmp_path)
    assert any("kpi.md" in e and "intent.question" in e for e in relatorio.erros), relatorio.erros


def test_modelo_com_menos_de_quatro_marcadores_vira_erro(tmp_path: Path):
    tres = "\n".join(marcador(c) for c in ("intent.question", "plain_summary", "owner"))
    montar(tmp_path, modelo=modelo_com(tres))
    relatorio, _ = rodar(tmp_path)
    assert any("kpi.md" in e and "pelo menos 4" in e for e in relatorio.erros), relatorio.erros


def test_marcador_mal_formado_vira_erro(tmp_path: Path):
    montar(tmp_path, modelo=modelo_com(MARCADORES_BASE + "\ntexto <!-- contexto:exemplo owner --> no meio da linha"))
    relatorio, _ = rodar(tmp_path)
    assert any("kpi.md" in e and "linha própria" in e for e in relatorio.erros), relatorio.erros


def test_saida_com_exemplos_e_deterministica_e_check_passa(tmp_path: Path):
    montar(tmp_path)
    rodar(tmp_path)
    primeira = instantaneo(tmp_path / "public")
    rodar(tmp_path)
    assert instantaneo(tmp_path / "public") == primeira
    relatorio, _ = rodar(tmp_path, check=True)
    assert relatorio.erros == []
