#!/usr/bin/env python3
"""Converte uma planilha CSV de plano de mensuração em rascunhos de Evento de coleta (I-31).

Uso: python3 scripts/planilha_para_evento.py PLANILHA.csv --saida PASTA [--data AAAA-MM-DD] [--substituir] [--raiz RAIZ]

Cada linha da planilha é um evento em uma operação; linhas com o mesmo Evento formam um documento só.
O rascunho sai sempre em draft, sem aprovação nem vigência. Célula vazia nunca é preenchida: vira
pergunta em aberto. Se houver qualquer erro, nada é escrito.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime
import io
from pathlib import Path
import re
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
import yaml

from check_schemas import _carregar_schemas, _registro, para_json
from comum import HEADER_ORDER, ROOT, Relatorio

COLUNAS = (
    "Evento", "Identificador", "Pergunta de negócio", "Responsável", "Gatilho", "Frequência esperada",
    "Prazo para os dados chegarem", "Data de lançamento", "Consentimento exigido",
    "Indicadores que dependem do evento",
    "Operação", "País", "Marca", "Ativo na operação", "Ativo desde", "Motivo", "Tolerância ao silêncio",
    "Ferramenta de destino", "Onde dentro da ferramenta", "Fuso horário",
)
NIVEL_DO_EVENTO = COLUNAS[:10]
COLUNAS_DE_DATA = ("Data de lançamento", "Ativo desde")
VERDADEIROS = frozenset({"sim", "true"})
FALSOS = frozenset({"não", "nao", "false"})
SCRIPT = "scripts/planilha_para_evento.py"

# coluna: (pergunta, impacto). "{op}" vira a operação da linha.
PERGUNTAS: dict[str, tuple[str, str]] = {
    "Identificador": ("Qual é o identificador do documento do evento {evento}?",
                      "Sem identificador, outros documentos não conseguem citar este evento."),
    "Pergunta de negócio": ("Que pergunta de negócio o evento {evento} ajuda a responder?",
                            "Sem a pergunta, ninguém sabe o que o documento precisa responder."),
    "Responsável": ("Quem responde pelo evento {evento}?",
                    "Sem responsável, as dúvidas sobre o evento não têm a quem ir."),
    "Gatilho": ("Qual ação faz o evento {evento} disparar?",
                "Sem o gatilho, não dá para saber se um zero é falha ou ausência de ação."),
    "Frequência esperada": ("Com que frequência o evento {evento} costuma disparar?",
                            "Sem o ritmo normal, não dá para separar silêncio esperado de falha."),
    "Prazo para os dados chegarem": ("Em quanto tempo os dados do evento {evento} ficam completos?",
                                     "Um dia incompleto pode ser lido como zero e virar alarme falso."),
    "Data de lançamento": ("Em que data o evento {evento} entrou no ar?",
                           "Sem a data, um zero antes do lançamento pode ser lido como falha."),
    "Consentimento exigido": ("Que consentimento o evento {evento} exige para disparar?",
                              "Sem isso, a diferença entre ferramentas pode ser lida como erro de coleta."),
    "Indicadores que dependem do evento": ("Que indicadores dependem do evento {evento}?",
                                           "Sem a lista, não se sabe o que quebra quando o evento falha."),
    "Operação": ("Qual é a operação da linha {linha} do evento {evento}?",
                 "Sem a operação, a linha não diz onde o evento vale."),
    "País": ("Qual é o país da operação {op} no evento {evento}?",
             "Sem o país, a operação {op} fica ambígua."),
    "Marca": ("Qual é a marca da operação {op} no evento {evento}?",
              "Sem a marca, a operação {op} pode ser confundida com outra."),
    "Ativo na operação": ("O evento {evento} está ativo na operação {op}?",
                          "Sem saber, um zero na operação {op} não pode ser julgado."),
    "Ativo desde": ("Desde quando o evento {evento} está ativo na operação {op}?",
                    "Sem a data, um zero antes dela na operação {op} pode ser lido como falha."),
    "Motivo": ("Por que o evento {evento} não está ativo na operação {op}?",
               "Sem o motivo, o zero na operação {op} parece falha e ninguém sabe se é esperado."),
    "Tolerância ao silêncio": ("Quantos dias seguidos sem disparo são aceitos na operação {op} para o evento {evento}?",
                               "Sem a tolerância, não há regra para chamar o evento de quebrado na operação {op}."),
    "Ferramenta de destino": ("Para qual ferramenta o evento {evento} vai na operação {op}?",
                              "Sem a ferramenta, não se sabe onde conferir os disparos da operação {op}."),
    "Onde dentro da ferramenta": ("Em que propriedade, tabela ou contêiner ficam os dados do evento {evento} na operação {op}?",
                                  "Sem o lugar exato, a conferência dos disparos da operação {op} não começa."),
    "Fuso horário": ("Em que fuso horário o dia é contado para o evento {evento} na operação {op}?",
                     "Fusos diferentes dão totais diários diferentes na operação {op}."),
}


@dataclass(frozen=True)
class Linha:
    numero: int
    valores: dict[str, str]


def _chave(texto: str) -> str:
    return texto.strip().casefold()


def nome_do_arquivo(evento: str) -> str:
    return "rascunho-" + re.sub(r"[^a-z0-9_-]", "-", evento.strip().lower()) + ".md"


def _data_iso(texto: str) -> str | None:
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato).date().isoformat()
        except ValueError:
            continue
    return None


def _celula(texto: str) -> str:
    """Valor da célula sem espaços nas pontas; quebra de linha do Windows vira quebra simples."""
    return texto.replace("\r\n", "\n").strip()


def _separador(cabecalho: str) -> str:
    return ";" if cabecalho.count(";") >= cabecalho.count(",") else ","


def ler_linhas(caminho: Path, relatorio: Relatorio) -> list[Linha]:
    """Lê o CSV. Registra erros e avisos com arquivo e linha; devolve as linhas não vazias."""
    try:
        texto = caminho.read_bytes().decode("utf-8-sig")
    except FileNotFoundError:
        relatorio.erro(caminho, "arquivo não encontrado")
        return []
    except UnicodeDecodeError as exc:
        relatorio.erro(caminho, f"o arquivo não está em UTF-8: {exc}")
        return []
    except OSError as exc:
        relatorio.erro(caminho, f"não foi possível ler o arquivo: {exc}")
        return []
    primeira = texto.split("\n", 1)[0]
    # newline="" deixa o csv ler a quebra de linha dentro de uma célula entre aspas (Alt+Enter no Excel).
    leitor = csv.reader(io.StringIO(texto, newline=""), delimiter=_separador(primeira))
    cabecalho = next(leitor, None)
    if not cabecalho:
        relatorio.erro(caminho, "linha 1: o arquivo está vazio ou sem cabeçalho")
        return []
    indices = {_chave(nome): i for i, nome in enumerate(cabecalho)}
    for nome in cabecalho:
        if nome.strip() and _chave(nome) not in {_chave(c) for c in COLUNAS}:
            relatorio.aviso(caminho, f"linha 1: coluna desconhecida {nome.strip()!r} ignorada")
    faltam = [c for c in COLUNAS if _chave(c) not in indices]
    for coluna in faltam:
        relatorio.erro(caminho, f"linha 1: falta a coluna {coluna!r}")
    if faltam:
        return []
    linhas = []
    # O número é o da linha da planilha (como o Excel numera), não o da linha física do arquivo:
    # uma célula com quebra de linha ocupa duas linhas do arquivo e continua sendo uma linha da planilha.
    for numero, celulas in enumerate(leitor, start=2):
        valores = {c: (_celula(celulas[indices[_chave(c)]]) if indices[_chave(c)] < len(celulas) else "")
                   for c in COLUNAS}
        if any(valores.values()):
            linhas.append(Linha(numero, valores))
    return linhas


def _validar_linhas(caminho: Path, linhas: list[Linha], relatorio: Relatorio) -> None:
    for linha in linhas:
        v = linha.valores
        if not v["Evento"]:
            relatorio.erro(caminho, f"linha {linha.numero}: a coluna Evento está vazia")
        for coluna in COLUNAS_DE_DATA:
            if v[coluna] and _data_iso(v[coluna]) is None:
                relatorio.erro(caminho, f"linha {linha.numero}: {coluna} {v[coluna]!r} não é uma data (use DD/MM/AAAA ou AAAA-MM-DD)")
        ativo = v["Ativo na operação"]
        if ativo and _chave(ativo) not in VERDADEIROS | FALSOS:
            relatorio.erro(caminho, f"linha {linha.numero}: Ativo na operação {ativo!r} deve ser sim, não, true ou false")


def _grupos(linhas: list[Linha]) -> dict[str, list[Linha]]:
    grupos: dict[str, list[Linha]] = {}
    for linha in linhas:
        if linha.valores["Evento"]:
            grupos.setdefault(_chave(linha.valores["Evento"]), []).append(linha)
    return grupos


def _normalizado(coluna: str, valor: str) -> str:
    return (_data_iso(valor) or valor) if coluna in COLUNAS_DE_DATA else valor


def _valores_do_evento(caminho: Path, evento: str, grupo: list[Linha], relatorio: Relatorio) -> dict[str, str]:
    """Valor de cada coluna de nível do evento; vazio se nenhuma linha preencheu. Conflito é erro."""
    resultado: dict[str, str] = {}
    for coluna in NIVEL_DO_EVENTO:
        primeira: Linha | None = None
        for linha in grupo:
            valor = linha.valores[coluna]
            if not valor:
                continue
            if primeira is None:
                primeira, resultado[coluna] = linha, valor
            elif _normalizado(coluna, valor) != _normalizado(coluna, resultado[coluna]):
                relatorio.erro(caminho, f"linhas {primeira.numero} e {linha.numero}: {coluna} do evento {evento} "
                                        f"tem valores diferentes ({resultado[coluna]!r} e {valor!r})")
        resultado.setdefault(coluna, "")
    return resultado


def _repeticoes(caminho: Path, evento: str, grupo: list[Linha], relatorio: Relatorio) -> None:
    vistas: dict[str, Linha] = {}
    for linha in grupo:
        operacao = linha.valores["Operação"]
        if not operacao:
            continue
        anterior = vistas.setdefault(_chave(operacao), linha)
        if anterior is not linha:
            relatorio.erro(caminho, f"linhas {anterior.numero} e {linha.numero}: a operação {operacao} aparece duas vezes "
                                    f"no evento {evento}")


def _ou_nulo(texto: str) -> str | None:
    return texto or None


def _perguntas(evento: str, evento_v: dict[str, str], grupo: list[Linha]) -> list[dict[str, Any]]:
    responsavel = _ou_nulo(evento_v["Responsável"])

    def pergunta(texto: str, impacto: str) -> dict[str, Any]:
        return {"question": texto, "impact": impacto, "owner_to_resolve": responsavel,
                "status": "unresolved", "resolution": None}

    achadas = []
    for coluna in NIVEL_DO_EVENTO:
        if not evento_v[coluna]:
            achadas.append(pergunta(*(t.format(evento=evento) for t in PERGUNTAS[coluna])))
    for linha in grupo:
        v = linha.valores
        op = v["Operação"] or f"da linha {linha.numero}"
        for coluna in COLUNAS[10:]:
            if v[coluna]:
                continue
            if coluna == "Motivo" and _chave(v["Ativo na operação"]) in VERDADEIROS:
                continue
            achadas.append(pergunta(*(t.format(evento=evento, op=op, linha=linha.numero) for t in PERGUNTAS[coluna])))
    achadas.append(pergunta(f"Quem aprova o documento do evento {evento}?",
                            "Sem quem aprova, o rascunho não vira regra e os agentes não podem usá-lo."))
    return achadas


def _escopo(v: dict[str, str]) -> dict[str, Any]:
    ativo = _chave(v["Ativo na operação"])
    return {"operation": _ou_nulo(v["Operação"]), "country": _ou_nulo(v["País"]), "brand": _ou_nulo(v["Marca"]),
            "active": True if ativo in VERDADEIROS else False if ativo in FALSOS else None,
            "since": _data_iso(v["Ativo desde"]) if v["Ativo desde"] else None, "reason": _ou_nulo(v["Motivo"])}


def _montar(caminho: Path, evento: str, grupo: list[Linha], data: str, relatorio: Relatorio) -> dict[str, Any]:
    e = _valores_do_evento(caminho, evento, grupo, relatorio)
    _repeticoes(caminho, evento, grupo, relatorio)
    id_ = _ou_nulo(e["Identificador"])
    numeros = [str(linha.numero) for linha in grupo]
    linhas_txt = numeros[0] if len(numeros) == 1 else ", ".join(numeros[:-1]) + " e " + numeros[-1]
    rotulo = "linha" if len(numeros) == 1 else "linhas"
    lancamento = e["Data de lançamento"]
    kpis = [k.strip() for k in e["Indicadores que dependem do evento"].split(",") if k.strip()]
    cabecalho: dict[str, Any] = {
        "id": id_, "schema_version": "1.1.0", "type": "evento-coleta", "title": f"Evento {evento}", "version": "0.1",
        "revision_id": f"{id_}@0.1" if id_ else None, "status": "draft", "owner": _ou_nulo(e["Responsável"]),
        "approver": None, "valid_from": None, "valid_to": None, "version_date": data, "last_reviewed": None,
        "review_interval": None, "source_of_truth": None, "supersedes_revision": None,
        "superseded_by_revision": None, "license": None, "source_url": None,
        "intent": {"question": _ou_nulo(e["Pergunta de negócio"]), "audience": [], "purpose": None, "decisions": []},
        "plain_summary": None, "open_questions": _perguntas(evento, e, grupo),
        "version_history": [{"version": "0.1", "date": data, "approved_by": None,
                             "change": f"Rascunho gerado da planilha {caminho.name}, {rotulo} {linhas_txt}, por {SCRIPT}"}],
    }
    cabecalho["version_history"][0] = {k: cabecalho["version_history"][0][k] for k in ("version", "date", "change", "approved_by")}
    corpo: dict[str, Any] = {
        "trigger": _ou_nulo(e["Gatilho"]), "parameters": [],
        "destination": [{"platform": _ou_nulo(l.valores["Ferramenta de destino"]),
                         "object": _ou_nulo(l.valores["Onde dentro da ferramenta"]),
                         "timezone": _ou_nulo(l.valores["Fuso horário"]), "note": None} for l in grupo],
        "active_scopes": [_escopo(l.valores) for l in grupo],
        "expected_behavior": {
            "expected_frequency": _ou_nulo(e["Frequência esperada"]), "baseline_by_scope": [], "seasonality": None,
            "silence_tolerance": [{"operation": _ou_nulo(l.valores["Operação"]),
                                   "rule": _ou_nulo(l.valores["Tolerância ao silêncio"])} for l in grupo],
            "expected_zero_conditions": []},
        "launch_date": _data_iso(lancamento) if lancamento else None, "retirement_date": None, "renamed_from": [],
        "consent_requirements": _ou_nulo(e["Consentimento exigido"]),
        "late_arrival_window": _ou_nulo(e["Prazo para os dados chegarem"]), "deduplication_key": None,
        "downstream_kpis": kpis, "known_exceptions": [], "validation_query": None, "missing_days_policy": None,
        "grain_note": None, "data_incidents": [], "disambiguation": [], "related_documents": [],
    }
    return {**cabecalho, **corpo}


def erros_no_schema(dados: dict[str, Any], raiz: Path) -> list[str]:
    """Erros do frontmatter no schema evento-coleta de `raiz`/schemas."""
    relatorio = Relatorio()
    schemas = _carregar_schemas(raiz / "schemas", relatorio)
    if "evento-coleta" not in schemas or "common" not in schemas:
        return relatorio.erros + ["schemas evento-coleta e common não encontrados em " + str(raiz / "schemas")]
    validador = Draft202012Validator(schemas["evento-coleta"], registry=_registro(schemas), format_checker=FormatChecker())
    achados = sorted(validador.iter_errors(para_json(dados)), key=lambda e: [str(p) for p in e.absolute_path])
    return [f"{'.'.join(str(p) for p in e.absolute_path) or '(raiz)'}: {e.message}" for e in achados]


def ler_e_montar(caminho: Path, data: str, raiz: Path, relatorio: Relatorio) -> list[dict[str, Any]]:
    """Lê a planilha e devolve os documentos; os erros ficam no relatório. Com erro, a lista pode estar incompleta."""
    linhas = ler_linhas(caminho, relatorio)
    _validar_linhas(caminho, linhas, relatorio)
    documentos = []
    for grupo in _grupos(linhas).values():
        documento = _montar(caminho, grupo[0].valores["Evento"], grupo, data, relatorio)
        for erro in erros_no_schema(documento, raiz):
            relatorio.erro(caminho, f"evento {grupo[0].valores['Evento']}: {erro}")
        documentos.append(documento)
    return documentos


def texto_do_rascunho(documento: dict[str, Any], arquivo: str) -> str:
    frontmatter = yaml.safe_dump(documento, sort_keys=False, allow_unicode=True, width=1000)
    evento = documento["title"]
    corpo = (
        f"Este texto é um rascunho gerado da planilha {arquivo}. Nada foi aprovado: o estado é draft e "
        "quem aprova, a vigência e a aprovação ficam em branco.\n\n"
        "Cada célula vazia da planilha virou uma pergunta em aberto, sem palpite. "
        f"O próximo passo é revisar o {evento} com quem responde pelo evento, resolver as perguntas "
        "e só então pedir a aprovação.\n"
    )
    return f"---\n{frontmatter}---\n\n{corpo}"


def escrever(documentos: list[dict[str, Any]], saida: Path, arquivo: str, substituir: bool, relatorio: Relatorio) -> list[Path]:
    destinos = [(saida / nome_do_arquivo(d["title"].removeprefix("Evento ")), d) for d in documentos]
    for destino, _ in destinos:
        if destino.exists() and not substituir:
            relatorio.erro(destino, "o arquivo já existe; use --substituir para sobrescrever")
    if relatorio.erros:
        return []
    saida.mkdir(parents=True, exist_ok=True)
    for destino, documento in destinos:
        destino.write_text(texto_do_rascunho(documento, arquivo), encoding="utf-8")
    return [d for d, _ in destinos]


def _data_do_argumento(texto: str) -> str:
    try:
        return date.fromisoformat(texto).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(f"data inválida {texto!r}; use AAAA-MM-DD") from None


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Converte uma planilha de plano de mensuração em rascunhos de Evento de coleta.")
    ap.add_argument("planilha", type=Path)
    ap.add_argument("--saida", type=Path, required=True)
    ap.add_argument("--data", type=_data_do_argumento, default=date.today().isoformat())
    ap.add_argument("--substituir", action="store_true")
    ap.add_argument("--raiz", type=Path, default=ROOT)
    args = ap.parse_args(argv)
    relatorio = Relatorio()
    if argv is None:
        relatorio.instalar()
    documentos = ler_e_montar(args.planilha, args.data, args.raiz, relatorio)
    if not relatorio.erros and not documentos:
        relatorio.erro(args.planilha, "nenhuma linha com dados na planilha")
    escritos = [] if relatorio.erros else escrever(documentos, args.saida, args.planilha.name, args.substituir, relatorio)
    relatorio.encerrar(f"OK: {len(escritos)} rascunho(s) em {args.saida}: " + ", ".join(p.name for p in escritos))


if __name__ == "__main__":
    main()
