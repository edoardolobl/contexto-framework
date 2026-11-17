# Direção proposta

Data: 2026-11-17 · Commit: d08c810 · Escopo: julgamento das três direções-alvo (pedagogia, consumo por IA, governança), direção recomendada, roteiro em fases, decisões do mantenedor e riscos

> **Isto é uma proposta.** Nenhum arquivo do repositório foi alterado. As afirmações sobre o repo trazem caminho, linha e citação exata, conferidas de novo nesta rodada. As demais remetem aos ids de achados (TEC, A11Y, EDI, MOD, NAV, VIS, MET, AUR) dos relatórios de dimensão desta auditoria.

## Resumo

- Três direções foram avaliadas por um juiz com cinco critérios de 1 a 5. A direção **Pedagogia** venceu com 21 pontos. **Consumo por IA** e **Governança** empataram com 19.
- A recomendação é usar a Pedagogia como esqueleto ("da pergunta ao documento aprovado") e enxertar os trilhos de verificação da Governança e as instruções ao agente da Consumo por IA.
- O Contexto passa a se apresentar como **guia e método abertos**, com uma promessa única: transformar perguntas de negócio em documentos aprovados e versionados que uma IA consegue consultar sem inventar definições.
- Os dois casos reais do mantenedor viram critério de saída: o tipo novo **Evento de coleta** e um segundo laboratório Aurora cobrem o evento raro tratado como quebrado; instruções explícitas ao agente cobrem o indicador calculado com a definição genérica.
- O roteiro tem oito fases (F0 a F7), cada uma com critério de saída. A v1.0 só sai depois de um piloto com pessoas reais reproduzindo os dois casos.
- Protocolos novos (WebMCP, UCP, Poppy) ficam em "monitorar". O núcleo de documentos não carrega nenhum campo de protocolo.

## 1. Direção recomendada pelo juiz

### 1.1 Pontuação das três propostas

| Critério | Pedagogia | Consumo por IA | Governança |
|---|---|---|---|
| (1) Aderência ao público misto não técnico | **5** | 3 | 3 |
| (2) Evita os erros dos casos reais (evento raro x quebrado; indicador genérico; cruzamento de fontes) | 4 | **5** | 4 |
| (3) Credibilidade (fundamentação, verificabilidade, versionamento) | 4 | 4 | **5** |
| (4) Custo de migração e incrementalidade | **4** | 2 | 3 |
| (5) Base para agentes, skills, MCP e WebMCP sem acoplar a protocolo imaturo | 4 | **5** | 4 |
| **Total** | **21** | 19 | 19 |

**Por que a Pedagogia venceu.** É a única que põe "como se aprende" no centro: exemplo completo comentado, depois o mesmo exemplo com campos apagados, depois o modelo com uma linha "Exemplo Aurora:" por campo (MOD-03, AUR-13), e um banco de perguntas em versão fraca e versão boa (MET-01, MET-02). Mantém o núcleo obrigatório curto, escolhe um só eixo de status e aplica YAGNI à ferramentaria: teste de paridade antes de qualquer gerador. Fraquezas: menos rigor nas instruções ao agente e fundamentação empírica deixada para o fim.

**Por que a Consumo por IA perdeu pontos.** Tem o melhor tratamento dos dois casos reais e a melhor regra de desacoplamento, mas troca o formato canônico para Markdown com frontmatter e exige "zero cópias à mão" já na primeira fase. Isso reescreve de uma vez os 10 modelos, os 20 exemplos e os validadores antes que o público veja ganho. Também renomeia `owner` para `steward`, o que quebra quem já usa os modelos.

**Por que a Governança perdeu pontos.** É a melhor em credibilidade (tabela de evidências por tipo de fonte, correções de citação, portão de v1.0, deploy condicionado ao check), mas divide o status em dois eixos, renomeia para `maintainer` e põe a migração MAJOR do schema antes da navegação. A colcha de retalhos visível ficaria no ar por muito tempo.

### 1.2 Tese da direção: "Da pergunta ao documento aprovado"

