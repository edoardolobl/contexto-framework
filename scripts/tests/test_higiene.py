"""Testes das checagens de higiene: caracteres invisíveis, descrições que só repetem o nome e versão."""
from pathlib import Path

import pytest

import check_higiene as h


class TestCaracteresInvisiveis:
    def test_texto_limpo_nao_acusa_nada(self):
        assert h.caracteres_invisiveis("Taxa de sessões convertidas: 25%\n") == []

    def test_acusa_espaco_de_largura_zero_com_linha_e_coluna(self):
        achados = h.caracteres_invisiveis("linha um\nab\u200bcd\n")
        assert achados == [(2, 3, "U+200B ZERO WIDTH SPACE")]

    def test_acusa_controle_bidirecional(self):
        achados = h.caracteres_invisiveis("nunca \u202ecalcule\n")
        assert [codigo for _, _, codigo in achados] == ["U+202E RIGHT-TO-LEFT OVERRIDE"]

    def test_acusa_marca_de_ordem_de_bytes(self):
        assert h.caracteres_invisiveis("\ufeffAGENTS")[0][2].startswith("U+FEFF")

    def test_acusa_caractere_de_tag_unicode(self):
        assert h.caracteres_invisiveis("ok\U000E0041")[0][2].startswith("U+E0041")

    def test_aceita_acentos_e_simbolos_comuns(self):
        assert h.caracteres_invisiveis("Ação, vigência, × 100, → próximo, R$ 10,00") == []


class TestDescricaoTautologica:
    @pytest.mark.parametrize(
        ("nome", "descricao"),
        [
            ("session_id", "Session ID"),
            ("Canal", "canal"),
            ("data_da_sessao", "Data da sessão."),
            ("Sessão interna", "sessão interna"),
        ],
    )
    def test_acusa_descricao_que_so_repete_o_nome(self, nome, descricao):
        assert h.descricao_tautologica(nome, descricao)

    @pytest.mark.parametrize(
        ("nome", "descricao"),
        [
            ("channel", "Plataforma em que ocorreu a sessão"),
            ("is_internal", "1 = sessão aberta na rede do escritório; 0 = qualquer outra"),
            ("session_date", "Data de referência no formato YYYY-MM-DD"),
        ],
    )
    def test_aceita_descricao_que_acrescenta_informacao(self, nome, descricao):
        assert not h.descricao_tautologica(nome, descricao)

    def test_descricao_vazia_nao_e_tautologia(self):
        assert not h.descricao_tautologica("channel", None)
        assert not h.descricao_tautologica("channel", "")


class TestPares:
    def test_encontra_pares_nome_e_significado_em_qualquer_nivel(self):
        dados = {"columns": [{"physicalName": "channel", "businessName": "Canal", "meaning": "canal"}]}
        pares = list(h.pares_nome_descricao(dados))
        assert ("Canal", "canal") in pares
        assert ("channel", "canal") in pares

    def test_chaves_antigas_em_snake_case_nao_formam_par(self):
        dados = {"columns": [{"physical_name": "channel", "business_name": "Canal", "meaning": "canal"}]}
        assert list(h.pares_nome_descricao(dados)) == []

    def test_ignora_mapas_sem_descricao(self):
        assert list(h.pares_nome_descricao({"name": "x", "type": "string"})) == []


