#!/usr/bin/env python3
"""Quality gates for the Contexto documentation, not certification of its business rules."""
from pathlib import Path
import re

import yaml

from comum import (DADOS, DOCS, DOWNLOADS, ESTADOS_DO_DOCUMENTO, ROOT, Relatorio, arquivo_de_download, carregar_dimensoes,
                   carregar_modelos, carregar_vocabulario, carregar_yaml, erros_do_markdown_de_download, exigir_minimo,
                   faltas_de_leitura, ids_citados, links_do_repositorio_ausentes, resolver_link, rota_da_pagina)

VALID_STATUSES = ESTADOS_DO_DOCUMENTO
relatorio = Relatorio()
relatorio.instalar()

PAGES = exigir_minimo([*DOCS.rglob("*.md"), *DOCS.rglob("*.mdx")], 20, "páginas em src/content/docs", relatorio)
# Tipos de documento: fonte única em src/data/modelos.yaml (níveis no ADR 0013).
MODELOS = carregar_modelos(DADOS / "modelos.yaml", relatorio)
REQUIRED_TYPES = tuple(m.slug for m in MODELOS)
# As oito dimensões do método: fonte única em src/data/dimensoes.yaml (ADR 0014).
carregar_dimensoes(DADOS / "dimensoes.yaml", relatorio)


def record(path: Path, msg: str) -> None:
    relatorio.erro(path, msg)


routes = {rota_da_pagina(p, DOCS): p for p in PAGES}
titles: dict[str, str] = {}

for path in PAGES:
    relatorio.arquivo_atual = path
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
    if isinstance(front.get("title"), str):
        titles[rota_da_pagina(path, DOCS)] = front["title"].strip()

    # Simple Markdown link check: verify routes, not remote URLs.
    for url in re.findall(r"\]\(([^)]+)\)", content):
        download = arquivo_de_download(url)
        if download:
            if not (DOWNLOADS / download).exists():
                record(path, f"download inexistente: {url}")
            continue
        # Subir além da raiz do site sai do subcaminho do projeto no GitHub Pages e resulta em 404.
        target, escaped = resolver_link(rota_da_pagina(path, DOCS), url)
        if escaped:
            record(path, f"link interno sobe além da raiz do site: {url}")
        elif target is not None and target not in routes:
            record(path, f"link interno não encontrado: {url} => {target}")

ID_PREFIXES = ("KPI-", "DATASET-", "REL-", "DASH-", "QA-", "RUBRIC-", "CONCEPT-", "PROCESS-", "DECISION-", "POLICY-", "EVENT-")
walk_references = ids_citados


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


template_keys: dict[str | None, set] = {}
example_ids: dict[str, list[str]] = {}
references: list[tuple[Path, str]] = []
loaded: dict[Path, dict] = {}
yaml_files = exigir_minimo(DOWNLOADS.glob("*.yaml"), 20, "YAML em public/downloads", relatorio)
yaml_count = len(yaml_files)
for path in yaml_files:
    data = carregar_yaml(path, relatorio)
    if data is None:
        continue
    loaded[path] = data
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
            # Regra editorial: aprovação só aparece em exemplo completo, com uma linha de aviso no topo,
            # cargo (nunca pessoa) da organização inventada e histórico de pelo menos duas versões.
            if data.get("status") != "approved":
                record(path, "exemplo completo deve estar approved")
            first_line = path.read_text(encoding="utf8").split("\n", 1)[0]
            if not first_line.startswith("# Exemplo do Contexto") or "organização inventada" not in first_line:
                record(path, "exemplo completo sem a linha de aviso no topo do arquivo")
            for key in ("owner", "approver", "source_of_truth", "valid_from", "version_date"):
                if data.get(key) in (None, "", []):
                    record(path, f"exemplo completo sem {key}")
            for key in ("owner", "approver"):
                if "(Aurora)" not in str(data.get(key)):
                    record(path, f"{key} deve ser um cargo ou área da organização fictícia Aurora")
            if data.get("open_questions"):
                record(path, "exemplo completo não deve ter open_questions")
            for falta in faltas_de_leitura(data):
                record(path, f"exemplo completo sem {falta} preenchido")
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
for path, data in loaded.items():
    if not path.name.startswith("exemplo-"):
        continue
    allowed = template_keys.get(data.get("type"), set())
    extra = sorted(set(data) - allowed)
    if extra:
        record(path, f"campos fora do template: {', '.join(extra)}")

