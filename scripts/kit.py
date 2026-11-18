"""Monta o kit para agentes (I-27): AGENTS.md, glossário, contratos, gabaritos, dados e skills.

Recebe os documentos já lidos e devolve arquivos em memória (caminho dentro do kit para bytes).
Quem escreve em disco, confere e remove órfãos é gerar_saidas.py.
"""
from __future__ import annotations

from dataclasses import dataclass
import io
import posixpath
from pathlib import Path
import re
from typing import Any
import zipfile

from comum import Relatorio, carregar_yaml, ler_frontmatter

MARCADOR_INDICE = "<!-- contexto:kit-indice -->"
TIPO_DO_GABARITO = "perguntas-de-negocio"
PADRAO_NOME_DA_SKILL = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAXIMO_NOME_DA_SKILL = 64
MAXIMO_DESCRICAO_DA_SKILL = 1024
LIMITE_LINHAS_DA_SKILL = 500
DATA_FIXA_DO_ZIP = (1980, 1, 1, 0, 0, 0)
PERMISSAO_DO_ZIP = 0o644
FRASE_DO_GLOSSARIO = ("Este glossário é gerado dos documentos aprovados. Quando houver dúvida, vale a definição "
                      "do documento citado.")
# Tipos cujos documentos viram termo do glossário; os outros só entram por um termo de kit.yaml.
TIPOS_DO_GLOSSARIO = ("conceito", "kpi", "evento-coleta")
# Tipos que nunca servem de fonte de termo: respostas esperadas, critérios de revisão e passos de trabalho.
TIPOS_FORA_DO_GLOSSARIO = ("perguntas-de-negocio", "rubrica", "processo")
_CERCA = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.MULTILINE | re.DOTALL)
_LINK = re.compile(r"\]\(([^)\s]+)\)")
_EXTERNO = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|#|/)", re.IGNORECASE)


@dataclass(frozen=True)
class Documento:
    id: str
    version: str
    title: str
    type: str
    status: str
    dados: dict[str, Any]
    md: bytes

    @property
    def rev(self) -> str:
        return f"{self.id}@{self.version}"


@dataclass(frozen=True)
class TermoDoKit:
    """Termo de kit.yaml sem campo próprio num documento; cita o documento aprovado que o define."""
    termo: str
    documento: str
    resumo: str
    sinonimos: tuple[str, ...] = ()
    nao_confundir: tuple[str, ...] = ()


@dataclass(frozen=True)
class Config:
    pasta: str
    dados: tuple[str, ...]
    skills: dict[str, tuple[str, ...]]
    termos: tuple[TermoDoKit, ...] = ()


@dataclass(frozen=True)
class Entrada:
    termo: str
    resumo: str
    sinonimos: tuple[str, ...]
    nao_confundir: tuple[str, ...]
    fonte: str


def _lista_de_textos(valor: Any) -> tuple[str, ...] | None:
    ok = isinstance(valor, list) and all(isinstance(v, str) and v for v in valor)
    return tuple(valor) if ok else None


def _termo_do_kit(item: Any, numero: int) -> tuple[TermoDoKit | None, list[str]]:
    if not isinstance(item, dict):
        return None, [f"termo {numero}: cada termo é um mapa com termo, documento e resumo"]
    termo, documento, resumo = item.get("termo"), item.get("documento"), item.get("resumo")
    nome = termo if isinstance(termo, str) and termo.strip() else f"{numero}"
    erros = [f"termo {nome}: falta '{chave}' (texto não vazio)" for chave, valor in
             (("termo", termo), ("documento", documento), ("resumo", resumo))
             if not isinstance(valor, str) or not valor.strip()]
    listas = {chave: [] if item.get(chave) is None else _lista_de_textos(item.get(chave))
              for chave in ("sinonimos", "nao_confundir")}
    erros += [f"termo {nome}: '{chave}' deve ser uma lista de textos" for chave, v in listas.items() if v is None]
    if erros:
        return None, erros
    return TermoDoKit(termo.strip(), documento.strip(), " ".join(resumo.split()),  # type: ignore[union-attr]
                      tuple(listas["sinonimos"] or ()), tuple(listas["nao_confundir"] or ())), []


def _termos_do_kit(valor: Any) -> tuple[tuple[TermoDoKit, ...], list[str]]:
    if valor is None:
        return (), []
    if not isinstance(valor, list):
        return (), ["'termos' deve ser uma lista de termos do glossário"]
    termos, erros = [], []
    for numero, item in enumerate(valor, start=1):
        termo, achados = _termo_do_kit(item, numero)
        erros += achados
        if termo is not None:
            termos.append(termo)
    return tuple(termos), erros


