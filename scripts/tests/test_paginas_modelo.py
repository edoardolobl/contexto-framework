"""Testes do validador de página de modelo: texto de mentira em memória e raiz de mentira em tmp_path."""
from pathlib import Path
import subprocess
import sys

import pytest

import check_paginas_modelo as c

ARQUIVO = "src/content/docs/templates/kpi.mdx"

PAGINA_VALIDA = """---
title: Indicador (KPI)
---

import X from 'x';

<TemplateStart kind="kpi" />

## O problema

Texto do problema.

<ParContrastante />

## Como estudar

<Steps>

<EtapaDeEstudo tipo="comentado">
<ExampleDoc file="exemplo-kpi-completo.yaml" />
<details><summary>Por que</summary>Porque sim.</details>
<Exercicio titulo="Achar a falta" />
</EtapaDeEstudo>

<EtapaDeEstudo tipo="diagnostico">
<ExampleDoc file="exemplo-kpi-lacunas.yaml" />
</EtapaDeEstudo>

<EtapaDeEstudo tipo="complete">
<Exercicio titulo="Complete" />
</EtapaDeEstudo>

<EtapaDeEstudo tipo="caso-novo">
Escreva o seu.
</EtapaDeEstudo>

<EtapaDeEstudo tipo="teste">
<Exercicio titulo="Teste 1" />
<Exercicio titulo="Teste 2" />
</EtapaDeEstudo>

</Steps>

## Baixe o modelo

<TemplateDownloads kind="kpi" />

Veja todos os campos em [referência de campos](../../referencias/campos/kpi/).
"""


def problemas(texto: str, slug: str = "kpi", campos_existe: bool = True) -> list[str]:
    return c.verificar_pagina(texto, slug, ARQUIVO, campos_existe=campos_existe)


def troca(texto: str, antigo: str, novo: str) -> str:
    assert antigo in texto
    return texto.replace(antigo, novo, 1)


def linha_de(texto: str, trecho: str) -> int:
    return next(i for i, linha in enumerate(texto.split("\n"), start=1) if trecho in linha)


def test_pagina_valida_nao_tem_problemas():
    assert problemas(PAGINA_VALIDA) == []


def test_triagem_opcional_entre_steps_e_baixe_e_aceita():
    texto = troca(PAGINA_VALIDA, "</Steps>\n", "</Steps>\n\n## Triagem\n\nQuando usar.\n")
    assert problemas(texto) == []


def test_mensagens_citam_arquivo_e_linha():
    texto = troca(PAGINA_VALIDA, '<TemplateStart kind="kpi" />', "")
    for mensagem in problemas(texto):
        assert mensagem.startswith(f"{ARQUIVO}:")
        assert mensagem.split(":")[1].isdigit()


class TestRegra1TemplateStart:
    def test_ausente(self):
        erros = problemas(troca(PAGINA_VALIDA, '<TemplateStart kind="kpi" />', ""))
        assert any("TemplateStart" in e for e in erros)

    def test_depois_do_problema(self):
        texto = troca(PAGINA_VALIDA, '<TemplateStart kind="kpi" />\n', "")
        texto = troca(texto, "<ParContrastante />", '<ParContrastante />\n\n<TemplateStart kind="kpi" />')
        assert any("TemplateStart" in e and "antes" in e for e in problemas(texto))

    def test_kind_de_outro_tipo(self):
        erros = problemas(troca(PAGINA_VALIDA, 'kind="kpi" />\n\n## O problema', 'kind="dataset" />\n\n## O problema'))
        assert any("TemplateStart" in e and 'kind="kpi"' in e for e in erros)


class TestRegra2OProblema:
    def test_ausente(self):
        erros = problemas(troca(PAGINA_VALIDA, "## O problema", "## Outro"))
        assert any("## O problema" in e and "exatamente um" in e for e in erros)

    def test_repetido_cita_a_linha_da_repeticao(self):
        texto = troca(PAGINA_VALIDA, "## Como estudar", "## O problema\n\n## Como estudar")
        segunda = max(i for i, linha in enumerate(texto.split("\n"), start=1) if linha == "## O problema")
        assert any("exatamente um" in e and f":{segunda}:" in e for e in problemas(texto))

    def test_sem_par_contrastante_antes_do_proximo_h2(self):
        erros = problemas(troca(PAGINA_VALIDA, "<ParContrastante />\n", ""))
        assert any("ParContrastante" in e for e in erros)

    def test_par_contrastante_depois_do_proximo_h2_nao_vale(self):
        texto = troca(PAGINA_VALIDA, "<ParContrastante />\n", "")
        texto = troca(texto, "## Como estudar", "## Como estudar\n\n<ParContrastante />")
        assert any("ParContrastante" in e for e in problemas(texto))


