#!/usr/bin/env python3
"""Quality gates for the Contexto documentation, not certification of its business rules."""
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "src" / "content" / "docs"
DOWNLOADS = ROOT / "public" / "downloads"
TEMPLATE_COMPONENT = ROOT / "src" / "components" / "TemplateDownloads.astro"

PAGES = sorted([*DOCS.rglob("*.md"), *DOCS.rglob("*.mdx")])
REQUIRED_TYPES = ("kpi", "conceito", "processo", "decisao", "politica", "dataset", "relacionamento", "dashboard", "rubrica", "casos-teste")
VALID_STATUSES = {"draft", "pending_approval", "approved", "deprecated"}
errors: list[str] = []


def record(path: Path, msg: str):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def route(path: Path):
    rel = path.relative_to(DOCS)
    parts = list(rel.parts)
    parts[-1] = path.stem
    if parts[-1] == "index":
        parts.pop()
    return "/" + "/".join(parts) + ("/" if parts else "")


routes = {route(p): p for p in PAGES}

for path in PAGES:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
    if not match:
        record(path, "frontmatter YAML ausente")
        continue
    try:
        front = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        record(path, f"frontmatter YAML inválido: {exc}")
        continue
    if not isinstance(front, dict):
        record(path, "frontmatter não é um objeto")
        continue
    for required in ("title", "description"):
        if not isinstance(front.get(required), str) or not front[required].strip():
            record(path, f"campo obrigatório {required} ausente/vazio")

    # Simple Markdown link check: verify routes, not remote URLs.
    for url in re.findall(r"\]\(([^)]+)\)", content):
        if re.match(r"^(https?:|mailto:|#|/)", url):
            continue
        rel_url = url.split("#")[0].split("?")[0]
        if not rel_url or "{" in rel_url or "}" in rel_url:
            continue
        if "downloads" in rel_url and rel_url.endswith((".yaml", ".md", ".pdf")):
            file = DOWNLOADS / Path(rel_url).name
            if not file.exists():
                record(path, f"download inexistente: {url}")
            continue
        # Resolve o link como o navegador faria. Subir além da raiz do site é erro:
        # no GitHub Pages isso sai do subcaminho do projeto e resulta em 404.
        segments = [seg for seg in route(path).strip("/").split("/") if seg]
        escaped = False
        for seg in rel_url.split("/"):
            if seg in ("", "."):
                continue
            if seg == "..":
                if not segments:
                    escaped = True
                    break
                segments.pop()
            else:
                segments.append(seg)
        if escaped:
            record(path, f"link interno sobe além da raiz do site: {url}")
            continue
        target = "/" + "/".join(segments) + "/" if segments else "/"
        if target not in routes:
            record(path, f"link interno não encontrado: {url} => {target}")

ID_PREFIXES = ("KPI-", "DATASET-", "REL-", "DASH-", "QA-", "RUBRIC-", "CONCEPT-", "PROCESS-", "DECISION-", "POLICY-")
REFERENCE_FIELDS = ("related_documents", "covered_documents", "metrics", "decision_rules",
                    "reference_questions", "valid_join_paths", "expected_questions_and_answers")


def walk_references(data):
    """Yield every document id cited by an example, wherever the convention allows one."""
    for field in REFERENCE_FIELDS:
        for value in data.get(field) or []:
            if isinstance(value, str):
                yield value
    sources = data.get("data_sources") or {}
    for field in ("valid_join_paths",):
        for value in sources.get(field) or []:
            yield value
    if isinstance(sources.get("authoritative_dataset"), str):
        yield sources["authoritative_dataset"]
    validation = data.get("validation") or {}
    for value in validation.get("expected_questions_and_answers") or []:
        if isinstance(value, str):
            yield value
    for question in data.get("questions") or []:
        for value in question.get("required_sources") or []:
            yield value


def check_version_history(path, data, minimum):
    history = data.get("version_history")
    if not isinstance(history, list) or len(history) < minimum:
        record(path, f"version_history precisa de pelo menos {minimum} entrada(s)")
        return
    for entry in history:
        if not isinstance(entry, dict) or set(entry) != {"version", "date", "change", "approved_by"}:
            record(path, "cada entrada de version_history tem version, date, change e approved_by")
            return
    if "version_date" not in data:
        record(path, "campo version_date ausente")
    if str(history[0]["version"]) != str(data.get("version")):
        record(path, "a primeira entrada de version_history deve ser a versão atual")


