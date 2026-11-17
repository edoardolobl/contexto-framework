#!/usr/bin/env python3
"""Verifica exemplos DIDÁTICOS de revisões e vigência sem simular um sistema RAG.

Uma versão citada no changelog não equivale a um snapshot histórico recuperável.
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import re
from typing import Any

from comum import DADOS, DOWNLOADS as DL, ESTADOS_JA_APROVADOS, Relatorio, carregar_yaml, exigir_minimo

DIAS_DE_FIM_DE_SEMANA = {5: "sábado", 6: "domingo"}
DATA_DA_AMOSTRA = date(2026, 10, 1)
CAMPOS_DO_ARTEFATO = ("nome", "desde", "origem", "padroes")

EXPECTATIVAS = [
    ("CONCEPT-ONBOARDING-001", "2026-07-25", []),
    ("CONCEPT-ONBOARDING-001", "2026-08-20", ["CONCEPT-ONBOARDING-001@1.0"]),
    ("CONCEPT-ONBOARDING-001", "2026-09-01", ["CONCEPT-ONBOARDING-001@2.0"]),
    ("KPI-AURORA-001", "2026-08-20", ["KPI-AURORA-001@1.0"]),
    ("KPI-AURORA-001", "2026-09-15", ["KPI-AURORA-001@2.0"]),
]


@dataclass(frozen=True)
class Artefato:
    nome: str
    desde: date
    origem: str
    padroes: tuple[re.Pattern[str], ...]


@dataclass
class Registro:
    """Quando cada id, cada ID@versão e cada artefato passou a existir."""

    ids: dict[str, date] = field(default_factory=dict)
    versoes: dict[str, date] = field(default_factory=dict)
    artefatos: list[Artefato] = field(default_factory=list)


def converter_data(valor: Any) -> date | None:
    if isinstance(valor, date):
        return valor
    try:
        return date.fromisoformat(str(valor))
    except ValueError:
        return None


def dia(caminho: Path, valor: Any, campo: str, relatorio: Relatorio) -> date | None:
    if valor in (None, ""):
        return None
    convertido = converter_data(valor)
    if convertido is None:
        relatorio.erro(caminho, f"{campo}: data inválida, esperado AAAA-MM-DD")
    return convertido


# ---------- artefatos e registro de datas ----------

def carregar_artefatos(caminho: Path, relatorio: Relatorio) -> list[Artefato]:
    """Lê src/data/artefatos.yaml. Item malformado vira erro e é descartado."""
    dados = carregar_yaml(caminho, relatorio)
    if dados is None:
        return []
    brutos = dados.get("artefatos")
    if not isinstance(brutos, list) or not brutos:
        relatorio.erro(caminho, "nenhum artefato encontrado em 'artefatos'")
        return []
    itens = (_artefato_de(item, n, caminho, relatorio) for n, item in enumerate(brutos, start=1))
    return [a for a in itens if a]


def _artefato_de(item: Any, numero: int, caminho: Path, relatorio: Relatorio) -> Artefato | None:
    def falha(motivo: str) -> None:
        relatorio.erro(caminho, f"artefato {numero} {motivo}")

    if not isinstance(item, dict):
        falha("não é um mapa")
        return None
    for campo in CAMPOS_DO_ARTEFATO:
        if item.get(campo) in (None, "", []):
            falha(f"sem '{campo}'")
            return None
    desde = converter_data(item["desde"])
    if desde is None:
        falha("tem 'desde' inválido, esperado AAAA-MM-DD")
        return None
    brutos = item["padroes"]
    if not isinstance(brutos, list) or not all(isinstance(p, str) for p in brutos):
        falha("tem 'padroes' que deve ser uma lista de textos")
        return None
    compilados = []
    for padrao in brutos:
        try:
            compilados.append(re.compile(padrao))
        except re.error as exc:
            falha(f"tem expressão inválida em padroes ({padrao}): {exc}")
            return None
    return Artefato(str(item["nome"]), desde, str(item["origem"]), tuple(compilados))


def montar_registro(documentos: dict[Path, dict], artefatos: list[Artefato]) -> Registro:
    registro = Registro(artefatos=list(artefatos))
    for dados in documentos.values():
        id_ = dados.get("id")
        if not isinstance(id_, str):
            continue
        for entrada in dados.get("version_history") or []:
            quando = converter_data(entrada.get("date")) if isinstance(entrada, dict) else None
            if quando is None:
                continue
            if id_ not in registro.ids or quando < registro.ids[id_]:
                registro.ids[id_] = quando
            registro.versoes[f"{id_}@{entrada.get('version')}"] = quando
    return registro


# ---------- datas de citações ----------

def textos_do_yaml(valor: Any, ignorar: tuple[str, ...] = ()) -> Iterator[str]:
    """Todos os textos do YAML já interpretado, pulando as chaves de 'ignorar' na raiz."""
    if isinstance(valor, str):
        yield valor
    elif isinstance(valor, dict):
        for chave, item in valor.items():
            if chave not in ignorar:
                yield from textos_do_yaml(item)
    elif isinstance(valor, list):
        for item in valor:
            yield from textos_do_yaml(item)


def citacoes_posteriores(texto: str, limite: date, registro: Registro) -> list[tuple[str, date]]:
    """Tudo o que o texto cita e que só passou a existir depois do limite."""
    achados: dict[str, date] = {}
    for id_, desde in registro.ids.items():
        if desde > limite and re.search(rf"(?<![\w-]){re.escape(id_)}(?![\w-])", texto):
            achados[id_] = desde
    for versao, desde in registro.versoes.items():
        if desde > limite and re.search(rf"(?<![\w-]){re.escape(versao)}(?![\w.])", texto):
            achados[versao] = desde
    for artefato in registro.artefatos:
        if artefato.desde > limite and any(p.search(texto) for p in artefato.padroes):
            achados[artefato.nome] = artefato.desde
    return sorted(achados.items())


def acusar_texto(caminho: Path, rotulo: str, limite: date, texto: str, registro: Registro, relatorio: Relatorio) -> None:
    for citado, desde in citacoes_posteriores(texto, limite, registro):
        relatorio.erro(caminho, f"{rotulo} de {limite.isoformat()} cita {citado}, que só existe a partir de {desde.isoformat()}")


def checar_datas(documentos: dict[Path, dict], registro: Registro, relatorio: Relatorio) -> None:
    """Nenhum documento cita algo que só passou a existir depois da sua própria version_date."""
    for caminho, dados in documentos.items():
        relatorio.arquivo_atual = caminho
        criado = converter_data(dados.get("version_date"))
        if criado is None:
            continue
        for texto in textos_do_yaml(dados, ignorar=("archival_note", "superseded_by_revision", "recorded_at")):
            acusar_texto(caminho, "versão", criado, texto, registro, relatorio)
        if "archival_note" in dados:
            _checar_nota_de_arquivo(caminho, dados["archival_note"], criado, registro, relatorio)


def _checar_nota_de_arquivo(caminho: Path, nota: Any, criado: date, registro: Registro, relatorio: Relatorio) -> None:
    if not isinstance(nota, dict) or not isinstance(nota.get("text"), str) or nota.get("date") in (None, ""):
        relatorio.erro(caminho, "archival_note deve ser um mapa com 'date' e 'text' (texto)")
        return
    data_da_nota = converter_data(nota["date"])
    if data_da_nota is None:
        relatorio.erro(caminho, "archival_note.date: data inválida, esperado AAAA-MM-DD")
        return
    if data_da_nota < criado:
        relatorio.erro(caminho, f"archival_note.date ({data_da_nota.isoformat()}) é anterior a version_date ({criado.isoformat()})")
    acusar_texto(caminho, "nota de arquivo", data_da_nota, nota["text"], registro, relatorio)


def avisar_fim_de_semana(caminho: Path, dados: dict, relatorio: Relatorio) -> None:
    """Aprovação registrada em sábado ou domingo merece uma segunda olhada, mas não é erro."""

    def avisar(quando: date | None, onde: str) -> None:
        if quando is not None and quando.weekday() in DIAS_DE_FIM_DE_SEMANA:
            nome = DIAS_DE_FIM_DE_SEMANA[quando.weekday()]
            relatorio.aviso(caminho, f"{onde} cai em {nome} ({quando.isoformat()}): confirme a data da aprovação")

    for numero, entrada in enumerate(dados.get("version_history") or []):
        if isinstance(entrada, dict) and entrada.get("approved_by"):
            avisar(converter_data(entrada.get("date")), f"version_history[{numero}] aprovada")
    if dados.get("status") == "approved":
        avisar(converter_data(dados.get("version_date")), "version_date de documento aprovado")


# ---------- regras por documento ----------

def checar_documentos(documentos: dict[Path, dict], relatorio: Relatorio) -> dict[str, dict]:
    """Regras de cada documento. Devolve as revisões por revision_id."""
    revisions: dict[str, dict] = {}
    for path, data in documentos.items():
        relatorio.arquivo_atual = path
        _checar_documento(path, data, revisions, relatorio)
        avisar_fim_de_semana(path, data, relatorio)
    return revisions


def _checar_documento(path: Path, data: dict, revisions: dict[str, dict], relatorio: Relatorio) -> None:
    err = relatorio.erro
    stable = data.get("id")
    version = str(data.get("version"))
    rev = data.get("revision_id")
    if rev != f"{stable}@{version}":
        err(path, "revision_id deve ser formado por id@version")
    if rev in revisions:
        err(path, f"revision_id repetido no arquivo {revisions[rev]['path'].name}")
    else:
        revisions[rev] = {"path": path, "data": data}

    created = dia(path, data.get("version_date"), "version_date", relatorio)
    start = dia(path, data.get("valid_from"), "valid_from", relatorio)
    end = dia(path, data.get("valid_to"), "valid_to", relatorio)

    raw_history = data.get("version_history") or []
    if not all(isinstance(h, dict) for h in raw_history):
        err(path, "version_history deve conter só mapas")
    history = [h for h in raw_history if isinstance(h, dict)]
    if not history or str(history[0].get("version")) != version:
        err(path, "histórico deve começar pela versão representada no arquivo")
    elif dia(path, history[0].get("date"), "version_history[0].date", relatorio) != created:
        err(path, "data do histórico atual difere de version_date")

    gravado = dia(path, data.get("recorded_at"), "recorded_at", relatorio)
    if gravado and created and gravado < created:
        err(path, f"recorded_at ({gravado.isoformat()}) é anterior a version_date ({created.isoformat()})")

    previous = data.get("supersedes_revision")
    if previous and (previous == rev or not str(previous).startswith(f"{stable}@")):
        err(path, "supersedes_revision deve apontar uma revisão anterior do mesmo assunto")
    if previous and not any(f"{stable}@{x.get('version')}" == previous for x in history[1:]):
        err(path, "revisão substituída precisa constar no histórico")

    ja_aprovada = data.get("status") in ESTADOS_JA_APROVADOS
    if ja_aprovada:
        if not start:
            err(path, "revisão aprovada precisa de valid_from")
        if created and start and start < created:
            err(path, "valid_from anterior à emissão; declarar retroatividade em registro próprio se existir")
        if end and start and end <= start:
            err(path, "valid_to deve ser posterior a valid_from")
    elif start or end:
        err(path, "rascunho pendente não deve se passar por regra vigente")
    if not ja_aprovada and previous:
        err(path, "rascunho inicial não deve afirmar que substitui uma revisão aprovada")


def checar_substituicao(revisions: dict[str, dict], relatorio: Relatorio) -> None:
    """Revisão superseded aponta o sucessor, o sucessor aponta de volta e a vigência passa sem folga."""
    for rev, item in revisions.items():
        path, data = item["path"], item["data"]
        if data.get("status") != "superseded":
            continue
        sucessora = data.get("superseded_by_revision")
        if not isinstance(sucessora, str) or sucessora.split("@")[0] != data.get("id"):
            relatorio.erro(path, "superseded exige superseded_by_revision com o mesmo id")
            continue
        if sucessora not in revisions:
            relatorio.erro(path, f"superseded_by_revision {sucessora} não está no registro")
            continue
        sucessor = revisions[sucessora]["data"]
        if sucessor.get("supersedes_revision") != rev:
            relatorio.erro(path, f"{sucessora} não é recíproca: supersedes_revision deveria ser {rev}")
        fim = converter_data(data.get("valid_to"))
        inicio_do_sucessor = converter_data(sucessor.get("valid_from"))
        if fim != inicio_do_sucessor:
            relatorio.erro(path, f"valid_to da revisão substituída ({data.get('valid_to')}) deve ser igual ao valid_from "
                                 f"do sucessor {sucessora} ({sucessor.get('valid_from')})")


def agrupar_por_id(documentos: dict[Path, dict]) -> dict[Any, list[tuple[Path, dict]]]:
    grouped: dict[Any, list[tuple[Path, dict]]] = defaultdict(list)
    for path, data in documentos.items():
        grouped[data.get("id")].append((path, data))
    return grouped


def checar_sobreposicao(grouped: dict, relatorio: Relatorio) -> None:
    for items in grouped.values():
        approved = []
        for path, data in items:
            start = dia(path, data.get("valid_from"), "valid_from", relatorio)
            if data.get("status") in ESTADOS_JA_APROVADOS and start:
                approved.append((start, dia(path, data.get("valid_to"), "valid_to", relatorio), path, data))
        approved.sort(key=lambda x: x[0])
        for earlier, later in zip(approved, approved[1:]):
            if earlier[1] is None or earlier[1] > later[0]:
                relatorio.erro(later[2], f"vigência se sobrepõe à revisão {earlier[3]['revision_id']}")


def select(grouped: dict, stable: str, as_of: str, relatorio: Relatorio) -> list[str]:
    """Consulta documental ilustrativa; não simula recuperação ou controle de acesso."""
    target = date.fromisoformat(as_of)
    found = []
    for path, data in grouped[stable]:
        start = dia(path, data.get("valid_from"), "valid_from", relatorio)
        if data.get("status") not in ESTADOS_JA_APROVADOS or not start:
            continue
        end = dia(path, data.get("valid_to"), "valid_to", relatorio)
        if start <= target and (end is None or target < end):
            found.append(data["revision_id"])
    return found


def checar_selecoes(grouped: dict, relatorio: Relatorio) -> None:
    for stable, as_of, expected in EXPECTATIVAS:
        actual = select(grouped, stable, as_of, relatorio)
        if actual != expected:
            relatorio.erro(None, f"Seleção histórica {stable} em {as_of}: esperado {expected}, obtido {actual}")


def checar_gabarito(revisions: dict[str, dict], relatorio: Relatorio) -> None:
    """Uma resposta calculada sobre dados de 01/10 não deveria ter sido aprovada em setembro."""
    qa = next((r for k, r in revisions.items() if k.startswith("QA-AURORA-001@") and r["data"].get("status") == "approved"), None)
    if not qa:
        relatorio.erro(None, "Gabarito QA-AURORA-001 aprovado não encontrado")
        return
    path, data = qa["path"], qa["data"]
    for q in data.get("questions", []):
        reviewed = dia(path, q.get("reviewed_at"), f"{q.get('id')}.reviewed_at", relatorio)
        if reviewed and reviewed < DATA_DA_AMOSTRA:
            relatorio.erro(path, f"{q.get('id')}: revisão anterior aos dados sintéticos referenciados")
    qa_date = dia(path, data.get("version_date"), "version_date", relatorio)
    if qa_date and qa_date < DATA_DA_AMOSTRA:
        relatorio.erro(path, "gabarito aprovado antes da data da amostra usada na avaliação")


def normalizar_janela(value: Any) -> Any:
    if isinstance(value, str):
        return re.sub(r"\b(?:30|60) dias\b", "N dias", value)
    if isinstance(value, list):
        return [normalizar_janela(item) for item in value]
    return value


def checar_conceito(revisions: dict[str, dict], relatorio: Relatorio) -> None:
    """A revisão histórica e a atual do conceito diferem APENAS na janela temporal."""
    historico = revisions.get("CONCEPT-ONBOARDING-001@1.0", {}).get("data")
    atual = revisions.get("CONCEPT-ONBOARDING-001@2.0", {}).get("data")
    if not historico or not atual:
        relatorio.erro(None, "Faltam revisões 1.0 e 2.0 do conceito fictício para comparar")
        return
    campos = (
        ("definition", historico["definition"], atual["definition"]),
        ("inclusion_criteria", historico["inclusion_criteria"], atual["inclusion_criteria"]),
        ("exclusion_criteria", historico["exclusion_criteria"], atual["exclusion_criteria"]),
        ("not_synonyms", historico["vocabulary"]["not_synonyms"], atual["vocabulary"]["not_synonyms"]),
    )
    for campo, antigo, novo in campos:
        if normalizar_janela(antigo) != normalizar_janela(novo):
            relatorio.erro(None, f"Conceito Aurora: {campo} diverge além da janela de atividade")
    if "60 dias" not in historico["definition"] or "30 dias" not in atual["definition"]:
        relatorio.erro(None, "Conceito Aurora: revisão 1.0 deve ter 60 dias e revisão 2.0, 30")
    if historico["valid_to"] != atual["valid_from"]:
        relatorio.erro(None, "Conceito Aurora: períodos de validade não se conectam corretamente")


def main() -> None:
    relatorio = Relatorio()
    relatorio.instalar()
    arquivos = (exigir_minimo(DL.glob("exemplo-*.yaml"), 20, "exemplos YAML", relatorio)
                + exigir_minimo((DL / "historico").glob("*.yaml"), 2, "versões históricas em historico/", relatorio))
    documentos: dict[Path, dict] = {}
    for caminho in arquivos:
        dados = carregar_yaml(caminho, relatorio)
        if dados is not None:
            documentos[caminho] = dados

    revisions = checar_documentos(documentos, relatorio)
    grouped = agrupar_por_id(documentos)
    checar_substituicao(revisions, relatorio)
    checar_sobreposicao(grouped, relatorio)
    checar_selecoes(grouped, relatorio)
    artefatos = carregar_artefatos(DADOS / "artefatos.yaml", relatorio)
    checar_datas(documentos, montar_registro(documentos, artefatos), relatorio)
    checar_gabarito(revisions, relatorio)
    checar_conceito(revisions, relatorio)

    relatorio.encerrar(f"OK: {len(documentos)} registros, IDs de revisão únicos, intervalos não sobrepostos, "
                       f"duas revisões históricas integrais e {len(EXPECTATIVAS)} seleções temporais verificadas.")


if __name__ == "__main__":
    main()
