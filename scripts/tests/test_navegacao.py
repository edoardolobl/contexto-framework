"""Testes do validador de navegação (check_navegacao.py) e das funções de rota de comum.py."""
from pathlib import Path

import pytest

import check_navegacao as nav
import comum
from comum import Modelo, Passo

CONFIG = """export default defineConfig({
  redirects: {
    '/exemplos/kpi/': `${base}/templates/kpi/`,
    '/fundamentos/promessa/': `${base}/metodo/visao-geral/`
  },
  integrations: [starlight({
    // sidebar: [ comentário com [ colchete
    sidebar: [
      { label: 'Início', link: '/' },
      { label: 'Percurso', items: ['percurso/um', "percurso/dois"] },
      { label: 'Modelos', items: [
        'templates/kpi', { label: 'Mais', items: ['templates/conceito'] }, 'templates/rubrica'
      ] },
      { label: 'Texto ]', items: ['metodo/limites'] }
    ]
  })]
});
"""


def _modelo(slug: str, nivel: str) -> Modelo:
    return Modelo(slug, slug, slug, nivel, "t", "r", "q", "re", "p", "rd")


# ---------- menu ----------
def test_bloco_do_menu_ignora_colchetes_em_strings_e_comentarios():
    bloco = nav.bloco_do_menu(CONFIG)
    assert bloco.strip().startswith("{ label: 'Início'") and bloco.strip().endswith("}")
    assert "metodo/limites" in bloco


def test_bloco_do_menu_ausente_devolve_vazio():
    assert nav.bloco_do_menu("export default {};") == ""


def test_grupos_do_menu_le_rotulos_paginas_e_subgrupos():
    grupos = nav.grupos_do_menu(nav.bloco_do_menu(CONFIG))
    assert [g.rotulo for g in grupos] == ["Início", "Percurso", "Modelos", "Texto ]"]
    assert grupos[0].paginas == ("/",)
    assert grupos[1].paginas == ("percurso/um", "percurso/dois")
    assert grupos[2].paginas == ("templates/kpi", "templates/conceito", "templates/rubrica")
    assert [s.rotulo for s in grupos[2].subgrupos] == ["Mais"]


def test_grupos_do_menu_vazio():
    assert nav.grupos_do_menu("") == []


def test_redirecionamentos_devolve_origem_e_destino():
    assert nav.redirecionamentos(CONFIG) == {"exemplos/kpi": "templates/kpi", "fundamentos/promessa": "metodo/visao-geral"}


def test_redirecionamentos_ausentes():
    assert nav.redirecionamentos("export default {};") == {}


# ---------- links ----------
def test_links_internos_le_markdown_e_href_e_ignora_externos_codigo_e_ancora():
    texto = (
        "Veja [a](../../metodo/limites/) e [b](https://x.com) e [c](#topo) e [d](./irma/).\n"
        '<a href="/contexto-framework/templates/kpi/">k</a> <a href="mailto:a@b.c">m</a>\n'
        "```md\n[e](../nao/conta/)\n```\n"
        "[f](../../downloads/x.yaml)\n"
    )
    assert nav.links_internos(texto, "/percurso/um/") == {"/metodo/limites/", "/percurso/um/irma/", "/templates/kpi/"}


def test_rota_da_pagina(tmp_path: Path):
    docs = tmp_path / "docs"
    assert comum.rota_da_pagina(docs / "a" / "b.mdx", docs) == "/a/b/"
    assert comum.rota_da_pagina(docs / "a" / "index.mdx", docs) == "/a/"
    assert comum.rota_da_pagina(docs / "index.mdx", docs) == "/"