O Contexto é um **guia e método abertos** que leva o leitor de uma pergunta de negócio a um documento aprovado e versionado, testado contra a IA que ele já usa. Os modelos são ferramentas desse percurso, não o ponto de partida. A fronteira atual continua valendo: o projeto não promete enforcement e o YAML não é especificação executável.

Promessa em uma frase, igual no README, na home e no contrato:

> "Transforme perguntas de negócio em documentos aprovados e versionados que uma IA consegue consultar sem inventar definições, seja a ferramenta que você usa direto, seja o sistema que a engenharia monta."

**Base:** o esqueleto da Pedagogia (percurso, núcleo curto, moldes, incrementalidade).
**Enxerto da Governança:** CI que bloqueia o deploy, versão única do produto, ADRs, correções de citação, limite fixo do Lab 2 e portão de v1.0.
**Enxerto da Consumo por IA:** bloco de instruções ao agente, regra de adaptadores descartáveis e critérios de saída mensuráveis.

### 1.3 Evidências que ancoram a direção

**Promessa centrada num intermediário técnico (EDI-01, NAV-02)**
- [docs/CONTRATO_EDITORIAL.md:13](../docs/CONTRATO_EDITORIAL.md#L13) `para que engenheiros de IA não precisem inventar regras ausentes ou inferir significados a partir de documentos ambíguos.`
- [src/content/docs/metodo/visao-geral.mdx:10](../src/content/docs/metodo/visao-geral.mdx#L10) `O engenheiro de IA não deveria inventar essa definição.`

**Fronteira que deve ser preservada**
- [docs/CONTRATO_EDITORIAL.md:15](../docs/CONTRATO_EDITORIAL.md#L15) `Este projeto **não promete** que os modelos resolvem por si só problemas de SQL, RAG, avaliação automática ou agentes.`
- [docs/CONTRATO_EDITORIAL.md:171](../docs/CONTRATO_EDITORIAL.md#L171) `nem presumir que o YAML de negócio é uma especificação executável em qualquer plataforma.`
- [docs/CONTRATO_EDITORIAL.md:235](../docs/CONTRATO_EDITORIAL.md#L235) `5. **Documentação não é enforcement:**`

**Identidade que oscila (EDI-09)**
- [src/content/docs/index.mdx:2](../src/content/docs/index.mdx#L2) `title: "Contexto: Framework de Conhecimento para IA"`

**Menu que não parte da pergunta (NAV-03, NAV-04)**
- [astro.config.mjs:46](../astro.config.mjs#L46) `{ label: 'Comece por uma tarefa', items: ['fundamentos/comece-em-5-minutos', 'validacao/checklist', 'templates'] },`
- [astro.config.mjs:53](../astro.config.mjs#L53) `'templates/relacionamento', 'templates/dashboard', 'templates/casos-teste'`
- [astro.config.mjs:55](../astro.config.mjs#L55) `{ label: 'Entenda o método', collapsed: true, items: [`
- [src/content/docs/metodo/visao-geral.mdx:16](../src/content/docs/metodo/visao-geral.mdx#L16) `| **1. Delimitar** | Identificar o assunto, quem o usa e quando vale | Objetivo e escopo |`

**Sem schema declarado (TEC-12, TEC-18, MOD-04, MOD-05)**
- [scripts/validate_content.py:147](../scripts/validate_content.py#L147) `template_keys[data.get("type")] = set(data)`
- [scripts/validate_content.py:15](../scripts/validate_content.py#L15) `REQUIRED_TYPES = ("kpi", "conceito", "processo", "decisao", "politica", "dataset", "relacionamento", "dashboard", "rubrica", "casos-teste")`
- [public/downloads/template-kpi.yaml:3](../public/downloads/template-kpi.yaml#L3) `# Exemplos e nomes de campos são convenções propostas, não um padrão universal.`

**O objetivo do documento com nomes diferentes em cada modelo (MOD-05)**
- [public/downloads/template-decisao.yaml:22](../public/downloads/template-decisao.yaml#L22) `decision_question: null`
- [public/downloads/template-dataset.yaml:25](../public/downloads/template-dataset.yaml#L25) `business_purpose: null`
- [public/downloads/template-dashboard.yaml:24](../public/downloads/template-dashboard.yaml#L24) `supported_decisions: []`

**Versionamento com tensão (MET-08)**
- [docs/CONTRATO_EDITORIAL.md:122](../docs/CONTRATO_EDITORIAL.md#L122) `| Correção só de texto | A mesma |`
- [public/downloads/template-kpi.yaml:18](../public/downloads/template-kpi.yaml#L18) `supersedes_revision: null` (só existe ponteiro para trás)

**O projeto não segue a própria regra de versão (EDI-19, MET-13)**
- [package.json:4](../package.json#L4) `"version": "0.4.0",`
- [README.md:13](../README.md#L13) `## O que existe na v0.4`
- [docs/CONTRATO_EDITORIAL.md:3](../docs/CONTRATO_EDITORIAL.md#L3) `**Versão:** 0.3`

**Deploy sem validadores (TEC-10)**
- [.github/workflows/deploy.yml:26](../.github/workflows/deploy.yml#L26) `- run: npm run build`

**Decisões sem base declarada**
- [src/content/docs/referencias/index.mdx:55](../src/content/docs/referencias/index.mdx#L55) `| Não resolver políticas conflitantes por data | Decisão própria,`
- [src/content/docs/referencias/index.mdx:57](../src/content/docs/referencias/index.mdx#L57) `| Mostrar o exemplo completo, já aprovado | Decisão própria |`
- [src/content/docs/metodo/elicitar.mdx:44](../src/content/docs/metodo/elicitar.mdx#L44) `Este roteiro de perguntas é uma adaptação original do projeto.`

**Seção duplicada no modelo KPI (EDI-29, MET-11)**
- [public/downloads/template-kpi.md:63](../public/downloads/template-kpi.md#L63) `## 8. Perguntas ainda em aberto`
- [public/downloads/template-kpi.md:66](../public/downloads/template-kpi.md#L66) `## Perguntas em aberto`

**Fonte declarada e não carregada (VIS-06)**
- [src/styles/custom.css:5](../src/styles/custom.css#L5) `--sl-font: Inter, ui-sans-serif`

**Fonte desatualizada (MET-05)**
- [README.md:79](../README.md#L79) `[KCS v6](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide)`

**Estrutura de página fixada no contrato**
- [docs/CONTRATO_EDITORIAL.md:139](../docs/CONTRATO_EDITORIAL.md#L139) `3. **Antes e depois da decisão**: o cartão com lacunas e o cartão completo`. Qualquer mudança de sequência didática passa pelo contrato primeiro.

**Ausência de mensuração.** Uma busca por "GA4", "GTM" e "tag plan" em `src/` e `public/downloads/` não retornou nenhuma ocorrência (EDI-31, NAV-01, AUR-01). Ausência não tem linha para citar; a afirmação vale para o commit d08c810.

### 1.4 O que manter

- **id separado do ID da versão e vigência em intervalo semiaberto.** [public/downloads/template-kpi.yaml:17](../public/downloads/template-kpi.yaml#L17) `valid_to: null  # fim exclusivo da vigência`
- **A tríade Confirmado / Relatado / Em aberto** e os desfechos answer / clarify / abstain no gabarito.
- **`not_synonyms` no Conceito**, um diferencial frente aos catálogos.
- **Laboratório Aurora 1 (conversão)**, com aritmética recalculada em SQLite. Cobre o caso 2.
- **Adaptação honesta de DMN no modelo Decisão.** `required_inputs` passa a apontar para o documento de origem.
- **Verificação de links no HTML final e o CI de PR.**
- **Componentes com valor próprio:** ExampleDoc (significado antes do YAML), ReadinessChecklist e JoinDiagram, com as correções de acessibilidade.
- **Par "com lacunas / completo"** como "Antes e depois da decisão", com o rascunho em `draft` (MOD-11, AUR-09).

### 1.5 O que mudar

1. **Promessa e identidade** (EDI-01, EDI-09). Adotar a frase da seção 1.2 e trocar "Framework" no título da home por "guia e método".
2. **Navegação em percurso** (NAV-03 a NAV-07, NAV-12, NAV-13).
   - Menu: Comece aqui (tutorial de negócio e tutorial de dados, EDI-30), Percurso, Modelos, Laboratórios, Entender, Consultar, Usar com IA.
   - Percurso: 1 Escreva a pergunta de negócio; 2 Delimite o acervo; 3 Descubra o que falta (oito dimensões, entrevista "Conte o último caso"); 4 Escreva com o modelo; 5 Revise e aprove; 6 Teste com as perguntas; 7 Leve à sua ferramenta de IA.
   - Regras: prev/next declarado no percurso; bloco "Próximo passo" em toda página; entrada por sintoma na home ("A IA respondeu com dados, mas errado para o nosso contexto"); pastas iguais aos grupos, com redirecionamentos.
3. **Tipo Perguntas de negócio**, fusão do atual "Perguntas de referência" ([src/content/docs/templates/casos-teste.mdx:2](../src/content/docs/templates/casos-teste.mdx#L2) `title: Perguntas de referência`). O mesmo objeto serve de ficha de entrada e de gabarito. Ganha `phrasings`, `onboarding`, `reference_sql` opcional e `depends_on_versions` completo (MET-01, MOD-15, MOD-17, EDI-08, EDI-17, AUR-10).
4. **Tipo novo Evento de coleta (plano de mensuração)**, para o caso 1 (MOD-01, MOD-02, MOD-08, MET-07, AUR-01, NAV-01, EDI-31). Campos: gatilho, parâmetros, presença por operação, destino, `expected_behavior` (linha de base por operação, sazonalidade, tolerância ao silêncio, quando zero é normal), `missing_days_policy` e `grain_note`.
5. **Instruções ao agente** (enxerto da Consumo por IA). Bloco opcional `ai_instructions` (`sql_generation`, `question_handling`), mais `disambiguation` e, no modelo KPI, `agent_instruction_if_missing`. Duas regras explícitas:
   - "Zero em um dia não é quebra; compare com a linha de base por operação."
   - "Sem indicador aprovado, não calcule com a definição de mercado; pergunte."
6. **Cabeçalho comum e bloco `intent` único** (MOD-05, MOD-07, MET-11). Mesma ordem nos 11 tipos; `last_reviewed` e `review_interval` em todos (hoje `last_reviewed` existe só em 3 modelos, por exemplo [public/downloads/template-kpi.yaml:19](../public/downloads/template-kpi.yaml#L19) `last_reviewed: null`); `open_questions` num formato único com campos de resolução.
7. **Versionamento** (MET-08, MOD-16). MAJOR.MINOR.PATCH com versão aprovada imutável; `recorded_at`/`approved_at` separados de `valid_from`/`valid_to`; `superseded_by_revision` e `replaced_by`; cópia integral em todos os tipos; `valid_to` exclusivo também no .md.
8. **Papéis** (EDI-13, MET-10). Tabela "quem faz o quê" por extenso, com a coluna do responsável. Linha nova "Rascunho assistido por IA": a IA cria só `draft`, e só quem aprova muda o estado. Tabela de equivalência com DAMA e catálogos. Hoje: [public/downloads/template-kpi.yaml:12](../public/downloads/template-kpi.yaml#L12) `owner: null                  # cargo ou área responsável`
9. **Moldes** (AUR-02, AUR-03, AUR-04, AUR-08, AUR-14, MOD-09, MOD-12, MOD-13, MOD-22). .md preenchido para download; "Exemplo Aurora:" em cada campo crítico; valores com cara de produção (nome qualificado, fuso IANA, D+2); linha do tempo coerente, com `archival_note` fora do conteúdo aprovado; exemplos gerais ligados ao universo de analytics.
10. **Fontes únicas em dados** (TEC-12, TEC-13, TEC-14, EDI-10, MET-03). `modelos.yaml` alimenta seletor, tabela, TemplateStart, README e `REQUIRED_TYPES`; `vocabulario.yaml` é lido pelo validador; as dimensões do checklist vêm de um arquivo só.
11. **Fundamentação** (enxerto da Governança; MET-05, MET-06, MET-12, MET-14, MET-15). Tabela de evidências com BIRD, Painter et al. e Sequeda (primárias), dbt e Snowflake (marcadas como fornecedor), Spider 2.0 e BEAVER (teto do problema); ressalva do preprint 2604.25149 reescrita; Knowledge-Centered Success no lugar do KCS v6; Polanyi junto de Nonaka; linhas "Decisão própria" trocadas por ADRs datados; literatura de exemplos trabalhados e com etapas apagadas citada com a ressalva de extrapolação.
12. **Visual e acessibilidade** (VIS-01 a VIS-20, A11Y-01 a A11Y-15). Tokens completos nos dois temas; quatro primitivas (cartão, rótulo, botão, aviso); componentes nativos do Starlight onde houver equivalente; `@layer`; contraste no CI, com prioridade para A11Y-05, A11Y-08, A11Y-01 e A11Y-06; hierarquia de títulos nos componentes (A11Y-02, A11Y-15, VIS-11).

### 1.6 O que remover

- **Seção duplicada** de perguntas em aberto no `template-kpi.md` (EDI-29).
- **Duplicidade entre o seletor e a tabela** na página de modelos (NAV-14, EDI-10). Fica um só mecanismo, lido da fonte única.
- **Ficha HANDOFF-001 avulsa**, absorvida pelo formato único de `open_questions` (AUR-20, MOD-07).
- **Ressalvas e a conta 25% x 50% repetidas** em várias páginas. Concentrar numa página e linkar (EDI-22, EDI-23, EDI-25).
- **YAML visível nas páginas de guia** do percurso não técnico (NAV-08).
- **CSS morto e `!important` como estratégia** (VIS-09, VIS-13). A declaração de Inter sai se a fonte não for carregada (VIS-06).
- **Termos em inglês nos rótulos visíveis**: "template" vira "modelo" (EDI-32).

## 2. Roteiro em fases

| Fase | Conteúdo | Critério de saída |
|---|---|---|
| **F0. Decisões e trilhos** (sem mudança visível) | ADRs para promessa, conjunto de tipos, nomes de papéis, eixo de estado e formato canônico. `vocabulario.yaml` e `modelos.yaml`. CHANGELOG (Keep a Changelog) e versão única do produto. `npm run check` único, com o deploy dependendo dele, ações fixadas por SHA e Dependabot (TEC-10, TEC-16). Módulo comum dos scripts com erros reportados em vez de traceback (TEC-04, TEC-09). | ADRs aprovados. Deploy bloqueado quando um validador falha. README, package.json e contrato com a mesma versão. |
| **F1. Correções baratas e credibilidade** | Remoções da seção 1.6. Correções de citação e tabela de evidências. Contraste e anúncios de acessibilidade (A11Y-01, A11Y-05, A11Y-06, A11Y-08). Linha do tempo Aurora coerente (AUR-03, AUR-04, AUR-08, AUR-11, AUR-14, MOD-11 a MOD-13, EDI-16). | Zero linhas "Decisão própria" sem ADR. Verificador acusa referência a artefato com data posterior. Tokens com contraste AA. |
| **F2. Porta de entrada** | Tipo Perguntas de negócio (fusão com redirecionamento). Guias "Escreva a pergunta", "Delimite o acervo" e "Leve à sua ferramenta de IA" (com trecho de AGENTS.md para os times). Menu em percurso, prev/next, home por sintoma. | Card sorting com 15 pessoas ou mais e tree test com 5 a 8 tarefas, com sucesso de pelo menos 80% nas tarefas do percurso. Nenhuma página órfã ou sem saída (NAV-06). |
| **F3. Schema 1.0** (MAJOR, marcado Breaking) | JSON Schema por tipo e `common.schema.json`. Cabeçalho e `intent` únicos. SemVer, datas bitemporais e cópia integral. Validação por schema e teste de paridade .md x .yaml, sem gerador por enquanto. Modelos 0.x preservados em `historico/`. | Todos os modelos e exemplos passam no schema. Paridade verificada no CI. Tabela de migração de campos publicada. |
| **F4. Mensuração** | Tipo Evento de coleta. Blocos `expected_behavior`, `segmentation`, `data_incidents`, `ai_instructions` e `disambiguation`. Lab 2 Aurora com limite fixo (2 operações, 3 eventos, 1 evento raro só na operação A, 1 incidente, 28 dias, 1 dia ainda incompleto em D+2), recalculado em SQLite. Gabarito "quais eventos pararam?". | Caso 1 reproduzido: um agente com a documentação segmenta por operação e consulta o histórico, e sem ela erra. Resultado registrado com modelo e data. |
| **F5. Moldes e visual** (pode correr em paralelo a F2 e F3) | Sequência didática nas 11 páginas (o contrato muda primeiro). .md preenchido e "Exemplo Aurora:" por campo. Tokens, primitivas, componentes nativos, guia visual e Stylelint. | Checklist de PR em tema claro, tema escuro e 390px. Achados A11Y de severidade média fechados. |
| **F6. Saídas para máquinas** | llms.txt (só depois de confirmar a compatibilidade do plugin com a versão do Starlight). .md dos exemplos, AGENTS.md no repo, schemas publicados, URL por `id@versão`, `license` SPDX e `source_url` como campos. Crosswalk documental com ODCS 3.2.0 e Ossie 0.1.1. Página "Preparar para NotebookLM ou RAG". | Um agente que recebeu só o llms.txt responde às perguntas marcadas `onboarding`. |
| **F7. Agentes e prova** | Skills `contexto-elicitar` e `contexto-consultar`. Nota de design MCP sem código. Piloto com 2 ou 3 pessoas reproduzindo os casos 1 e 2, antes e depois (MET-16). | **Portão da v1.0:** piloto registrado e citável. |

**Regra de desacoplamento, válida em todas as fases**
- O núcleo (documentos, schema, IDs) não carrega nenhum campo de protocolo.
- Cada adaptador declara a versão alvo e pode ser descartado.
- WebMCP, UCP, Poppy e Ossie 0.3.0.dev0 ficam em "monitorar". UCP e Poppy exigem `/.well-known` e domínio próprio; por isso entram como tema que os times documentam, não como recurso do portal.

## 3. Decisões do mantenedor

1. **Foco.** O produto passa a priorizar dados e mensuração, com Política, Processo, Decisão e Rubrica como trilha secundária ligada ao caso de analytics, ou os dois trilhos ficam com peso igual (MOD-22)?
2. **Rubrica.** Fica no núcleo, vai para uma trilha complementar ou é fundida com Decisão (NAV-16, EDI-20)?
3. **Papéis.** Manter `owner`/`approver` com tabela de equivalência, renomear para `steward`/`approver` (padrão DAMA e catálogos) ou para `maintainer`/`approver`? Qualquer renomeação é Breaking.
4. **Estado do documento.** Um eixo (`draft`, `pending_approval`, `approved`, `superseded`, `deprecated`), mais simples, ou dois eixos (aprovação e ciclo de vida), mais preciso?
5. **Formato canônico.** Manter o par .yaml + .md com teste de paridade (recomendado agora) ou migrar para Markdown com frontmatter como fonte única, com o YAML gerado?
6. **Nome do tipo de perguntas.** Usar "Perguntas de negócio" para o tipo fundido? Qual slug, com redirecionamento a partir de `templates/casos-teste`?
7. **Identidade.** Tirar "Framework" do título e adotar "guia e método abertos"?
8. **Esquema de versão.** Separar a versão do produto (package.json) da versão dos modelos (`template_version`)? Qual número marca o schema 1.0?
9. **Validação com usuários.** Há acesso a pelo menos 15 pessoas do público misto para o card sorting e a 2 ou 3 para o piloto? Sem isso, F2 e o portão da v1.0 ficam sem critério de saída.
10. **Domínio próprio.** Fica fora do roadmap por enquanto? Isso adia qualquer protocolo baseado em `/.well-known`.
11. **Exemplos realistas.** Usar nomes plausíveis de projeto BigQuery, catálogo Databricks, propriedade GA4 e contêiner GTM, com aviso de ficção em todos os formatos, inclusive .sql (AUR-21)?

## 4. Riscos e mitigação

- **Modelos inflados afastarem o público não técnico.** Núcleo de cerca de 8 campos obrigatórios, blocos técnicos opcionais marcados "para quem é técnico", YAML fora do percurso e teste com usuários em F2.
- **Quebrar quem já baixou os modelos.** `template_version`, CHANGELOG com **Breaking:**, cópia dos modelos 0.x, redirecionamentos e tabela de migração de campos.
- **Ferramentaria virar produto para um mantenedor sozinho.** Teste de paridade antes de gerador (YAGNI). Gerar só .md, dicionário e dados de componentes. Fases pequenas com critério de saída.
- **Acoplamento a padrões que ainda mudam** (Ossie 0.3.0.dev0, orientação da Snowflake sobre sinônimos, Poppy e WebMCP com dias ou semanas de vida). Crosswalk só documental, com versão alvo declarada, e nada no núcleo.
- **Lab 2 crescer sem controle.** Limite fixo de escopo e o mesmo verificador SQLite.
- **Instruções para IA envelhecerem ou serem lidas como garantia.** `review_interval` obrigatório quando houver `ai_instructions`, e a ressalva de que skill e instrução orientam, mas não garantem o comportamento do agente.
- **Credibilidade empírica frágil.** Fontes primárias revisadas por pares, relatos de fornecedor marcados como tal e piloto próprio como portão da v1.0.
- **Validador rígido travar contribuições.** Separar erro de aviso (fim de semana e revisão vencida são aviso) e mensagens que citam arquivo e linha.
- **Rascunho por IA e dados sensíveis.** `access_classification` preenchido só por uma pessoa, com a regra declarada no guia de papéis.
- **Pesquisa muito recente** (até 13/11/2026). Reconferir MCP, Poppy, WebMCP e a compatibilidade do plugin de llms.txt no início de F6.

## Anexo. Resumo das três propostas

Resumo de cada proposta avaliada. Os textos completos não foram reproduzidos aqui.

### A. Pedagogia primeiro (21 pontos)

- **Tese:** o Contexto deixa de ser um catálogo de 10 modelos e vira um percurso que começa numa pergunta de negócio e termina num documento aprovado, testado contra a IA que a pessoa já usa.
- **Público:** três perfis declarados no contrato (especialista de negócio, analista de dados ou martech, quem monta agentes ou RAG). Categoria "guia e método abertos".
- **Navegação:** Comece aqui, Percurso em cinco guias numerados, Modelos, Laboratório Aurora (Lab 1 vendas, Lab 2 mensuração), Entender, Consultar, Usar com IA. Classificação das páginas pelo Diátaxis registrada no contrato.
- **Tipos:** cria Pergunta de negócio (fundida com o gabarito) e Evento de coleta; amplia KPI e Dataset; rebaixa Rubrica para trilha complementar; glossário vira índice gerado; ADR curto formalizado.
- **Formato:** JSON Schema 2020-12 por tipo como contrato; autoria em Markdown com frontmatter curto ou Google Docs; cabeçalho comum; dois níveis de exigência (núcleo e ampliado).
- **Exemplos:** sequência didática de sete passos por página (problema, perguntas, exemplo comentado, exemplo com lacunas, prática com campos apagados, downloads, referência recolhida). Banco de perguntas em versão fraca e versão boa.
- **Versionamento:** três perguntas simples para MAJOR, MINOR e PATCH; um só eixo de estado por escolha deliberada; rótulos de papéis mantidos com tabela de equivalência.
- **Agentes:** agora llms.txt, AGENTS.md, schemas e URI canônica; depois skills e crosswalk; MCP só como nota de design; WebMCP, UCP e Poppy em monitorar.
- **Ponto fraco apontado pelo juiz:** instruções ao agente sem a regra explícita de abstenção e fundamentação empírica só na última fase.

### B. Consumo por IA primeiro (19 pontos)

- **Tese:** o Contexto é a camada de autoria e descoberta que entrega a fonte aprovada para agentes, RAG, NotebookLM, catálogos e camadas semânticas. Cada fato fica num só lugar, com id e versão; o resto é gerado.
- **Promessa:** "Escreva as perguntas que a IA vai receber, registre as regras que ela não tem como adivinhar e entregue um documento que qualquer agente consiga ler e citar."
- **Navegação:** percurso de seis guias, Modelos como referência com dicionário gerado, dois laboratórios (Conversão e Tagueamento), área "Para agentes".
- **Tipos:** cria Evento de coleta (7Ws, presença por operação, `expected_behavior`, `grain_note`, `missing_days_policy`) e funde o banco de perguntas com o gabarito; remove a ficha HANDOFF; ADR só no repositório.
- **Formato:** Markdown com frontmatter como formato canônico, YAML gerado como exportação; papéis `steward` e `approver`; `schema_version`; bloco `ai_instructions` com `sql_generation` e `question_handling`.
- **Versionamento:** SemVer imutável; dois eixos de estado (aprovação e ciclo de vida); revalidação das perguntas dependentes a cada MAJOR.
- **Validação:** checagens semânticas novas e avaliação com agente antes e depois, com protocolo documentado.
- **Agentes:** regra de que o núcleo não carrega campos de protocolo e cada protocolo é um adaptador descartável.
- **Ponto fraco apontado pelo juiz:** custo de migração alto logo na F1 ("zero cópias à mão"), renomeação Breaking de papéis e frontmatter longo para o público não técnico.

### C. Credibilidade e governança primeiro (19 pontos)

- **Tese:** o projeto precisa praticar o que ensina (versão, aprovação, fonte única, verificação) antes de crescer. Transformar o Contexto num padrão de autoria versionado, e só depois adicionar tipos novos e camadas para agentes.
- **Público:** dois perfis, uma trilha; escopo principal em dados e mensuração, com negócio como trilha secundária. Identidade "guia e padrão de documentação".
- **Navegação:** percurso de sete guias, Aprender, Consultar, Entender; card sorting antes de fechar o menu.
- **Tipos:** promove Perguntas de negócio (formas "formulada" e "verificada"); cria Evento de coleta; blocos comuns reaproveitáveis em vez de tipo novo de fonte; Rubrica reavaliada.
- **Formato:** JSON Schema 2020-12 por tipo; .md para pessoas e .yaml para máquina com paridade verificada; estado em dois eixos (`approval_status` e `lifecycle`); papéis `maintainer` e `approver`.
- **Fundamentação:** tabela de evidências por tipo de fonte, correções de citação (KCS, Polanyi, origem de esclarecer e abster-se), página de correspondência com plataformas, piloto antes da v1.0.
- **Validação:** `npm run check` único com deploy condicionado; regras de governança no validador; expectativas dos laboratórios fora do código.
- **Agentes:** camadas de 0 (legível por máquina) a 4 (monitorar), com o schema nunca dependendo de adaptador.
- **Ponto fraco apontado pelo juiz:** mais carga cognitiva (dois eixos, renomeação) e migração MAJOR antes da navegação, o que mantém a colcha de retalhos visível por mais tempo.

## Fontes web mencionadas

Links das referências citadas por nome nesta direção. As demais referências (Painter et al., Sequeda, BEAVER, ODCS 3.2.0, Ossie, Poppy, UCP, DAMA, Knowledge-Centered Success) estão com link nos relatórios de dimensão desta auditoria.

- Keep a Changelog: https://keepachangelog.com/pt-BR/1.1.0/
- Versionamento Semântico: https://semver.org/lang/pt-BR/
- Diátaxis: https://diataxis.fr/
- JSON Schema 2020-12: https://json-schema.org/draft/2020-12
- Architecture Decision Records: https://adr.github.io/
- llms.txt: https://llmstxt.org/
- AGENTS.md: https://agents.md/
- Model Context Protocol: https://modelcontextprotocol.io/
- BIRD: https://bird-bench.github.io/
- Spider 2.0: https://spider2-sql.github.io/
- Preprint 2604.25149: https://arxiv.org/abs/2604.25149

## Não coberto nesta rodada

- Estimativa de esforço por fase em horas ou semanas.
- Desenho detalhado de cada JSON Schema, do tipo Evento de coleta e da tabela de migração de campos.
- Conteúdo concreto do Lab 2 Aurora (dados sintéticos, gabarito, consultas SQL).
- Teste prático do plugin de llms.txt com a versão atual do Starlight e do Astro, já que a execução de build estava bloqueada nesta sessão.
- Validação com usuários reais (card sorting, tree test, piloto); a direção depende da decisão 9.
- Verificação de comportamento de agentes (Claude Code, Codex, Antigravity) com e sem a documentação; prevista para F4 e F7.