class TestRegra3Steps:
    def test_sem_steps(self):
        texto = troca(troca(PAGINA_VALIDA, "<Steps>", ""), "</Steps>", "")
        assert any("<Steps>" in e for e in problemas(texto))

    def test_steps_nao_fechado(self):
        assert any("</Steps>" in e for e in problemas(troca(PAGINA_VALIDA, "</Steps>", "")))

    def test_steps_antes_do_problema_nao_conta(self):
        texto = troca(troca(PAGINA_VALIDA, "<Steps>", ""), "</Steps>", "")
        texto = troca(texto, "## O problema", "<Steps>\n</Steps>\n\n## O problema")
        assert any("<Steps>" in e for e in problemas(texto))


class TestRegra4Etapas:
    @pytest.mark.parametrize("tipo", ["comentado", "diagnostico", "complete", "caso-novo", "teste"])
    def test_etapa_ausente(self, tipo):
        texto = troca(PAGINA_VALIDA, f'tipo="{tipo}"', 'tipo="outra"')
        erros = problemas(texto)
        assert any(f'tipo="{tipo}"' in e and "falta" in e for e in erros)

    def test_etapa_repetida(self):
        texto = troca(PAGINA_VALIDA, 'tipo="caso-novo"', 'tipo="teste"')
        assert any('tipo="teste"' in e and "uma vez" in e for e in problemas(texto))

    def test_ordem_trocada(self):
        texto = troca(PAGINA_VALIDA, 'tipo="diagnostico"', 'tipo="TMP"')
        texto = troca(texto, 'tipo="complete"', 'tipo="diagnostico"')
        texto = troca(texto, 'tipo="TMP"', 'tipo="complete"')
        assert any("ordem" in e for e in problemas(texto))

    def test_etapa_fora_do_bloco_steps_nao_conta(self):
        texto = troca(PAGINA_VALIDA, "</Steps>", '</Steps>\n\n<EtapaDeEstudo tipo="teste">\n</EtapaDeEstudo>')
        assert problemas(texto) == []


class TestRegra5ConteudoDasEtapas:
    def test_comentado_sem_exemplo_completo(self):
        erros = problemas(troca(PAGINA_VALIDA, "exemplo-kpi-completo.yaml", "exemplo-dataset-completo.yaml"))
        assert any("comentado" in e and "exemplo-kpi-completo.yaml" in e for e in erros)

    def test_comentado_com_menos_de_dois_details_ou_exercicios(self):
        texto = troca(PAGINA_VALIDA, '<details><summary>Por que</summary>Porque sim.</details>\n', "")
        assert any("comentado" in e and "pelo menos 2" in e for e in problemas(texto))

    def test_comentado_soma_details_e_exercicio(self):
        texto = troca(PAGINA_VALIDA, '<Exercicio titulo="Achar a falta" />', '<details>b</details>')
        assert problemas(texto) == []

    def test_diagnostico_sem_exemplo_de_lacunas(self):
        erros = problemas(troca(PAGINA_VALIDA, "exemplo-kpi-lacunas.yaml", "exemplo-kpi-completo.yaml"))
        assert any("diagnostico" in e and "exemplo-kpi-lacunas.yaml" in e for e in erros)

    def test_complete_sem_exercicio(self):
        erros = problemas(troca(PAGINA_VALIDA, '<Exercicio titulo="Complete" />', ""))
        assert any("complete" in e and "pelo menos 1" in e for e in erros)

    def test_teste_com_um_exercicio_so(self):
        erros = problemas(troca(PAGINA_VALIDA, '<Exercicio titulo="Teste 2" />', ""))
        assert any("teste" in e and "pelo menos 2" in e for e in erros)

    def test_exercicio_de_outra_etapa_nao_conta(self):
        texto = troca(PAGINA_VALIDA, '<Exercicio titulo="Teste 2" />', "")
        texto = troca(texto, '<Exercicio titulo="Complete" />', '<Exercicio titulo="Complete" />\n<Exercicio titulo="Extra" />')
        assert any("teste" in e and "pelo menos 2" in e for e in problemas(texto))


class TestRegra6Baixe:
    def test_sem_h2_baixe(self):
        erros = problemas(troca(PAGINA_VALIDA, "## Baixe o modelo", "## Pegue"))
        assert any("## Baixe o modelo" in e for e in erros)

    def test_baixe_nao_e_o_ultimo_h2(self):
        erros = problemas(PAGINA_VALIDA + "\n## Depois\n")
        assert any("último" in e for e in erros)

    def test_dois_h2_entre_steps_e_baixe(self):
        texto = troca(PAGINA_VALIDA, "</Steps>\n", "</Steps>\n\n## Triagem\n\n## Outra\n")
        assert any("triagem" in e for e in problemas(texto))

    def test_sem_template_downloads_no_baixe(self):
        erros = problemas(troca(PAGINA_VALIDA, '<TemplateDownloads kind="kpi" />', ""))
        assert any('<TemplateDownloads kind="kpi"' in e for e in erros)

    def test_sem_link_para_referencia_de_campos(self):
        erros = problemas(troca(PAGINA_VALIDA, "referencias/campos/kpi/", "referencias/outra/"))
        assert any("referencias/campos/kpi/" in e for e in erros)