@pytest.mark.parametrize(
    ("url", "esperado"),
    [
        ("../../metodo/x/", ("/metodo/x/", False)),
        ("./y#ancora", ("/percurso/um/y/", False)),
        ("https://a.com", (None, False)),
        ("#topo", (None, False)),
        ("mailto:a@b.c", (None, False)),
        ("/absoluto/", (None, False)),
        ("../../downloads/a.yaml", (None, False)),
        ("../../../acima/", ("/acima/", True)),
        ("../../..", ("/", True)),
    ],
)
def test_resolver_link(url: str, esperado: tuple):
    rota, subiu = comum.resolver_link("/percurso/um/", url)
    assert (rota, subiu) == esperado or (subiu and esperado[1])


# ---------- regras ----------
def test_pagina_orfa_e_a_que_nao_esta_no_menu_nem_recebe_link():
    rotas = {"/", "a", "b", "c"}
    assert nav.paginas_orfas({"a", "b", "c"}, {"a"}, {"a": {"b"}, "b": set(), "c": {"c"}}) == ["c"]
    assert nav.paginas_orfas(rotas, {"/", "a", "b", "c"}, {}) == []


def test_pagina_sem_menu_com_link_de_outra_nao_e_orfa():
    assert nav.paginas_orfas({"a", "b"}, {"a"}, {"a": {"b"}}) == []


def test_passos_sem_saida():
    passos = (Passo(1, "p/um", "Um"), Passo(2, "p/dois", "Dois"))
    textos = {"p/um": "texto <NextStep />", "p/dois": "sem componente"}
    assert nav.passos_sem_saida(passos, textos) == ["p/dois"]
    assert nav.passos_sem_saida(passos, {"p/um": "<NextStep />", "p/dois": "<NextStep passo={2} />"}) == []


@pytest.mark.parametrize(
    ("texto", "achou"),
    [("```yaml\na: 1\n```", True), ("```yml\na: 1\n```", True), ("<ExampleDoc file='x' />", True),
     ("```sql\nselect 1\n```", False), ("só texto", False)],
)
def test_yaml_no_percurso(texto: str, achou: bool):
    assert bool(nav.yaml_no_percurso(texto)) is achou


def test_ordem_dos_modelos_aceita_nucleo_segundo_complementar():
    modelos = [_modelo("kpi", "nucleo"), _modelo("conceito", "segundo"), _modelo("rubrica", "complementar")]
    assert nav.ordem_dos_modelos(["templates/kpi", "templates/conceito", "templates/rubrica"], modelos) == []


def test_ordem_dos_modelos_acusa_segundo_antes_de_nucleo_e_complementar_antes_de_segundo():
    modelos = [_modelo("kpi", "nucleo"), _modelo("conceito", "segundo"), _modelo("rubrica", "complementar")]
    assert nav.ordem_dos_modelos(["templates/conceito", "templates/kpi"], modelos)
    assert nav.ordem_dos_modelos(["templates/rubrica", "templates/conceito"], modelos)


def test_percurso_no_menu_exige_mesmas_paginas_na_mesma_ordem():
    passos = (Passo(1, "percurso/um", "U"), Passo(2, "percurso/dois", "D"))
    grupos = nav.grupos_do_menu(nav.bloco_do_menu(CONFIG))
    assert nav.percurso_no_menu(grupos, passos) == []
    invertido = (passos[1], passos[0])
    assert nav.percurso_no_menu(grupos, invertido)
    assert nav.percurso_no_menu(grupos, passos[:1])
    assert nav.percurso_no_menu([], passos)


def test_titulos_do_percurso_divergente_ou_pagina_ausente():
    passos = (Passo(1, "percurso/um", "Um"), Passo(2, "percurso/dois", "Dois"))
    assert nav.titulos_do_percurso(passos, {"percurso/um": "Um", "percurso/dois": "Dois"}) == []
    erros = nav.titulos_do_percurso(passos, {"percurso/um": "Outro"})
    assert len(erros) == 2 and "Outro" in erros[0] and "percurso/dois" in erros[1]


