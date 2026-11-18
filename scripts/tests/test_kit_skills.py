"""Testes das Skills reais do kit (contexto-elicitar e contexto-consultar), lendo os arquivos do repositório."""
import re

import pytest

import comum
import kit
from comum import ROOT, Relatorio

SKILLS = ROOT / "src" / "kit" / "skills"
NOMES = ("contexto-elicitar", "contexto-consultar")
CODIGO = re.compile(r"^[ \t]*```.*?^[ \t]*```|`[^`\n]*`", re.MULTILINE | re.DOTALL)
FICCAO = re.compile(r"\bfict[íi]ci\w*|\bhipot[ée]tic\w*|\bdemonstrativ\w*|\bilustrativ\w*|\bdid[áa]tic\w*|\bfic[çc][ãa]o\b|\bexemplificativ\w*|\blaborat[óo]rio pedag[óo]gico|A Aurora não existe", re.I)


def textos_visiveis(nome: str) -> list[tuple[str, str]]:
    achados = []
    for caminho in sorted((SKILLS / nome).rglob("*.md")):
        texto = caminho.read_text(encoding="utf-8")
        if caminho.name == "SKILL.md":  # só description é lida pelo validador; name e license ficam de fora
            _, descricao, corpo = texto.split("---\n", 2)
            descricao = "\n".join(l for l in descricao.splitlines() if l.startswith("description:"))
            texto = descricao + "\n" + corpo
        achados.append((caminho.relative_to(ROOT).as_posix(), CODIGO.sub(" ", texto)))
    return achados


def test_kit_yaml_real_carrega_sem_erro():
    relatorio = Relatorio()
    config = kit.carregar_config(ROOT / "src" / "kit" / "kit.yaml", relatorio)
    assert relatorio.erros == []
    assert config is not None
    assert {"auditar-coleta", "contexto-elicitar", "contexto-consultar"} <= set(config.skills)
    assert config.skills["contexto-elicitar"] == () and config.skills["contexto-consultar"] == ()


@pytest.mark.parametrize("nome", NOMES + ("auditar-coleta",))
def test_skill_real_passa_nas_regras_do_kit(nome):
    relatorio = Relatorio()
    kit.erros_da_skill(SKILLS / nome / "SKILL.md", nome, relatorio)
    assert relatorio.erros == []


def test_description_da_elicitar_nao_usa_a_palavra_do_vocabulario():
    lido = comum.ler_frontmatter(SKILLS / "contexto-elicitar" / "SKILL.md", Relatorio())
    assert lido is not None and "elicit" not in lido[0]["description"].lower()


def test_tipos_cita_todo_slug_de_modelos():
    relatorio = Relatorio()
    modelos = comum.carregar_modelos(ROOT / "src" / "data" / "modelos.yaml", relatorio)
    assert relatorio.erros == [] and len(modelos) == 11
    texto = (SKILLS / "contexto-elicitar" / "references" / "tipos.md").read_text(encoding="utf-8")
    for m in modelos:
        assert f"downloads/template-{m.slug}.md" in texto
        assert f"schemas/1.1.0/{m.slug}.schema.json" in texto


def test_perguntas_por_incidente_cita_as_oito_familias_da_pagina():
    pagina = (ROOT / "src/content/docs/percurso/descubra-o-que-falta.mdx").read_text(encoding="utf-8")
    familias = [l.split("|")[1].strip() for l in pagina.splitlines()
                if l.startswith("|") and not l.startswith("|--") and l.split("|")[1].strip() not in ("Família", "Confirmado")]
    familias = familias[:8]
    assert len(familias) == 8
    texto = (SKILLS / "contexto-elicitar" / "references" / "perguntas-por-incidente.md").read_text(encoding="utf-8")
    for familia in familias:
        assert re.search(rf"^\| {familia} \|", texto, re.MULTILINE), familia


@pytest.mark.parametrize("nome", NOMES)
def test_textos_nao_casam_vocabulario_nem_aviso_de_ficcao_nem_travessao(nome):
    regras = comum.carregar_vocabulario(ROOT / "src" / "data" / "vocabulario.yaml", Relatorio())
    assert regras
    for caminho, texto in textos_visiveis(nome):
        assert "—" not in texto and "–" not in texto, caminho
        assert not FICCAO.search(texto), caminho
        for regra in regras:
            achado = re.search(regra.padrao, texto, regra.flags)
            assert not achado, f"{caminho}: {achado.group(0)!r}; use {regra.sugestao}"
    for caminho in (SKILLS / nome).rglob("*.md"):
        bruto = caminho.read_text(encoding="utf-8")
        assert "—" not in bruto and "–" not in bruto, caminho