template_keys: dict[str, set] = {}
example_ids: dict[str, list[str]] = {}
references: list[tuple[Path, str]] = []
yaml_count = 0
for path in sorted(DOWNLOADS.glob("*.yaml")):
    yaml_count += 1
    try:
        data = yaml.safe_load(path.read_text(encoding="utf8"))
    except yaml.YAMLError as exc:
        record(path, f"YAML inválido: {exc}")
        continue
    if not isinstance(data, dict):
        record(path, "YAML deve ser mapa na raiz")
        continue
    if not data.get("type"):
        record(path, "campo type ausente")
    if data.get("status") not in VALID_STATUSES:
        record(path, f"status inválido: {data.get('status')}")
    is_complete = path.name.endswith("-completo.yaml")
    if path.name.startswith("template-"):
        template_keys[data.get("type")] = set(data)
        check_version_history(path, data, 1)
    if path.name.startswith("exemplo-"):
        if not data.get("id"):
            record(path, "exemplo sem identificador")
        else:
            example_ids.setdefault(data["id"], []).append(path.name)
        references.extend((path, ref) for ref in walk_references(data))
        if is_complete:
            # Regra editorial: aprovação só aparece em exemplo fictício completo, com aviso,
            # cargo (nunca pessoa) da organização inventada e histórico de pelo menos duas versões.
            if data.get("status") != "approved":
                record(path, "exemplo completo deve estar approved")
            if "fictícia" not in str(data.get("example_notice", "")):
                record(path, "exemplo completo sem example_notice de aprovação fictícia")
            for key in ("owner", "approver", "source_of_truth", "valid_from", "version_date"):
                if data.get(key) in (None, "", []):
                    record(path, f"exemplo completo sem {key}")
            for key in ("owner", "approver"):
                if "(Aurora)" not in str(data.get(key)):
                    record(path, f"{key} deve ser um cargo ou área da organização fictícia Aurora")
            if data.get("open_questions"):
                record(path, "exemplo completo não deve ter open_questions")
            check_version_history(path, data, 2)
            if isinstance(data.get("version_history"), list) and data["version_history"] and not data["version_history"][0].get("approved_by"):
                record(path, "a versão atual de um exemplo completo precisa de approved_by")
        else:
            if data.get("status") == "approved":
                record(path, "só o exemplo completo pode usar approved")
            check_version_history(path, data, 1)

# O mesmo id só pode se repetir entre o exemplo com lacunas e o seu par completo.
for doc_id, names in example_ids.items():
    if len(names) > 2 or (len(names) == 2 and sum(n.endswith("-completo.yaml") for n in names) != 1):
        record(DOWNLOADS, f"identificador {doc_id} repetido em {', '.join(names)}")

# Toda referência a outro documento precisa existir entre os exemplos publicados.
for path, ref in references:
    if ref.startswith(ID_PREFIXES) and ref not in example_ids:
        record(path, f"referência a documento inexistente: {ref}")

# Exemplo não pode usar campo de primeiro nível que o template do mesmo tipo não tem.
for path in sorted(DOWNLOADS.glob("exemplo-*.yaml")):
    data = yaml.safe_load(path.read_text(encoding="utf8"))
    allowed = template_keys.get(data.get("type"), set()) | {"example_notice"}
    extra = sorted(set(data) - allowed)
    if extra:
        record(path, f"campos fora do template: {', '.join(extra)}")

markdown_count = 0
for path in sorted(DOWNLOADS.glob("*.md")):
    markdown_count += 1
    content = path.read_text(encoding="utf-8")
    if content.startswith("---"):
        record(path, "template Markdown não deve começar com bloco YAML")
    for heading in ("## Identificação", "## Histórico de versões"):
        if heading not in content:
            record(path, f"template Markdown sem a seção {heading}")

# Every download card must lead to an existing file.
component = TEMPLATE_COMPONENT.read_text(encoding="utf-8")
for filename in re.findall(r"href:\s*'([^']+)'", component):
    if not (DOWNLOADS / filename).is_file():
        record(TEMPLATE_COMPONENT, f"arquivo de download ausente: {filename}")

# Check the SQLite example links separately; they are not included in template cards.
analytics = ROOT / "src" / "components" / "AnalyticsLabDownloads.astro"
if analytics.exists():
    for filename in re.findall(r"file:\s*'([^']+)'", analytics.read_text(encoding="utf8")):
        if not (DOWNLOADS / filename).is_file():
            record(analytics, f"arquivo SQL não encontrado: {filename}")

for kind in REQUIRED_TYPES:
    for suffix in (".md", ".yaml"):
        expected = DOWNLOADS / f"template-{kind}{suffix}"
        if not expected.exists():
            record(TEMPLATE_COMPONENT, f"template anunciado não existe: {expected.name}")
    if not (DOWNLOADS / f"exemplo-{kind}-completo.yaml").exists():
        record(TEMPLATE_COMPONENT, f"falta o exemplo completo de {kind}")