def test_destinos_inexistentes_e_redirecionamentos():
    paginas = {"a", "b", "templates"}
    entradas = [comum.Entrada("s", "t", "a", False, "")]
    assert nav.destinos(entradas, "templates", {"velha": "b"}, paginas) == []
    assert nav.destinos([comum.Entrada("s", "t", "nao-existe", False, "")], "templates", {}, paginas)
    assert nav.destinos(entradas, "nao-existe", {}, paginas)
    assert nav.destinos(entradas, "templates", {"velha": "nao-existe"}, paginas)
    assert nav.destinos(entradas, "templates", {"a": "b"}, paginas)  # origem ainda é página


# ---------- integração em árvore mínima ----------
def _arvore(raiz: Path, nextstep: bool = True, link_para_c: bool = False) -> None:
    docs = raiz / "src" / "content" / "docs"
    (docs / "percurso").mkdir(parents=True)
    dados = raiz / "src" / "data"
    dados.mkdir(parents=True)

    def pagina(rel: str, titulo: str, corpo: str = "") -> None:
        arq = docs / rel
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(f"---\ntitle: {titulo}\ndescription: d\n---\n{corpo}\n", encoding="utf-8")

    pagina("index.mdx", "Início", "[um](percurso/um/)")
    pagina("percurso/um.mdx", "Um", "[dois](../dois/)\n<NextStep />" if nextstep else "[dois](../dois/)")
    pagina("percurso/dois.mdx", "Dois", "<NextStep />\n[mod](../../templates/kpi/)")
    pagina("templates/index.mdx", "Modelos", "[k](kpi/)")
    pagina("templates/kpi.mdx", "Indicador", "[voltar](../)")
    pagina("solta.mdx", "Solta", "[c](../c/)" if link_para_c else "texto")
    (dados / "percurso.yaml").write_text(
        "passos:\n  - numero: 1\n    pagina: percurso/um\n    titulo: Um\n"
        "  - numero: 2\n    pagina: percurso/dois\n    titulo: Dois\ndepois_do_ultimo: templates\n", encoding="utf-8")
    (dados / "entradas.yaml").write_text(
        "entradas:\n  - sintoma: s\n    texto: t\n    pagina: percurso/um\n", encoding="utf-8")
    (dados / "modelos.yaml").write_text(
        "tipos:\n  - slug: kpi\n    nome: Indicador\n    nivel: nucleo\n    tarefa: a\n    resumo: b\n"
        "    quando: c\n    resultado: d\n    preparar: e\n    rotulo_download: f\n", encoding="utf-8")
    (raiz / "astro.config.mjs").write_text(
        "export default { redirects: {}, x: { sidebar: [\n"
        "  { label: 'Início', link: '/' },\n  { label: 'Percurso', items: ['percurso/um', 'percurso/dois'] },\n"
        "  { label: 'Modelos', items: ['templates', 'templates/kpi'] }\n] } };\n", encoding="utf-8")


def _rodar(raiz: Path) -> comum.Relatorio:
    relatorio = comum.Relatorio()
    nav.executar(raiz, relatorio)
    return relatorio


def test_arvore_valida_nao_tem_erros_e_avisa_pagina_sem_saida(tmp_path: Path):
    _arvore(tmp_path)
    (tmp_path / "src/content/docs/solta.mdx").unlink()
    relatorio = _rodar(tmp_path)
    assert relatorio.erros == []


def test_arvore_sem_nextstep_acusa_proximo_passo(tmp_path: Path):
    _arvore(tmp_path, nextstep=False)
    assert any("próximo passo ausente" in e for e in _rodar(tmp_path).erros)


def test_arvore_com_pagina_orfa(tmp_path: Path):
    _arvore(tmp_path)
    erros = _rodar(tmp_path).erros
    assert any("página órfã" in e and "solta" in e for e in erros)