markdown_files = exigir_minimo(DOWNLOADS.glob("*.md"), 10, "modelos Markdown em public/downloads", relatorio)
markdown_count = len(markdown_files)
for path in markdown_files:
    relatorio.arquivo_atual = path
    content = path.read_text(encoding="utf-8")
    for mensagem in erros_do_markdown_de_download(path.name, content):
        record(path, mensagem)

# Check the SQLite example links separately; they are not included in template cards.
analytics = ROOT / "src" / "components" / "AnalyticsLabDownloads.astro"
if analytics.exists():
    for filename in re.findall(r"file:\s*'([^']+)'", analytics.read_text(encoding="utf8")):
        if not (DOWNLOADS / filename).is_file():
            record(analytics, f"arquivo SQL não encontrado: {filename}")

# Cada modelo precisa de página, de título igual ao nome (rótulo canônico) e dos quatro arquivos de download.
MODELOS_YAML = DADOS / "modelos.yaml"
for modelo in MODELOS:
    pagina = DOCS / "templates" / f"{modelo.pagina}.mdx"
    if not pagina.exists():
        record(MODELOS_YAML, f"tipo {modelo.slug} sem a página templates/{modelo.pagina}.mdx")
    elif titles.get(rota_da_pagina(pagina, DOCS)) not in (None, modelo.nome):
        record(MODELOS_YAML, f"nome de {modelo.slug} ({modelo.nome!r}) difere do title de templates/{modelo.pagina}.mdx "
                             f"({titles[rota_da_pagina(pagina, DOCS)]!r})")
    for arquivo in (f"template-{modelo.slug}.md", f"template-{modelo.slug}.yaml",
                    f"exemplo-{modelo.slug}-lacunas.yaml", f"exemplo-{modelo.slug}-completo.yaml"):
        if not (DOWNLOADS / arquivo).is_file():
            record(MODELOS_YAML, f"arquivo de download ausente para {modelo.slug}: {arquivo}")

# Dados editoriais que alimentam o portal. vocabulario.yaml, contraste.yaml e artefatos.yaml ficam de fora
# de propósito: trazem os padrões proibidos.
NOVOS_DADOS = [DADOS / nome for nome in ("modelos.yaml", "percurso.yaml", "entradas.yaml", "dimensoes.yaml", "campos.yaml")]

# Editorial rule: no em dashes in published text, components, downloads or docs.
EDITORIAL_FILES = [
    *PAGES,
    *sorted((ROOT / "src" / "components").glob("*.astro")),
    *sorted(DOWNLOADS.rglob("*.md")),
    *sorted(DOWNLOADS.rglob("*.yaml")),
    *sorted((ROOT / "docs").rglob("*.md")),
    *sorted((ROOT / "src" / "modelos").rglob("*.md")),
    *sorted((ROOT / "src" / "exemplos").rglob("*.md")),
    ROOT / "README.md",
    ROOT / "astro.config.mjs",
    *NOVOS_DADOS,
]
for path in EDITORIAL_FILES:
    if not path.is_file():
        continue
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if "\u2014" in line:
            record(path, f"linha {lineno}: travessão (use dois-pontos, vírgula ou parênteses)")

# Links para arquivos do repositório (blob/main, tree/main) precisam de arquivo local correspondente.
for path in EDITORIAL_FILES:
    if path.is_file():
        for caminho in links_do_repositorio_ausentes(path.read_text(encoding="utf-8"), ROOT):
            record(path, f"link para arquivo do repositório que não existe: {caminho}")

# Terminology: one concept, one term. The rules live in src/data/vocabulario.yaml (pattern,
# preferred term and the pages where the variant is allowed: references and their sources).
TERM_RULES = [(r.padrao, r.sugestao, r.flags, r.permitido_em) for r in carregar_vocabulario(DADOS / "vocabulario.yaml", relatorio)]
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
            if re.match(r"^\s*-?\s*(pagina|slug)\s*:", line):
                continue  # endereço de página, não texto lido
            line = re.sub(r"^\s*-?\s*[a-z_0-9]+:\s*", "", line)
            yield lineno, re.sub(r"[\w.-]+\.(sql|yaml|csv|md)\b", " ", line)