# Editorial rule: no em dashes in published text, components, downloads or docs.
EDITORIAL_FILES = [
    *PAGES,
    *sorted((ROOT / "src" / "components").glob("*.astro")),
    *sorted(DOWNLOADS.rglob("*.md")),
    *sorted(DOWNLOADS.rglob("*.yaml")),
    *sorted((ROOT / "docs").rglob("*.md")),
    ROOT / "README.md",
    ROOT / "astro.config.mjs",
]
for path in EDITORIAL_FILES:
    if not path.is_file():
        continue
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if "—" in line:
            record(path, f"linha {lineno}: travessão (use dois-pontos, vírgula ou parênteses)")

# Terminology: one concept, one term. Each rule: variant pattern, preferred term,
# and the pages where the variant is allowed (references and their sources).
TERM_RULES = [
    (r"\bcasos? de fronteira\b|\bedge cases?\b", "caso-limite", 0, ()),
    (r"\bvalidade\b", "vigência", re.I, ()),
    (r"\bID da revisão\b|\brevis(?:ão|ões) (?:`?\d|histórica|anterior|vigente|específica)", "versão (revisão é só o ato de revisar)", re.I, ()),
    (r"\bdonos?\b", "responsável ou quem aprova", re.I, ()),
    (r"\baprovador(?:a|es)?\b", "quem aprova", re.I, ()),
    (r"\bpropriet[aá]ri[oa]s?\b", "responsável ou quem aprova", re.I, ()),
    (r"\bpend[eê]ncias?\b", "pergunta em aberto", re.I, ()),
    (r"\bpendentes?\b(?! de aprovação)", "em aberto (o estado do documento é 'pendente de aprovação')", re.I, ()),
    (r"\bpain[eé]is\b|\bpainel\b", "dashboard", re.I, ()),
    (r"\brespostas? de refer[eê]ncia\b", "gabarito ou resposta esperada", re.I, ()),
    (r"\bjoins?\b", "junção (JOIN só no SQL)", 0, ()),
    (r"\belicita\w*", "descobrir ou perguntar", re.I, ("referencias/index.mdx",)),
    (r"\bbriefing\b", "brief", re.I, ()),
    (r"\bm[eé]tricas?\b", "indicador", re.I, ("referencias/index.mdx",)),
    (r"\bconjuntos? de dados\b", "dataset", re.I, ()),
]
SOURCE_SECTION = re.compile(r"^#{2,4} (Fundamentação|Referências|Fontes)", re.I)


def visible_lines(path: Path):
    """Yield (lineno, text) for prose a reader sees; code, URLs and YAML keys are skipped."""
    text = path.read_text(encoding="utf-8")
    in_code = in_front = in_sources = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if path.suffix in (".md", ".mdx"):
            if lineno == 1 and line == "---":
                in_front = True
                continue
            if in_front:
                if line == "---":
                    in_front = False
                elif re.match(r"(title|description):", line):
                    yield lineno, line.split(":", 1)[1]
                continue
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code or line.startswith("import "):
                continue
            if re.match(r"^#{2,4} ", line):
                in_sources = bool(SOURCE_SECTION.match(line))
            if in_sources:
                continue
            line = re.sub(r"`[^`]*`", " ", line)
            line = re.sub(r"\]\([^)]*\)", "]", line)
            line = re.sub(r"https?://\S+", " ", line)
            if "IIBA" in line:
                continue
            yield lineno, line
        elif path.suffix == ".astro":
            parts = re.findall(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"|>([^<>{}]+)<", line)
            yield lineno, " ".join("".join(p) for p in parts)
        elif path.suffix == ".yaml":
            line = re.sub(r"^\s*-?\s*[a-z_0-9]+:\s*", "", line)
            yield lineno, re.sub(r"[\w.-]+\.(sql|yaml|csv|md)\b", " ", line)


TERM_FILES = [
    *PAGES,
    *sorted((ROOT / "src" / "components").glob("*.astro")),
    *sorted(DOWNLOADS.rglob("*.md")),
    *sorted(DOWNLOADS.rglob("*.yaml")),
]
for path in TERM_FILES:
    rel = str(path.relative_to(DOCS)) if DOCS in path.parents else ""
    for lineno, line in visible_lines(path):
        for pattern, preferred, flags, allowed in TERM_RULES:
            if rel in allowed:
                continue
            m = re.search(pattern, line, flags)
            if m:
                record(path, f"linha {lineno}: \"{m.group(0)}\" fora do vocabulário; use {preferred}")

# One H1 per page: Starlight renders the frontmatter title as the page H1.
for path in PAGES:
    in_code = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code and re.match(r"^# \S", line):
            record(path, f"linha {lineno}: título H1 no corpo duplica o título da página")

if errors:
    print("\n".join("ERRO: " + error for error in errors))
    sys.exit(1)
print(f"OK: {len(PAGES)} páginas, {markdown_count} templates Markdown, "
      f"{yaml_count} arquivos YAML, rotas internas e downloads verificados.")
