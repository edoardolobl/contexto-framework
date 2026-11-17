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


def carregar_tipos(caminho: Path, relatorio: Relatorio) -> list[str]:
    """Lê os slugs de src/data/modelos.yaml, validando slug, nível e unicidade."""
    dados = carregar_yaml(caminho, relatorio)
    if dados is None:
        return []
    brutos = dados.get("tipos")
    if not isinstance(brutos, list) or not brutos:
        relatorio.erro(caminho, "nenhum tipo de documento encontrado")
        return []
    slugs: list[str] = []
    for numero, item in enumerate(brutos, start=1):
        slug = item.get("slug") if isinstance(item, dict) else None
        if not isinstance(slug, str) or not slug:
            relatorio.erro(caminho, f"tipo {numero} sem slug")
            continue
        if item.get("nivel") not in NIVEIS_DE_TIPO:
            relatorio.erro(caminho, f"tipo {slug} com nível inválido: {item.get('nivel')!r}")
        if slug in slugs:
            relatorio.erro(caminho, f"slug repetido: {slug}")
            continue
        slugs.append(slug)
    return slugs