TERM_FILES = [
    *PAGES,
    *sorted((ROOT / "src" / "components").glob("*.astro")),
    *sorted(DOWNLOADS.rglob("*.md")),
    *sorted(DOWNLOADS.rglob("*.yaml")),
    *NOVOS_DADOS,
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

# Fiction notices: one sentence on the home page, the section in Autoria and the first
# comment line of each example YAML. Repeating it elsewhere reads as distrust of the reader.
FICTION = re.compile(r"\bfict[íi]ci\w*|\bhipot[ée]tic\w*|\bdemonstrativ\w*|\bilustrativ\w*|\bdid[áa]tic\w*|\bfic[çc][ãa]o\b|\bexemplificativ\w*|\blaborat[óo]rio pedag[óo]gico|A Aurora não existe", re.I)
SYNTHETIC = re.compile(r"\bsint[ée]tic\w*", re.I)
FICTION_ALLOWED = {"index.mdx", "sobre/creditos.mdx"}
for path in TERM_FILES:
    rel = str(path.relative_to(DOCS)) if DOCS in path.parents else ""
    for lineno, line in visible_lines(path):
        line = re.sub(r"[\w-]+\.(yaml|md|sql)\b", " ", line)
        if path.suffix == ".yaml" and lineno == 1:
            continue
        m = FICTION.search(line)
        if m and rel not in FICTION_ALLOWED:
            record(path, f"linha {lineno}: aviso de ficção \"{m.group(0)}\" fora dos lugares combinados")
        m = SYNTHETIC.search(line)
        if m and rel != "exemplos/analytics-integrado.mdx":
            record(path, f"linha {lineno}: \"{m.group(0)}\" só no laboratório")

# Menu = título: o sidebar lista só slugs, sem rótulo próprio, e nenhuma página muda o rótulo.
CONFIG_PATH = ROOT / "astro.config.mjs"
CONFIG = CONFIG_PATH.read_text(encoding="utf8")
if "sidebar: [" not in CONFIG:
    record(CONFIG_PATH, "bloco 'sidebar: [' não encontrado; as checagens do menu não rodaram")
sidebar = CONFIG.split("sidebar: [", 1)[1] if "sidebar: [" in CONFIG else ""
if re.search(r"\bslug\s*:", sidebar):
    record(CONFIG_PATH, "item do menu com slug e rótulo próprio; use só o slug para o menu mostrar o título da página")
for modelo in MODELOS:
    if not re.search(rf"""['"]templates/{re.escape(modelo.pagina)}['"]""", sidebar):
        record(CONFIG_PATH, f"o menu não lista templates/{modelo.pagina}, que está em src/data/modelos.yaml")
for path in sorted(DOCS.rglob("*.mdx")):
    front = re.match(r"\A---\r?\n(.*?)\r?\n---", path.read_text(encoding="utf8"), re.S)
    if not front:
        continue  # a falta de frontmatter já foi registrada no início
    head = front.group(1)
    if re.search(r"^sidebar\s*:\s*\n(?:[ \t]+.*\n)*?[ \t]+label\s*:", head + "\n", re.M):
        record(path, "frontmatter 'sidebar' muda o rótulo do menu; o menu deve mostrar o título")
# Endereços que viraram redirecionamento não devem ser usados em links do portal.
moved = re.findall(r"'/([\w/-]+)/'\s*:\s*`", CONFIG)
for path in [*DOCS.rglob("*.mdx"), *(DOCS.parents[1] / "components").glob("*.astro"), *NOVOS_DADOS]:
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf8")
    for old in moved:
        if re.search(r"[(/'\"]" + re.escape(old) + r"/", text):
            record(path, f"link para endereço antigo {old}/; aponte para o destino do redirecionamento")

# One H1 per page: Starlight renders the frontmatter title as the page H1.
for path in PAGES:
    in_code = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code and re.match(r"^# \S", line):
            record(path, f"linha {lineno}: título H1 no corpo duplica o título da página")

relatorio.encerrar(f"OK: {len(PAGES)} páginas, {markdown_count} templates Markdown, "
                   f"{yaml_count} arquivos YAML, {len(REQUIRED_TYPES)} tipos, {len(TERM_RULES)} regras de vocabulário, "
                   "rotas internas e downloads verificados.")
