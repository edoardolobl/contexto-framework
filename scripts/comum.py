"""Peças comuns dos validadores do Contexto.

Todo validador lê arquivos do repositório, junta os erros e termina com código 1 se houver algum.
Este módulo concentra essas três coisas para que nenhum script morra com traceback quando um YAML
está vazio, quebrado ou sem um campo esperado: a falha vira uma linha "ERRO:" com o arquivo.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys
import traceback
import unicodedata
from types import TracebackType
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "src" / "content" / "docs"
DOWNLOADS = ROOT / "public" / "downloads"
DADOS = ROOT / "src" / "data"
ESTADOS_DO_DOCUMENTO = frozenset({"draft", "pending_approval", "approved", "superseded", "deprecated"})
ESTADOS_JA_APROVADOS = frozenset({"approved", "superseded"})
HEADER_ORDER = (
    "id", "schema_version", "type", "title", "version", "revision_id", "status", "owner", "approver",
    "valid_from", "valid_to", "recorded_at", "version_date", "last_reviewed", "review_interval",
    "source_of_truth", "supersedes_revision", "superseded_by_revision", "license", "source_url", "intent", "plain_summary",
    "open_questions", "version_history",
)
REPOSITORIO = "github.com/edoardolobl/contexto-framework"
_LINK_DO_REPOSITORIO = re.compile(re.escape(REPOSITORIO) + r"/(?:blob|tree)/main/([^\s)\"'#?<>]+)")


@dataclass
class Relatorio:
    """Junta os erros de um validador e decide o código de saída."""

    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)
    arquivo_atual: Path | None = None

    def erro(self, caminho: Path | None, mensagem: str) -> None:
        texto = f"{relativo(caminho)}: {mensagem}" if caminho else mensagem
        if texto not in self.erros:
            self.erros.append(texto)

    def aviso(self, caminho: Path | None, mensagem: str) -> None:
        """Registra um aviso: aparece na saída, mas não muda o código de saída."""
        texto = f"{relativo(caminho)}: {mensagem}" if caminho else mensagem
        if texto not in self.avisos:
            self.avisos.append(texto)

    def encerrar(self, mensagem_ok: str) -> None:
        if self.avisos:
            print("\n".join("AVISO: " + aviso for aviso in self.avisos))
        if self.erros:
            print("\n".join("ERRO: " + erro for erro in self.erros))
            sys.exit(1)
        print(mensagem_ok)

    def instalar(self) -> None:
        """Troca o traceback de uma falha inesperada por uma linha de erro legível."""

        def gancho(tipo: type[BaseException], valor: BaseException, _tb: TracebackType | None) -> None:
            if issubclass(tipo, KeyboardInterrupt):
                sys.__excepthook__(tipo, valor, _tb)
                return
            partes = []
            if self.arquivo_atual:
                partes.append(f"último arquivo lido: {relativo(self.arquivo_atual)}")
            quadros = traceback.extract_tb(_tb) if _tb else []
            if quadros:
                partes.append(f"em {relativo(Path(quadros[-1].filename))}:{quadros[-1].lineno}")
            onde = f" ({'; '.join(partes)})" if partes else ""
            self.erros.append(f"falha inesperada{onde}: {tipo.__name__} {valor}")
            print("\n".join("ERRO: " + erro for erro in self.erros))
            sys.exit(1)

        sys.excepthook = gancho



def links_do_repositorio_ausentes(texto: str, raiz: Path) -> list[str]:
    """Caminhos citados em links blob/main ou tree/main do repositório que não existem em `raiz`.

    O portal aponta para arquivos do repositório (ADRs, plano de validação). Se o arquivo não
    existe na cópia local, o link publicado leva a uma página 404 no GitHub.
    """
    caminhos = dict.fromkeys(m.rstrip("/.,;") for m in _LINK_DO_REPOSITORIO.findall(texto))
    return [c for c in caminhos if not (raiz / c).exists()]


def relativo(caminho: Path | None) -> str:
    if caminho is None:
        return ""
    try:
        return caminho.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(caminho)


def carregar_yaml(caminho: Path, relatorio: Relatorio) -> dict[str, Any] | None:
    """Lê um YAML que deve ter um mapa na raiz. Devolve None e registra o erro se não tiver."""
    relatorio.arquivo_atual = caminho
    try:
        dados = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    except FileNotFoundError:
        relatorio.erro(caminho, "arquivo não encontrado")
        return None
    except yaml.YAMLError as exc:
        relatorio.erro(caminho, f"YAML inválido: {exc}")
        return None
    except UnicodeDecodeError as exc:
        relatorio.erro(caminho, f"o arquivo não está em UTF-8: {exc}")
        return None
    except ValueError as exc:
        relatorio.erro(caminho, f"valor impossível no YAML (data inválida?): {exc}")
        return None
    except OSError as exc:
        relatorio.erro(caminho, f"não foi possível ler o arquivo: {exc}")
        return None
    if not isinstance(dados, dict):
        relatorio.erro(caminho, "YAML deve ter um mapa na raiz")
        return None
    return dados


def ler_frontmatter(caminho: Path, relatorio: Relatorio) -> tuple[dict[str, Any], str, str] | None:
    """Lê um .md com frontmatter. Devolve (dados, texto do frontmatter, corpo) ou None com o erro registrado.

    Linha 1 é '---'; o frontmatter vai até a próxima linha que é só '---'.
    """
    relatorio.arquivo_atual = caminho
    try:
        bruto = caminho.read_bytes().decode("utf-8")
    except FileNotFoundError:
        relatorio.erro(caminho, "arquivo não encontrado")
        return None
    except UnicodeDecodeError as exc:
        relatorio.erro(caminho, f"o arquivo não está em UTF-8: {exc}")
        return None
    except OSError as exc:
        relatorio.erro(caminho, f"não foi possível ler o arquivo: {exc}")
        return None
    linhas = bruto.replace("\r\n", "\n").split("\n")
    if linhas[0] != "---":
        relatorio.erro(caminho, "frontmatter ausente (a primeira linha deve ser ---)")
        return None
    fim = next((i for i in range(1, len(linhas)) if linhas[i] == "---"), None)
    if fim is None:
        relatorio.erro(caminho, "frontmatter não fechado (falta a linha --- depois do YAML)")
        return None
    texto, corpo = "\n".join(linhas[1:fim]), "\n".join(linhas[fim + 1:])
    try:
        dados = yaml.safe_load(texto)
    except yaml.YAMLError as exc:
        relatorio.erro(caminho, f"frontmatter com YAML inválido: {exc}")
        return None
    except ValueError as exc:
        relatorio.erro(caminho, f"frontmatter com valor impossível (data inválida?): {exc}")
        return None
    if not isinstance(dados, dict):
        relatorio.erro(caminho, "frontmatter deve ser um mapa YAML")
        return None
    return dados, texto, corpo


def exigir_minimo(itens: Iterable[Path], minimo: int, descricao: str, relatorio: Relatorio) -> list[Path]:
    """Falha se uma busca de arquivos voltar com menos itens do que o esperado.

    Sem isso, uma pasta movida ou renomeada faz o validador imprimir OK sem ter lido nada.
    """
    lista = sorted(itens)
    if len(lista) < minimo:
        relatorio.erro(None, f"esperado pelo menos {minimo} {descricao}, encontrado {len(lista)}")
    return lista


NIVEIS_DE_TIPO = {"nucleo", "segundo", "complementar"}


@dataclass(frozen=True)
class Regra:
    """Uma regra do vocabulário: o padrão proibido, o termo preferido e onde a variante é permitida."""

    padrao: str
    sugestao: str
    flags: int
    permitido_em: tuple[str, ...]


def _regra_de(item: Any, numero: int, caminho: Path, relatorio: Relatorio) -> Regra | None:
    def falha(motivo: str) -> None:
        relatorio.erro(caminho, f"regra {numero} {motivo}")

    if not isinstance(item, dict):
        falha("não é um mapa")
        return None
    padrao, sugestao = item.get("padrao"), item.get("sugestao")
    if not isinstance(padrao, str) or not padrao:
        falha("sem padrao")
        return None
    if not isinstance(sugestao, str) or not sugestao.strip():
        falha("sem sugestao")
        return None
    if any(unicodedata.category(c) == "Cc" for c in padrao):
        falha("tem caractere de controle no padrao (use aspas simples no YAML para preservar a barra invertida)")
        return None
    try:
        re.compile(padrao)
    except re.error as exc:
        falha(f"tem expressão inválida no padrao: {exc}")
        return None
    ignorar = item.get("ignorar_maiusculas", False)
    if not isinstance(ignorar, bool):
        falha("tem ignorar_maiusculas que deve ser true ou false")
        return None
    permitido = item.get("permitido_em", [])
    if permitido is None:
        permitido = []
    if not isinstance(permitido, list) or not all(isinstance(p, str) for p in permitido):
        falha("tem permitido_em que deve ser uma lista de caminhos")
        return None
    return Regra(padrao, sugestao, re.I if ignorar else 0, tuple(permitido))


def carregar_vocabulario(caminho: Path, relatorio: Relatorio) -> list[Regra]:
    """Lê src/data/vocabulario.yaml. Regra malformada vira erro e é descartada."""
    dados = carregar_yaml(caminho, relatorio)
    if dados is None:
        return []
    brutas = dados.get("regras")
    if not isinstance(brutas, list):
        brutas = []
    regras = [r for n, item in enumerate(brutas, start=1) if (r := _regra_de(item, n, caminho, relatorio))]
    if not brutas:
        relatorio.erro(caminho, "nenhuma regra de vocabulário encontrada")
    return regras


@dataclass(frozen=True)
class Modelo:
    """Um tipo de documento de src/data/modelos.yaml (fonte única dos modelos)."""

    slug: str
    pagina: str
    nome: str
    nivel: str
    tarefa: str
    resumo: str
    quando: str
    resultado: str
    preparar: str
    rotulo_download: str


@dataclass(frozen=True)
class Passo:
    numero: int
    pagina: str
    titulo: str


@dataclass(frozen=True)
class Percurso:
    passos: tuple[Passo, ...]
    depois_do_ultimo: str
    titulo_depois: str = ""


@dataclass(frozen=True)
class Entrada:
    sintoma: str
    texto: str
    pagina: str
    provisorio: bool
    nota: str


@dataclass(frozen=True)
class Dimensao:
    nome: str
    pergunta: str
    revisao: str
    resposta_fraca: str
    resposta_util: str
    onde_procurar: str
    metadado_comum: str | None


CAMPOS_DE_TEXTO_DO_MODELO = ("nome", "tarefa", "resumo", "quando", "resultado", "preparar", "rotulo_download")
CAMPOS_DA_DIMENSAO = ("nome", "pergunta", "revisao", "resposta_fraca", "resposta_util", "onde_procurar")
METADADOS_COMUNS = {"escopo", "vigência", "evidência", "responsável"}
TOTAL_DE_DIMENSOES = 8


def _texto(item: dict[str, Any], campo: str) -> str | None:
    valor = item.get(campo)
    return valor.strip() if isinstance(valor, str) and valor.strip() else None


def _lista_da_raiz(caminho: Path, chave: str, vazio: str, relatorio: Relatorio) -> list[Any]:
    dados = carregar_yaml(caminho, relatorio)
    if dados is None:
        return []
    brutos = dados.get(chave)
    if not isinstance(brutos, list) or not brutos:
        relatorio.erro(caminho, vazio)
        return []
    return brutos


def _modelo_de(item: Any, numero: int, caminho: Path, relatorio: Relatorio) -> Modelo | None:
    slug = _texto(item, "slug") if isinstance(item, dict) else None
    if slug is None or not isinstance(item, dict):
        relatorio.erro(caminho, f"tipo {numero} sem slug")
        return None
    textos = {campo: _texto(item, campo) for campo in CAMPOS_DE_TEXTO_DO_MODELO}
    faltando = [campo for campo, valor in textos.items() if valor is None]
    for campo in faltando:
        relatorio.erro(caminho, f"tipo {slug} sem {campo} (texto obrigatório)")
    if item.get("nivel") not in NIVEIS_DE_TIPO:
        relatorio.erro(caminho, f"tipo {slug} com nível inválido: {item.get('nivel')!r}")
        return None
    pagina = item.get("pagina", slug)
    if not isinstance(pagina, str) or not pagina.strip():
        relatorio.erro(caminho, f"tipo {slug} com pagina inválida: {pagina!r}")
        return None
    if faltando:
        return None
    return Modelo(slug=slug, pagina=pagina.strip(), nivel=item["nivel"], **{c: v or "" for c, v in textos.items()})


def carregar_modelos(caminho: Path, relatorio: Relatorio) -> list[Modelo]:
    """Lê src/data/modelos.yaml. Tipo malformado vira erro (com o slug) e é descartado."""
    brutos = _lista_da_raiz(caminho, "tipos", "nenhum tipo de documento encontrado", relatorio)
    modelos: list[Modelo] = []
    slugs: set[str] = set()
    paginas: set[str] = set()
    for numero, item in enumerate(brutos, start=1):
        slug = item.get("slug") if isinstance(item, dict) else None
        if isinstance(slug, str) and slug in slugs:
            relatorio.erro(caminho, f"slug repetido: {slug}")
            continue
        modelo = _modelo_de(item, numero, caminho, relatorio)
        if isinstance(slug, str):
            slugs.add(slug)
        if modelo is None:
            continue
        if modelo.pagina in paginas:
            relatorio.erro(caminho, f"pagina repetida: {modelo.pagina} (tipo {modelo.slug})")
            continue
        paginas.add(modelo.pagina)
        modelos.append(modelo)
    return modelos


def carregar_tipos(caminho: Path, relatorio: Relatorio) -> list[str]:
    """Slugs dos modelos válidos de src/data/modelos.yaml (invólucro de carregar_modelos)."""
    return [m.slug for m in carregar_modelos(caminho, relatorio)]


def _passo_de(item: Any, numero: int, caminho: Path, relatorio: Relatorio) -> Passo | None:
    if not isinstance(item, dict):
        relatorio.erro(caminho, f"passo {numero} não é um mapa")
        return None
    ordem, pagina, titulo = item.get("numero"), _texto(item, "pagina"), _texto(item, "titulo")
    if isinstance(ordem, bool) or not isinstance(ordem, int):
        relatorio.erro(caminho, f"passo {numero} com numero inválido: {ordem!r}")
        return None
    for campo, valor in (("pagina", pagina), ("titulo", titulo)):
        if valor is None:
            relatorio.erro(caminho, f"passo {numero} sem {campo}")
    return Passo(ordem, pagina, titulo) if pagina and titulo else None


def carregar_percurso(caminho: Path, relatorio: Relatorio) -> Percurso:
    """Lê src/data/percurso.yaml: passos 1..N contínuos, páginas únicas, depois_do_ultimo obrigatório."""
    vazio = Percurso((), "")
    dados = carregar_yaml(caminho, relatorio)
    if dados is None:
        return vazio
    brutos = dados.get("passos")
    if not isinstance(brutos, list) or not brutos:
        relatorio.erro(caminho, "nenhum passo do percurso encontrado")
        return vazio
    passos = [p for n, item in enumerate(brutos, start=1) if (p := _passo_de(item, n, caminho, relatorio))]
    if [p.numero for p in passos] != list(range(1, len(brutos) + 1)):
        relatorio.erro(caminho, "numeração dos passos deve ser 1..N contínua e em ordem")
    for pagina in dict.fromkeys(p.pagina for p in passos if [q.pagina for q in passos].count(p.pagina) > 1):
        relatorio.erro(caminho, f"página repetida no percurso: {pagina}")
    bruto = dados.get("depois_do_ultimo")
    depois = _texto(bruto, "pagina") if isinstance(bruto, dict) else (bruto.strip() if isinstance(bruto, str) else "")
    if not depois:
        relatorio.erro(caminho, "depois_do_ultimo é obrigatório (texto ou mapa com pagina e titulo)")
    titulo = (_texto(bruto, "titulo") if isinstance(bruto, dict) else None) or ""
    return Percurso(tuple(passos), depois or "", titulo)


def _entrada_de(item: Any, numero: int, caminho: Path, relatorio: Relatorio) -> Entrada | None:
    if not isinstance(item, dict):
        relatorio.erro(caminho, f"entrada {numero} não é um mapa")
        return None
    textos = {campo: _texto(item, campo) for campo in ("sintoma", "texto", "pagina")}
    for campo, valor in textos.items():
        if valor is None:
            relatorio.erro(caminho, f"entrada {numero} sem {campo}")
    provisorio, nota = item.get("provisorio", False), _texto(item, "nota")
    if not isinstance(provisorio, bool):
        relatorio.erro(caminho, f"entrada {numero} com provisorio que deve ser true ou false")
        return None
    if provisorio and nota is None:
        relatorio.erro(caminho, f"entrada {numero} provisória sem nota")
        return None
    if None in textos.values():
        return None
    return Entrada(textos["sintoma"] or "", textos["texto"] or "", textos["pagina"] or "", provisorio, nota or "")


def carregar_entradas(caminho: Path, relatorio: Relatorio) -> list[Entrada]:
    """Lê src/data/entradas.yaml (porta de entrada por sintoma). Sintoma repetido vira erro; a página pode repetir."""
    brutos = _lista_da_raiz(caminho, "entradas", "nenhuma entrada encontrada", relatorio)
    entradas: list[Entrada] = []
    for numero, item in enumerate(brutos, start=1):
        entrada = _entrada_de(item, numero, caminho, relatorio)
        if entrada is None:
            continue
        if any(e.sintoma == entrada.sintoma for e in entradas):
            relatorio.erro(caminho, f"sintoma repetido: {entrada.sintoma}")
        else:
            entradas.append(entrada)
    return entradas


def _dimensao_de(item: Any, numero: int, caminho: Path, relatorio: Relatorio) -> Dimensao | None:
    if not isinstance(item, dict):
        relatorio.erro(caminho, f"dimensão {numero} não é um mapa")
        return None
    nome = _texto(item, "nome") or f"#{numero}"
    textos = {campo: _texto(item, campo) for campo in CAMPOS_DA_DIMENSAO}
    for campo, valor in textos.items():
        if valor is None:
            relatorio.erro(caminho, f"dimensão {nome} sem {campo}")
    metadado = item.get("metadado_comum")
    if metadado is not None and metadado not in METADADOS_COMUNS:
        relatorio.erro(caminho, f"dimensão {nome} com metadado_comum inválido: {metadado!r} (use {', '.join(sorted(METADADOS_COMUNS))})")
        return None
    if None in textos.values():
        return None
    return Dimensao(metadado_comum=metadado, **{c: v or "" for c, v in textos.items()})


def carregar_dimensoes(caminho: Path, relatorio: Relatorio) -> list[Dimensao]:
    """Lê src/data/dimensoes.yaml: exatamente 8 dimensões (ADR 0014), nomes únicos."""
    brutos = _lista_da_raiz(caminho, "dimensoes", "nenhuma dimensão encontrada", relatorio)
    if brutos and len(brutos) != TOTAL_DE_DIMENSOES:
        relatorio.erro(caminho, f"esperadas exatamente {TOTAL_DE_DIMENSOES} dimensões, encontradas {len(brutos)}")
    dimensoes: list[Dimensao] = []
    for numero, item in enumerate(brutos, start=1):
        dimensao = _dimensao_de(item, numero, caminho, relatorio)
        if dimensao is None:
            continue
        if any(d.nome == dimensao.nome for d in dimensoes):
            relatorio.erro(caminho, f"nome repetido: {dimensao.nome}")
        else:
            dimensoes.append(dimensao)
    return dimensoes


def rota_da_pagina(path: Path, docs: Path) -> str:
    """Rota publicada de uma página de `docs`: a/b.mdx vira /a/b/ e a/index.mdx vira /a/."""
    partes = list(path.relative_to(docs).parts)
    partes[-1] = path.stem
    if partes[-1] == "index":
        partes.pop()
    return "/" + "/".join(partes) + ("/" if partes else "")


_EXTERNO = re.compile(r"^(https?:|mailto:|#|/)")
_ARQUIVO_PUBLICADO = (".yaml", ".md", ".pdf")
_EXTENSOES_PUBLICADAS = (".json", ".zip", ".txt", ".md", ".yaml", ".sql", ".pdf", ".csv")


def _sem_ancora(url: str) -> str:
    return url.split("#")[0].split("?")[0]


def arquivo_de_download(url: str) -> str | None:
    """Caminho relativo a downloads/ se o link aponta para um download publicado (yaml, md ou pdf), senão None."""
    limpo = _sem_ancora(url)
    if _EXTERNO.match(url) or "downloads" not in limpo or not limpo.endswith(_ARQUIVO_PUBLICADO):
        return None
    if "downloads/" in limpo:
        return limpo.split("downloads/", 1)[1]
    return Path(limpo).name


def arquivo_publicado(rota_origem: str, url: str) -> str | None:
    """Caminho relativo a public/ se o link relativo aponta para um arquivo publicado, senão None.

    Resolve como o navegador. Link externo, âncora, endereço absoluto, chaves de modelo, rota que
    termina em barra e link que sobe além da raiz do site não são arquivo publicado.
    """
    limpo = _sem_ancora(url)
    if _EXTERNO.match(url) or not limpo or "{" in limpo or "}" in limpo or limpo.endswith("/"):
        return None
    if not limpo.lower().endswith(_EXTENSOES_PUBLICADAS):
        return None
    segmentos = [s for s in rota_origem.strip("/").split("/") if s]
    for parte in limpo.split("/"):
        if parte in ("", "."):
            continue
        if parte != "..":
            segmentos.append(parte)
        elif segmentos:
            segmentos.pop()
        else:
            return None
    return "/".join(segmentos)


def arquivo_publicado_ausente(rota_origem: str, url: str, publico: Path) -> str | None:
    """Caminho relativo a public/ se o link aponta para um arquivo publicado que não existe em `publico`."""
    caminho = arquivo_publicado(rota_origem, url)
    return caminho if caminho and not (publico / caminho).is_file() else None


def resolver_link(rota_origem: str, url: str) -> tuple[str | None, bool]:
    """Resolve um link relativo como o navegador faria.

    Devolve (rota, subiu_alem_da_raiz). A rota é None para link externo, âncora, endereço absoluto,
    download, arquivo publicado (ver arquivo_publicado) ou link com chaves de modelo. Subir além da raiz do site dá 404 no GitHub Pages.
    """
    limpo = _sem_ancora(url)
    if _EXTERNO.match(url) or not limpo or "{" in limpo or "}" in limpo or arquivo_de_download(url):
        return None, False
    if arquivo_publicado(rota_origem, url):
        return None, False
    segmentos = [s for s in rota_origem.strip("/").split("/") if s]
    subiu = False
    for parte in limpo.split("/"):
        if parte in ("", "."):
            continue
        if parte == "..":
            if not segmentos:
                subiu = True
                continue
            segmentos.pop()
        else:
            segmentos.append(parte)
    return ("/" + "/".join(segmentos) + "/" if segmentos else "/"), subiu


# ---------- regras puras do validate_content ----------

REFERENCE_FIELDS = ("related_documents", "covered_documents", "metrics", "decision_rules",
                    "reference_questions", "valid_join_paths", "expected_questions_and_answers")


def ids_citados(data: dict[str, Any]) -> Iterable[str]:
    """Cada id de documento citado por um exemplo, onde quer que a convenção permita."""
    for campo in REFERENCE_FIELDS:
        for valor in data.get(campo) or []:
            if isinstance(valor, str):
                yield valor
    depende = data.get("depends_on_versions")
    if isinstance(depende, dict):
        for chave in depende:
            if isinstance(chave, str):
                yield chave
    fontes = data.get("data_sources") or {}
    for valor in fontes.get("valid_join_paths") or []:
        yield valor
    if isinstance(fontes.get("authoritative_dataset"), str):
        yield fontes["authoritative_dataset"]
    validacao = data.get("validation") or {}
    for valor in validacao.get("expected_questions_and_answers") or []:
        if isinstance(valor, str):
            yield valor
    for pergunta in data.get("questions") or []:
        for valor in pergunta.get("required_sources") or []:
            yield valor


def faltas_de_leitura(data: dict[str, Any]) -> list[str]:
    """Campos de leitura que um exemplo completo precisa trazer preenchidos (I-16)."""
    intent = data.get("intent")
    pergunta = intent.get("question") if isinstance(intent, dict) else None
    resumo = data.get("plain_summary")
    faltas = []
    if not isinstance(pergunta, str) or not pergunta.strip():
        faltas.append("intent.question")
    if not isinstance(resumo, str) or not resumo.strip():
        faltas.append("plain_summary")
    return faltas


def erros_do_markdown_de_download(nome: str, conteudo: str) -> list[str]:
    """Regras de um .md da raiz de downloads: modelo começa com frontmatter; todos têm as duas seções."""
    erros = []
    if nome.startswith("template-") and not conteudo.startswith("---"):
        erros.append("modelo Markdown deve começar com frontmatter (ADR 0006)")
    for titulo in ("## Identificação", "## Histórico de versões"):
        if titulo not in conteudo:
            erros.append(f"template Markdown sem a seção {titulo}")
    return erros
