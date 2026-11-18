#!/usr/bin/env python3
"""Validador do Lab 2 Aurora: refaz no SQLite as contas citadas e confere os textos que as repetem.

Confere o limite fixo da amostra, a regra canônica de evento quebrado (lida de um YAML), a consulta
de referência, o gabarito "quais eventos pararam?", a consulta de receita, o KPI-AURORA-002, as Q03 e Q06 e a página e os documentos do evento.
Não chama nenhum modelo de IA e não avalia nenhum (ADR 0022). Funções puras no topo; `executar` junta
tudo e `main` imprime o resultado.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
import re
import sqlite3
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import ROOT, Relatorio, carregar_yaml, ler_frontmatter  # noqa: E402

CONSULTA = "2026-11-17"
ATRASO_EM_DIAS = 2
ARQUIVO_AMOSTRA = "aurora-lab2-fixture.sql"
ARQUIVO_CONSULTA = "aurora-lab2-reference-query.sql"
ARQUIVO_REGRA = "exemplo-decisao-evento-quebrado-completo.yaml"
ARQUIVO_GABARITO = "exemplo-perguntas-de-negocio-eventos-completo.yaml"
ARQUIVO_EVENTO = "exemplo-evento-coleta-completo.yaml"
ARQUIVO_RECEITA = "aurora-lab2-receita-purchase.sql"
FONTE_KPI_RECEITA = Path("src/exemplos/exemplo-kpi-receita-purchase-completo.md")
FONTE_GABARITO = Path("src/exemplos/exemplo-perguntas-de-negocio-eventos-completo.md")
ID_KPI_RECEITA, VERSAO_KPI_RECEITA = "KPI-AURORA-002", "1.0"
PAGINA = Path("src/content/docs/exemplos/laboratorio-eventos.mdx")
PAGINA_MODELO = Path("src/content/docs/templates/evento-coleta.mdx")
OPERACOES = {"BR", "MX"}
EVENTOS = {"add_to_cart", "purchase", "generate_lead"}
PRIMEIRO_DIA, ULTIMO_DIA, DIA_INCOMPLETO = "2026-10-20", "2026-11-16", "2026-11-16"
TOTAL_DE_DIAS = 28
CANDIDATO = ("add_to_cart", "MX")
LEAD_BR = ("generate_lead", "BR")
LEAD_MX = ("generate_lead", "MX")
DIA_DO_PEDIDO = "2026-11-02"
RECEITA_CERTA, RECEITA_INFLADA = 500, 1100
COMPORTAMENTOS = {"Q01": "answer", "Q02": "answer", "Q03": "clarify", "Q04": "abstain", "Q05": "abstain", "Q06": "answer"}
ENTRADAS = ("active_in_scope", "ingestion_complete", "expected_in_window",
            "deviation_streak_reached", "known_exception_applies")


# ---------- funções puras ----------
def dias_completos(db: sqlite3.Connection, operacao: str, consulta: str, atraso: int = ATRASO_EM_DIAS) -> list[str]:
    """Dias com carga completa de uma operação, até `atraso` dias antes da consulta (regra D+2)."""
    limite = (date.fromisoformat(consulta) - timedelta(days=atraso)).isoformat()
    linhas = db.execute("SELECT event_date FROM lab2_carga WHERE operation=? AND is_complete=1 AND event_date<=? "
                        "ORDER BY event_date", (operacao, limite))
    return [linha[0] for linha in linhas]


def contagens_do_par(db: sqlite3.Connection, evento: str, operacao: str) -> dict[str, int]:
    """Disparos por dia de um evento numa operação; dia sem linha não aparece."""
    linhas = db.execute("SELECT event_date, event_count FROM lab2_eventos_diarios WHERE event_name=? AND operation=?",
                        (evento, operacao))
    return {dia: total for dia, total in linhas}


def sequencia_atual_zero(dias: list[str], contagens: dict[str, int]) -> int:
    """Dias completos seguidos em zero até o último dia; falta de linha conta como zero."""
    total = 0
    for dia in reversed(dias):
        if contagens.get(dia, 0) > 0:
            break
        total += 1
    return total


def maior_sequencia_zero(dias: list[str], contagens: dict[str, int]) -> int:
    """Maior número de dias completos seguidos em zero em toda a janela."""
    maior = atual = 0
    for dia in dias:
        atual = atual + 1 if contagens.get(dia, 0) == 0 else 0
        maior = max(maior, atual)
    return maior


def periodo_da_maior_sequencia(dias: list[str], contagens: dict[str, int]) -> tuple[str, str] | None:
    """Primeiro e último dia da maior sequência em zero; a primeira vence em caso de empate; None se não há zero."""
    melhor: tuple[str, str] | None = None
    maior = atual = 0
    for indice, dia in enumerate(dias):
        atual = atual + 1 if contagens.get(dia, 0) == 0 else 0
        if atual > maior:
            maior, melhor = atual, (dias[indice - atual + 1], dia)
    return melhor


def resumo_da_janela(dias: list[str], contagens: dict[str, int]) -> tuple[float, int]:
    """Média diária de disparos e quantidade de dias em zero na janela."""
    if not dias:
        return 0.0, 0
    valores = [contagens.get(dia, 0) for dia in dias]
    return sum(valores) / len(valores), sum(1 for valor in valores if valor == 0)


def classificar(entradas: dict[str, Any], tabela: list[dict[str, Any]]) -> str | None:
    """Resultado da única linha da tabela de decisão que vale; None se nenhuma ou mais de uma valer."""
    achadas = []
    for linha in tabela:
        quando = linha.get("when")
        if not isinstance(quando, dict):
            continue
        if all(nome in entradas and (valor == "any" or valor == entradas[nome]) for nome, valor in quando.items()):
            achadas.append(linha.get("then"))
    return achadas[0] if len(achadas) == 1 else None


def receita_certa(db: sqlite3.Connection, operacao: str, dia: str) -> int:
    """Receita dos pedidos do dia, somada na tabela de pedidos."""
    return db.execute("SELECT COALESCE(SUM(revenue), 0) FROM lab2_pedidos WHERE operation=? AND order_date=?",
                      (operacao, dia)).fetchone()[0]


def receita_apos_juncao(db: sqlite3.Connection, operacao: str, dia: str) -> int:
    """Receita somada depois de juntar pedidos com itens: cada pedido repete uma vez por item (fan-out)."""
    return db.execute("SELECT COALESCE(SUM(p.revenue), 0) FROM lab2_pedidos AS p JOIN lab2_itens AS i "
                      "ON i.order_id=p.order_id WHERE p.operation=? AND p.order_date=?", (operacao, dia)).fetchone()[0]


def formatar_decimal(valor: float) -> str:
    return f"{valor:.1f}".replace(".", ",")


def formatar_decimal_curto(valor: float) -> str:
    """Como formatar_decimal, sem a casa decimal quando ela é zero: 30,0 vira 30."""
    texto = formatar_decimal(valor)
    return texto[:-2] if texto.endswith(",0") else texto


def formatar_periodo(inicio: str, fim: str) -> str:
    """Período em dias completos como as páginas escrevem: 27 a 29/10, 14 e 15/11, 30/10 a 02/11, 11/11."""
    a, b = date.fromisoformat(inicio), date.fromisoformat(fim)
    if a == b:
        return f"{b:%d/%m}"
    conector = " e " if (b - a).days == 1 else " a "
    primeiro = f"{a:%d}" if a.month == b.month else f"{a:%d/%m}"
    return f"{primeiro}{conector}{b:%d/%m}"


def formatar_reais(valor: int) -> str:
    return "R$ " + f"{valor:,}".replace(",", ".")


# ---------- números do par evento e operação ----------
@dataclass(frozen=True)
class Par:
    evento: str
    operacao: str
    ativo: bool
    dias: int
    dias_em_zero: int
    media: float
    total: int
    maior_sequencia: int
    sequencia_atual: int
    ultimo_disparo: str | None
    entradas: dict[str, Any]
    periodo_maior: tuple[str, str] | None = None
    periodo_atual: tuple[str, str] | None = None


def calcular_par(db: sqlite3.Connection, plano: tuple[str, str, int, str, int], consulta: str) -> Par:
    evento, operacao, ativo, lancamento, tolerancia = plano
    todos = dias_completos(db, operacao, consulta)
    dias = [dia for dia in todos if dia >= lancamento]
    contagens = contagens_do_par(db, evento, operacao)
    media, zeros = resumo_da_janela(dias, contagens)
    atual = sequencia_atual_zero(dias, contagens)
    ultimo = max((dia for dia in dias if contagens.get(dia, 0) > 0), default=None)
    limite = (date.fromisoformat(consulta) - timedelta(days=ATRASO_EM_DIAS)).isoformat()
    entradas = {
        "active_in_scope": bool(ativo) and lancamento <= consulta,
        "ingestion_complete": limite in todos,
        "expected_in_window": media > 0,
        "deviation_streak_reached": atual >= tolerancia,
        "known_exception_applies": False,
    }
    periodo_atual = (dias[-atual], dias[-1]) if atual else None
    return Par(evento, operacao, bool(ativo), len(dias), zeros, media, sum(contagens.get(d, 0) for d in dias),
               maior_sequencia_zero(dias, contagens), atual, ultimo, entradas,
               periodo_da_maior_sequencia(dias, contagens), periodo_atual)


def calcular_pares(db: sqlite3.Connection, consulta: str = CONSULTA) -> dict[tuple[str, str], Par]:
    planos = db.execute("SELECT event_name, operation, active, launch_date, silence_tolerance_days FROM lab2_plano")
    return {(p[0], p[1]): calcular_par(db, p, consulta) for p in planos.fetchall()}


def limite_fixo(db: sqlite3.Connection) -> list[str]:
    """Mensagens de erro do limite fixo de escopo do Lab 2; lista vazia se tudo confere."""
    erros: list[str] = []
    operacoes = {r[0] for r in db.execute("SELECT operation FROM lab2_plano UNION SELECT operation FROM lab2_carga "
                                          "UNION SELECT operation FROM lab2_eventos_diarios")}
    eventos = {r[0] for r in db.execute("SELECT event_name FROM lab2_plano UNION SELECT event_name FROM lab2_eventos_diarios")}
    if operacoes != OPERACOES:
        erros.append(f"limite fixo: devem ser 2 operações ({', '.join(sorted(OPERACOES))}), há {sorted(operacoes)}")
    if eventos != EVENTOS:
        erros.append(f"limite fixo: devem ser 3 eventos ({', '.join(sorted(EVENTOS))}), há {sorted(eventos)}")
    ops_lead = {r[0] for r in db.execute("SELECT DISTINCT operation FROM lab2_eventos_diarios WHERE event_name='generate_lead'")}
    if ops_lead != {"BR"}:
        erros.append(f"limite fixo: generate_lead só tem linhas na BR, e há linhas em {sorted(ops_lead)}; no MX não dispara")
    erros += _limite_de_datas(db)
    return erros


def _limite_de_datas(db: sqlite3.Connection) -> list[str]:
    erros: list[str] = []
    for operacao in sorted(OPERACOES):
        datas = [r[0] for r in db.execute("SELECT event_date FROM lab2_carga WHERE operation=? ORDER BY event_date", (operacao,))]
        if len(datas) != TOTAL_DE_DIAS or datas[:1] != [PRIMEIRO_DIA] or datas[-1:] != [ULTIMO_DIA]:
            erros.append(f"limite fixo: {operacao} deve ter {TOTAL_DE_DIAS} dias de {PRIMEIRO_DIA} a {ULTIMO_DIA}, há {len(datas)}")
        incompletos = [r[0] for r in db.execute("SELECT event_date FROM lab2_carga WHERE operation=? AND is_complete=0", (operacao,))]
        if incompletos != [DIA_INCOMPLETO]:
            erros.append(f"limite fixo: só {DIA_INCOMPLETO} pode estar incompleto em {operacao}, há {incompletos}")
    return erros


# ---------- frases que os textos repetem ----------
def linha_da_tabela(par: Par) -> str:
    """Linha do quadro-resumo da página do laboratório, montada com os números recalculados."""
    agora = "0" if par.sequencia_atual == 0 else f"{par.sequencia_atual} dia{'s' if par.sequencia_atual > 1 else ''}"
    return (f"| {par.operacao} | {par.evento} | {par.dias_em_zero} de {par.dias} | "
            f"{formatar_decimal(par.media)} | {agora} |")


def _periodo(periodo: tuple[str, str] | None) -> str:
    return formatar_periodo(*periodo) if periodo else "sem período"


def frases_esperadas(pares: dict[tuple[str, str], Par], db: sqlite3.Connection) -> dict[str, tuple[str, ...]]:
    """Trechos que cada texto deve repetir literalmente, todos montados a partir da amostra."""
    lead, fim = pares[LEAD_BR], pares[CANDIDATO]
    media, zeros = formatar_decimal(lead.media), f"zero em {lead.dias_em_zero} de {lead.dias}"
    maior, atual = _periodo(lead.periodo_maior), _periodo(lead.periodo_atual)
    desde = "desde " + (_periodo((fim.periodo_atual[0],) * 2) if fim.periodo_atual else "sem data")
    reais = (formatar_reais(receita_certa(db, "BR", DIA_DO_PEDIDO)), formatar_reais(receita_apos_juncao(db, "BR", DIA_DO_PEDIDO)))
    tabela = tuple(linha_da_tabela(par) for par in pares.values() if par.ativo)
    return {
        "pagina": tabela + (
            f"{lead.total} disparos em {lead.dias} dias completos, média de {media} por dia, {zeros} dias",
            f"A maior sequência em zero foi de {lead.maior_sequencia} dias ({maior})",
            f"em zero há {lead.sequencia_atual} dias ({atual})",
            f"{desde}: são {fim.sequencia_atual} dias completos seguidos em zero", *reais),
        "evento": (f"média de {media} por dia", f"{zeros} dias completos",
                   f"maior sequência em zero: {lead.maior_sequencia} dias", maior, f"{lead.dias} dias completos"),
        "gabarito": (f"{desde} ({fim.sequencia_atual} dias completos seguidos em zero, com média de "
                     f"{formatar_decimal_curto(fim.media)} por dia", f"em zero há {lead.sequencia_atual} dias",
                     f"{zeros} dias completos", f"Em {atual}", f"{lead.maior_sequencia} dias ({maior})",
                     f"média de {formatar_decimal_curto(fim.media)} por dia", desde, *reais),
        "modelo": (f"{zeros} dias completos", f"Média de {media} por dia", f"Até {lead.maior_sequencia} dias seguidos",
                   f"({atual})", f"{lead.sequencia_atual} dias completos seguidos em zero"),
    }


# ---------- conferências sobre arquivos ----------
def _ler(caminho: Path, relatorio: Relatorio) -> str | None:
    relatorio.arquivo_atual = caminho
    try:
        return caminho.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError):
        relatorio.erro(caminho, "arquivo não encontrado")
    except (OSError, UnicodeDecodeError) as exc:
        relatorio.erro(caminho, f"não foi possível ler: {exc}")
    return None


def _montar_banco(downloads: Path, relatorio: Relatorio) -> sqlite3.Connection | None:
    sql = _ler(downloads / ARQUIVO_AMOSTRA, relatorio)
    if sql is None:
        return None
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(sql)
    except sqlite3.Error as exc:
        relatorio.erro(downloads / ARQUIVO_AMOSTRA, f"SQL inválido: {exc}")
        return None
    return db


def conferir_numeros(caminho: Path, numeros: tuple[str, ...], relatorio: Relatorio) -> None:
    texto = _ler(caminho, relatorio)
    if texto is None:
        return
    for numero in numeros:
        if numero not in texto:
            relatorio.erro(caminho, f"falta o trecho {numero!r}, recalculado na amostra")


def conferir_numeros_do_caso(raiz: Path, downloads: Path, pares: dict[tuple[str, str], Par], db: sqlite3.Connection,
                             relatorio: Relatorio) -> None:
    lead, fim = pares[LEAD_BR], pares[CANDIDATO]
    esperado = {"dias completos": (lead.dias, 27), "dias em zero": (lead.dias_em_zero, 9), "maior sequência": (lead.maior_sequencia, 3),
                "sequência atual": (lead.sequencia_atual, 2), "disparos": (lead.total, 30), "média": (formatar_decimal(lead.media), "1,1"),
                "último disparo de add_to_cart no MX": (fim.ultimo_disparo, "2026-11-10"), "sequência de add_to_cart no MX": (fim.sequencia_atual, 5)}
    for nome, (observado, certo) in esperado.items():
        if observado != certo:
            relatorio.erro(downloads / ARQUIVO_AMOSTRA, f"generate_lead BR e add_to_cart MX: {nome} esperado {certo}, observado {observado}")
    frases = frases_esperadas(pares, db)
    conferir_numeros(downloads / ARQUIVO_GABARITO, frases["gabarito"], relatorio)
    conferir_numeros(raiz / PAGINA, frases["pagina"], relatorio)
    conferir_numeros(downloads / ARQUIVO_EVENTO, frases["evento"], relatorio)
    conferir_numeros(raiz / PAGINA_MODELO, frases["modelo"], relatorio)


def conferir_regra(downloads: Path, pares: dict[tuple[str, str], Par], relatorio: Relatorio) -> int:
    """Classifica cada par pela regra canônica; devolve quantos candidatos a falha há."""
    regra = carregar_yaml(downloads / ARQUIVO_REGRA, relatorio)
    tabela = regra.get("decision_table") if regra else None
    if not isinstance(tabela, list):
        relatorio.erro(downloads / ARQUIVO_REGRA, "falta decision_table (lista) para classificar os pares")
        return -1
    resultados = {chave: classificar(par.entradas, tabela) for chave, par in pares.items()}
    for chave, resultado in resultados.items():
        if resultado is None:
            relatorio.erro(downloads / ARQUIVO_REGRA, f"{chave[0]} {chave[1]}: a tabela não dá um único resultado para {pares[chave].entradas}")
    candidatos = sorted(chave for chave, r in resultados.items() if r == "failure_candidate")
    if candidatos != [CANDIDATO]:
        relatorio.erro(downloads / ARQUIVO_REGRA, f"o único failure_candidate deve ser add_to_cart MX, observado {candidatos}")
    for chave, certo in ((LEAD_MX, "not_active_in_scope"), (LEAD_BR, "within_expected")):
        if resultados.get(chave) != certo:
            relatorio.erro(downloads / ARQUIVO_REGRA, f"{chave[0]} {chave[1]} deve dar {certo}, observado {resultados.get(chave)}")
    return len(candidatos)


def conferir_consulta(db: sqlite3.Connection, downloads: Path, pares: dict[tuple[str, str], Par], relatorio: Relatorio) -> None:
    sql = _ler(downloads / ARQUIVO_CONSULTA, relatorio)
    if sql is None:
        return
    try:
        linhas = db.execute(sql).fetchall()
    except sqlite3.Error as exc:
        relatorio.erro(downloads / ARQUIVO_CONSULTA, f"SQL inválido: {exc}")
        return
    observado = {(r[0], r[1]): tuple(r[2:]) for r in linhas}
    esperado = {chave: (int(p.ativo), round(p.media, 1) if p.dias else None, p.dias, p.dias_em_zero, p.sequencia_atual)
                for chave, p in pares.items()}
    if observado != esperado:
        relatorio.erro(downloads / ARQUIVO_CONSULTA, f"a consulta devolve {observado}, o recálculo em Python dá {esperado}")


def conferir_fan_out(db: sqlite3.Connection, relatorio: Relatorio) -> None:
    certa, inflada = receita_certa(db, "BR", DIA_DO_PEDIDO), receita_apos_juncao(db, "BR", DIA_DO_PEDIDO)
    if (certa, inflada) != (RECEITA_CERTA, RECEITA_INFLADA):
        relatorio.erro(None, f"receita da BR em {DIA_DO_PEDIDO}: esperado {RECEITA_CERTA} certa e {RECEITA_INFLADA} após a junção, observado {certa} e {inflada}")
    compras = db.execute("SELECT event_count FROM lab2_eventos_diarios WHERE event_date=? AND operation='BR' AND event_name='purchase'",
                         (DIA_DO_PEDIDO,)).fetchone()
    pedidos = db.execute("SELECT COUNT(*) FROM lab2_pedidos WHERE order_date=? AND operation='BR'", (DIA_DO_PEDIDO,)).fetchone()[0]
    if not compras or compras[0] != pedidos:
        relatorio.erro(None, f"purchase da BR em {DIA_DO_PEDIDO} deve bater com os {pedidos} pedidos da amostra, observado {compras}")
    parciais = db.execute("SELECT COUNT(*) FROM lab2_eventos_diarios WHERE event_date=? AND event_name='purchase'", (DIA_INCOMPLETO,)).fetchone()[0]
    if parciais != 2:
        relatorio.erro(None, f"{DIA_INCOMPLETO} deve ter contagens parciais de purchase nas duas operações, há {parciais}")


def conferir_gabarito(downloads: Path, relatorio: Relatorio) -> None:
    doc = carregar_yaml(downloads / ARQUIVO_GABARITO, relatorio)
    perguntas = doc.get("questions") if doc else None
    if not isinstance(perguntas, list):
        relatorio.erro(downloads / ARQUIVO_GABARITO, "falta a lista questions")
        return
    mapa = {q.get("id"): q.get("expected_behavior") for q in perguntas if isinstance(q, dict)}
    if mapa != COMPORTAMENTOS:
        relatorio.erro(downloads / ARQUIVO_GABARITO, f"comportamentos documentados diferentes do esperado: {mapa}")
    for q in (q for q in perguntas if isinstance(q, dict)):
        _conferir_pergunta(downloads / ARQUIVO_GABARITO, q, relatorio)


def _conferir_pergunta(caminho: Path, q: dict[str, Any], relatorio: Relatorio) -> None:
    comportamento, id_ = q.get("expected_behavior"), q.get("id")
    if comportamento == "abstain" and (q.get("reference_answer") is not None or not q.get("reason_if_abstain")):
        relatorio.erro(caminho, f"{id_} é abstenção e precisa de motivo, sem resposta numérica")
    if comportamento == "clarify" and not q.get("ambiguity"):
        relatorio.erro(caminho, f"{id_} pede esclarecimento e precisa dizer o que falta")
    if id_ == "Q01" and q.get("reference_sql") != ARQUIVO_CONSULTA:
        relatorio.erro(caminho, f"Q01 deve usar a consulta {ARQUIVO_CONSULTA}")


def conferir_receita_sql(db: sqlite3.Connection, downloads: Path, relatorio: Relatorio) -> None:
    """Roda a consulta de receita no SQLite: sem JOIN, cada linha igual a receita_certa, BR em 02/11 = 500."""
    caminho = downloads / ARQUIVO_RECEITA
    sql = _ler(caminho, relatorio)
    if sql is None:
        return
    if re.search(r"\bJOIN\b", re.sub(r"--[^\n]*", "", sql), re.IGNORECASE):
        relatorio.erro(caminho, "a consulta de receita não pode usar JOIN: a soma deve ser feita na tabela de pedidos")
    try:
        linhas = db.execute(sql).fetchall()
    except sqlite3.Error as exc:
        relatorio.erro(caminho, f"SQL inválido: {exc}")
        return
    observado = {(r[0], r[1]): r[2] for r in linhas if len(r) >= 3}
    esperado = {(o, d): receita_certa(db, o, d) for o, d in db.execute("SELECT DISTINCT operation, order_date FROM lab2_pedidos")}
    if observado != esperado:
        relatorio.erro(caminho, f"a consulta devolve {observado}, o recálculo em Python dá {esperado}")
    if observado.get(("BR", DIA_DO_PEDIDO)) != RECEITA_CERTA:
        relatorio.erro(caminho, f"BR em {DIA_DO_PEDIDO} deve dar {RECEITA_CERTA}, a consulta dá {observado.get(('BR', DIA_DO_PEDIDO))}")


def conferir_kpi_receita(raiz: Path, db: sqlite3.Connection, relatorio: Relatorio) -> None:
    """KPI-AURORA-002 cita os dois valores recalculados: o certo e o inflado pela junção."""
    frases = (formatar_reais(receita_certa(db, "BR", DIA_DO_PEDIDO)), formatar_reais(receita_apos_juncao(db, "BR", DIA_DO_PEDIDO)))
    conferir_numeros(raiz / FONTE_KPI_RECEITA, frases, relatorio)


def conferir_perguntas_da_receita(raiz: Path, relatorio: Relatorio) -> None:
    """Q06 depende do KPI aprovado; Q03 aceita também a resposta que avalia as duas operações."""
    caminho = raiz / FONTE_GABARITO
    lido = ler_frontmatter(caminho, relatorio)
    if lido is None:
        return
    dados = lido[0]
    perguntas = {q.get("id"): q for q in dados.get("questions") or [] if isinstance(q, dict)}
    q06, q03 = perguntas.get("Q06", {}), perguntas.get("Q03", {})
    if ID_KPI_RECEITA not in (q06.get("required_sources") or []):
        relatorio.erro(caminho, f"Q06 deve ter {ID_KPI_RECEITA} em required_sources")
    versoes = dados.get("depends_on_versions")
    if not isinstance(versoes, dict) or str(versoes.get(ID_KPI_RECEITA)) != VERSAO_KPI_RECEITA:
        relatorio.erro(caminho, f'depends_on_versions deve ter {ID_KPI_RECEITA}: "{VERSAO_KPI_RECEITA}"')
    aceitas = q03.get("also_accepted")
    if not isinstance(aceitas, list) or not any(isinstance(a, dict) and a.get("behavior") == "answer" for a in aceitas):
        relatorio.erro(caminho, "Q03 deve ter also_accepted com behavior answer (resposta que avalia Brasil e México)")


def resumo(pares: dict[tuple[str, str], Par], db: sqlite3.Connection) -> str:
    lead, fim = pares[LEAD_BR], pares[CANDIDATO]
    return (f"OK: limite fixo respeitado (2 operações, 3 eventos, {TOTAL_DE_DIAS} dias, 1 dia incompleto, "
            f"1 candidato a falha: add_to_cart MX); generate_lead BR: {lead.total} disparos, zero em {lead.dias_em_zero} de "
            f"{lead.dias} dias completos, média {formatar_decimal(lead.media)}, maior sequência {lead.maior_sequencia} dias, "
            f"sequência atual {lead.sequencia_atual} dias; add_to_cart MX: {fim.sequencia_atual} dias seguidos em zero desde 11/11; "
            f"receita da BR em 02/11: {formatar_reais(receita_certa(db, 'BR', DIA_DO_PEDIDO))} certa e "
            f"{formatar_reais(receita_apos_juncao(db, 'BR', DIA_DO_PEDIDO))} depois da junção.")


def executar(raiz: Path = ROOT) -> Relatorio:
    relatorio = Relatorio()
    downloads = raiz / "public" / "downloads"
    db = _montar_banco(downloads, relatorio)
    if db is None:
        return relatorio
    with db:
        for mensagem in limite_fixo(db):
            relatorio.erro(downloads / ARQUIVO_AMOSTRA, mensagem)
        if relatorio.erros:
            return relatorio
        pares = calcular_pares(db)
        conferir_numeros_do_caso(raiz, downloads, pares, db, relatorio)
        conferir_regra(downloads, pares, relatorio)
        conferir_consulta(db, downloads, pares, relatorio)
        conferir_fan_out(db, relatorio)
        conferir_receita_sql(db, downloads, relatorio)
        conferir_kpi_receita(raiz, db, relatorio)
        conferir_perguntas_da_receita(raiz, relatorio)
        conferir_gabarito(downloads, relatorio)
        relatorio.avisos.append(resumo(pares, db))
    return relatorio


def main() -> None:
    relatorio = Relatorio()
    relatorio.instalar()
    resultado = executar()
    relatorio.erros.extend(resultado.erros)
    mensagem = next((a for a in resultado.avisos if a.startswith("OK:")), "")
    relatorio.avisos.extend(a for a in resultado.avisos if not a.startswith("OK:"))
    relatorio.encerrar(mensagem)


if __name__ == "__main__":
    main()
