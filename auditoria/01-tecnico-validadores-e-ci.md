# Técnico: validadores, build e CI

Data: 2026-11-17 · Commit: d08c810 · Escopo: scripts de verificação em `scripts/`, workflows em `.github/workflows/`, `package.json`, `astro.config.mjs` e componentes Astro que leem arquivos no build ou montam links de download.

## Resumo

- A base técnica é boa: o projeto confere links como o navegador resolveria, refaz no HTML gerado a checagem contra o subcaminho publicado e recalcula em SQLite os números dos exemplos. Isso sustenta a credibilidade e deve ser mantido.
- Nenhum achado é de severidade alta. Seis são de severidade média e tratam de manutenção e crescimento, não de erro publicado hoje.
- O deploy na `main` não roda os validadores. Só os PRs rodam. Um push direto publica sem verificação (TEC-10).
- Regras e listas existem em dois ou mais lugares mantidos à mão: vocabulário (contrato e validador, já divergentes em `query`), nomes de modelos para download, normalização da base URL e expectativas de versões fixas no script (TEC-12, TEC-13, TEC-14, TEC-15, TEC-17).
- Os scripts rodam no nível do módulo, sem `main()` e sem testes, e vários caminhos de erro viram traceback em vez de mensagem que cite o arquivo. Isso pesa para quem contribui sem perfil técnico (TEC-04, TEC-09).
- Antes de acrescentar documentação para agentes, skills ou novos protocolos, vale centralizar dados (vocabulário, lista de modelos, casos de versão) e um módulo comum para os validadores.

## Pontos fortes (manter)

### Resolução de links internos fiel ao navegador, com detecção de fuga da raiz do site

Evita 404 no subcaminho do GitHub Pages. Vale manter e reaproveitar quando surgirem novas seções.

