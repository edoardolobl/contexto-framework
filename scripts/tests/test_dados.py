"""Testes da leitura de src/data/vocabulario.yaml e src/data/modelos.yaml."""
from pathlib import Path
import re

import pytest

import comum

# As 15 regras que estavam escritas em scripts/validate_content.py no commit d08c810,
# mais a regra 'modelo' (EDI-32, contrato 0.5) e a regra 'Perguntas de negócio'
# (ADR 0007, contrato 0.6).
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
    (r"\btemplates?\b(?![-_./])", "modelo (template só em nome de arquivo, endereço e código)", re.I, ()),
    (r"\bperguntas de refer[eê]ncia\b|\bcasos? de teste\b", "Perguntas de negócio (o tipo) ou gabarito (as respostas)", re.I, ("referencias/index.mdx",)),
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
                                    "relacionamento", "dashboard", "rubrica", "perguntas-de-negocio"])


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


# ---------- carregar_modelos, percurso, entradas, dimensoes ----------
MODELO_OK = {"slug": "kpi", "nome": "Indicador", "nivel": "nucleo", "tarefa": "t", "resumo": "r",
             "quando": "q", "resultado": "re", "preparar": "p", "rotulo_download": "rd"}


def _yaml(tmp_path: Path, nome: str, dados: object) -> Path:
    import yaml
    arquivo = tmp_path / nome
    arquivo.write_text(yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8")
    return arquivo


def _modelos(tmp_path: Path, itens: list) -> tuple[list, list[str]]:
    relatorio = comum.Relatorio()
    modelos = comum.carregar_modelos(_yaml(tmp_path, "modelos.yaml", {"tipos": itens}), relatorio)
    return modelos, relatorio.erros


def test_modelo_valido_e_pagina_assume_o_slug(tmp_path: Path):
    modelos, erros = _modelos(tmp_path, [MODELO_OK, {**MODELO_OK, "slug": "outro", "pagina": "pagina-outra"}])
    assert erros == []
    assert [(m.slug, m.pagina) for m in modelos] == [("kpi", "kpi"), ("outro", "pagina-outra")]
    with pytest.raises(Exception):
        modelos[0].nome = "x"  # type: ignore[misc]


@pytest.mark.parametrize("campo", ["nome", "tarefa", "resumo", "quando", "resultado", "preparar", "rotulo_download"])
@pytest.mark.parametrize("valor", ["ausente", "", "   ", 3])
def test_modelo_com_campo_de_texto_invalido(tmp_path: Path, campo: str, valor: object):
    item = {k: v for k, v in MODELO_OK.items() if k != campo}
    if valor != "ausente":
        item[campo] = valor
    modelos, erros = _modelos(tmp_path, [item])
    assert modelos == [] and len(erros) == 1 and "kpi" in erros[0] and campo in erros[0]


def test_modelo_com_nivel_invalido_slug_ou_pagina_repetidos(tmp_path: Path):
    assert "nível" in _modelos(tmp_path, [{**MODELO_OK, "nivel": "x"}])[1][0]
    assert "slug repetido" in _modelos(tmp_path, [MODELO_OK, MODELO_OK])[1][0]
    assert "pagina repetida" in _modelos(tmp_path, [MODELO_OK, {**MODELO_OK, "slug": "b", "pagina": "kpi"}])[1][0]
    assert "sem slug" in _modelos(tmp_path, [{"nome": "x"}, "texto"])[1][0]


def test_modelos_sem_lista_ou_arquivo_ausente(tmp_path: Path):
    assert "nenhum tipo" in _modelos(tmp_path, [])[1][0]
    relatorio = comum.Relatorio()
    assert comum.carregar_modelos(tmp_path / "nao.yaml", relatorio) == []
    assert "não encontrado" in relatorio.erros[0]


def test_carregar_tipos_e_involucro_que_devolve_slugs(tmp_path: Path):
    relatorio = comum.Relatorio()
    arquivo = _yaml(tmp_path, "modelos.yaml", {"tipos": [MODELO_OK, {**MODELO_OK, "slug": "b"}]})
    assert comum.carregar_tipos(arquivo, relatorio) == ["kpi", "b"]


PASSOS_OK = [{"numero": 1, "pagina": "percurso/a", "titulo": "A"}, {"numero": 2, "pagina": "percurso/b", "titulo": "B"}]


def _percurso(tmp_path: Path, dados: object) -> tuple[comum.Percurso, list[str]]:
    relatorio = comum.Relatorio()
    return comum.carregar_percurso(_yaml(tmp_path, "percurso.yaml", dados), relatorio), relatorio.erros


def test_percurso_valido(tmp_path: Path):
    percurso, erros = _percurso(tmp_path, {"passos": PASSOS_OK, "depois_do_ultimo": "templates"})
    assert erros == [] and percurso.depois_do_ultimo == "templates"
    assert percurso.passos == (comum.Passo(1, "percurso/a", "A"), comum.Passo(2, "percurso/b", "B"))


def test_percurso_com_depois_do_ultimo_em_mapa(tmp_path: Path):
    percurso, erros = _percurso(tmp_path, {"passos": PASSOS_OK, "depois_do_ultimo": {"pagina": "exemplos/x", "titulo": "X"}})
    assert erros == [] and percurso.depois_do_ultimo == "exemplos/x" and percurso.titulo_depois == "X"


@pytest.mark.parametrize(
    ("dados", "trecho"),
    [
        ({"passos": PASSOS_OK, "depois_do_ultimo": {"titulo": "X"}}, "depois_do_ultimo"),
        ({"passos": PASSOS_OK, "depois_do_ultimo": 3}, "depois_do_ultimo"),
        ({"passos": PASSOS_OK}, "depois_do_ultimo"),
        ({"passos": PASSOS_OK, "depois_do_ultimo": ""}, "depois_do_ultimo"),
        ({"passos": [PASSOS_OK[1], PASSOS_OK[0]], "depois_do_ultimo": "t"}, "numeração"),
        ({"passos": [PASSOS_OK[0], {**PASSOS_OK[1], "numero": 3}], "depois_do_ultimo": "t"}, "numeração"),
        ({"passos": [PASSOS_OK[0], {**PASSOS_OK[1], "pagina": "percurso/a"}], "depois_do_ultimo": "t"}, "página repetida"),
        ({"passos": [PASSOS_OK[0], {"numero": 2, "pagina": "x"}], "depois_do_ultimo": "t"}, "titulo"),
        ({"passos": [{**PASSOS_OK[0], "numero": "um"}], "depois_do_ultimo": "t"}, "numero"),
        ({"passos": [{**PASSOS_OK[0], "numero": True}], "depois_do_ultimo": "t"}, "numero"),
        ({"passos": [], "depois_do_ultimo": "t"}, "nenhum passo"),
        ({"passos": ["x"], "depois_do_ultimo": "t"}, "passo 1"),
    ],
)
def test_percurso_invalido_vira_erro(tmp_path: Path, dados: dict, trecho: str):
    _, erros = _percurso(tmp_path, dados)
    assert any(trecho in e for e in erros), erros


ENTRADA_OK = {"sintoma": "s", "texto": "t", "pagina": "p"}


def _entradas(tmp_path: Path, itens: list) -> tuple[list, list[str]]:
    relatorio = comum.Relatorio()
    return comum.carregar_entradas(_yaml(tmp_path, "entradas.yaml", {"entradas": itens}), relatorio), relatorio.erros


def test_entrada_valida_e_provisoria_com_nota(tmp_path: Path):
    entradas, erros = _entradas(tmp_path, [ENTRADA_OK, {**ENTRADA_OK, "sintoma": "s2", "provisorio": True, "nota": "em revisão"}])
    assert erros == [] and [e.provisorio for e in entradas] == [False, True] and entradas[1].nota == "em revisão"


@pytest.mark.parametrize(
    ("item", "trecho"),
    [
        ({"texto": "t", "pagina": "p"}, "sintoma"),
        ({"sintoma": "s", "pagina": "p"}, "texto"),
        ({"sintoma": "s", "texto": "t"}, "pagina"),
        ({**ENTRADA_OK, "sintoma": ""}, "sintoma"),
        ({**ENTRADA_OK, "provisorio": "sim"}, "provisorio"),
        ({**ENTRADA_OK, "provisorio": True}, "nota"),
        ({**ENTRADA_OK, "provisorio": True, "nota": " "}, "nota"),
        ("solto", "entrada 1"),
    ],
)
def test_entrada_invalida_vira_erro(tmp_path: Path, item: object, trecho: str):
    entradas, erros = _entradas(tmp_path, [item])
    assert entradas == [] and any(trecho in e for e in erros), erros


def test_entrada_com_sintoma_repetido_vira_erro(tmp_path: Path):
    entradas, erros = _entradas(tmp_path, [ENTRADA_OK, {**ENTRADA_OK, "texto": "outro", "pagina": "q"}])
    assert [e.sintoma for e in entradas] == ["s"] and any("sintoma repetido" in e for e in erros), erros


def test_entradas_com_a_mesma_pagina_sao_aceitas(tmp_path: Path):
    entradas, erros = _entradas(tmp_path, [ENTRADA_OK, {**ENTRADA_OK, "sintoma": "outro"}])
    assert erros == [] and len(entradas) == 2


def test_entradas_vazias(tmp_path: Path):
    assert "nenhuma entrada" in _entradas(tmp_path, [])[1][0]


def _dim(n: int) -> dict:
    return {"nome": f"Dim {n}", "pergunta": "p", "revisao": "r", "resposta_fraca": "f",
            "resposta_util": "u", "onde_procurar": "o"}


def _dimensoes(tmp_path: Path, itens: list) -> tuple[list, list[str]]:
    relatorio = comum.Relatorio()
    return comum.carregar_dimensoes(_yaml(tmp_path, "dimensoes.yaml", {"dimensoes": itens}), relatorio), relatorio.erros


def test_oito_dimensoes_validas_com_metadado_comum_opcional(tmp_path: Path):
    itens = [_dim(n) for n in range(8)]
    itens[0]["metadado_comum"] = "vigência"
    dimensoes, erros = _dimensoes(tmp_path, itens)
    assert erros == [] and len(dimensoes) == 8
    assert dimensoes[0].metadado_comum == "vigência" and dimensoes[1].metadado_comum is None


def test_dimensoes_vazias(tmp_path: Path):
    assert any("nenhuma dimensão" in e for e in _dimensoes(tmp_path, [])[1])


@pytest.mark.parametrize("quantidade", [7, 9])
def test_dimensoes_fora_de_oito(tmp_path: Path, quantidade: int):
    assert any("exatamente 8" in e for e in _dimensoes(tmp_path, [_dim(n) for n in range(quantidade)])[1])


def test_dimensao_sem_nome(tmp_path: Path):
    itens = [_dim(n) for n in range(8)]
    del itens[3]["nome"]
    assert any("dimensão #4 sem nome" in e for e in _dimensoes(tmp_path, itens)[1])


@pytest.mark.parametrize("campo", ["pergunta", "revisao", "resposta_fraca", "resposta_util", "onde_procurar"])
def test_dimensao_sem_campo(tmp_path: Path, campo: str):
    itens = [_dim(n) for n in range(8)]
    del itens[3][campo]
    _, erros = _dimensoes(tmp_path, itens)
    assert any(campo in e and "Dim 3" in e for e in erros), erros


def test_dimensao_nome_repetido_e_metadado_invalido(tmp_path: Path):
    itens = [_dim(n) for n in range(8)]
    itens[1]["nome"] = "Dim 0"
    itens[2]["metadado_comum"] = "prazo"
    _, erros = _dimensoes(tmp_path, itens)
    assert any("nome repetido" in e for e in erros) and any("metadado_comum" in e for e in erros)


def test_dimensao_que_nao_e_mapa(tmp_path: Path):
    _, erros = _dimensoes(tmp_path, ["x"] + [_dim(n) for n in range(7)])
    assert any("dimensão 1" in e for e in erros)


@pytest.mark.parametrize("carregador", ["carregar_percurso", "carregar_entradas", "carregar_dimensoes"])
def test_arquivo_ausente_ou_sem_mapa_nao_gera_traceback(tmp_path: Path, carregador: str):
    funcao = getattr(comum, carregador)
    relatorio = comum.Relatorio()
    funcao(tmp_path / "nao.yaml", relatorio)
    assert "não encontrado" in relatorio.erros[0]
    lista = tmp_path / "lista.yaml"
    lista.write_text("- a\n", encoding="utf-8")
    relatorio = comum.Relatorio()
    funcao(lista, relatorio)
    assert "mapa na raiz" in relatorio.erros[0]
