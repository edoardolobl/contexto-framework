"""Testes da leitura de src/data/vocabulario.yaml e src/data/modelos.yaml."""
from pathlib import Path
import re

import pytest

import comum

# As 15 regras que estavam escritas em scripts/validate_content.py no commit d08c810.
# Se o YAML mudar, este teste lembra de atualizar a tabela do contrato junto.
REGRAS_ORIGINAIS = [
    (r"\bcasos? de fronteira\b|\bedge cases?\b|\bcasos? limites?\b", "caso-limite", re.I, ()),
    (r"\bvalidade\b", "vigência", re.I, ()),
    (r"\bID da revisão\b|\brevis(?:ão|ões) (?:`?\d|histórica|anterior|vigente|específica)", "versão (revisão é só o ato de revisar)", re.I, ()),
    (r"\bdonos?\b", "responsável ou quem aprova", re.I, ()),
    (r"\baprovador(?:a|es)?\b", "quem aprova", re.I, ()),
    (r"\bpropriet[aá]ri[oa]s?\b", "responsável ou quem aprova", re.I, ()),
    (r"\bpend[eê]ncias?\b", "pergunta em aberto", re.I, ()),
    (r"\bpendentes?\b(?! de aprovação)", "em aberto (o estado do documento é 'pendente de aprovação')", re.I, ()),
    (r"\bpain[eé]is\b|\bpainel\b", "dashboard", re.I, ()),
    (r"\brespostas? de refer[eê]ncia\b", "gabarito ou resposta esperada", re.I, ()),
    (r"\bjoins?\b", "junção (JOIN só no SQL)", 0, ()),
    (r"\belicita\w*", "descobrir ou perguntar", re.I, ("referencias/index.mdx",)),
    (r"\bbriefing\b", "brief", re.I, ()),
    (r"\bm[eé]tricas?\b", "indicador", re.I, ("referencias/index.mdx",)),
    (r"\bconjuntos? de dados\b", "dataset", re.I, ()),
]

REGRA_OK = "  - termo: dashboard\n    padrao: '\\bpainel\\b'\n    sugestao: dashboard\n    ignorar_maiusculas: true\n    permitido_em: []\n"


def _vocab(tmp_path: Path, corpo: str) -> tuple[list, list[str]]:
    arquivo = tmp_path / "vocabulario.yaml"
    arquivo.write_text("regras:\n" + corpo, encoding="utf-8")
    relatorio = comum.Relatorio()
    return comum.carregar_vocabulario(arquivo, relatorio), relatorio.erros


def test_vocabulario_real_reproduz_as_regras_originais():
    relatorio = comum.Relatorio()
    regras = comum.carregar_vocabulario(comum.DADOS / "vocabulario.yaml", relatorio)
    assert relatorio.erros == []
    assert [(r.padrao, r.sugestao, r.flags, r.permitido_em) for r in regras] == REGRAS_ORIGINAIS


def test_regra_valida_vira_regra(tmp_path: Path):
    regras, erros = _vocab(tmp_path, REGRA_OK)
    assert erros == [] and regras[0].padrao == r"\bpainel\b" and regras[0].flags == re.I


@pytest.mark.parametrize(
    ("trocar", "por", "trecho"),
    [
        ("padrao:", "padroa:", "sem padrao"),
        ("sugestao: dashboard", "sugestao: ''", "sem sugestao"),
        ("'\\bpainel\\b'", "'(painel'", "expressão inválida"),
        ("'\\bpainel\\b'", '"\\bpainel\\b"', "caractere de controle"),
        ("ignorar_maiusculas: true", "ignorar_maiusculas: sim", "true ou false"),
        ("permitido_em: []", "permitido_em: index.mdx", "lista"),
    ],
)
def test_regra_malformada_vira_erro_e_nao_some(tmp_path: Path, trocar: str, por: str, trecho: str):
    regras, erros = _vocab(tmp_path, REGRA_OK.replace(trocar, por))
    assert regras == []
    assert len(erros) == 1 and "regra 1" in erros[0] and trecho in erros[0]


def test_vocabulario_vazio_vira_erro(tmp_path: Path):
    arquivo = tmp_path / "vocabulario.yaml"
    arquivo.write_text("regras: []\n", encoding="utf-8")
    relatorio = comum.Relatorio()
    assert comum.carregar_vocabulario(arquivo, relatorio) == []
    assert "nenhuma regra" in relatorio.erros[0]


def test_tipos_reais_tem_os_dez_slugs():
    relatorio = comum.Relatorio()
    slugs = comum.carregar_tipos(comum.DADOS / "modelos.yaml", relatorio)
    assert relatorio.erros == []
    assert sorted(slugs) == sorted(["kpi", "conceito", "processo", "decisao", "politica", "dataset",
                                    "relacionamento", "dashboard", "rubrica", "casos-teste"])


@pytest.mark.parametrize(
    ("corpo", "trecho"),
    [
        ("  - nome: Indicador\n    nivel: nucleo\n", "sem slug"),
        ("  - slug: kpi\n    nome: Indicador\n    nivel: principal\n", "nível"),
        ("  - slug: kpi\n    nome: Indicador\n    nivel: nucleo\n  - slug: kpi\n    nome: Outro\n    nivel: segundo\n", "repetido"),
        ("", "nenhum tipo"),
    ],
)
def test_tipo_malformado_vira_erro(tmp_path: Path, corpo: str, trecho: str):
    arquivo = tmp_path / "modelos.yaml"
    arquivo.write_text("tipos:\n" + corpo if corpo else "tipos: []\n", encoding="utf-8")
    relatorio = comum.Relatorio()
    comum.carregar_tipos(arquivo, relatorio)
    assert any(trecho in e for e in relatorio.erros), relatorio.erros