def carregar_config(caminho: Path, relatorio: Relatorio) -> Config | None:
    dados = carregar_yaml(caminho, relatorio)
    if dados is None:
        return None
    pasta, arquivos, skills = dados.get("pasta"), _lista_de_textos(dados.get("dados")), dados.get("skills")
    if not isinstance(pasta, str) or not pasta:
        relatorio.erro(caminho, "falta 'pasta' (nome da pasta do kit)")
    if arquivos is None:
        relatorio.erro(caminho, "'dados' deve ser uma lista de nomes de arquivo de public/downloads")
    if not isinstance(skills, dict) or not skills:
        relatorio.erro(caminho, "'skills' deve ser um mapa de nome da skill para lista de ids")
        return None
    ids = {nome: _lista_de_textos(lista) for nome, lista in skills.items()}
    if any(v is None for v in ids.values()):
        relatorio.erro(caminho, "cada skill deve listar os ids de references como lista de textos")
    termos, erros_dos_termos = _termos_do_kit(dados.get("termos"))
    for erro in erros_dos_termos:
        relatorio.erro(caminho, erro)
    if relatorio.erros or arquivos is None or not isinstance(pasta, str):
        return None
    return Config(pasta, arquivos, {nome: v or () for nome, v in ids.items()}, termos)


def erros_do_frontmatter_da_skill(dados: dict[str, Any], pasta: str) -> list[str]:
    """Regras da especificação Agent Skills para o frontmatter de um SKILL.md."""
    nome, descricao, erros = dados.get("name"), dados.get("description"), []
    if not isinstance(nome, str) or not PADRAO_NOME_DA_SKILL.match(nome) or len(nome) > MAXIMO_NOME_DA_SKILL:
        erros.append(f"name deve casar {PADRAO_NOME_DA_SKILL.pattern} com até {MAXIMO_NOME_DA_SKILL} caracteres (veio {nome!r})")
    elif nome != pasta:
        erros.append(f"name ({nome}) deve ser igual ao nome da pasta ({pasta})")
    if not isinstance(descricao, str) or not descricao.strip() or len(descricao) > MAXIMO_DESCRICAO_DA_SKILL:
        erros.append(f"description deve ter de 1 a {MAXIMO_DESCRICAO_DA_SKILL} caracteres")
    return erros


def erros_da_skill(caminho: Path, pasta: str, relatorio: Relatorio) -> None:
    lido = ler_frontmatter(caminho, relatorio)
    if lido is None:
        return
    for erro in erros_do_frontmatter_da_skill(lido[0], pasta):
        relatorio.erro(caminho, erro)
    linhas = len(lido[2].strip("\n").splitlines())
    if linhas >= LIMITE_LINHAS_DA_SKILL:
        relatorio.erro(caminho, f"corpo com {linhas} linhas; o limite é menos de {LIMITE_LINHAS_DA_SKILL}")


def links_quebrados(nome: str, texto: str, arquivos: set[str]) -> list[str]:
    """Links relativos de `texto` (arquivo `nome` dentro do kit) que não apontam para um arquivo do kit."""
    erros = []
    for alvo in _LINK.findall(_CERCA.sub("", texto)):
        if _EXTERNO.match(alvo):
            continue
        caminho = posixpath.normpath(posixpath.join(posixpath.dirname(nome), alvo.split("#")[0].split("?")[0]))
        if caminho not in arquivos and not any(a.startswith(caminho.rstrip("/") + "/") for a in arquivos):
            erros.append(f"{nome}: link relativo quebrado, {alvo} não existe no kit")
    return erros


def _vigente(documentos: list[Documento], id_: str) -> Documento | None:
    versoes = [d for d in documentos if d.id == id_ and d.status == "approved"]
    return max(versoes, key=lambda d: tuple(int(p) for p in d.version.split(".")), default=None)


def _lista(valor: Any) -> list[str]:
    itens = valor if isinstance(valor, list) else []
    return [" ".join(str(i).split()) for i in itens if i is not None and str(i).strip()]


def _sem_repeticao(itens: list[str]) -> list[str]:
    return list(dict.fromkeys(itens))


def _mapa(valor: Any) -> dict[str, Any]:
    return valor if isinstance(valor, dict) else {}


def _texto_curto(valor: Any) -> str:
    return " ".join(str(valor).split()) if isinstance(valor, str) else ""