class TestVersao:
    def test_reduz_versao_a_maior_e_menor(self):
        assert h.maior_menor("0.4.0") == "0.4"
        assert h.maior_menor("v0.4") == "0.4"
        assert h.maior_menor("1.12.3-rc1") == "1.12"

    def test_versao_ilegivel_vira_none(self):
        assert h.maior_menor("sem versão") is None

    def test_versoes_do_produto_le_as_quatro_fontes(self, tmp_path: Path):
        (tmp_path / "package.json").write_text('{"version": "0.4.0"}', encoding="utf-8")
        (tmp_path / "README.md").write_text("## O que existe na v0.4\n", encoding="utf-8")
        docs = tmp_path / "src" / "content" / "docs"
        docs.mkdir(parents=True)
        (docs / "index.mdx").write_text("Versão 0.4 · exemplos\n", encoding="utf-8")
        (tmp_path / "CHANGELOG.md").write_text("## [Não lançado]\n\n## [0.4.0] - 2026-11-16\n", encoding="utf-8")
        assert h.versoes_do_produto(tmp_path) == {
            "package.json": "0.4",
            "README.md": "0.4",
            "src/content/docs/index.mdx": "0.4",
            "CHANGELOG.md": "0.4",
        }

    def _raiz_com_changelog(self, tmp_path: Path, changelog: str, versao: str = "1.0.0-rc.1") -> Path:
        (tmp_path / "package.json").write_text(f'{{"version": "{versao}"}}', encoding="utf-8")
        (tmp_path / "README.md").write_text("## O que existe na v1.0\n", encoding="utf-8")
        docs = tmp_path / "src" / "content" / "docs"
        docs.mkdir(parents=True)
        (docs / "index.mdx").write_text("Versão 1.0 · exemplos\n", encoding="utf-8")
        (tmp_path / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
        return tmp_path

    def test_changelog_com_pre_lancamento_fica_em_1_0_e_bate_com_as_outras_fontes(self, tmp_path: Path):
        raiz = self._raiz_com_changelog(tmp_path, "## [Não lançado]\n\n## [1.0.0-rc.1] - 2026-11-17\n")
        assert set(h.versoes_do_produto(raiz).values()) == {"1.0"}

    def test_nao_lancado_sozinho_nao_conta_como_versao(self, tmp_path: Path):
        raiz = self._raiz_com_changelog(tmp_path, "## [Não lançado]\n")
        assert h.versoes_do_produto(raiz)["CHANGELOG.md"] is None

    def test_fonte_sem_versao_aparece_como_none(self, tmp_path: Path):
        (tmp_path / "package.json").write_text('{"version": "0.4.0"}', encoding="utf-8")
        assert h.versoes_do_produto(tmp_path)["README.md"] is None


class TestVocabularioNoContrato:
    def test_termo_ausente_da_tabela_do_contrato_e_acusado(self):
        contrato = "| Ideia | Termo | Não usar |\n|---|---|---|\n| Período em que vale | vigência | validade |\n"
        termos = [{"termo": "vigência"}, {"termo": "junção"}]
        assert h.termos_fora_do_contrato(termos, contrato) == ["junção"]


class TestCaracteresInvisiveisAmpliado:
    """Além da categoria Cf: seletores de variação, preenchedores, controles e separadores."""

    @pytest.mark.parametrize("codigo", [0xFE0F, 0xE0100, 0x3164, 0x115F, 0x2800, 0x001B, 0x0000, 0x2028, 0x2029, 0xFFA0])
    def test_acusa_caractere_que_esconde_texto(self, codigo):
        assert h.caracteres_invisiveis("a" + chr(codigo) + "b"), hex(codigo)

    def test_tab_e_retorno_de_carro_sao_aceitos(self):
        assert h.caracteres_invisiveis("coluna\tvalor\r\nlinha") == []


class TestPlural:
    def test_plural_simples_conta_como_repeticao(self):
        assert h.descricao_tautologica("Canais", "canal")


class TestContratoPorCelula:
    CONTRATO = (
        "## Vocabulário\n\n| Ideia | Termo | Não usar |\n|---|---|---|\n"
        "| Estado numerado | versão; “ID da versão” | revisão |\n"
        "| Painel | dashboard | painel |\n\n## Exemplos\n\n| A | junção | B |\n"
    )

    def test_termo_casa_com_parte_da_celula_separada_por_ponto_e_virgula(self):
        assert h.termos_fora_do_contrato([{"termo": "versão"}, {"termo": "ID da versão"}], self.CONTRATO) == []

    def test_pedaco_de_palavra_nao_conta(self):
        assert h.termos_fora_do_contrato([{"termo": "dash"}], self.CONTRATO) == ["dash"]

    def test_tabela_de_outra_secao_nao_conta(self):
        assert h.termos_fora_do_contrato([{"termo": "junção"}], self.CONTRATO) == ["junção"]


class TestChavesNovas:
    def test_campos_yaml_rotulo_e_descricao(self):
        dados = {"cabecalho": [{"chave": "id", "rotulo": "Identificador", "descricao": "identificador"}]}
        assert ("Identificador", "identificador") in list(h.pares_nome_descricao(dados))

    def test_prefLabel_conta_como_nome(self):
        assert ("Canal", "canal") in list(h.pares_nome_descricao({"prefLabel": "Canal", "description": "canal"}))

    def test_descricao_acrescenta_informacao_nao_e_acusada(self):
        dados = {"rotulo": "Identificador", "descricao": "Código único e estável do documento"}
        assert not any(h.descricao_tautologica(n, d) for n, d in h.pares_nome_descricao(dados))


class TestParesDeSchema:
    def test_objeto_com_title_e_description_iguais_e_acusado(self):
        schema = {"properties": {"owner": {"title": "Responsável", "description": "responsável"}}}
        assert list(h.pares_de_schema(schema)) == [("Responsável", "responsável")]

    def test_ignora_propriedade_chamada_title(self):
        schema = {"properties": {"title": {"type": "string", "description": "Nome do documento"}}}
        assert list(h.pares_de_schema(schema)) == []

    def test_percorre_listas_e_niveis(self):
        schema = {"allOf": [{"title": "A", "description": "a"}], "$defs": {"x": {"title": "B", "description": "c"}}}
        assert set(h.pares_de_schema(schema)) == {("A", "a"), ("B", "c")}


class TestStyleEmComponente:
    def test_acusa_bloco_style_com_arquivo_e_linha(self, tmp_path: Path):
        pasta = tmp_path / "src" / "components"
        pasta.mkdir(parents=True)
        (pasta / "Falso.astro").write_text("---\nconst a = 1;\n---\n<div>x</div>\n<style>\n  div { color: red; }\n</style>\n", encoding="utf-8")
        achados = h.componentes_com_style(tmp_path)
        assert achados == [(pasta / "Falso.astro", 5)]

    def test_acusa_style_com_atributos(self, tmp_path: Path):
        pasta = tmp_path / "src" / "components"
        pasta.mkdir(parents=True)
        (pasta / "Falso.astro").write_text("<div />\n<style is:global lang=\"css\">\n a { color: red }\n</style>\n", encoding="utf-8")
        assert [linha for _, linha in h.componentes_com_style(tmp_path)] == [2]

    def test_componente_sem_style_passa(self, tmp_path: Path):
        pasta = tmp_path / "src" / "components"
        pasta.mkdir(parents=True)
        (pasta / "Limpo.astro").write_text('---\n---\n<div class="caixa" style="color: red">x</div>\n', encoding="utf-8")
        assert h.componentes_com_style(tmp_path) == []

    def test_sem_pasta_de_componentes_nao_acusa_nada(self, tmp_path: Path):
        assert h.componentes_com_style(tmp_path) == []

    def test_mensagem_manda_o_css_para_src_styles(self, tmp_path: Path):
        pasta = tmp_path / "src" / "components"
        pasta.mkdir(parents=True)
        (pasta / "Falso.astro").write_text("<style>a{}</style>\n", encoding="utf-8")
        mensagens = h.erros_de_style(tmp_path)
        assert len(mensagens) == 1 and "src/styles" in mensagens[0] and "Falso.astro:1" in mensagens[0]