- [scripts/validate_content.py:65](../scripts/validate_content.py#L65) `# Resolve o link como o navegador faria. Subir além da raiz do site é erro:`
- [scripts/validate_content.py:84](../scripts/validate_content.py#L84) `record(path, f"link interno não encontrado: {url} => {target}")`

### Verificação do HTML final contra o subcaminho publicado

Pega o que a checagem de fonte não vê, como links gerados por componentes e o base path. É a segunda camada que mitiga vários achados abaixo.

- [scripts/check_built_links.py:35](../scripts/check_built_links.py#L35) `if BASE and not (resolved == BASE or resolved.startswith(BASE + "/")):`
- [.github/workflows/content-check.yml:35](../.github/workflows/content-check.yml#L35) `run: python scripts/check_built_links.py`

### Os scripts declaram o que não provam

A verificação não se apresenta como certificação de regra de negócio nem de acurácia de IA. Isso conversa com a promessa do contrato editorial.

- [scripts/validate_content.py:2](../scripts/validate_content.py#L2) `"""Quality gates for the Contexto documentation, not certification of its business rules."""`
- [scripts/check_revisions.py:4](../scripts/check_revisions.py#L4) `Uma versão citada no changelog não equivale a um snapshot histórico recuperável.`
- [scripts/check_analytics_fixture.py:4](../scripts/check_analytics_fixture.py#L4) `Does not test RAG, LLM accuracy, policies or live analytics systems.`

### Números dos exemplos recalculados em SQLite, não digitados

É o melhor argumento de credibilidade do projeto: o exemplo é executável. Vale generalizar para novos laboratórios.

- [scripts/check_analytics_fixture.py:19](../scripts/check_analytics_fixture.py#L19) `with sqlite3.connect(":memory:") as db:`
- [scripts/check_analytics_fixture.py:84](../scripts/check_analytics_fixture.py#L84) `# Os números citados no dicionário e nas páginas saem da amostra, não de digitação.`

### Cadeia de CI completa e dependências reproduzíveis

PyYAML fixado, `npm ci` com lockfile, permissão mínima no workflow de PR e Node 22 alinhado ao `engines`.

- [requirements.txt:1](../requirements.txt#L1) `PyYAML==6.0.3`
- [.github/workflows/content-check.yml:31](../.github/workflows/content-check.yml#L31) `run: npm ci --no-audit --no-fund`
- [.github/workflows/content-check.yml:7](../.github/workflows/content-check.yml#L7) `contents: read`

### Verificação semântica da tabela de decisão e da rubrica

Confere completude e exclusividade das regras por produto cartesiano e recalcula as notas. É uma boa base para novos tipos de documento.

- [scripts/check_decision_examples.py:35](../scripts/check_decision_examples.py#L35) `for combination in product(*domains):`
- [scripts/check_decision_examples.py:74](../scripts/check_decision_examples.py#L74) `score = round(sum(levels[k] / 4 * weights[k] for k in weights), 2)`

### Configuração de conteúdo enxuta e no padrão do Starlight

Pouco código próprio para manter na camada de conteúdo.

- [src/content.config.ts:6](../src/content.config.ts#L6) `docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),`

## Índice de achados

| ID | Severidade | Título |
|---|---|---|
| TEC-04 | Média | Caminhos que terminam em traceback em vez de erro reportado |
| TEC-09 | Média | Lógica duplicada e scripts sem `main()`, sem testes |
| TEC-10 | Média | `deploy.yml` publica sem rodar validadores; permissões e ações pouco endurecidas |
| TEC-12 | Média | Validador acoplado por regex à formatação de componentes e do `astro.config` |
| TEC-14 | Média | Vocabulário controlado duplicado entre o validador e o contrato editorial, já divergente |
| TEC-17 | Média | Expectativas de negócio fixas em `check_revisions.py` não escalam para novos tipos de documento |
| TEC-01 | Baixa | Link de download validado só pelo nome do arquivo e só para .yaml, .md e .pdf |
| TEC-02 | Baixa | Links internos que começam com `/` são ignorados pelo validador de fonte |
| TEC-03 | Baixa | Checagens que imprimem OK sem piso mínimo de itens verificados |
| TEC-05 | Baixa | `check_built_links.py`: regex limitada a `<a>` com aspas duplas, sem decodificação |
| TEC-06 | Baixa | `TERM_RULES` e `visible_lines` com falsos negativos e positivos previsíveis |
| TEC-07 | Baixa | `check_decision_examples.py`: calibração pulada na rubrica não aprovada e KeyError em vez de erro |
| TEC-08 | Baixa | `check_analytics_fixture.py`: mensagem de sucesso fixa e páginas conferidas por substring |
| TEC-11 | Baixa | `ExampleDoc` e `RevisionComparison` leem YAML por `process.cwd()` sem tratamento de erro |
| TEC-13 | Baixa | Nomes de download em `TemplateFinder` e `TemplateStart` fora da validação direta |
| TEC-15 | Baixa | Base URL: normalização duplicada em 9 componentes e redirects sem normalizar a barra |
| TEC-16 | Baixa | `package.json` sem script único de verificação; README omite `check_revisions.py` |
| TEC-18 | Baixa | Modelo Markdown só é conferido por duas seções, sem paridade com o YAML |

## Achados

### TEC-04 · Caminhos que terminam em traceback em vez de erro reportado

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Em `validate_content.py`, o YAML é validado com `try/except` na primeira passada (linha 134), mas é lido de novo sem proteção na linha 191. Se o arquivo já tinha falhado antes (YAML inválido ou raiz que não é mapa), o script quebra ali com `YAMLError` ou `AttributeError` e nunca imprime os erros acumulados. `split("---", 2)[1]` gera `IndexError` em .mdx sem frontmatter (caso já registrado na linha 39), e `CONFIG.index("sidebar: [")` gera `ValueError` se a formatação mudar. Os dois derrubam o script. Em `check_revisions.py`, `data.get` é chamado direto sobre `yaml.safe_load`, e a linha 83 faz `date.fromisoformat(data["valid_from"])`, que dá `KeyError` ou `ValueError` numa versão aprovada sem `valid_from` ou com data inválida, casos que a linha 67 e a função `day()` já tinham registrado como erro.

**Evidências:**

- [scripts/validate_content.py:191](../scripts/validate_content.py#L191) `data = yaml.safe_load(path.read_text(encoding="utf8"))`
- [scripts/validate_content.py:345](../scripts/validate_content.py#L345) `head = path.read_text(encoding="utf8").split("---", 2)[1]`
- [scripts/validate_content.py:341](../scripts/validate_content.py#L341) `sidebar = CONFIG[CONFIG.index("sidebar: ["):]`
- [scripts/check_revisions.py:37](../scripts/check_revisions.py#L37) `data = yaml.safe_load(path.read_text(encoding="utf-8"))`
- [scripts/check_revisions.py:83](../scripts/check_revisions.py#L83) `approved.append((date.fromisoformat(data["valid_from"]),`

**Impacto:** Quem edita um YAML com erro (muitas vezes público não técnico, via PR) recebe um stack trace sem o arquivo nem a linha e perde as outras mensagens úteis. Isso piora a experiência de contribuição.

**Recomendação:** Reaproveitar os dados já lidos (um dicionário de caminho para dados) em vez de ler de novo. Tratar frontmatter ausente e a âncora do sidebar como erro reportado. Concentrar o carregamento de YAML numa função única que devolve erro formatado com o caminho do arquivo.

### TEC-09 · Lógica duplicada e scripts sem `main()`, sem testes

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Os 5 scripts repetem `ROOT`, a lista `errors` e o bloco final de impressão e `sys.exit`, e quatro deles repetem o carregamento de YAML. Não há `main()` nem funções importáveis que devolvam erros, o que impede teste unitário. `validate_content.py` tem 370 linhas executadas no import. Não existe diretório `tests/` nem arquivo `test_*.py` para os validadores. `check_revisions.py` importa `re` no meio do arquivo.

**Evidências:**

- [scripts/validate_content.py:17](../scripts/validate_content.py#L17) `errors: list[str] = []`
- [scripts/check_decision_examples.py:13](../scripts/check_decision_examples.py#L13) `errors = []`
- [scripts/check_analytics_fixture.py:14](../scripts/check_analytics_fixture.py#L14) `errors = []`
- [scripts/check_revisions.py:147](../scripts/check_revisions.py#L147) `import re`
- [scripts/check_built_links.py:14](../scripts/check_built_links.py#L14) `ROOT = Path(__file__).resolve().parents[1]`

**Impacto:** Cada validador evolui sozinho. Não dá para escrever um teste que prove que o validador falha com entrada inválida. Novos tipos de documento (agentes, skills) vão aumentar a duplicação.

**Recomendação:** Extrair um módulo comum (por exemplo `scripts/_common.py` com `ROOT`, `load_yaml` com erro formatado e um `Report`). Cada script expõe `check(root) -> list[str]` e `main()`. Adicionar alguns testes com fixtures mínimas boas e ruins para cada validador.

### TEC-10 · `deploy.yml` publica sem rodar validadores; permissões e ações pouco endurecidas

**Severidade:** Média (rebaixada de alta na verificação)

**Confiança:** Alta

**O que acontece:** O deploy em push na `main` roda só `npm ci` e build, sem os validadores nem a checagem de links do HTML. O `content-check` roda só em `pull_request` e `workflow_dispatch`, então um push direto na `main` publica sem verificação. As permissões `pages: write` e `id-token: write` estão no nível do workflow e valem também para o job de build, que não precisa delas. As ações são referenciadas por tag móvel (`@v4`, `@v5`), não por SHA. O diretório `.github` só tem `workflows/`, sem `dependabot.yml`. Os jobs não têm `timeout-minutes`.

**Evidências:**

- [.github/workflows/deploy.yml:26](../.github/workflows/deploy.yml#L26) `- run: npm run build`
- [.github/workflows/content-check.yml:3](../.github/workflows/content-check.yml#L3) `pull_request:`
- [.github/workflows/deploy.yml:10](../.github/workflows/deploy.yml#L10) `pages: write`
- [.github/workflows/deploy.yml:11](../.github/workflows/deploy.yml#L11) `id-token: write`
- [.github/workflows/deploy.yml:21](../.github/workflows/deploy.yml#L21) `- uses: actions/checkout@v4`
- [.github/workflows/deploy.yml:38](../.github/workflows/deploy.yml#L38) `uses: actions/deploy-pages@v4`

**Impacto:** Conteúdo que quebra o vocabulário, o YAML ou um link pode ir ao ar por push direto, o que contradiz o portão de qualidade que o projeto anuncia. Foi rebaixado de alta porque o fluxo por PR roda todos os checks e as ações referenciadas são oficiais do GitHub, o que reduz o risco de cadeia de suprimentos.

**Recomendação:** Fazer o deploy depender dos mesmos checks (reaproveitar o `content-check` via `workflow_call` ou `needs`). Mover `pages` e `id-token` para o job de deploy. Fixar as ações por SHA com a versão em comentário e habilitar Dependabot para `github-actions`, npm e pip.

**Observação da verificação:** Não verifiquei a proteção de branch no GitHub, que poderia exigir PR e reduzir o risco de push direto.

### TEC-12 · Validador acoplado por regex à formatação de componentes e do `astro.config`

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** A checagem de downloads extrai os nomes com `href:\s*'...'` (só aspas simples) em `TemplateDownloads` e `file:\s*'...'` em `AnalyticsLabDownloads`. A lista de redirects sai de uma regex que exige chave entre aspas simples e valor em template literal. Se alguém trocar as aspas, usar crase ou reformatar, o `findall` devolve lista vazia e nenhum erro aparece, porque nada confere se a extração encontrou algo. A âncora `sidebar: [` é diferente: ela não falha em silêncio, derruba o script com `ValueError` (ver TEC-04).

**Evidências:**

- [scripts/validate_content.py:209](../scripts/validate_content.py#L209) `for filename in re.findall(r"href:\s*'([^']+)'", component):`
- [scripts/validate_content.py:216](../scripts/validate_content.py#L216) `for filename in re.findall(r"file:\s*'([^']+)'", analytics.read_text(encoding="utf8")):`
- [scripts/validate_content.py:349](../scripts/validate_content.py#L349) `moved = re.findall(r"'/([\w/-]+)/'`
- [astro.config.mjs:11](../astro.config.mjs#L11) `` '/exemplos/conceito-onboarding/': `${base}/templates/conceito/`, ``

**Impacto:** A checagem imprime OK sem ter verificado nada. Uma ferramenta de formatação que troque as aspas desliga três controles de uma vez.

**Recomendação:** Mover as listas (downloads, redirects) para dados estruturados (JSON ou YAML em `src/data`) lidos pelos componentes e pelo validador. Enquanto isso, exigir um mínimo de itens extraídos e falhar abaixo dele.

### TEC-14 · Vocabulário controlado duplicado entre o validador e o contrato editorial, já divergente

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Os termos preferidos e proibidos existem como tabela em `docs/CONTRATO_EDITORIAL.md` e como `TERM_RULES` em `validate_content.py`, mantidos à mão. O contrato afirma que o validador recusa as formas da coluna "Não usar", mas as duas listas já divergem: a tabela proíbe `query` (use "consulta") e `TERM_RULES` não tem nenhuma regra para `query` (a busca por `query` em `validate_content.py` não retorna nada).

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:58](../docs/CONTRATO_EDITORIAL.md#L58) ``O validador (`scripts/validate_content.py`) recusa as formas da coluna “Não usar” fora da bibliografia.``
- [docs/CONTRATO_EDITORIAL.md:54](../docs/CONTRATO_EDITORIAL.md#L54) `| Pedido ao banco | consulta | query |`
- [docs/CONTRATO_EDITORIAL.md:41](../docs/CONTRATO_EDITORIAL.md#L41) `| Caso no limite da regra | caso-limite | caso de fronteira, edge case, casos limites |`
- [scripts/validate_content.py:248](../scripts/validate_content.py#L248) `(r"\bcasos? de fronteira\b|\bedge cases?\b|\bcasos? limites?\b", "caso-limite", re.I, ()),`

**Impacto:** O contrato promete uma regra que o código não aplica, o que mina a credibilidade do contrato editorial.

**Recomendação:** Tornar um arquivo de dados (por exemplo `vocabulario.yaml`) a fonte única: o validador lê esse arquivo, e a tabela do contrato é gerada ou conferida contra ele.

### TEC-17 · Expectativas de negócio fixas em `check_revisions.py` não escalam para novos tipos de documento

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O script codifica IDs e datas de documentos específicos (`CONCEPT-ONBOARDING-001`, `KPI-AURORA-001`, `QA-AURORA-001`, 2026-10-01) e a comparação entre 30 e 60 dias. Cada novo exemplo com versões exige editar o script, e exemplos novos (de agentes ou skills) não ganham a checagem de seleção por vigência automaticamente.

**Evidências:**

- [scripts/check_revisions.py:107](../scripts/check_revisions.py#L107) `("CONCEPT-ONBOARDING-001", "2026-07-25", []),`
- [scripts/check_revisions.py:120](../scripts/check_revisions.py#L120) `LAB_DAY = date(2026, 10, 1)`
- [scripts/check_revisions.py:154](../scripts/check_revisions.py#L154) `return re.sub(r"\b(?:30|60) dias\b", "N dias", value)`

**Impacto:** Aumenta o custo de crescer o projeto. A base para as próximas camadas precisa ser parametrizada para não virar mais um remendo.

**Recomendação:** Mover as expectativas (consultas por data, data do laboratório, par de versões comparáveis) para um arquivo de casos declarado junto aos exemplos e deixar o script genérico.

### TEC-01 · Link de download validado só pelo nome do arquivo e só para .yaml, .md e .pdf

**Severidade:** Baixa (rebaixada na verificação)

**Confiança:** Alta

**O que acontece:** A checagem de downloads em Markdown ignora o caminho relativo e compara só `Path(rel_url).name` com `public/downloads`. Um link com profundidade errada (`../downloads` no lugar de `../../downloads`) passa no validador de fonte. Links para .sql ou .csv não entram nesse ramo e cairiam na resolução de rotas, que não os encontraria. Hoje não existe nenhum link Markdown para .sql ou .csv: todos os links de download no conteúdo apontam para .md.

**Evidências:**

- [scripts/validate_content.py:60](../scripts/validate_content.py#L60) `if "downloads" in rel_url and rel_url.endswith((".yaml", ".md", ".pdf")):`
- [scripts/validate_content.py:61](../scripts/validate_content.py#L61) `file = DOWNLOADS / Path(rel_url).name`
- [src/content/docs/templates/index.mdx:16](../src/content/docs/templates/index.mdx#L16) `](../downloads/template-conceito.md)`

**Impacto:** Um link de download quebrado só aparece depois do build (`check_built_links.py`), com mensagem sobre o HTML e não sobre o .mdx de origem.

**Recomendação:** Resolver o caminho relativo contra a rota da página e conferir que o destino existe em `public/`. Cobrir qualquer extensão que não seja rota. Manter `check_built_links.py` como segunda camada.

**Observação da verificação:** Mitigado. A checagem de links no HTML gerado roda no CI depois do build, então hoje o erro seria pego tarde, mas não passaria.

### TEC-02 · Links internos que começam com `/` são ignorados pelo validador de fonte

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A regex de exclusão trata `/` como externo. Um link absoluto como `/templates/kpi/` não é conferido e, no GitHub Pages com base `/contexto-framework`, daria 404. Hoje não há nenhum no conteúdo (a busca por `](/` em `src/content` não retornou nada), então o risco é latente.

**Evidências:**

- [scripts/validate_content.py:55](../scripts/validate_content.py#L55) `if re.match(r"^(https?:|mailto:|#|/)", url):`

**Impacto:** Um autor novo que copie de outra documentação pode introduzir link absoluto sem aviso na etapa de fonte.

**Recomendação:** Tratar `/` como erro explícito ("use link relativo") ou validar contra o base. O `check_built_links.py` já reprova no HTML, então a mudança serve para avisar mais cedo e na linha certa.

### TEC-03 · Checagens que imprimem OK sem piso mínimo de itens verificados

**Severidade:** Baixa (rebaixada na verificação)

**Confiança:** Alta

**O que acontece:** `check_built_links.py` imprime OK mesmo com 0 links conferidos, por exemplo se a regex deixar de casar com o HTML gerado ou se `dist/` não tiver .html. `validate_content.py` não exige que `PAGES` tenha itens. `check_revisions.py` imprime `len(FILES)` sem exigir mínimo, mas as expectativas fixas e a busca do gabarito QA mitigam o caso de glob vazio.

**Evidências:**

- [scripts/check_built_links.py:45](../scripts/check_built_links.py#L45) `print(f"OK: {checked} links internos conferidos no HTML gerado.")`
- [scripts/validate_content.py:14](../scripts/validate_content.py#L14) `PAGES = sorted([*DOCS.rglob("*.md"), *DOCS.rglob("*.mdx")])`
- [scripts/validate_content.py:369](../scripts/validate_content.py#L369) `print(f"OK: {len(PAGES)} páginas, {markdown_count} templates Markdown, "`
- [scripts/check_revisions.py:182](../scripts/check_revisions.py#L182) `print(f"OK: {len(FILES)} registros, IDs de revisão únicos, intervalos não sobrepostos, "`

**Impacto:** Uma mudança de caminho (mover `src/content/docs`, por exemplo) ou de formato do HTML desliga a verificação sem falhar o CI, e a mensagem de sucesso passa falsa segurança. O risco ainda não aconteceu.

**Recomendação:** Falhar quando as contagens ficarem abaixo de um piso (páginas >= 1, links no HTML >= 1) e tratar as contagens como critério, não só como relatório.

**Observação da verificação:** Em `validate_content.py`, os modelos e exemplos anunciados são conferidos nas linhas 220 a 226. Isso cobre downloads ausentes, mas não `PAGES` vazio.

### TEC-05 · `check_built_links.py`: regex limitada a `<a>` com aspas duplas, sem decodificação

**Severidade:** Baixa (rebaixada na verificação)

**Confiança:** Alta

**O que acontece:** A regex só captura `href` entre aspas duplas em tags `<a>`. Não decodifica `%XX` nem entidades HTML (`&amp;`), e `href` sem aspas não é visto. Não confere `<link>`, `<img>` nem `<script>`, então favicons, CSS e imagens quebrados passam. Esquemas como `tel:`, `javascript:` e `data:` não são ignorados e virariam falso destino inexistente. Links atribuídos por script em tempo de execução (`TemplateFinder`) não aparecem no HTML estático.

**Evidências:**

- [scripts/check_built_links.py:29](../scripts/check_built_links.py#L29) `for href in re.findall(r'<a\s[^>]*?href="([^"]+)"', html):`
- [scripts/check_built_links.py:30](../scripts/check_built_links.py#L30) `if re.match(r"^(https?:|mailto:|#)", href):`
- [scripts/check_built_links.py:33](../scripts/check_built_links.py#L33) `target = href.split("#")[0].split("?")[0]`

**Impacto:** A lacuna real é a falta de cobertura de recursos (favicons em PNG e ICO montados no `astro.config.mjs`, imagens). Os falsos positivos por esquema ou codificação dependem de conteúdo que hoje não existe.

**Recomendação:** Trocar a regex pelo `html.parser` da biblioteca padrão, aplicar `urllib.parse.unquote` e `html.unescape`, cobrir `a`, `link`, `img`, `script` e `source`, e ignorar esquemas que não sejam HTTP.

### TEC-06 · `TERM_RULES` e `visible_lines` com falsos negativos e positivos previsíveis

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** (a) O conteúdo entre crases é removido antes da checagem, então um termo proibido dentro de crase passa. (b) Em .astro, o texto é extraído linha a linha por regex, então texto de JSX que ocupa várias linhas não é checado. (c) A linha com "IIBA" é ignorada inteira, com prosa e tudo, embora as seções de Fundamentação já sejam puladas. (d) A regra de `join` usa flags 0, então `Join` no início de frase não é pego. (e) A regra de `pendente` marca a palavra em qualquer contexto, exceto "de aprovação".

**Evidências:**

- [scripts/validate_content.py:291](../scripts/validate_content.py#L291) `` line = re.sub(r"`[^`]*`", " ", line) ``
- [scripts/validate_content.py:294](../scripts/validate_content.py#L294) `if "IIBA" in line:`
- [scripts/validate_content.py:298](../scripts/validate_content.py#L298) `parts = re.findall(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"|>([^<>{}]+)<", line)`
- [scripts/validate_content.py:258](../scripts/validate_content.py#L258) `(r"\bjoins?\b", "junção (JOIN só no SQL)", 0, ()),`
- [scripts/validate_content.py:255](../scripts/validate_content.py#L255) `(r"\bpendentes?\b(?! de aprovação)", "em aberto (o estado do documento é 'pendente de aprovação')", re.I, ()),`
- [src/content/docs/templates/rubrica.mdx:102](../src/content/docs/templates/rubrica.mdx#L102) `[IIBA](https://www.iiba.org/knowledgehub/the-business-analysis-standard/) inspira a especificação de critérios verificáveis.`

**Impacto:** O vocabulário controlado parece garantido, mas tem lacunas. A linha de IIBA em `rubrica.mdx` (linha 102) fica sob "### Fundamentação" (linha 100), seção que já é pulada, então hoje a exceção não tem efeito, mas pode esconder prosa no futuro.

**Recomendação:** Remover a exceção de IIBA, porque a seção de fontes já cobre. Usar `re.I` na regra de `join`, aceitando `JOIN` em maiúsculas só dentro de código. Para .astro, usar um parser de verdade ou declarar os textos visíveis em dados (arrays) em vez de extrair por regex.

**Observação da verificação:** Item (e): não há "pendente de revisão" em `src`, `public` nem `docs`. É risco da regra, não falha atual.

### TEC-07 · `check_decision_examples.py`: calibração pulada na rubrica não aprovada e KeyError em vez de erro

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A rubrica com lacunas sai do laço antes da calibração, então a calibração desse exemplo nunca é checada (decisão de projeto defensável). Todos os acessos são por indexação direta (`doc["required_inputs"]`, `r["when"][k]`, `rubric["criteria"]`, `rubric["scoring"]`), e um campo ausente gera `KeyError` com traceback, sem mensagem que cite o arquivo. A regra de `evidence_sufficient` está presa a `claims_with_proof >= 3`, fixo no script.

**Evidências:**

- [scripts/check_decision_examples.py:65](../scripts/check_decision_examples.py#L65) `if rubric["status"] != "approved":`
- [scripts/check_decision_examples.py:18](../scripts/check_decision_examples.py#L18) `inputs = doc["required_inputs"]`
- [scripts/check_decision_examples.py:77](../scripts/check_decision_examples.py#L77) `sufficient = levels["claims_with_proof"] >= 3`

**Impacto:** Quem criar um exemplo novo de decisão ou rubrica e esquecer um campo vê um erro técnico. A regra de negócio de suficiência de evidência fica escondida no código, e não no YAML.

**Recomendação:** Usar `.get` com mensagem por arquivo, ou validar antes com esquema (jsonschema). Mover o limiar de evidência para o YAML da rubrica, para que o exemplo o declare.

### TEC-08 · `check_analytics_fixture.py`: mensagem de sucesso fixa e páginas conferidas por substring

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A mensagem final com 25.0%, 50%, 40% e "sete perguntas" é texto fixo, não calculado. Como cada número é conferido antes (linhas 23, 30 e 86), a mensagem não mente hoje, mas fica desatualizada se um limite mudar. A checagem das páginas só procura o texto do número em qualquer parte da página, então "50%" passa dentro de "150%" ou em contexto errado.

**Evidências:**

- [scripts/check_analytics_fixture.py:23](../scripts/check_analytics_fixture.py#L23) `if not result or result[0] != 25.0:`
- [scripts/check_analytics_fixture.py:151](../scripts/check_analytics_fixture.py#L151) `print("OK: SQLite retorna 25.0% (1 de 4 sessões); pedidos por sessão dá 50% (2 de 4); "`
- [scripts/check_analytics_fixture.py:98](../scripts/check_analytics_fixture.py#L98) `if number not in text:`

**Impacto:** A garantia de que os números das páginas saem da amostra é mais fraca do que o comentário da linha 84 sugere.

**Recomendação:** Montar a mensagem final a partir dos valores calculados e procurar o número num trecho marcado (por exemplo, um componente que lê o valor do YAML) em vez de buscar substring livre. A comparação exata com 25.0 pode virar comparação com tolerância, por robustez.

### TEC-11 · `ExampleDoc` e `RevisionComparison` leem YAML por `process.cwd()` sem tratamento de erro

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** Os dois componentes montam o caminho com `process.cwd()` e chamam `readFileSync` sem `try`. Se o arquivo faltar, o build falha com `ENOENT` genérico, sem indicar a página que passou o prop `file`. O validador não confere os props `file` das chamadas `<ExampleDoc file=...>` nas .mdx, só os componentes de download.

**Evidências:**

- [src/components/ExampleDoc.astro:16](../src/components/ExampleDoc.astro#L16) `const raw = fs.readFileSync(path.join(process.cwd(), 'public', 'downloads', file), 'utf8');`
- [src/components/RevisionComparison.astro:12](../src/components/RevisionComparison.astro#L12) `const raw = fs.readFileSync(path.join(process.cwd(), 'public', 'downloads', file), 'utf8');`
- [src/content/docs/templates/kpi.mdx:40](../src/content/docs/templates/kpi.mdx#L40) `<ExampleDoc file="exemplo-kpi-lacunas.yaml" />`

**Impacto:** A falha é alta e visível (o build quebra, não publica errado), então o risco é baixo. Mas a mensagem é ruim para quem contribui, e o build depende de rodar a partir da raiz.

**Recomendação:** Resolver o caminho com uma constante compartilhada ou `new URL(..., import.meta.url)`, envolver em `try` com erro que cite o arquivo e a página, e validar os props `file` no `validate_content.py`.

### TEC-13 · Nomes de download em `TemplateFinder` e `TemplateStart` fora da validação direta

**Severidade:** Baixa (rebaixada na verificação)

**Confiança:** Média

**O que acontece:** `TemplateFinder` define os nomes de download num array próprio (campo `download:`) e os aplica por JavaScript no cliente. O validador só lê o campo `href:` de `TemplateDownloads`, então esses nomes não são conferidos diretamente. No HTML estático, o link de download do `TemplateFinder` aponta para a página `templates/`, e o `href` real só é atribuído em tempo de execução, então `check_built_links.py` também não o vê. `TemplateStart` monta o nome com `'template-' + kind + '.md'`. Mitigação: o laço de `REQUIRED_TYPES` exige que `template-{tipo}.md` exista para os 10 tipos, que são exatamente os usados nesses componentes. Renomear o arquivo é detectado. Um erro de digitação no nome dentro do `TemplateFinder` não é.

**Evidências:**

- [src/components/TemplateFinder.astro:3](../src/components/TemplateFinder.astro#L3) `{ group: 'negocio', id: 'conceito', label: 'Explicar o significado de um termo', href: 'templates/conceito/', download: 'template-conceito.md'`
- [src/components/TemplateFinder.astro:59](../src/components/TemplateFinder.astro#L59) `download.setAttribute('href', base + 'downloads/' + item.download);`
- [src/components/TemplateFinder.astro:41](../src/components/TemplateFinder.astro#L41) `<a data-download href={base + 'templates/'} download>Baixar modelo em texto <span aria-hidden="true">↓</span></a>`
- [src/components/TemplateStart.astro:86](../src/components/TemplateStart.astro#L86) `<a href={base + 'downloads/template-' + kind + '.md'} download>`
- [scripts/validate_content.py:222](../scripts/validate_content.py#L222) `expected = DOWNLOADS / f"template-{kind}{suffix}"`

**Impacto:** Os nomes dos arquivos de modelo aparecem em pelo menos quatro lugares (`TemplateDownloads`, `TemplateFinder`, `TemplateStart`, `REQUIRED_TYPES`), mantidos à mão. Um erro de digitação só no `TemplateFinder` quebra o botão de download sem que nenhum check falhe.

**Recomendação:** Manter uma lista única de modelos em dados e gerar os componentes e o `REQUIRED_TYPES` a partir dela. No mínimo, estender o validador para conferir os campos `download:` do `TemplateFinder`.

### TEC-15 · Base URL: normalização duplicada em 9 componentes e redirects sem normalizar a barra

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** Os componentes normalizam a barra final do `BASE_URL`, então não há concatenação ingênua. O problema real é o mesmo bloco repetido em 9 componentes (`AnalyticsLabDownloads`, `ExampleDoc`, `LandingHero`, `PrincipleTiles`, `RevisionComparison`, `SiteFooter`, `TemplateDownloads`, `TemplateFinder`, `TemplateStart`) e a inconsistência no `astro.config.mjs`, que normaliza no head com `replace(/\/$/, '')` mas não nos redirects, onde `${base}/` gera barra dupla se `BASE_PATH` vier com barra final ou for `/`.

**Evidências:**

- [src/components/SiteFooter.astro:4](../src/components/SiteFooter.astro#L4) `const base = raw.endsWith('/') ? raw : raw + '/';`
- [src/components/LandingHero.astro:3](../src/components/LandingHero.astro#L3) ``const base = rawBase.endsWith('/') ? rawBase : `${rawBase}/`;``
- [astro.config.mjs:11](../astro.config.mjs#L11) `` '/exemplos/conceito-onboarding/': `${base}/templates/conceito/`, ``
- [astro.config.mjs:32](../astro.config.mjs#L32) `href: base.replace(/\/$/, '') + '/favicon-32.png'`

**Impacto:** Baixo hoje, porque o padrão `/contexto-framework` não termina em barra. Vira risco ao publicar em domínio próprio com `BASE_PATH='/'`, que geraria `//templates/`.

**Recomendação:** Criar um helper único (por exemplo `src/utils/url.ts`) para links internos e usá-lo no `astro.config.mjs` e nos componentes.

### TEC-16 · `package.json` sem script único de verificação; README omite `check_revisions.py`

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** Os ranges com `^` são mitigados pelo `package-lock.json` e pelo `npm ci` no CI. Em 0.x, `^0.43.1` só aceita patches; `astro ^7.4.4` aceita minors. O ponto real é que o `package.json` só tem o script `validate:content`, sem um comando único que rode todos os validadores e o check de links, e o build não os chama. Por isso a lista local de comandos já divergiu do CI: o README lista `validate_content`, `check_decision_examples`, `check_analytics_fixture`, build e `check_built_links`, mas não `check_revisions.py`, que o CI roda.

**Evidências:**

- [package.json:14](../package.json#L14) `"@astrojs/starlight": "^0.43.1",`
- [package.json:10](../package.json#L10) `"validate:content": "python3 scripts/validate_content.py"`
- [package.json:8](../package.json#L8) `"build": "astro build",`
- [README.md:50](../README.md#L50) `python3 scripts/check_analytics_fixture.py`
- [.github/workflows/content-check.yml:26](../.github/workflows/content-check.yml#L26) `run: python scripts/check_revisions.py`

**Impacto:** Quem segue o README localmente não roda a checagem de versões e vigência e só descobre o erro no PR. Sem Dependabot, as atualizações de dependência também dependem de ação manual.

**Recomendação:** Adicionar `npm run check` (todos os validadores, build e links) e apontar o README só para ele. Automatizar as atualizações com Dependabot e documentar a política de atualização do Starlight.

### TEC-18 · Modelo Markdown só é conferido por duas seções, sem paridade com o YAML

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** Para os modelos .md, o validador só confere a ausência de frontmatter e as seções "Identificação" e "Histórico de versões". As chaves de primeiro nível dos modelos YAML são coletadas e usadas para conferir os exemplos YAML, mas nunca são comparadas com o .md do mesmo tipo, embora o projeto ofereça os dois formatos como equivalentes.

**Evidências:**

- [scripts/validate_content.py:203](../scripts/validate_content.py#L203) `for heading in ("## Identificação", "## Histórico de versões"):`
- [scripts/validate_content.py:147](../scripts/validate_content.py#L147) `template_keys[data.get("type")] = set(data)`

**Impacto:** Um campo acrescentado no YAML e esquecido no Markdown (ou o contrário) cria dois modelos divergentes para o mesmo tipo, justamente a inconsistência que o mantenedor quer eliminar.

**Recomendação:** Gerar o .md a partir do .yaml (ou o contrário) ou adicionar um teste de paridade de campos por tipo.

## Descartados na verificação

Nenhum achado foi refutado por inteiro. As partes abaixo foram descartadas e o restante ficou nos achados indicados.

- **prev-14-parcial:** a suspeita de que a base URL é concatenada à mão sem normalização não se sustenta nos componentes, porque os 9 normalizam a barra final. Sobra a duplicação e a inconsistência nos redirects (TEC-15).
- **prev-15-parcial:** o risco de cadeia de suprimentos pelo `^` é menor, porque há `package-lock.json` e o CI usa `npm ci`. Em 0.x, `^0.43.1` só aceita patches. Mantido como baixa em TEC-16.
- **prev-8-parcial:** o script não imprime OK sem checar, porque cada número da mensagem é conferido antes, e o float 25.0 é representável. Sobra só o risco da mensagem fixa e da busca por substring (TEC-08).
- **TEC-13-parcial:** o impacto original ("renomear um modelo quebra o botão sem que nenhum check falhe") não se sustenta, porque `validate_content.py`, linhas 220 a 224, exige `template-{tipo}.md` para os 10 tipos de `REQUIRED_TYPES`. Mantido como baixa, restrito a erro de digitação no array do `TemplateFinder`.
- **TEC-12-parcial:** a âncora `sidebar: [` não falha em silêncio: `CONFIG.index` gera `ValueError` e derruba o script. A regex de slug confere ausência, então lista vazia é o resultado esperado e não uma falha silenciosa. O achado ficou restrito às extrações de downloads e redirects.

## Não coberto nesta rodada

- Nenhum script, build nem CI foi executado. As conclusões vêm só da leitura do código.
- Não foram lidos `ExampleMeaning.astro`, `JoinDiagram`, `ReadinessChecklist`, `ReviewStages`, `BeforeAfter` nem `src/styles/custom.css`.
- O HTML gerado em `dist/` não foi verificado, nem se o Astro emite `href` sem aspas ou com entidades.
- Configurações do GitHub (proteção de branch, ambiente `github-pages`, Dependabot habilitado nas configurações do repositório) não foram verificadas.
- O conteúdo dos YAMLs de downloads não foi auditado além do que os validadores referenciam, nem o `package-lock.json` por vulnerabilidades conhecidas.
- Não houve pesquisa web (Exa ou outra) para comparar com boas práticas externas de validação ou CI. Nenhuma fonte web é citada neste documento.
- Não foi verificado se `valid_from` nos YAMLs está entre aspas. Sem aspas, o PyYAML devolve `date`, e `date.fromisoformat` em `check_revisions.py` daria `TypeError`.