def _entradas_do_documento(d: Documento) -> list[Entrada]:
    """Conceito e Indicador: um termo; Evento de coleta: um termo por item de disambiguation, ou o título."""
    dados, vocabulario = d.dados, _mapa(d.dados.get("vocabulary"))
    if d.type == "evento-coleta":
        itens = [i for i in dados.get("disambiguation") or [] if isinstance(i, dict) and _texto_curto(i.get("term"))]
        if itens:
            return [Entrada(_texto_curto(i.get("term")), _texto_curto(i.get("means")), (),
                            tuple(_lista([i.get("not_to_confuse_with")])), d.rev) for i in itens]
    definicao = _mapa(dados.get("business_definition"))
    termo = _texto_curto(vocabulario.get("prefLabel")) or d.title.split(":")[0].strip()
    resumo = (_texto_curto(dados.get("definition")) or _texto_curto(definicao.get("concept"))
              or _texto_curto(dados.get("plain_summary")))
    sinonimos = _sem_repeticao(_lista(dados.get("synonyms")) + _lista(vocabulario.get("altLabel")))
    evitar = _sem_repeticao(_lista(vocabulario.get("not_synonyms")) + _lista(vocabulario.get("other_domain_meanings"))
                            + _lista(definicao.get("different_meanings_in_other_domains")))
    return [Entrada(termo, resumo, tuple(sinonimos), tuple(evitar), d.rev)]


def _entrada_do_termo(termo: TermoDoKit, documentos: list[Documento]) -> tuple[Entrada | None, str | None]:
    documento = _vigente(documentos, termo.documento)
    if documento is None:
        return None, f"termo {termo.termo!r} cita {termo.documento}, que não tem documento aprovado"
    if documento.type in TIPOS_FORA_DO_GLOSSARIO:
        return None, f"termo {termo.termo!r} cita {documento.rev}, do tipo {documento.type}, que não serve de fonte do glossário"
    return Entrada(termo.termo, termo.resumo, termo.sinonimos, termo.nao_confundir, documento.rev), None


def _formatar(entrada: Entrada) -> str:
    partes = [f"## {entrada.termo}", entrada.resumo]
    if entrada.sinonimos:
        partes.append(f"**Também chamado:** {'; '.join(entrada.sinonimos)}")
    if entrada.nao_confundir:
        partes.append(f"**Não confundir com:** {'; '.join(entrada.nao_confundir)}")
    partes.append(f"**Fonte:** `{entrada.fonte}`")
    return "\n\n".join(p for p in partes if p)


def glossario(documentos: list[Documento], termos: tuple[TermoDoKit, ...] = ()) -> tuple[str, list[str]]:
    """Glossário de conceitos (ADR 0028): termos dos conceitos, indicadores e eventos aprovados e de kit.yaml.

    Devolve o texto e os erros. Gabaritos, rubricas e processos ficam fora.
    """
    entradas: list[Entrada] = []
    for d in documentos:
        if d.status == "approved" and d.type in TIPOS_DO_GLOSSARIO:
            entradas += _entradas_do_documento(d)
    erros = []
    for termo in termos:
        entrada, erro = _entrada_do_termo(termo, documentos)
        if erro:
            erros.append(erro)
        if entrada:
            entradas.append(entrada)
    vistos: dict[str, str] = {}
    for e in entradas:
        chave = e.termo.casefold()
        if chave in vistos:
            erros.append(f"termo {e.termo!r} aparece duas vezes no glossário ({vistos[chave]} e {e.fonte})")
        vistos.setdefault(chave, e.fonte)
    ordenadas = sorted(entradas, key=lambda e: (e.termo.casefold(), e.fonte))
    texto = "\n\n".join(["# Glossário do kit", FRASE_DO_GLOSSARIO] + [_formatar(e) for e in ordenadas]) + "\n"
    return texto, erros


def _indice(arquivos: dict[str, bytes], titulos: dict[str, str]) -> str:
    linhas = []
    for nome in sorted(arquivos, key=lambda n: (n != "glossario.md", n)):
        if nome != "AGENTS.md":
            linhas.append(f"- [{titulos.get(nome, nome)}]({nome})")
    return "\n".join(linhas)