def test_arvore_pagina_com_link_de_outra_deixa_de_ser_orfa_mas_avisa_beco(tmp_path: Path):
    _arvore(tmp_path, link_para_c=True)
    (tmp_path / "src/content/docs/c.mdx").write_text("---\ntitle: C\ndescription: d\n---\nfim\n", encoding="utf-8")
    relatorio = _rodar(tmp_path)
    assert "página órfã: c" not in " | ".join(e.split(" (")[0] for e in relatorio.erros)
    assert any(a.endswith(": c") and "sem link" in a for a in relatorio.avisos)


def test_arvore_com_yaml_no_percurso(tmp_path: Path):
    _arvore(tmp_path)
    arq = tmp_path / "src/content/docs/percurso/um.mdx"
    arq.write_text(arq.read_text(encoding="utf-8") + "\n```yaml\na: 1\n```\n", encoding="utf-8")
    assert any("YAML" in e for e in _rodar(tmp_path).erros)


def test_arvore_com_titulo_divergente(tmp_path: Path):
    _arvore(tmp_path)
    arq = tmp_path / "src/content/docs/percurso/um.mdx"
    arq.write_text(arq.read_text(encoding="utf-8").replace("title: Um", "title: Primeiro"), encoding="utf-8")
    assert any("Primeiro" in e for e in _rodar(tmp_path).erros)


def test_arvore_com_percurso_diferente_do_menu(tmp_path: Path):
    _arvore(tmp_path)
    cfg = tmp_path / "astro.config.mjs"
    cfg.write_text(cfg.read_text(encoding="utf-8").replace("'percurso/um', 'percurso/dois'", "'percurso/dois', 'percurso/um'"), encoding="utf-8")
    assert any("grupo Percurso" in e for e in _rodar(tmp_path).erros)


def test_arvore_com_destino_inexistente(tmp_path: Path):
    _arvore(tmp_path)
    arq = tmp_path / "src/data/entradas.yaml"
    arq.write_text(arq.read_text(encoding="utf-8").replace("percurso/um", "percurso/nada"), encoding="utf-8")
    assert any("percurso/nada" in e for e in _rodar(tmp_path).erros)


def test_arvore_com_redirecionamento_para_pagina_inexistente(tmp_path: Path):
    _arvore(tmp_path)
    cfg = tmp_path / "astro.config.mjs"
    cfg.write_text(cfg.read_text(encoding="utf-8").replace("redirects: {}", "redirects: { '/velha/': `${base}/nao/existe/` }"), encoding="utf-8")
    assert any("nao/existe" in e for e in _rodar(tmp_path).erros)


def test_arvore_com_modelos_fora_de_ordem(tmp_path: Path):
    _arvore(tmp_path)
    (tmp_path / "src/data/modelos.yaml").write_text(
        "tipos:\n"
        "  - {slug: kpi, nome: Indicador, nivel: segundo, tarefa: a, resumo: b, quando: c, resultado: d, preparar: e, rotulo_download: f}\n"
        "  - {slug: conceito, nome: Conceito, nivel: nucleo, tarefa: a, resumo: b, quando: c, resultado: d, preparar: e, rotulo_download: f}\n",
        encoding="utf-8")
    cfg = tmp_path / "astro.config.mjs"
    cfg.write_text(cfg.read_text(encoding="utf-8").replace("'templates/kpi'", "'templates/kpi', 'templates/conceito'"), encoding="utf-8")
    (tmp_path / "src/content/docs/templates/conceito.mdx").write_text("---\ntitle: Conceito\ndescription: d\n---\n[k](../kpi/)\n", encoding="utf-8")
    assert any("ordem" in e for e in _rodar(tmp_path).erros)


def test_arvore_sem_bloco_de_menu_vira_erro_sem_traceback(tmp_path: Path):
    _arvore(tmp_path)
    (tmp_path / "astro.config.mjs").write_text("export default {};\n", encoding="utf-8")
    assert any("sidebar" in e for e in _rodar(tmp_path).erros)