class TestRegra7DownloadsCedo:
    def test_template_downloads_antes_do_baixe(self):
        texto = troca(PAGINA_VALIDA, "Texto do problema.", 'Texto do problema.\n\n<TemplateDownloads kind="kpi" />')
        erros = problemas(texto)
        assert any("antes de ## Baixe o modelo" in e and f":{linha_de(texto, '<TemplateDownloads')}:" in e for e in erros)

    def test_link_de_download_antes_do_baixe(self):
        texto = troca(PAGINA_VALIDA, "Texto do problema.", "[baixar](../../../downloads/template-kpi.md)")
        assert any("downloads/template-" in e for e in problemas(texto))

    def test_link_de_download_depois_do_baixe_e_aceito(self):
        texto = PAGINA_VALIDA + "\n[arquivo](/downloads/template-kpi.yaml)\n"
        assert problemas(texto) == []


class TestBlocosCercados:
    def test_ignora_o_que_esta_dentro_de_cerca(self):
        texto = troca(PAGINA_VALIDA, "Texto do problema.", 'Texto do problema.\n\n```mdx\n<TemplateDownloads kind="kpi" />\n## O problema\n```')
        assert problemas(texto) == []

    def test_cerca_nao_esconde_o_que_falta(self):
        texto = troca(PAGINA_VALIDA, '<TemplateDownloads kind="kpi" />', '```\n<TemplateDownloads kind="kpi" />\n```')
        assert any("<TemplateDownloads" in e for e in problemas(texto))

    def test_numeros_de_linha_contam_as_linhas_cercadas(self):
        texto = troca(PAGINA_VALIDA, "Texto do problema.", "```\na\nb\n```\n\n[x](../downloads/template-kpi.md)")
        erros = problemas(texto)
        assert any(f":{linha_de(texto, 'downloads/template-')}:" in e for e in erros)


class TestRegra8PaginaDeCampos:
    def test_pagina_de_campos_ausente(self):
        erros = problemas(PAGINA_VALIDA, campos_existe=False)
        assert any("referencias/campos/kpi.md" in e for e in erros)


def montar(raiz: Path, pagina: str | None = PAGINA_VALIDA, campos: bool = True) -> None:
    (raiz / "src/data").mkdir(parents=True)
    (raiz / "src/content/docs/templates").mkdir(parents=True)
    (raiz / "src/content/docs/referencias/campos").mkdir(parents=True)
    (raiz / "src/data/modelos.yaml").write_text(
        "tipos:\n  - slug: kpi\n    pagina: kpi\n    nome: KPI\n    nivel: nucleo\n    tarefa: a\n    resumo: b\n"
        "    quando: c\n    resultado: d\n    preparar: e\n    rotulo_download: f\n", encoding="utf-8")
    if pagina is not None:
        (raiz / "src/content/docs/templates/kpi.mdx").write_text(pagina, encoding="utf-8")
    if campos:
        (raiz / "src/content/docs/referencias/campos/kpi.md").write_text("x\n", encoding="utf-8")


def test_executar_passa_com_pagina_valida(tmp_path: Path):
    montar(tmp_path)
    relatorio, mensagem = c.executar(tmp_path)
    assert relatorio.erros == [] and mensagem.startswith("OK: 1 página")


def test_executar_acusa_pagina_ausente(tmp_path: Path):
    montar(tmp_path, pagina=None)
    relatorio, _ = c.executar(tmp_path)
    assert any("kpi.mdx" in e for e in relatorio.erros)


def test_executar_acusa_regra_violada_e_campos_ausentes(tmp_path: Path):
    montar(tmp_path, pagina=troca(PAGINA_VALIDA, '<TemplateStart kind="kpi" />', ""), campos=False)
    relatorio, _ = c.executar(tmp_path)
    assert any("TemplateStart" in e for e in relatorio.erros)
    assert any("referencias/campos/kpi.md" in e for e in relatorio.erros)


def test_cli_sai_1_sem_traceback(tmp_path: Path):
    montar(tmp_path, pagina="sem nada\n")
    resultado = subprocess.run([sys.executable, str(Path(c.__file__)), "--raiz", str(tmp_path)],
                               capture_output=True, text=True, timeout=60)
    assert resultado.returncode == 1
    assert "ERRO:" in resultado.stdout and "Traceback" not in resultado.stderr + resultado.stdout