def _referencias(raiz: Path, config: Config, documentos: list[Documento], relatorio: Relatorio) -> tuple[dict[str, bytes], dict[str, str]]:
    arquivos: dict[str, bytes] = {}
    titulos: dict[str, str] = {}
    for skill, ids in config.skills.items():
        fonte = raiz / "src" / "kit" / "skills" / skill / "SKILL.md"
        if not fonte.is_file():
            relatorio.erro(fonte, "SKILL.md não encontrado")
            continue
        erros_da_skill(fonte, skill, relatorio)
        nome = f"skills/{skill}/SKILL.md"
        arquivos[nome], titulos[nome] = fonte.read_bytes(), f"Skill {skill}"
        for id_ in ids:
            documento = _vigente(documentos, id_)
            if documento is None:
                relatorio.erro(raiz / "src/kit/kit.yaml", f"skill {skill} cita {id_}, que não tem documento aprovado")
                continue
            referencia = f"skills/{skill}/references/{documento.rev}.md"
            arquivos[referencia], titulos[referencia] = documento.md, f"{documento.title} ({documento.rev})"
    return arquivos, titulos


def _documentos_do_kit(documentos: list[Documento]) -> tuple[dict[str, bytes], dict[str, str]]:
    arquivos: dict[str, bytes] = {}
    titulos: dict[str, str] = {}
    for d in documentos:
        if d.status == "approved":
            pasta = "gabaritos" if d.type == TIPO_DO_GABARITO else "contratos"
        elif d.status == "superseded":
            pasta = "contratos/historico"
        else:
            continue
        nome = f"{pasta}/{d.rev}.md"
        arquivos[nome], titulos[nome] = d.md, f"{d.title} ({d.rev})"
    return arquivos, titulos


def montar_kit(raiz: Path, config: Config, documentos: list[Documento], relatorio: Relatorio) -> dict[str, bytes] | None:
    """Arquivos do kit (caminho dentro do kit para bytes), ou None com os erros registrados."""
    arquivos, titulos = _documentos_do_kit(documentos)
    texto_do_glossario, erros_do_glossario = glossario(documentos, config.termos)
    for erro in erros_do_glossario:
        relatorio.erro(raiz / "src/kit/kit.yaml", erro)
    arquivos["glossario.md"], titulos["glossario.md"] = texto_do_glossario.encode("utf-8"), "Glossário"
    for nome in config.dados:
        fonte = raiz / "public" / "downloads" / nome
        if not fonte.is_file():
            relatorio.erro(fonte, "arquivo de dados do kit não encontrado")
            continue
        arquivos[f"dados/{nome}"], titulos[f"dados/{nome}"] = fonte.read_bytes(), f"Dados: {nome}"
    extras, extras_titulos = _referencias(raiz, config, documentos, relatorio)
    arquivos.update(extras)
    titulos.update(extras_titulos)
    agents = raiz / "src" / "kit" / "AGENTS.md"
    if not agents.is_file():
        relatorio.erro(agents, "arquivo não encontrado")
        return None
    texto = agents.read_text(encoding="utf-8")
    vezes = texto.count(MARCADOR_INDICE)
    if vezes != 1:
        relatorio.erro(agents, f"o marcador {MARCADOR_INDICE} deve aparecer exatamente uma vez (aparece {vezes})")
        return None
    arquivos["AGENTS.md"] = texto.replace(MARCADOR_INDICE, _indice(arquivos, titulos)).encode("utf-8")
    nomes = set(arquivos)
    for nome in sorted(n for n in nomes if n == "AGENTS.md" or n.endswith("/SKILL.md")):
        for erro in links_quebrados(nome, arquivos[nome].decode("utf-8"), nomes):
            relatorio.erro(None, erro)
    return None if relatorio.erros else arquivos


def montar_zip(pasta: str, arquivos: dict[str, bytes]) -> bytes:
    """Zip determinístico: ordem alfabética, sem compressão, data e permissões fixas."""
    saida = io.BytesIO()
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_STORED) as zip_:
        for nome in sorted(f"{pasta}/{n}" for n in arquivos):
            info = zipfile.ZipInfo(nome, date_time=DATA_FIXA_DO_ZIP)
            info.compress_type, info.create_system = zipfile.ZIP_STORED, 3
            info.external_attr = PERMISSAO_DO_ZIP << 16
            zip_.writestr(info, arquivos[nome[len(pasta) + 1:]])
    return saida.getvalue()


def entradas_do_zip(conteudo: bytes) -> dict[str, bytes] | None:
    """Nome e bytes de cada entrada; None se o conteúdo não for um zip válido."""
    try:
        with zipfile.ZipFile(io.BytesIO(conteudo)) as zip_:
            return {n: zip_.read(n) for n in zip_.namelist()}
    except zipfile.BadZipFile:
        return None
