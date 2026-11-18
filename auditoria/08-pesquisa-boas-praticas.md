# Pesquisa de boas práticas e literatura

Data: 2026-11-17 · Commit: d08c810 · Escopo: seis frentes de pesquisa externa (camada semântica; evidência empírica e martech; agentes e protocolos; perguntas de negócio e versionamento; experiência para público misto; governança e catálogos), comparadas com os modelos, as páginas, os componentes e a configuração do portal.

## Resumo

1. A literatura primária confirma a tese central do Contexto: contexto de negócio explícito melhora muito a acurácia de IA sobre dados (BIRD, Painter et al. no JAMIA Open, Sequeda et al.). Hoje o portal apoia essa tese num único preprint de autores ligados a um fornecedor de camada semântica, e a descrição desse preprint tem uma imprecisão.
2. As plataformas (Snowflake, Databricks, dbt, Looker, BigQuery, Cube, Apache Ossie) convergem em quatro blocos que o Contexto ainda não tem: consulta verificada no formato pergunta + consulta + quem verificou; expressão de cálculo estruturada; filtros nomeados; instruções para a IA separadas entre gerar SQL e tratar a pergunta. O Contexto é mais forte que elas em governança (status, responsável por cargo, histórico de versões, vigência) e em `not_synonyms` e `answer | clarify | abstain`.
3. Os dois casos reais do mantenedor têm resposta direta na literatura e nenhuma no portal: não existe modelo de evento ou tag plan, nem campos de volume esperado, linha de base, sazonalidade e granularidade por operação (caso 1), nem instrução explícita para a IA não usar a definição de mercado de um indicador ausente ou em rascunho (caso 2).
4. A porta de entrada não parte da pergunta de negócio. O roteiro de descoberta é uma adaptação original sem método citado (GQM, Critical Decision Method, BEAM), e o bloco de objetivo aparece com cinco nomes de campo diferentes nos modelos.
5. Versionamento e governança têm base boa, mas faltam: versão imutável em três níveis, separação entre data de registro e vigência, ponteiro para a versão seguinte, prazo de revisão em todos os modelos, equivalência entre `owner`/`approver` e os papéis do DAMA, e um changelog do próprio framework.
6. Para a pauta futura (agentes, skills, WebMCP, Poppy, UCP), o que dá para fazer já sem esperar protocolo nenhum é: llms.txt, JSON Schema por tipo, URI canônica por id e versão, licença legível por máquina, AGENTS.md, empacotar o método como Agent Skills e publicar um crosswalk com ODCS e Apache Ossie. WebMCP, UCP e Poppy têm baixa relevância imediata para um portal estático em subcaminho do GitHub Pages.

## Como ler este documento

- Cada prática tem um ID por frente: CS (camada semântica), EM (evidência e martech), AG (agentes e protocolos), PV (perguntas e versionamento), UX (público misto), GC (governança e catálogos).
- Todas as práticas listadas foram conferidas nas fontes por um verificador. O que ficou sem confirmação está em "Não verificado" ao fim de cada frente. Afirmações removidas pelo verificador estão em "Descartados na verificação".
- A confiança é a do verificador (alta ou média). Nenhuma prática foi testada com usuários reais nem executada no repositório: build, scripts e npm estavam bloqueados nesta sessão.
- As evidências do repositório trazem caminho, linha e citação exata. As fontes web trazem link completo. A lista completa de fontes está no fim.
- Os nomes de campos YAML propostos aqui são sugestões das frentes, não decisões. Vários se sobrepõem entre frentes; ver "Convergências entre frentes".

## Pontos fortes (manter)

- **Separação entre assunto e versão, com histórico de dependências.** As perguntas de referência registram de qual versão de cada documento dependem, o que nenhuma plataforma pesquisada oferece.
  - [public/downloads/exemplo-casos-teste-completo.yaml:37](../public/downloads/exemplo-casos-teste-completo.yaml#L37) `depends_on_versions:`
  - [src/content/docs/fundamentos/como-ler-os-campos.mdx:29](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L29) `duas versões nunca compartilham o mesmo ID`
- **Critério de nova versão baseado no resultado.** Equivale ao MAJOR do SemVer e é fácil de explicar a quem não é técnico.
  - [src/content/docs/fundamentos/como-ler-os-campos.mdx:86](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L86) `**alguém que aplicar a regra nova chega a um resultado diferente em algum caso?**`
- **Sinônimos separados de termos relacionados e de não sinônimos.** Combina com o Knowledge Catalog e o SKOS; `not_synonyms` não tem equivalente nativo nas fontes consultadas.
  - [public/downloads/template-conceito.yaml:31](../public/downloads/template-conceito.yaml#L31) `synonyms: []`
  - [public/downloads/template-conceito.yaml:33](../public/downloads/template-conceito.yaml#L33) `not_synonyms: []`
- **Comportamento esperado com três saídas.** `answer | clarify | abstain` cobre mais que os benchmarks dos fornecedores, que só avaliam respostas.
  - [public/downloads/template-casos-teste.yaml:31](../public/downloads/template-casos-teste.yaml#L31) `expected_behavior: null  # answer | clarify | abstain`
- **Honestidade sobre o que o YAML não é.** O portal não se apresenta como especificação executável nem como DMN.
  - [public/downloads/template-dataset.yaml:1](../public/downloads/template-dataset.yaml#L1) `# Convenção documental, não é schema executável de fornecedor.`
  - [src/content/docs/templates/decisao.mdx:82](../src/content/docs/templates/decisao.mdx#L82) `O modelo é **simplificado e autoral**: não usa a notação DMN nem sua semântica de execução`
- **Granularidade e risco de duplicação na junção.** Cobre uma falha silenciosa que o preprint da Cube descreve.
  - [src/content/docs/exemplos/analytics-integrado.mdx:60](../src/content/docs/exemplos/analytics-integrado.mdx#L60) `O erro está em não declarar a **granularidade**, o que uma linha representa.`
  - [public/downloads/exemplo-dataset-completo.yaml:93](../public/downloads/exemplo-dataset-completo.yaml#L93) `invalid_aggregations: ["Contar sessões com COUNT(*) após junção 1:N sem avaliar duplicidade"]`

## Como as frentes respondem aos dois casos reais

| Caso | O que faltou | Práticas que resolvem |
|---|---|---|
| 1. Evento raro marcado como quebrado (tag plan no Google Sheets contra Databricks) | Regra para quebrar por operação, olhar o histórico e tratar raridade | EM-07, EM-08, EM-09, EM-04, CS-05, PV-03, PV-04, AG-08, GC-04 |
| 2. Indicador calculado com a definição genérica do treinamento | Definição aprovada do time ao alcance da IA e instrução de não improvisar | EM-12, CS-05, GC-06, AG-05, AG-06, EM-03 |

## Índice de práticas

| ID | Frente | Prática | Confiança |
|---|---|---|---|
| CS-01 | Camada semântica | Valores amostrais, lista completa e sinônimos só para jargão | média |
| CS-02 | Camada semântica | Consulta verificada como par pergunta + consulta | alta |
| CS-03 | Camada semântica | Expressão de cálculo estruturada | alta |
| CS-04 | Camada semântica | Filtros nomeados e reutilizáveis | alta |
| CS-05 | Camada semântica | Instruções para a IA separadas por finalidade | alta |
| CS-06 | Camada semântica | Dimensão de tempo e granularidade explícitas | média |
| CS-07 | Camada semântica | Relacionamento com lado muitos e lado um | média |
| CS-08 | Camada semântica | Glossário ligado a colunas | média |
| CS-09 | Camada semântica | Conjunto de avaliação com consulta e paráfrases | alta |
| CS-10 | Camada semântica | Curadoria por domínio e ocultação de campos técnicos | média |
| CS-11 | Camada semântica | Mapeamento de exportação para formatos de plataforma | média |
| EM-01 | Evidência e martech | Ampliar a base empírica | alta |
| EM-02 | Evidência e martech | Descrever o preprint 2604.25149 com precisão | média |
| EM-03 | Evidência e martech | Quatro categorias de evidência do BIRD como checklist | alta |
| EM-04 | Evidência e martech | Padrões de desambiguação e quando pedir esclarecimento | alta |
| EM-05 | Evidência e martech | Perguntas com SQL, formulações e medição antes e depois | alta |
| EM-06 | Evidência e martech | Definições estruturadas antes de texto livre | média |
| EM-07 | Evidência e martech | Modelo de evento (tag plan) | alta |
| EM-08 | Evidência e martech | Distinguir evento quebrado de evento raro | alta |
| EM-09 | Evidência e martech | Frescor, latência e dado tardio estruturados | alta |
| EM-10 | Evidência e martech | Reconciliação entre mídia e analytics | alta |
| EM-11 | Evidência e martech | Manter e estender granularidade e duplicação | alta |
| EM-12 | Evidência e martech | Bloquear a definição genérica de indicador | média |
| AG-01 | Agentes e protocolos | llms.txt e versões Markdown | alta |
| AG-02 | Agentes e protocolos | JSON Schema por tipo e cabeçalho comum | alta |
| AG-03 | Agentes e protocolos | URI canônica por id e versão | média |
| AG-04 | Agentes e protocolos | Licença e procedência legíveis por máquina | alta |
| AG-05 | Agentes e protocolos | AGENTS.md no repositório e para os times | alta |
| AG-06 | Agentes e protocolos | Método empacotado como Agent Skills | alta |
| AG-07 | Agentes e protocolos | Nota de design para MCP | média |
| AG-08 | Agentes e protocolos | Vínculo com servidores MCP de dados | alta |
| AG-09 | Agentes e protocolos | Crosswalk com ODCS, ODPS e Apache Ossie | alta |
| AG-10 | Agentes e protocolos | Preparar documentos para RAG e NotebookLM | alta |
| AG-11 | Agentes e protocolos | Decidir sobre domínio próprio antes de /.well-known | alta |
| PV-01 | Perguntas e versionamento | Banco de perguntas de negócio baseado em GQM | alta |
| PV-02 | Perguntas e versionamento | Bloco de objetivo igual em todos os modelos | alta |
| PV-03 | Perguntas e versionamento | Descritor de indicador inspirado na ISO 22400-2 | alta |
| PV-04 | Perguntas e versionamento | BEAM e 7Ws para eventos | média |
| PV-05 | Perguntas e versionamento | Árvore de indicadores | média |
| PV-06 | Perguntas e versionamento | Entrevista por incidente crítico (CDM) | alta |
| PV-07 | Perguntas e versionamento | SECI como explicação, não como método | média |
| PV-08 | Perguntas e versionamento | Ciclo de mudança conforme BABOK e KCS | alta |
| PV-09 | Perguntas e versionamento | Versão imutável em três níveis | alta |
| PV-10 | Perguntas e versionamento | Vigência bitemporal | alta |
| PV-11 | Perguntas e versionamento | Ponteiro para a versão seguinte e descontinuação | alta |
| PV-12 | Perguntas e versionamento | ADR para desempates e decisões do framework | alta |
| PV-13 | Perguntas e versionamento | Changelog (Keep a Changelog 2.0.0) | alta |
| PV-14 | Perguntas e versionamento | Perguntas verificadas com várias formulações | alta |
| PV-15 | Perguntas e versionamento | Manter a adaptação honesta de DMN | alta |
| UX-01 | Público misto | Compasso do Diátaxis | alta |
| UX-02 | Público misto | Guia de estilo em linguagem simples | alta |
| UX-03 | Público misto | Exemplos trabalhados e exemplos com etapas apagadas | média |
| UX-04 | Público misto | Guia de preenchimento por modelo | média |
| UX-05 | Público misto | Entrada pela pergunta de negócio | alta |
| UX-06 | Público misto | Fonte única para rótulos | alta |
| UX-07 | Público misto | Card sorting e tree testing | média |
| UX-08 | Público misto | Divulgação progressiva em dois níveis | média |
| UX-09 | Público misto | Componentes nativos do Starlight e CSS controlado | alta |
| GC-01 | Governança e catálogos | Separar quem mantém de quem responde pela definição | alta |
| GC-02 | Governança e catálogos | Certificação com prazo e recertificação | alta |
| GC-03 | Governança e catálogos | Obsolescência com ponteiro para o substituto | alta |
| GC-04 | Governança e catálogos | Ligar termo ao ativo físico | alta |
| GC-05 | Governança e catálogos | YAML do repositório alimentando o catálogo | alta |
| GC-06 | Governança e catálogos | Conhecimento modelado prevalece sobre o aprendido | alta |
| GC-07 | Governança e catálogos | Rascunho por IA com aprovação humana | alta |
| GC-08 | Governança e catálogos | Sensibilidade e acesso | média |
| GC-09 | Governança e catálogos | Domínio único e hierarquia de termos | média |
| GC-10 | Governança e catálogos | DCAT 3 e schema.org como referência | média |

## Convergências entre frentes

Várias frentes chegaram à mesma recomendação por caminhos diferentes. Isso aumenta a confiança e ajuda a decidir a ordem.

| Tema | Práticas | Leitura conjunta |
|---|---|---|
| Consulta verificada (pergunta, consulta, quem verificou, quando, formulações) | CS-02, CS-09, EM-05, EM-06, PV-14 | Um único bloco comum em vez de cinco formatos diferentes |
| Instruções para a IA e desambiguação | CS-05, EM-04, EM-12 | Um bloco por finalidade: gerar consulta e tratar a pergunta |
| Modelo de evento e volume esperado | EM-07, EM-08, EM-09, PV-03, PV-04, AG-08 | Novo modelo no grupo de dados, com o caso 1 como exemplo |
| Exportação e crosswalk (Ossie, ODCS, dbt, catálogos) | CS-11, AG-09, GC-05, GC-10 | Documentar o mapeamento já; implementar depois |
| Revisão, obsolescência e substituto | PV-08, PV-11, GC-02, GC-03 | Campos comuns a todos os modelos e checados pelo validador |
| Cabeçalho comum e schema | AG-02, PV-02, PV-09, GC-09 | Definir o núcleo antes da v1 do esquema |
| Ligação com plataformas | CS-11, AG-08, GC-04 | Um único bloco (por exemplo `asset_refs` ou `platform_bindings`) |
| Pergunta de negócio como entrada | PV-01, UX-05, EM-03, PV-06 | Uma porta de entrada nova, ligada ao modelo de perguntas de referência |

## Frente 1 · Camada semântica

Como as plataformas estruturam a camada semântica para IA e como os modelos do Contexto (indicador, dataset, relacionamento, dashboard, perguntas de referência) se comparam e podem ser exportados. Sete plataformas foram lidas em fontes primárias: dbt MetricFlow, Apache Ossie (antigo OSI), Snowflake Semantic Views e Cortex Analyst, Databricks Metric Views e Genie, Looker Conversational Analytics, BigQuery Conversational Analytics e Knowledge Catalog (antigo Dataplex), e Cube.

### CS-01 · Valores amostrais, lista completa e sinônimos só para jargão

**Confiança:** média (rebaixada porque o guia da Snowflake deixou de recomendar sinônimos genéricos).

**O que é:** no Snowflake, dimensões aceitam `synonyms`, `sample_values` e `is_enum`; com `is_enum: true`, os valores amostrais viram a lista completa (só em dimensões). O guia de fevereiro de 2026 diz que sinônimos não são mais recomendados, salvo para termos próprios ou de setor. O Databricks YAML 1.1 aceita até 10 sinônimos por campo. BigQuery, Genie e Looker também registram valores e sinônimos por coluna.

**Fontes:** [Snowflake, YAML de semantic views](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec); [Snowflake, boas práticas para semantic views](https://www.snowflake.com/en/developers/guides/best-practices-semantic-views-cortex-analyst/); [Databricks, sintaxe de metric views](https://docs.databricks.com/aws/en/metric-views/data-modeling/syntax); [Databricks, instruções do Genie](https://docs.databricks.com/aws/en/genie/add-instructions); [BigQuery, contexto de agente de dados](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/data-agent-authored-context-bq); [Looker, boas práticas](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices).

**Situação no Contexto:** a coluna do dataset tem valores permitidos e exemplos, mas não tem sinônimos, e nada diz se a lista de valores é completa. No indicador, sinônimos ficam só no nível do indicador.

**Evidências:**
- [public/downloads/template-dataset.yaml:37](../public/downloads/template-dataset.yaml#L37) `allowed_values: []`
- [public/downloads/template-dataset.yaml:40](../public/downloads/template-dataset.yaml#L40) `examples: []`
- [public/downloads/template-kpi.yaml:30](../public/downloads/template-kpi.yaml#L30) `synonyms: []`

**Recomendação:** acrescentar `allowed_values_complete: true|false` (vira `is_enum` nas dimensões do Snowflake; é a parte de maior valor). Acrescentar `synonyms: []` opcional por coluna, com a orientação de usar só para jargão interno, siglas e nomes de sistema legado. Exemplo da Aurora: a sigla interna de uma operação, não "site" para web.

### CS-02 · Consulta verificada como par pergunta + consulta

**Confiança:** alta.

**O que é:** o Verified Query Repository do Snowflake guarda `name`, `question`, `sql`, `verified_by`, `verified_at` (segundos desde epoch) e `use_as_onboarding_question`, com recomendação de começar com 10 a 20 consultas. O BigQuery usa `example_queries`. No Looker, a consulta verificada é uma consulta de Explore, não SQL, com teto recomendado de 30 a 50 por agente. O Genie aceita SQL de exemplo parametrizável.

**Fontes:** [Snowflake, YAML de semantic views](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec); [Snowflake, Verified Query Repository](https://docs.snowflake.com/en/user-guide/views-semantic/verified-query-repository); [Snowflake, boas práticas](https://www.snowflake.com/en/developers/guides/best-practices-semantic-views-cortex-analyst/); [Snowflake, onboarding questions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/suggested-questions-feature); [BigQuery, contexto de agente](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/data-agent-authored-context-bq); [Looker, agentes de Explore](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-data-agents); [Databricks, instruções do Genie](https://docs.databricks.com/aws/en/genie/add-instructions).

**Situação no Contexto:** cada modelo guarda a consulta de um jeito (lista livre no indicador, nome de arquivo no dataset, texto único no relacionamento). As perguntas de referência têm pergunta e resposta esperada em texto, sem SQL. Nenhum formato liga pergunta, consulta e quem verificou.

**Evidências:**
- [public/downloads/template-kpi.yaml:63](../public/downloads/template-kpi.yaml#L63) `expected_questions_and_answers: []`
- [public/downloads/template-dataset.yaml:55](../public/downloads/template-dataset.yaml#L55) `sample_queries: []`
- [public/downloads/template-relacionamento.yaml:43](../public/downloads/template-relacionamento.yaml#L43) `verified_query: null`
- [public/downloads/exemplo-dataset-completo.yaml:98](../public/downloads/exemplo-dataset-completo.yaml#L98) `sample_queries: ["aurora-reference-query.sql"]`
- [public/downloads/template-casos-teste.yaml:32](../public/downloads/template-casos-teste.yaml#L32) `reference_answer: null`

**Recomendação:** criar um bloco comum `verified_queries: [{name, question, sql_ref ou sql, dialect, parameters, verified_by (cargo), verified_at (AAAA-MM-DD), onboarding}]` e usá-lo nos cinco modelos. Para o público não técnico, a pergunta vem primeiro e o SQL pode ficar `null`, com a pergunta em aberto registrada. Na exportação, converter a data para epoch no Snowflake; para o Looker, a consulta precisa ser refeita como Explore.

### CS-03 · Expressão de cálculo estruturada

**Confiança:** alta.

**O que é:** o dbt v1.12 tem indicadores do tipo ratio (numerador e denominador, cada um com filtro) e conversion (entidade, janela, propriedades constantes). No Ossie, toda medida tem `expression` com SQL ou dialetos. Snowflake e Databricks usam `expr`.

**Fontes:** [dbt, ratio](https://docs.getdbt.com/docs/build/ratio); [dbt, conversion](https://docs.getdbt.com/docs/build/conversion); [Apache Ossie, especificação](https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md); [Snowflake, YAML](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec); [Databricks, metric views](https://docs.databricks.com/aws/en/metric-views/data-modeling/syntax).

**Situação no Contexto:** o cálculo é só texto. Serve para leitura humana, mas não dá para exportar nem validar.

**Evidências:**
- [public/downloads/template-kpi.yaml:40](../public/downloads/template-kpi.yaml#L40) `formula_description: null`
- [public/downloads/template-kpi.yaml:45](../public/downloads/template-kpi.yaml#L45) `aggregation_rule: null`
- [public/downloads/exemplo-kpi-completo.yaml:51](../public/downloads/exemplo-kpi-completo.yaml#L51) `aggregation_rule: "Para períodos maiores, somar numeradores e denominadores dos dias e só então dividir. Não tirar média das taxas diárias"`
- [public/downloads/exemplo-kpi-completo.yaml:48](../public/downloads/exemplo-kpi-completo.yaml#L48) `denominator: "Quantidade de sessões elegíveis: channel = web e is_internal = 0"`

**Recomendação:** manter o texto e acrescentar um bloco opcional `calculation.expression` com tipo (simple, ratio, derived, cumulative, conversion), numerador, denominador, filtros referenciados e SQL com dialeto. A taxa de conversão da Aurora já é um bom ratio. Um segundo exemplo do tipo conversion com janela, comum em GA4, ajudaria.

### CS-04 · Filtros nomeados e reutilizáveis

**Confiança:** alta.

**O que é:** o Snowflake tem `filters` com nome, sinônimos, descrição e expressão; o guia diz que filtros são pouco usados e críticos para a acurácia. O Genie tem SQL expressions do tipo filtro. O Looker prefere valores de filtro padrão no LookML. O dbt aplica filtro por componente.

**Fontes:** [Snowflake, YAML](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec); [Snowflake, boas práticas](https://www.snowflake.com/en/developers/guides/best-practices-semantic-views-cortex-analyst/); [Databricks, instruções do Genie](https://docs.databricks.com/aws/en/genie/add-instructions); [Looker, boas práticas](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices); [dbt, ratio](https://docs.getdbt.com/docs/build/ratio).

**Situação no Contexto:** o dashboard guarda filtros como mapa sem nome nem descrição, e o indicador descreve exclusões em texto. O mesmo filtro (tráfego interno) se repete sem identificador comum.

**Evidências:**
- [public/downloads/template-dashboard.yaml:26](../public/downloads/template-dashboard.yaml#L26) `default_filters: {}`
- [public/downloads/exemplo-dashboard-completo.yaml:40](../public/downloads/exemplo-dashboard-completo.yaml#L40) `is_internal: 0`
- [public/downloads/template-kpi.yaml:37](../public/downloads/template-kpi.yaml#L37) `exclusions: []`

**Recomendação:** acrescentar `named_filters: [{id, name, description, expr, synonyms}]` no dataset; indicador e dashboard apontam para o id (por exemplo `FILTER-AURORA-EXCLUI-INTERNO`). O Ossie 0.3.0.dev0 não tem construto de filtro: exportar como campo booleano descrito ou em `nonportable_extensions`.

### CS-05 · Instruções para a IA separadas por finalidade

**Confiança:** alta.

**O que é:** o Snowflake separa `sql_generation` de `question_categorization` e diz que o erro mais comum é misturar os dois. Genie, Looker e BigQuery dizem para usar texto livre só no que a estrutura não cobre; o Looker lembra que instrução em texto envelhece. O Ossie tem `ai_context.instructions`. O Cube tem `meta.ai_context`, até 2.000 caracteres, com truncamento silencioso e ignorado no nível do cube.

**Fontes:** [Snowflake, custom instructions](https://docs.snowflake.com/en/user-guide/views-semantic/custom-instructions); [Snowflake, boas práticas](https://www.snowflake.com/en/developers/guides/best-practices-semantic-views-cortex-analyst/); [Databricks, instruções do Genie](https://docs.databricks.com/aws/en/genie/add-instructions); [Looker, boas práticas](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices); [BigQuery, contexto de agente](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/data-agent-authored-context-bq); [Apache Ossie, especificação](https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md); [Cube, AI context](https://docs.cube.dev/docs/data-modeling/ai-context).

**Situação no Contexto:** nenhum modelo tem lugar para regras de interpretação dirigidas à IA; elas ficam espalhadas em ressalvas e casos-limite. As perguntas de referência já têm o equivalente ao `question_categorization`, mas isso não volta para os documentos de origem.

**Evidências:**
- [public/downloads/template-dataset.yaml:54](../public/downloads/template-dataset.yaml#L54) `known_caveats: []`
- [public/downloads/template-kpi.yaml:64](../public/downloads/template-kpi.yaml#L64) `known_edge_cases: []`
- [public/downloads/template-casos-teste.yaml:31](../public/downloads/template-casos-teste.yaml#L31) `expected_behavior: null  # answer | clarify | abstain`
- [public/downloads/exemplo-casos-teste-completo.yaml:68](../public/downloads/exemplo-casos-teste-completo.yaml#L68) `expected_behavior: clarify`

**Recomendação:** acrescentar `ai_instructions: {sql_generation: [], question_handling: []}` ao dataset e ao indicador. Exemplo para o caso 1: "Antes de declarar um evento como zerado, comparar com os últimos 28 dias e quebrar por operação; evento com frequência histórica abaixo de X por dia é raro, não quebrado". As regras de `question_handling` saem das perguntas `clarify` e `abstain`. Avisar no guia que instrução em texto precisa de revisão junto com a versão do documento.

### CS-06 · Dimensão de tempo e granularidade explícitas

**Confiança:** média.

**O que é:** o dbt exige `agg_time_dimension` e granularidade na coluna de tempo. O Ossie marca `dimension.is_time`. O Snowflake separa `time_dimensions` e pede o fuso na descrição. O Looker alerta que fuso ambíguo leva a filtro ou agregação errados.

**Fontes:** [dbt, semantic models](https://docs.getdbt.com/docs/build/semantic-models); [Apache Ossie, especificação](https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md); [Snowflake, YAML](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec); [Looker, boas práticas](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices).

**Situação no Contexto:** o campo de data e a granularidade existem, o que é bom, mas são texto livre. As colunas do dataset não marcam qual é a dimensão de tempo.

**Evidências:**
- [public/downloads/template-kpi.yaml:50](../public/downloads/template-kpi.yaml#L50) `reference_date_field: null`
- [public/downloads/template-kpi.yaml:44](../public/downloads/template-kpi.yaml#L44) `granularity: null`

**Recomendação:** vocabulário controlado para granularidade (day, week, month, quarter, year) e `role: dimension|time_dimension|measure|key` em cada coluna do dataset.

### CS-07 · Relacionamento com lado muitos e lado um

**Confiança:** média.

**O que é:** no Ossie, `from` é o lado muitos e `to` o lado um, com colunas na mesma ordem. No Snowflake, a tabela da esquerda tem a chave estrangeira e há junção temporal `asof` ou `range`. No Databricks, `one_to_many` exige Runtime 18.1+ e YAML 1.1. O Cube aceita `one_to_one`, `one_to_many` e `many_to_one`.

**Fontes:** [Apache Ossie, especificação](https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md); [Snowflake, YAML](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec); [Databricks, metric views](https://docs.databricks.com/aws/en/metric-views/data-modeling/syntax); [Cube, joins](https://docs.cube.dev/reference/data-modeling/joins); [BigQuery, contexto de agente](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/data-agent-authored-context-bq).

**Situação no Contexto:** chaves, cardinalidade e regra temporal já existem, e a regra temporal e os riscos de duplicação vão além do que os fornecedores pedem. A cardinalidade não tem vocabulário fixo e não há tipo de junção.

**Evidências:**
- [public/downloads/template-relacionamento.yaml:30](../public/downloads/template-relacionamento.yaml#L30) `cardinality: null`
- [public/downloads/template-relacionamento.yaml:34](../public/downloads/template-relacionamento.yaml#L34) `temporal_join_rule: null`
- [public/downloads/template-relacionamento.yaml:29](../public/downloads/template-relacionamento.yaml#L29) `join_keys: []`

**Recomendação:** fixar `cardinality` em many_to_one, one_to_many, one_to_one ou many_to_many; acrescentar `join_type` (inner, left) e `temporal_join_type` (none, asof, range). Na exportação de um documento one_to_many, inverter os lados para Ossie e Snowflake.

### CS-08 · Glossário ligado a colunas

**Confiança:** média.

**O que é:** no Knowledge Catalog, cada termo tem sinônimos, termos relacionados, entradas ligadas (ativos e colunas), regras de qualidade e contatos. O agente de dados importa no máximo 10 termos por tabela.

**Fontes:** [Knowledge Catalog, glossário de negócio](https://docs.cloud.google.com/knowledge-catalog/docs/manage-glossaries); [BigQuery, contexto de agente](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/data-agent-authored-context-bq).

**Situação no Contexto:** o modelo de conceito já separa sinônimos, termos relacionados e não sinônimos. Falta ligar o conceito às colunas e datasets que o representam.

**Evidências:**
- [public/downloads/template-conceito.yaml:31](../public/downloads/template-conceito.yaml#L31) `synonyms: []`
- [public/downloads/template-conceito.yaml:32](../public/downloads/template-conceito.yaml#L32) `related_terms: []`
- [public/downloads/template-conceito.yaml:33](../public/downloads/template-conceito.yaml#L33) `not_synonyms: []`

**Recomendação:** acrescentar `linked_columns: ['DATASET-X.coluna']` ao conceito e avisar no guia sobre o limite de 10 termos por tabela, que obriga a priorizar.

### CS-09 · Conjunto de avaliação com consulta e paráfrases

**Confiança:** alta.

**O que é:** no Genie, cada benchmark tem pergunta, SQL opcional (necessário para avaliação automática no modo Chat) e nota de avaliação usada no modo Agent; a recomendação é de 2 a 4 formulações por pergunta, até 500 por agente. A Snowflake recomenda começar com cerca de 10 perguntas tiradas do uso real.

**Fontes:** [Databricks, benchmarks do Genie](https://docs.databricks.com/aws/en/genie/benchmarks); [Snowflake, boas práticas](https://www.snowflake.com/en/developers/guides/best-practices-semantic-views-cortex-analyst/).

**Situação no Contexto:** as perguntas de referência cobrem mais que os benchmarks (incluem `clarify` e `abstain`), mas não têm SQL nem variações de redação.

**Evidências:**
- [public/downloads/template-casos-teste.yaml:28](../public/downloads/template-casos-teste.yaml#L28) `question: null`
- [public/downloads/template-casos-teste.yaml:33](../public/downloads/template-casos-teste.yaml#L33) `required_sources: []`
- [public/downloads/exemplo-casos-teste-completo.yaml:65](../public/downloads/exemplo-casos-teste-completo.yaml#L65) `question: "Qual foi a conversão em 2026-10-01?"`

**Recomendação:** acrescentar `paraphrases: []` (2 a 4) e `reference_sql` opcional, preenchido por alguém técnico. Perguntas `answer` viram benchmarks e consultas verificadas; `clarify` e `abstain` viram regras de `question_handling`. Isso fecha o ciclo "pergunta de negócio primeiro".

### CS-10 · Curadoria por domínio e ocultação de campos técnicos

**Confiança:** média.

**O que é:** Looker recomenda agentes por domínio e esconder chaves e campos técnicos; Cube usa views pequenas e `public: false`; Snowflake recomenda organizar por domínio de negócio e incluir só colunas que o usuário vai perguntar; Genie recomenda ocultar colunas desnecessárias.

**Fontes:** [Looker, boas práticas](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices); [Cube, views](https://docs.cube.dev/docs/data-modeling/views); [Snowflake, boas práticas](https://www.snowflake.com/en/developers/guides/best-practices-semantic-views-cortex-analyst/); [Databricks, instruções do Genie](https://docs.databricks.com/aws/en/genie/add-instructions).

**Situação no Contexto:** `do_not_use_for` já é um bom equivalente semântico. Não há domínio no dataset nem marcação de exposição à IA por coluna.

**Evidências:**
- [public/downloads/template-dataset.yaml:41](../public/downloads/template-dataset.yaml#L41) `do_not_use_for: []`
- [public/downloads/template-kpi.yaml:10](../public/downloads/template-kpi.yaml#L10) `domain: null`

**Recomendação:** acrescentar `domain` ao dataset e ao dashboard, e `expose_to_ai: true|false` por coluna. No Snowflake, só fatos e indicadores têm acesso privado; dimensões ocultas simplesmente não entram.

### CS-11 · Mapeamento de exportação para formatos de plataforma

**Confiança:** média.

**O que é:** o Ossie é o único formato neutro comum: datasets com campos e medidas, relacionamentos, `ai_context` em todos os níveis e `nonportable_extensions`. O dbt v1.12 aceita documentos Ossie, e há conversores de referência no repositório apache/ossie-converters.

**Fontes:** [Apache Ossie, especificação](https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md); [apache/ossie](https://github.com/apache/ossie); [Ossie, índice de documentação](https://github.com/open-semantic-interchange/OSI/blob/main/docs/index.md); [dbt, semantic models](https://docs.getdbt.com/docs/build/semantic-models); [Snowflake, YAML](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec); [Databricks, metric views](https://docs.databricks.com/aws/en/metric-views/data-modeling/syntax); [BigQuery, contexto de agente](https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/data-agent-authored-context-bq); [Cube, AI context](https://docs.cube.dev/docs/data-modeling/ai-context).

**Situação no Contexto:** o repositório diz corretamente que não é schema executável, mas não cita Ossie, Looker nem BigQuery. O Cube aparece só como afiliação dos autores de um preprint e numa ressalva do modelo de indicador, sem link para a documentação. O campo de plataforma é texto livre.

**Evidências:**
- [public/downloads/template-dataset.yaml:1](../public/downloads/template-dataset.yaml#L1) `# Convenção documental, não é schema executável de fornecedor.`
- [src/content/docs/templates/kpi.mdx:70](../src/content/docs/templates/kpi.mdx#L70) `Não são uma norma universal nem uma especificação executável por dbt, Cube ou Snowflake.`
- [src/content/docs/referencias/index.mdx:37](../src/content/docs/referencias/index.mdx#L37) `| [dbt MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow) | Modelos de entidade, dimensão e métrica | O YAML do portal não é arquivo MetricFlow executável |`
- [src/content/docs/referencias/index.mdx:36](../src/content/docs/referencias/index.mdx#L36) `Autores vinculados à Cube, fornecedora de camada semântica.`
- [src/content/docs/referencias/index.mdx:38](../src/content/docs/referencias/index.mdx#L38) `Nosso modelo não é arquivo Snowflake válido`
- [public/downloads/template-dataset.yaml:24](../public/downloads/template-dataset.yaml#L24) `platform: null`

**Recomendação:** documentar já, e implementar depois, um mapeamento por modelo:
- Dataset: nome físico para `source` (Ossie), `base_table` (Snowflake), `source` (Databricks), `sql_table` (Cube); granularidade e finalidade para `description`; chaves para `primary_key` e `unique_keys`; valores permitidos para `sample_values` + `is_enum`; `do_not_use_for` e ressalvas para `ai_context.instructions`.
- Indicador: conceito para `description`; expressão nova (CS-03) para `metrics[].expression`, ratio do dbt, `measures.expr` ou `metrics.expr`; data de referência para `agg_time_dimension`; exclusões para filtros nomeados (CS-04).
- Relacionamento: chaves e cardinalidade para `relationships` (Ossie), `relationship_columns` (Snowflake), `joins` (Databricks); regras e riscos para `ai_context`.
- Dashboard: sem objeto equivalente; vira view do Cube ou Explore curado, e o resto vai para instruções do agente.
- Perguntas de referência: `answer` para consultas verificadas e benchmarks; `clarify` e `abstain` para `question_categorization`.
- Governança: os fornecedores cobrem partes (`verified_by`, `verified_at`, tags, contatos, `config.meta`), mas nenhum tem status, histórico de versões e vigência juntos; isso vai para `nonportable_extensions` com `vendor_name: CONTEXTO`.

Acrescentar um bloco opcional `platform_bindings: [{platform, object_ref}]`, citar Ossie, Looker, BigQuery e Cube nas referências e declarar a versão Ossie alvo (0.1.1 lançada ou 0.3.0.dev0 em rascunho).

### Não verificado nesta frente

- Se o LookML tem parâmetro `synonyms` próprio: a página de boas práticas fala em sinônimos definidos no modelo LookML, mas a visão geral não lista o parâmetro.
- Se as Metric Views do Databricks (YAML 1.1) estão em GA ou em preview; só as relações entre metric views aparecem como Beta.
- A lista de mais de 50 organizações participantes do Ossie, que é autodeclarada.
- Se a avaliação nativa no Snowsight para Cortex Analyst já está disponível.
- Campos de semantic model do dbt anteriores à v1.12.
- Versão da API e estágio do produto Conversational Analytics do BigQuery.
- Se o Genie afirma que SQL expressions dão resultado mais consistente que texto livre.
- Estágio de lançamento das consultas verificadas do Looker.
- O efeito numérico de camadas semânticas vem só do preprint Rumiantsau e Fokeev (2026), sem confirmação independente.

## Frente 2 · Evidência empírica e martech

Quanto o contexto de negócio melhora análises de dados feitas por IA, os modos de falha típicos e o que o Contexto precisa para martech (tag plan, observabilidade, reconciliação entre mídia e analytics). Uma busca textual no repositório não encontrou GA4, GTM, tag plan nem os benchmarks citados abaixo.

### EM-01 · Ampliar a base empírica

**Confiança:** alta.

**O que é:** o ganho de contexto de negócio aparece em vários estudos primários com método claro:
- BIRD (Tabela 2): GPT-4 vai de 34,88% para 54,89% com evidência externa; humanos, de 72,37% para 92,96%.
- Painter et al. (JAMIA Open, revisado por pares, 60 perguntas, autores da GSK): 8,3% só com schema, 10% com schema reduzido, 78,3% com documento de contexto de negócio.
- Sequeda et al. (data.world): de 16% para 54% com grafo de conhecimento.
- dbt 2026 (relato de fornecedor): 98,2% a 100% com camada semântica depois de modelagem mínima; quando falha, recusa em vez de devolver número plausível e errado.
- Spider 2.0 (21,3% com o1-preview) e BEAVER (10,8% com GPT-5.2, 30,1% com dicas oráculo) mostram o teto do problema corporativo.

**Fontes:** [Rumiantsau e Fokeev, arXiv 2604.25149v1](https://arxiv.org/pdf/2604.25149v1); [BIRD](https://arxiv.org/html/2305.03111); [Spider 2.0](https://arxiv.org/abs/2411.07763); [Sequeda, Allemang, Jacob](https://arxiv.org/abs/2311.07509); [BEAVER](https://arxiv.org/abs/2409.02038); [Painter et al., JAMIA Open](https://pmc.ncbi.nlm.nih.gov/articles/PMC11806702/); [Painter et al., arXiv 2406.10690v3](https://arxiv.org/html/2406.10690v3); [dbt, Semantic Layer vs. Text-to-SQL 2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026).

**Situação no Contexto:** a tese empírica se apoia num único preprint de autores ligados a fornecedor.

**Evidências:**
- [src/content/docs/dados/visao-geral.mdx:41](../src/content/docs/dados/visao-geral.mdx#L41) `Num preprint ainda sem revisão por pares, Rumiantsau e Fokeev (2026) compararam schema puro com schema mais um documento semântico em 99 perguntas.`
- [src/content/docs/referencias/index.mdx:36](../src/content/docs/referencias/index.mdx#L36) `Com um documento semântico adicional, houve ganho de 17 a 23 pontos percentuais em 99 perguntas, em três modelos`

**Recomendação:** montar uma tabela de evidências com estudos primários, relatos de fornecedor (marcados como tal) e benchmarks de teto, registrando desenho, tamanho da amostra, juiz e limite. Citar sempre a fonte primária. O preprint atribui o estudo do JAMIA a "Bayer / Zargari Marandi et al.", mas o DOI e o arXiv 2406.10690 mostram Painter, Chalamalasetti, Kassekert e Bate; não copiar citações secundárias.

### EM-02 · Descrever o preprint 2604.25149 com precisão

**Confiança:** média.

**O que é:** o preprint testou 100 perguntas e excluiu a q33 (consulta de referência não executava), ficando com 99. O juiz foi claude-sonnet-4-6, da mesma família de dois modelos testados; tentativa única com esforço médio. Sobre o documento semântico, o paper diz que o autor viu o dataset, mas não as perguntas na forma final, e que um documento totalmente cego poderia render menos.

**Fontes:** [Rumiantsau e Fokeev, arXiv 2604.25149v1](https://arxiv.org/pdf/2604.25149v1).

**Situação no Contexto:** o resto da descrição confere. A frase sobre o documento não ter sido escrito às cegas é menos matizada que o paper.

**Evidências:**
- [src/content/docs/referencias/index.mdx:36](../src/content/docs/referencias/index.mdx#L36) `O documento semântico não foi escrito às cegas em relação às perguntas.`

**Recomendação:** reescrever como "o autor do documento conhecia o dataset, mas não as perguntas na forma final; os próprios autores admitem que um documento totalmente cego poderia render menos". Acrescentar que 100 perguntas viraram 99 e que código e dados estão em https://github.com/cubedevinc/semantic-layer-benchmark.

### EM-03 · Quatro categorias de evidência do BIRD como checklist

**Confiança:** alta.

**O que é:** o BIRD classifica o conhecimento externo necessário em raciocínio numérico, conhecimento de domínio, sinônimos e ilustração de valores. É uma taxonomia simples e citável para público não técnico.

**Fontes:** [BIRD](https://arxiv.org/html/2305.03111).

**Situação no Contexto:** os campos existem, mas não estão ligados a uma taxonomia publicada; o usuário não sabe que tipo de conhecimento está faltando.

**Evidências:**
- [public/downloads/template-kpi.yaml:31](../public/downloads/template-kpi.yaml#L31) `different_meanings_in_other_domains: []`
- [src/content/docs/dados/visao-geral.mdx:16](../src/content/docs/dados/visao-geral.mdx#L16) `` - **Valores especiais:** `status='C'` é concluído ou cancelado? O que um nulo significa? ``

**Recomendação:** na página de descoberta, um quadro que mapeie as quatro categorias para perguntas de negócio e campos: fórmula para `calculation`, domínio para `business_definition`, sinônimo para `synonyms`, valor para `allowed_values` e valores especiais. Um exemplo da Aurora por categoria.

### EM-04 · Padrões de desambiguação e quando pedir esclarecimento

**Confiança:** alta.

**O que é:** no preprint, o documento semântico tinha regras explícitas de desambiguação (vendas online ou todos os canais, região do cliente ou da loja, "último trimestre" relativo a hoje ou à última data do dataset). A Databricks recomenda instruções que obriguem o agente a pedir esclarecimento quando faltar algo. A Snowflake usa filtros nomeados com sinônimos.

**Fontes:** [Rumiantsau e Fokeev](https://arxiv.org/pdf/2604.25149v1); [Snowflake, Cortex Analyst text-to-SQL](https://www.snowflake.com/en/blog/engineering/cortex-analyst-text-to-sql-accuracy-bi/); [Databricks, boas práticas do Genie](https://docs.databricks.com/aws/en/genie-agents/best-practices).

**Situação no Contexto:** o indicador tem escopo de canais, mas nenhum campo diz o que fazer quando a pergunta não especifica operação, canal ou período. `clarify` só existe nas perguntas de referência.

**Evidências:**
- [public/downloads/template-kpi.yaml:34](../public/downloads/template-kpi.yaml#L34) `included_channels: []`
- [public/downloads/template-casos-teste.yaml:31](../public/downloads/template-casos-teste.yaml#L31) `expected_behavior: null  # answer | clarify | abstain`

**Recomendação:** acrescentar ao indicador e ao dataset um bloco `disambiguation` com `defaults` (por exemplo "sem operação informada, quebrar por operação e não somar") e `ask_when` (por exemplo "pergunta sobre evento zerado sem período: perguntar a janela"). Pode ser o mesmo bloco de CS-05.

### EM-05 · Perguntas com SQL, várias formulações e medição antes e depois

**Confiança:** alta.

**O que é:** no Genie, só perguntas com SQL são avaliadas automaticamente, e a recomendação é de duas a quatro formulações. A Snowflake aceita várias consultas corretas escolhidas por humanos e diz que avaliar SQL com IA como juiz é tão difícil quanto gerar o SQL. O preprint usa desenho pareado (mesmo modelo, com e sem contexto).

**Fontes:** [Rumiantsau e Fokeev](https://arxiv.org/pdf/2604.25149v1); [Snowflake, Cortex Analyst text-to-SQL](https://www.snowflake.com/en/blog/engineering/cortex-analyst-text-to-sql-accuracy-bi/); [Databricks, monitorar Genie](https://docs.databricks.com/aws/en/genie-agents/monitor).

**Situação no Contexto:** o modelo não tem formulações alternativas nem protocolo de linha de base, e o portal declara que não atribui pontuação.

**Evidências:**
- [src/content/docs/referencias/index.mdx:41](../src/content/docs/referencias/index.mdx#L41) `Não atribuímos pontuação de RAG neste portal`
- [public/downloads/template-casos-teste.yaml:31](../public/downloads/template-casos-teste.yaml#L31) `expected_behavior: null  # answer | clarify | abstain`

**Recomendação:** acrescentar `phrasings: []` e `reference_sql` opcional. Na página de validação, um roteiro de teste pareado em cinco passos, sem prometer nota universal: rodar sem documentação, rodar com documentação, comparar, registrar data e modelo.

### EM-06 · Definições estruturadas antes de texto livre

**Confiança:** média.

**O que é:** a Databricks orienta usar SQL expressions para indicadores e filtros e consultas completas como exemplo; texto livre é último recurso. A dbt observou que, com camada semântica, a falha vira recusa em vez de número errado.

**Fontes:** [dbt, benchmark 2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026); [Databricks, boas práticas do Genie](https://docs.databricks.com/aws/en/genie-agents/best-practices); [Snowflake, Cortex Analyst text-to-SQL](https://www.snowflake.com/en/blog/engineering/cortex-analyst-text-to-sql-accuracy-bi/).

**Situação no Contexto:** `sample_queries` existe, mas não diz quais consultas foram verificadas nem por quem.

**Evidências:**
- [public/downloads/template-dataset.yaml:55](../public/downloads/template-dataset.yaml#L55) `sample_queries: []`
- [src/content/docs/dados/visao-geral.mdx:35](../src/content/docs/dados/visao-geral.mdx#L35) `Uma camada semântica **documental** registra significados em linguagem natural ou metadados.`

**Recomendação:** transformar `sample_queries` em lista de objetos (pergunta, SQL, quem verificou, quando, resultado na amostra), ou adotar o bloco de CS-02. Ensinar ao público misto três níveis: texto, consulta verificada e indicador executável.

### EM-07 · Modelo de evento (tag plan)

**Confiança:** alta.

**O que é:** os padrões de mercado convergem num núcleo comum. Avo: fontes, presença de propriedade por evento e por fonte, valores permitidos. Segment: nome, descrição, obrigatoriedade, tipo e valores validados por JSON Schema. Amplitude: status do evento (Unexpected, Valid, Invalid, Out of Date). Snowplow: SchemaVer. GA4: parâmetros personalizados precisam ser registrados como dimensões ou indicadores personalizados para aparecer em relatórios.

**Fontes:** [Avo, propriedades](https://www.avo.app/docs/data-design/avo-tracking-plan/properties); [Avo, fontes](https://www.avo.app/docs/data-design/avo-tracking-plan/define-sources-and-destinations); [Segment Protocols](https://www.twilio.com/docs/segment/protocols/tracking-plan/create); [Amplitude Observe](https://amplitude.com/docs/data/validate-events); [Snowplow, versionamento](https://docs.snowplow.io/docs/fundamentals/schemas/versioning/); [GA4, parâmetros de evento](https://developers.google.com/analytics/devguides/collection/ga4/event-parameters).

**Situação no Contexto:** o seletor de modelos lista 10 tipos e nenhum de evento. O contrato editorial menciona eventos só como grão a diferenciar.

**Evidências:**
- [src/components/TemplateFinder.astro:9](../src/components/TemplateFinder.astro#L9) `{ group: 'dados', id: 'dataset', label: 'Explicar uma tabela e seus campos'`
- [docs/CONTRATO_EDITORIAL.md:231](../docs/CONTRATO_EDITORIAL.md#L231) `diferenciar pedidos, sessões, clientes, itens e eventos antes de mostrar a conta.`

**Recomendação:** criar o modelo "Evento (tag plan)" com: nome do evento; pergunta de negócio; gatilho (ação visível e condição técnica de sucesso); fontes e plataformas; operações (marca, país, loja) com presença por operação; ambiente; parâmetros (nome, tipo, obrigatoriedade por fonte, valores permitidos, registrado como dimensão personalizada); uso como evento principal e em mídia; destinos (GA4, tabela `events_*` no BigQuery); frequência esperada por operação; raridade; versão do schema; estado da implementação; responsável; perguntas em aberto. O exemplo deve ser um evento raro que só existe na operação A.

### EM-08 · Distinguir evento quebrado de evento raro

**Confiança:** alta.

**O que é:** a Amplitude diz explicitamente que ausência de atividade não prova que um evento está obsoleto (fluxo raro, função desligada, lançamento futuro), e manda olhar dados brutos além da janela de 14 dias do Observe. A detecção de anomalia do GA4 treina com 90 dias para série diária. O Elementary permite sazonalidade por dia da semana e alerta que ignorá-la pode gerar falsos positivos; o `volume_anomalies` treina com 14 dias e só avalia períodos completos.

**Fontes:** [Amplitude, eventos planejados que nunca chegaram](https://amplitude.com/docs/data/data-assistant-user-solutions/planned-unseen-events-audit); [Amplitude Observe](https://amplitude.com/docs/data/validate-events); [GA4, detecção de anomalia](https://support.google.com/analytics/answer/9517187?hl=en); [Elementary, sazonalidade](https://docs.elementary-data.com/data-tests/anomaly-detection-configuration/seasonality); [Elementary, volume_anomalies](https://docs.elementary-data.com/data-tests/anomaly-detection-tests/volume-anomalies).

**Situação no Contexto:** o dataset tem frequência de atualização, mas nenhum campo de volume esperado, linha de base, sazonalidade ou segmentação por operação. A linha de base só aparece no exemplo de dashboard.

**Evidências:**
- [public/downloads/template-dataset.yaml:46](../public/downloads/template-dataset.yaml#L46) `update_frequency: null`
- [public/downloads/exemplo-dashboard-completo.yaml:46](../public/downloads/exemplo-dashboard-completo.yaml#L46) `comparison_baseline: "Mesmo dia da semana anterior, somente a partir de 2026-09-15, quando a definição 2.0 do KPI passou a valer"`

**Recomendação:** no modelo de evento, bloco `expected_volume` com `segment_by`, `baseline_window` (por exemplo 8 semanas), `seasonality`, `min_expected_per_period`, `silence_tolerance` (por exemplo "evento raro: só considerar quebrado após 14 dias sem disparo na operação que o implementa") e `operations_where_not_expected`. Regra explícita para agentes: "zero em um dia não é quebra; compare com a linha de base por operação".

### EM-09 · Frescor, latência e dado tardio estruturados

**Confiança:** alta.

**O que é:** no GA4, o processamento leva de 24 a 48 horas e alguns dados chegam até 7 dias depois; a exportação diária para o BigQuery não tem SLA. A dbt formaliza `warn_after` e `error_after`. O ODCS v3.2.0 tem propriedades de SLA como latência, frequência e horário de disponibilidade.

**Fontes:** [GA4, data freshness](https://support.google.com/analytics/answer/11198161?hl=en); [dbt, freshness](https://docs.getdbt.com/reference/resource-configs/freshness); [ODCS v3.2.0, SLA](https://bitol-io.github.io/open-data-contract-standard/v3.2.0/service-level-agreement/).

**Situação no Contexto:** frescor é um único campo de texto livre, e o exemplo completo não serve de molde para GA4.

**Evidências:**
- [public/downloads/template-kpi.yaml:53](../public/downloads/template-kpi.yaml#L53) `data_freshness: null`
- [public/downloads/exemplo-kpi-completo.yaml:59](../public/downloads/exemplo-kpi-completo.yaml#L59) `data_freshness: "Carga estática no laboratório"`

**Recomendação:** dividir em `expected_latency`, `late_arriving_window`, `complete_after` e `source_timezone`, com exemplo baseado no GA4: "o dia D só é considerado completo após D+2; não declarar zero para D antes disso".

### EM-10 · Reconciliação entre mídia e analytics

**Confiança:** alta.

**O que é:** segundo o Google, o Google Ads credita a conversão à data do clique e o GA4 à data da conversão. Método de contagem, colunas de conversão e janelas de 1 a 90 dias mudam os números; é preciso esperar 24 a 48 horas antes de comparar, e discrepâncias são comuns mesmo com configuração correta.

**Fontes:** [Google Ads, conversões a partir do GA](https://support.google.com/google-ads/answer/2375435?hl=en); [Google Ads, discrepâncias de dados](https://support.google.com/google-ads/answer/7457111?hl=en).

**Situação no Contexto:** o indicador registra conflitos e precedência entre fontes, mas não tem campo de atribuição. O laboratório não tem indicador de mídia.

**Evidências:**
- [public/downloads/template-kpi.yaml:59](../public/downloads/template-kpi.yaml#L59) `source_conflicts_and_precedence: []`
- [src/content/docs/governanca/papeis.mdx:29](../src/content/docs/governanca/papeis.mdx#L29) `“Qual cardinalidade, fuso e regra temporal foram verificados?”`

**Recomendação:** bloco `attribution` no indicador, só para mídia e conversão: plataforma, modelo, janela de clique e de visualização, base da data (clique ou conversão), método de contagem, coluna de conversões, fuso e divergência esperada. Um exemplo Aurora "Conversões Google Ads x GA4 em 01/10" com os dois números e a explicação.

### EM-11 · Manter e estender granularidade e duplicação

**Confiança:** alta.

**O que é:** o preprint descreve junção por caminho inválido como falha silenciosa e cita tabelas de snapshot que não podem ser somadas ao longo do tempo. A Snowflake mostra que eixos de tempo com dias faltantes fazem comparações com LEAD/LAG parecerem certas e estarem erradas.

**Fontes:** [Rumiantsau e Fokeev](https://arxiv.org/pdf/2604.25149v1); [Snowflake, Cortex Analyst text-to-SQL](https://www.snowflake.com/en/blog/engineering/cortex-analyst-text-to-sql-accuracy-bi/).

**Situação no Contexto:** bem coberto para sessão e pedido; não para eventos nem para séries com dias sem dado.

**Evidências:**
- [src/content/docs/exemplos/analytics-integrado.mdx:60](../src/content/docs/exemplos/analytics-integrado.mdx#L60) `O erro está em não declarar a **granularidade**, o que uma linha representa.`
- [public/downloads/exemplo-dataset-completo.yaml:93](../public/downloads/exemplo-dataset-completo.yaml#L93) `invalid_aggregations: ["Contar sessões com COUNT(*) após junção 1:N sem avaliar duplicidade"]`

**Recomendação:** preservar. No modelo de evento, acrescentar `grain_note` (uma linha é um disparo, não uma sessão nem um usuário) e `missing_days_policy` (dia sem linha significa zero ou falta de dado).

### EM-12 · Bloquear a definição genérica de indicador

**Confiança:** média.

**O que é:** a Snowflake diz que definições como "Daily Active Users" variam muito entre organizações, e no benchmark da Cortex o SQL só conta como certo se aplicar exatamente as medidas e filtros do modelo semântico. A Databricks recomenda definir termos de negócio como SQL expressions. O BIRD classifica isso como conhecimento de domínio. É o caso real 2.

**Fontes:** [Snowflake, Cortex Analyst text-to-SQL](https://www.snowflake.com/en/blog/engineering/cortex-analyst-text-to-sql-accuracy-bi/); [Databricks, boas práticas do Genie](https://docs.databricks.com/aws/en/genie-agents/best-practices); [BIRD](https://arxiv.org/html/2305.03111).

**Situação no Contexto:** o campo de significados divergentes existe e o exemplo é bom. Falta instruir o agente a não usar a definição de mercado quando o indicador estiver ausente ou em rascunho.

**Evidências:**
- [public/downloads/exemplo-kpi-completo.yaml:35](../public/downloads/exemplo-kpi-completo.yaml#L35) `different_meanings_in_other_domains:`
- [src/content/docs/templates/kpi.mdx:27](../src/content/docs/templates/kpi.mdx#L27) `` | “Conversão” é pedido criado, pago, confirmado ou entregue? | Evento que conta no numerador | `calculation` | ``

**Recomendação:** campo `agent_instruction_if_missing` (por exemplo "se não houver indicador aprovado, não calcule com a definição de mercado; responda que a definição não está aprovada e cite as perguntas em aberto"), ligado a uma pergunta `abstain` nas perguntas de referência.

### Não verificado nesta frente

- Atribuição padrão do Meta Ads (7 dias após clique, 1 dia após visualização): não checada em fonte primária.
- Databricks Genie 53% para 80% para 100% (Syren, 2025), AtScale 92,5% e Tiger Data +27 pp: só como citação secundária no preprint.
- Allemang e Sequeda (2024), OBQC com cerca de 72%: visto só via preprint.
- Incubação do Ossie na Apache Incubator: esta frente não confirmou pela especificação; a frente de agentes confirmou por anúncio da Snowflake e a de camada semântica pelo índice de documentação do Ossie.
- Licença da especificação UCP em si.

## Frente 3 · Agentes e protocolos

O que o portal expõe hoje a máquinas e o que fazer para chegar à pauta futura (agentes, skills, WebMCP, Poppy, UCP).

**Observação no portal:** em 17/11/2026, `/contexto-framework/llms.txt`, `llms-full.txt`, `robots.txt` e `AGENTS.md` respondem 404 no portal publicado (https://edoardolobl.github.io/contexto-framework/); `sitemap-index.xml` responde 200 porque o Starlight o gera sozinho. No repositório não existem `AGENTS.md`, `public/llms.txt` nem `public/robots.txt`.

### AG-01 · llms.txt e versões Markdown das páginas

**Confiança:** alta.

**O que é:** o llms.txt v2 é um Markdown com H1, resumo em citação e seções H2 com listas de links; pode ficar num subcaminho e vale para as páginas abaixo dele. A seção Optional reúne o que pode ser pulado. A proposta pede versão .md de cada página e sugere testar perguntando a um agente que só recebeu o arquivo. O plugin starlight-llms-txt gera `llms.txt`, `llms-full.txt` e `llms-small.txt`, com `customSets` e `optionalLinks`.

**Fontes:** [llms.txt v2](https://llmstxt.org/); [starlight-llms-txt, configuração](https://delucis.github.io/starlight-llms-txt/configuration/).

**Situação no Contexto:** a configuração registra só a integração Starlight, sem plugin de llms.txt.

**Evidências:**
- [astro.config.mjs:4](../astro.config.mjs#L4) `const base = process.env.BASE_PATH || '/contexto-framework';`
- [astro.config.mjs:7](../astro.config.mjs#L7) `site: process.env.SITE_URL || 'https://edoardolobl.github.io',`
- [astro.config.mjs:25](../astro.config.mjs#L25) `starlight({`

**Recomendação:** adotar o starlight-llms-txt com conjuntos que espelhem os grupos do menu, com Referências e Créditos em Optional, e links diretos para os YAML de exemplo e, depois, para os schemas. Antes de instalar, confirmar compatibilidade com Starlight 0.43 e Astro 7.

**Observação no portal:** ver a observação no início da frente.

### AG-02 · JSON Schema por tipo e cabeçalho comum versionado

**Confiança:** alta.

**O que é:** MCP 2026-07-28 usa JSON Schema 2020-12 por padrão em tools; WebMCP aceita JSON Schema; o ODCS publica schema oficial e media type versionado; no UCP toda capability declara uma URL de schema.

**Fontes:** [MCP, tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools); [WebMCP](https://webmachinelearning.github.io/webmcp/); [Bitol, ODCS 3.2.0 e ODPS 1.1.0](https://bitol.io/data-contracts-data-products-for-ai/); [UCP, visão geral](https://ucp.dev/latest/specification/overview/index.md).

**Situação no Contexto:** não há schema declarado; o validador deduz as chaves válidas a partir de cada modelo. O cabeçalho varia: `domain` só em indicador e perguntas de referência, `last_reviewed` só em indicador, conceito e política, separador `---` só no modelo de indicador.

**Evidências:**
- [scripts/validate_content.py:147](../scripts/validate_content.py#L147) `template_keys[data.get("type")] = set(data)`
- [public/downloads/template-kpi.yaml:3](../public/downloads/template-kpi.yaml#L3) `# Exemplos e nomes de campos são convenções propostas, não um padrão universal.`
- [public/downloads/template-kpi.yaml:5](../public/downloads/template-kpi.yaml#L5) `---`
- [public/downloads/template-kpi.yaml:10](../public/downloads/template-kpi.yaml#L10) `domain: null`
- [public/downloads/template-casos-teste.yaml:22](../public/downloads/template-casos-teste.yaml#L22) `domain: null`
- [public/downloads/template-conceito.yaml:15](../public/downloads/template-conceito.yaml#L15) `last_reviewed: null`
- [docs/CONTRATO_EDITORIAL.md:171](../docs/CONTRATO_EDITORIAL.md#L171) `nem presumir que o YAML de negócio é uma especificação executável em qualquer plataforma`

**Recomendação:** núcleo comum obrigatório (id, revision_id, type, title, status, owner, approver, version, version_date, valid_from, valid_to, supersedes_revision, last_reviewed, domain, license, source_url), um JSON Schema 2020-12 por tipo em `/contexto-framework/schemas/<tipo>.schema.json` e um campo `schema` ou `contexto_version` em cada YAML. O validador passa a validar contra os schemas. Isso não torna o YAML executável; dá a agentes e IDEs um contrato estável de leitura.

### AG-03 · URI canônica por id e versão

**Confiança:** média.

**O que é:** no MCP, cada resource tem URI única e há URI templates (RFC 6570). O ODCS 3.2.0 pede ids estáveis entre versões. A Microsoft recomenda ID e fonte por trecho recuperado para que a resposta possa citar.

**Fontes:** [MCP, resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources); [ODCS, CHANGELOG](https://github.com/bitol-io/open-data-contract-standard/blob/main/CHANGELOG.md); [Microsoft, RAG enrichment](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-enrichment-phase).

**Situação no Contexto:** o par id e revision_id é bem desenhado, mas as referências usam o id solto e não há URL por documento ou versão. As perguntas de referência já registram versões; `related_documents` não.

**Evidências:**
- [public/downloads/exemplo-kpi-completo.yaml:79](../public/downloads/exemplo-kpi-completo.yaml#L79) `related_documents: ["DATASET-AURORA-SESSIONS", "DATASET-AURORA-ORDERS"`
- [public/downloads/exemplo-casos-teste-completo.yaml:37](../public/downloads/exemplo-casos-teste-completo.yaml#L37) `depends_on_versions:`
- [src/content/docs/metodo/identificacao-versoes.mdx:69](../src/content/docs/metodo/identificacao-versoes.mdx#L69) `1. **Localize o ID certo para o domínio e a pergunta.**`

**Recomendação:** ensinar a convenção `<base>/<id>/` e `<base>/<id>/<versão>/`, publicá-la para os exemplos Aurora e aceitar `id@versão` em `related_documents`.

### AG-04 · Licença e procedência legíveis por máquina

**Confiança:** alta.

**O que é:** Agent Skills tem campo opcional `license`; a Microsoft recomenda guardar a fonte de cada trecho; a ajuda do Gemini Notebook pede não enviar documentos sem direitos.

**Fontes:** [Agent Skills, especificação](https://agentskills.io/specification); [Microsoft, RAG enrichment](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-enrichment-phase); [Gemini Notebook, fontes](https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en).

**Situação no Contexto:** a licença CC BY 4.0 está em `LICENSE-CONTENT`, mas nenhum arquivo baixado a declara como campo; os avisos de origem são comentários YAML, que se perdem no parse.

**Evidências:**
- [LICENSE-CONTENT:4](../LICENSE-CONTENT#L4) `O conteúdo deste repositório é licenciado sob a Creative Commons Attribution 4.0`
- [public/downloads/exemplo-kpi-completo.yaml:1](../public/downloads/exemplo-kpi-completo.yaml#L1) `# Exemplo do Contexto. A Aurora é uma organização inventada`
- [public/downloads/template-dataset.yaml:1](../public/downloads/template-dataset.yaml#L1) `# Convenção documental, não é schema executável de fornecedor.`

**Recomendação:** nos exemplos, `license: CC-BY-4.0` (SPDX) e `source_url` como campos. Nos modelos em branco, deixar `null` e explicar que cada time define a licença dos seus documentos.

### AG-05 · AGENTS.md no repositório e para os times

**Confiança:** alta.

**O que é:** AGENTS.md é um Markdown livre, mantido pela Agentic AI Foundation (Linux Foundation); o arquivo mais próximo do arquivo editado prevalece. O site lista Codex, Cursor, Gemini CLI, agente do GitHub Copilot e Jules, entre outros, mas não o Claude Code.

**Fontes:** [AGENTS.md](https://agents.md/).

**Situação no Contexto:** não há AGENTS.md. As regras que um agente precisa seguir estão só no contrato editorial, escrito para pessoas. O portal não ensina os times a apontar o agente deles para as definições aprovadas, que é a causa do caso 2.

**Evidências:**
- [docs/CONTRATO_EDITORIAL.md:235](../docs/CONTRATO_EDITORIAL.md#L235) `5. **Documentação não é enforcement:**`
- [src/content/docs/dados/visao-geral.mdx:35](../src/content/docs/dados/visao-geral.mdx#L35) `Serve de contexto para busca, RAG e agentes, mas não obriga o modelo a seguir cada regra.`

**Recomendação:** (1) AGENTS.md curto na raiz apontando para o contrato editorial, os comandos de validação e as regras de estados. (2) Um trecho modelo para o AGENTS.md dos times de analytics, com exemplo Aurora: "antes de calcular um indicador, abra a definição aprovada em <URL>; se não houver versão vigente, pergunte em vez de usar uma definição genérica". Para o Claude Code, que lê CLAUDE.md, conferir a documentação do produto antes de prometer compatibilidade.

### AG-06 · Método empacotado como Agent Skills

**Confiança:** alta.

**O que é:** uma skill é uma pasta com `SKILL.md` (nome em minúsculas com hífens, igual ao da pasta; descrição até 1024 caracteres dizendo quando usar) e pastas opcionais `scripts/`, `references/` e `assets/`, carregadas aos poucos; recomenda-se corpo abaixo de 500 linhas. Criado pela Anthropic e lançado como padrão aberto.

**Fontes:** [Agent Skills, especificação](https://agentskills.io/specification); [Agent Skills, visão geral](https://agentskills.io/).

**Situação no Contexto:** o roteiro de 8 perguntas e o roteiro de escolha de versão existem só para leitura humana.

**Evidências:**
- [src/content/docs/metodo/elicitar.mdx:14](../src/content/docs/metodo/elicitar.mdx#L14) `1. **Onde alguém novo costuma errar?**`
- [src/content/docs/metodo/elicitar.mdx:21](../src/content/docs/metodo/elicitar.mdx#L21) `8. **O que ainda não foi formalmente decidido?**`
- [src/content/docs/metodo/identificacao-versoes.mdx:76](../src/content/docs/metodo/identificacao-versoes.mdx#L76) `Esse roteiro é um **critério para documentar e revisar**; não implementa nem garante a recuperação correta de um RAG ou agente.`

**Recomendação:** desenhar duas skills: uma que entrevista o analista com as 8 perguntas e preenche o YAML usando `null` e perguntas em aberto, sem inventar valor; outra que, antes de responder a uma pergunta de dados, localiza o id, confere status e vigência e pede esclarecimento ou se abstém. Modelos em `assets/`, exemplos Aurora em `references/`. Manter a ressalva de que a skill orienta, mas não garante o comportamento do agente.

### AG-07 · Nota de design para MCP

**Confiança:** média.

**O que é:** no MCP, resources são contexto escolhido pela aplicação (com `audience`, `priority` e `lastModified`), prompts são acionados pelo usuário e tools são chamadas pelo modelo. A revisão 2026-07-28 removeu `initialize` e sessões; servidores implementam `server/discover`; `ttlMs` e `cacheScope` são obrigatórios em list e read; Roots, Sampling e Logging foram depreciados.

**Fontes:** [MCP 2026-07-28, changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx); [MCP, anúncio 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/); [MCP, resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources); [MCP, prompts](https://modelcontextprotocol.io/specification/2025-11-25/server/prompts).

**Situação no Contexto:** não há desenho de exposição, e o projeto declara que não certifica agentes.

**Evidências:**
- [docs/ROADMAP.md:58](../docs/ROADMAP.md#L58) `Não certifica agentes, RAG ou SQL gerado.`
- [src/content/docs/governanca/papeis.mdx:42](../src/content/docs/governanca/papeis.mdx#L42) `| Testar a aplicação em RAG ou agente | C | C | I | **A/R** |`

**Recomendação:** escrever só uma nota de design, sem código: resource template `contexto://{id}@{versão}` com `lastModified` vindo da data da versão; documentos fora de `approved` com prioridade baixa ou fora da listagem; prompts correspondentes às 8 perguntas; uma tool só de leitura `resolver_versao(id, data_referencia)`.

### AG-08 · Vínculo com servidores MCP de dados

**Confiança:** alta.

**O que é:** o BigQuery tem servidor MCP remoto com `execute_sql` e `execute_sql_readonly` (até 3.000 linhas e 3 minutos). A Databricks diz que o Genie resolve termos, indicadores e relacionamentos pelo Genie Ontology e que isso dá respostas mais precisas que SQL direto nas tabelas. O servidor do GA4 é só de leitura segundo a página oficial (o README lista ferramentas de escrita atrás de `--allow-write`). O do Google Ads monta consultas a partir de parâmetros estruturados. Todos entregam schema e execução; nenhum entrega a regra de negócio do time.

**Fontes:** [BigQuery MCP](https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp); [Databricks, MCPs](https://docs.databricks.com/aws/en/agents/mcp-tools/built-in-mcp-services); [Genie One MCP](https://docs.databricks.com/aws/en/agents/mcp-tools/genie-mcp); [GA4 MCP](https://developers.google.com/analytics/devguides/MCP); [google-analytics-mcp](https://github.com/googleanalytics/google-analytics-mcp/); [Google Ads MCP](https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server); [google-ads-mcp](https://github.com/googleads/google-ads-mcp).

**Situação no Contexto:** plataforma é texto livre, o laboratório usa SQLite e não há onde registrar o nome qualificado do objeto nem o comportamento esperado do dado (só a frequência de atualização da tabela). Foi isso que faltou no caso 1.

**Evidências:**
- [public/downloads/template-dataset.yaml:24](../public/downloads/template-dataset.yaml#L24) `platform: null`
- [public/downloads/template-dataset.yaml:46](../public/downloads/template-dataset.yaml#L46) `update_frequency: null`
- [public/downloads/exemplo-dataset-completo.yaml:35](../public/downloads/exemplo-dataset-completo.yaml#L35) `platform: SQLite (laboratório)`
- [src/content/docs/templates/dataset.mdx:68](../src/content/docs/templates/dataset.mdx#L68) `Os nossos campos são **uma proposta**, não schemas dessas plataformas.`

**Recomendação:** seção opcional de vínculos (plataforma, nome qualificado, ferramenta MCP esperada, acesso só de leitura) e seção de comportamento esperado (frequência típica, operações onde deve ou não disparar, janela de histórico antes de concluir quebra). Um exemplo Aurora de tag plan contra tabela de eventos que reproduza o caso 1. Na página de dados, recomendar ferramentas só de leitura e citar a afirmação da Databricks como evidência de mercado.

### AG-09 · Crosswalk com ODCS, ODPS e Apache Ossie

**Confiança:** alta.

**O que é:** o ODCS 3.2.0 saiu com o ODPS 1.1.0, sem mudanças incompatíveis, e trouxe o bloco `context` para IA (instructions, verifiedStatements, constraints), `synonyms` com locale, `semanticType`, `enum` e `deprecated`. O Apache Ossie é YAML neutro de modelo semântico; 0.1.1 é de 11/12/2025 e 0.3.0.dev0 é rascunho.

**Fontes:** [ODCS, CHANGELOG](https://github.com/bitol-io/open-data-contract-standard/blob/main/CHANGELOG.md); [Bitol, ODCS 3.2.0 e ODPS 1.1.0](https://bitol.io/data-contracts-data-products-for-ai/); [Apache Ossie, especificação](https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md); [Snowflake, Apache Ossie (Incubating)](https://www.snowflake.com/en/blog/apache-ossie-open-semantic-interchange-incubator/).

**Situação no Contexto:** os modelos reinventam parte desses campos, e as referências citam só fornecedores, nenhum padrão aberto de contrato ou modelo semântico.

**Evidências:**
- [src/content/docs/referencias/index.mdx:58](../src/content/docs/referencias/index.mdx#L58) `| Documentar granularidade e códigos | Snowflake, Databricks | Modelo semântico de dataset portável |`
- [public/downloads/template-kpi.yaml:30](../public/downloads/template-kpi.yaml#L30) `synonyms: []`
- [public/downloads/template-kpi.yaml:63](../public/downloads/template-kpi.yaml#L63) `expected_questions_and_answers: []`
- [public/downloads/template-dataset.yaml:41](../public/downloads/template-dataset.yaml#L41) `do_not_use_for: []`

**Recomendação:** não trocar os modelos pelo ODCS, que é contrato técnico e não serve de formulário para público não técnico. Publicar uma tabela campo a campo Contexto x ODCS 3.2.0 x Ossie, adotar o nome do padrão quando o significado for idêntico, incluir ODCS, ODPS e Ossie na bibliografia com versão e data, e posicionar o Contexto como camada de autoria e descoberta que alimenta esses formatos. Mapear contra a Ossie 0.1.1, que é estável.

### AG-10 · Preparar documentos para RAG e NotebookLM

**Confiança:** alta.

**O que é:** a Microsoft recomenda enriquecer cada trecho com ID, título, resumo, perguntas que responde e fonte. A Anthropic mostrou que acrescentar contexto antes do embedding reduziu falhas de recuperação no top 20 em 35% (49% com BM25 contextual). O Gemini Notebook aceita docx, txt, md, pdf, csv, pptx e Google Docs, Slides e Sheets, entre outros, mas não lista YAML; até 50 fontes no plano gratuito e 500 mil palavras por fonte; fontes do Drive se atualizam.

**Fontes:** [Microsoft, RAG enrichment](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-enrichment-phase); [Microsoft, RAG chunking](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase); [Anthropic, contextual retrieval](https://www.anthropic.com/research/contextual-retrieval); [Gemini Notebook, fontes](https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en); [Gemini Notebook API, sources](https://developers.google.com/notebook/docs/sources).

**Situação no Contexto:** o download principal é YAML; os títulos do modelo Markdown são genéricos e não carregam nome nem ID; o modelo de indicador repete a seção de perguntas em aberto com dois títulos.

**Evidências:**
- [src/components/TemplateDownloads.astro:9](../src/components/TemplateDownloads.astro#L9) `{ name: 'Modelo estruturado', href: 'template-conceito.yaml', format: 'YAML · campos vazios' },`
- [public/downloads/template-kpi.md:36](../public/downloads/template-kpi.md#L36) `## 3. Cálculo`
- [public/downloads/template-kpi.md:63](../public/downloads/template-kpi.md#L63) `## 8. Perguntas ainda em aberto`
- [public/downloads/template-kpi.md:66](../public/downloads/template-kpi.md#L66) `## Perguntas em aberto`
- [docs/ROADMAP.md:36](../docs/ROADMAP.md#L36) `Modelos Markdown sem bloco YAML`

**Recomendação:** página curta "Preparar para NotebookLM ou RAG": um documento por arquivo; bloco no topo com id, título, versão, status e vigência; títulos autoexplicativos (por exemplo "Cálculo da Taxa de sessões convertidas (KPI-AURORA-001 v2.0)"); seção final "Perguntas que este documento responde". Oferecer cada exemplo completo também em .md e unificar a seção de perguntas em aberto.

### AG-11 · Decidir sobre domínio próprio antes de /.well-known

**Confiança:** alta.

**O que é:** UCP publica em `/.well-known/ucp` e Poppy em `/.well-known/poppy.json`; os dois exigem a raiz da origem. A spec do llms.txt lembra que site de projeto no GitHub Pages não consegue publicar no `/.well-known` do host, enquanto o llms.txt funciona em subcaminho.

**Fontes:** [llms.txt v2](https://llmstxt.org/); [UCP, conceitos](http://ucp.dev/documentation/core-concepts/); [Sierra, rascunho do Poppy](https://sierra.ai/blog/poppy).

**Situação no Contexto:** o portal vive num subcaminho do GitHub Pages, e o roadmap registra a decisão de não ter domínio próprio por enquanto.

**Evidências:**
- [docs/ROADMAP.md:54](../docs/ROADMAP.md#L54) `Sem domínio próprio por enquanto; o portal segue no GitHub Pages`
- [astro.config.mjs:4](../astro.config.mjs#L4) `const base = process.env.BASE_PATH || '/contexto-framework';`

**Recomendação:** manter o GitHub Pages enquanto a pauta for llms.txt, schemas e Markdown. Registrar no roadmap que qualquer protocolo baseado em `/.well-known` exige domínio próprio. UCP e Poppy entram como tema para os times documentarem, não como recurso do portal.

### Não verificado nesta frente

- Que o Chrome Lighthouse audite llms.txt: vem só do texto da proposta.
- A relação NotebookLM e Gemini Notebook (troca de nome) e a data de julho de 2026: fonte secundária; a ajuda oficial só usa Gemini Notebook.
- Que a especificação Poppy 1.0 ainda leve rótulo de rascunho: vem de imprensa.
- Remoção da API declarativa do WebMCP: esta frente não confirmou; a frente de público misto confirmou pelo PR #338 (ver UX e a tabela de protocolos).
- Se o servidor MCP remoto do BigQuery está em Preview ou GA.
- Números de adoção de AGENTS.md e llms.txt, autodeclarados.
- Se o Starlight 0.43 gera llms.txt nativamente e quais versões o plugin suporta (o projeto usa astro ^7.4.4 e @astrojs/starlight ^0.43.1).
- Como o Gemini Notebook importa páginas com componentes interativos.
- Licença e data de criação da especificação Agent Skills.
- Compatibilidade do Claude Code com AGENTS.md.
- Data de aprovação do ODCS 3.2.0 (o CHANGELOG não traz data; 08/09/2026 é a atualização da página da Bitol).
- Se "referências totalmente qualificadas" é uma regra nova do ODCS 3.2.0 ou só nome de estrutura.

## Frente 4 · Perguntas de negócio e versionamento

Como ensinar a formular perguntas de negócio e como versionar documentação e metadados.

### PV-01 · Banco de perguntas de negócio baseado em GQM

**Confiança:** alta.

**O que é:** no GQM (Goal, Question, Metric), o objetivo especifica propósito, objeto, questão e ponto de vista; desdobra-se em perguntas e cada pergunta em medidas. A definição é de cima para baixo: sem objetivo, não fica claro o que medir nem como interpretar.

**Fontes:** [Basili, Caldiera, Rombach (1994)](http://www.cs.umd.edu/projects/SoftEng/ESEG/papers/gqm.pdf).

**Situação no Contexto:** o roteiro não começa por uma pergunta de negócio; ela aparece só como item da tabela de dimensões. As perguntas de referência são apresentadas como gabarito depois que os documentos existem, não como ponto de partida.

**Evidências:**
- [src/content/docs/metodo/oito-dimensoes.mdx:27](../src/content/docs/metodo/oito-dimensoes.mdx#L27) `| Objetivo | Finalidade, pergunta de negócio, decisão apoiada |`
- [src/content/docs/metodo/elicitar.mdx:10](../src/content/docs/metodo/elicitar.mdx#L10) `Identifique quem utiliza a informação, qual decisão ela apoia e quem pode aprovar a interpretação.`
- [src/content/docs/templates/index.mdx:25](../src/content/docs/templates/index.mdx#L25) `| Definir perguntas que o acervo deve responder | [Perguntas de referência](casos-teste/) |`
- [public/downloads/template-casos-teste.yaml:1](../public/downloads/template-casos-teste.yaml#L1) `# Gabarito documental, não resultado de teste de um modelo de IA.`

**Recomendação:** criar um "Banco de perguntas de negócio" (página e modelo) com cadeia explícita: objetivo, perguntas (2 a 4 formas de perguntar), indicadores e conceitos necessários (ids), fontes e comportamento esperado. Reaproveitar o modelo de perguntas de referência como segunda metade do ciclo. Incluir bancos por domínio já preenchidos com a Aurora (tag plan e GA4, mídia, e-commerce), cada pergunta em versão fraca e versão boa.

### PV-02 · Bloco de objetivo igual em todos os modelos

**Confiança:** alta.

**O que é:** o GQM trata propósito e ponto de vista como parte obrigatória do objetivo; a ISO 22400-2 inclui o público (Audience) no descritor de indicador; o ODCS usa um objeto `description` com `purpose`, `limitations` e `usage` igual em todo contrato.

**Fontes:** [GQM](http://www.cs.umd.edu/projects/SoftEng/ESEG/papers/gqm.pdf); [ISO 22400-2:2014, amostra](https://cdn.standards.iteh.ai/samples/54497/10e33d2a34c144558b5e3024ee5e1cb0/ISO-22400-2-2014.pdf); [ODCS, fundamentos](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/fundamentals.md).

**Situação no Contexto:** a mesma dimensão tem nomes e níveis diferentes em cada modelo, o que impede a IA de procurar sempre o mesmo campo.

**Evidências:**
- [public/downloads/template-kpi.yaml:29](../public/downloads/template-kpi.yaml#L29) `purpose: null`
- [public/downloads/template-politica.yaml:23](../public/downloads/template-politica.yaml#L23) `purpose: null`
- [public/downloads/template-dataset.yaml:25](../public/downloads/template-dataset.yaml#L25) `business_purpose: null`
- [public/downloads/template-dataset.yaml:51](../public/downloads/template-dataset.yaml#L51) `authoritative_questions: []`
- [public/downloads/template-decisao.yaml:22](../public/downloads/template-decisao.yaml#L22) `decision_question: null`
- [public/downloads/template-dashboard.yaml:24](../public/downloads/template-dashboard.yaml#L24) `supported_decisions: []`
- [public/downloads/template-relacionamento.md:26](../public/downloads/template-relacionamento.md#L26) `## Pergunta de negócio`

**Recomendação:** um bloco comum, por exemplo `intent: {business_questions, decisions_supported, audience, purpose, limitations}`, com o mesmo rótulo em português nos .md. Registrar a mudança como versão MAJOR do esquema dos modelos (PV-13).

### PV-03 · Descritor de indicador inspirado na ISO 22400-2

**Confiança:** alta.

**O que é:** a Tabela 1 da ISO 22400-2 descreve cada indicador com nome, ID, descrição, escopo, fórmula, unidade, Range (limites lógicos), Trend (direção de melhoria), Timing, Audience, metodologia, diagrama de efeitos e notas. É norma de manufatura e está em revisão; serve como inspiração de estrutura.

**Fontes:** [ISO 22400-2:2014, amostra](https://cdn.standards.iteh.ai/samples/54497/10e33d2a34c144558b5e3024ee5e1cb0/ISO-22400-2-2014.pdf).

**Situação no Contexto:** o indicador cobre fórmula, escopo e tempo, mas não direção, limites nem linha de base de volume. Sem isso a IA não diferencia zero esperado de quebra (caso 1). Só o dashboard tem linha de base.

**Evidências:**
- [public/downloads/template-kpi.yaml:44](../public/downloads/template-kpi.yaml#L44) `granularity: null`
- [public/downloads/template-kpi.yaml:52](../public/downloads/template-kpi.yaml#L52) `reporting_window: null`
- [public/downloads/template-dashboard.yaml:32](../public/downloads/template-dashboard.yaml#L32) `comparison_baseline: null`

**Recomendação:** acrescentar `direction` (Trend), `logical_range` (Range), `timing` e `audience`. Como extensão própria do Contexto, sem respaldo da ISO: `expected_volume` com janela histórica (por exemplo mediana de 28 dias por operação), `segment_by_required` e `zero_value_interpretation`. Exemplo Aurora com evento raro em uma só operação.

### PV-04 · BEAM e 7Ws para eventos

**Confiança:** média.

**O que é:** no BEAM (Corr e Stagnitto), requisitos partem de histórias de eventos de negócio contadas com os 7Ws (quem, o quê, quando, onde, quanto, por quê, como), modelando por exemplo junto com as pessoas de negócio. O site do autor oferece o BEAM Canvas, o BEAM Table e a Event Matrix.

**Fontes:** [Agile Data Warehouse Design](https://books.google.com/books/about/Agile_Data_Warehouse_Design.html?id=TRWFmnv8jP0C); [BEAM Templates](https://modelstorming.com/templates).

**Situação no Contexto:** não há modelo de evento de coleta; o índice de modelos só oferece indicador e dataset como pontos mais próximos.

**Evidências:**
- [src/content/docs/templates/index.mdx:21](../src/content/docs/templates/index.mdx#L21) `| Explicar como um indicador é calculado | [Indicador (KPI)](kpi/) |`
- [src/content/docs/templates/index.mdx:22](../src/content/docs/templates/index.mdx#L22) `| Explicar o significado de tabelas e campos | [Dataset](dataset/) |`

**Recomendação:** construir o modelo de evento (EM-07) no formato 7Ws, com linhas de exemplo da Aurora (por exemplo `purchase` e um evento raro `gift_card_redeem`), e usar a matriz de eventos do BEAM para ligar eventos a indicadores e dashboards em consultas com várias tabelas.

### PV-05 · Árvore de indicadores

**Confiança:** média.

**O que é:** uma árvore de indicadores decompõe o indicador principal em componentes por fórmula. Relações de influência são diferentes: aceitas ou supostas, com força e confiança. O diagrama de efeitos da ISO 22400-2 é um paralelo normativo.

**Fontes:** [Levers Labs, Designing Metric Trees](https://www.leverslabs.com/article/designing-metric-trees); [ISO 22400-2:2014, amostra](https://cdn.standards.iteh.ai/samples/54497/10e33d2a34c144558b5e3024ee5e1cb0/ISO-22400-2-2014.pdf).

**Situação no Contexto:** relações entre documentos são uma lista plana, sem tipo. A IA não sabe se dois indicadores devem bater aritmeticamente ou só se influenciam, e é isso que decide se uma divergência entre dashboards é erro.

**Evidências:**
- [public/downloads/exemplo-kpi-completo.yaml:79](../public/downloads/exemplo-kpi-completo.yaml#L79) `related_documents: ["DATASET-AURORA-SESSIONS", "DATASET-AURORA-ORDERS", "REL-AURORA-SESSIONS-ORDERS", "DASH-AURORA-WEB"]`

**Recomendação:** `metric_relations: [{target, relation: component|influence, formula_or_hypothesis, strength, confidence}]` no indicador, com uma árvore pequena da Aurora (receita = sessões x conversão x ticket médio). Avisar que relação de influência não autoriza conclusão causal.

### PV-06 · Entrevista por incidente crítico (Critical Decision Method)

**Confiança:** alta.

**O que é:** o CDM é uma entrevista retrospectiva sobre incidentes reais fora da rotina: escolher o incidente, relato livre, linha do tempo, pontos de decisão e sondas (pistas, conhecimento, análogos, objetivos, opções, base da escolha, pressão de tempo, avaliação da situação e perguntas do tipo "e se uma característica fosse diferente"). Os autores dizem que as razões aparecem melhor pelas opções não escolhidas.

**Fontes:** [Klein, Calderwood, MacGregor (1989), IEEE](https://ieeexplore.ieee.org/document/31053/); [texto integral, cópia hospedada](https://www.theisrm.org/documents/Klein%20(1989)%20Critical%20Decision%20Method%20for%20Eliciting%20Knowledge.pdf).

**Situação no Contexto:** a pergunta 3 já pede um caso concreto, mas não há linha do tempo nem sondas. As perguntas do tipo "e se" são as que revelam regras como "evento raro" ou "só dispara numa operação". O roteiro é declarado como adaptação original.

**Evidências:**
- [src/content/docs/metodo/elicitar.mdx:16](../src/content/docs/metodo/elicitar.mdx#L16) `**Qual foi a última exceção?** Peça um caso concreto, com desfecho e responsável pela decisão.`
- [src/content/docs/metodo/elicitar.mdx:44](../src/content/docs/metodo/elicitar.mdx#L44) `Este roteiro de perguntas é uma adaptação original do projeto.`

**Recomendação:** manter as 8 perguntas e acrescentar um modo "Conte o último caso" em 4 passos (relato, linha do tempo, decisões, sondas), com exemplo trabalhado do evento zerado. Citar Klein et al. (1989) como base, declarando a adaptação simplificada.

### PV-07 · SECI como explicação, não como método

**Confiança:** média.

**O que é:** o modelo SECI (socialização, externalização, combinação, internalização), consolidado por Nonaka, Toyama e Konno (2000), explica como o conhecimento circula entre as formas tácita e explícita. Só os metadados do artigo foram lidos.

**Fontes:** [Nonaka, Toyama, Konno (2000)](https://www.sciencedirect.com/science/article/pii/S0024630199001156).

**Situação no Contexto:** a página cita só Nonaka (1994) e não diz em que etapa o Contexto atua.

**Evidências:**
- [src/content/docs/fundamentos/conhecimento-tacito.mdx:9](../src/content/docs/fundamentos/conhecimento-tacito.mdx#L9) `especialmente em Nonaka (1994)`

**Recomendação:** uma frase dizendo que o Contexto apoia a externalização (entrevista para documento) e a combinação (ligar documentos), com a referência de 2000. Não transformar o SECI em etapas do método.

### PV-08 · Ciclo de mudança conforme BABOK e KCS

**Confiança:** alta.

**O que é:** o IIBA lista na gestão do ciclo de vida de requisitos as tarefas rastrear, manter, priorizar, avaliar mudanças e aprovar. O KCS v6 usa estados de confiança, trata o reúso de um artigo não validado como sua revisão, prefere arquivar a apagar e admite cópia exata quando há exigência regulatória.

**Fontes:** [IIBA, Elicitation and Collaboration](https://www.iiba.org/knowledgehub/the-business-analysis-standard/5-applying-business-analysis-tasks/5-3-business-analysis-knowledge-areas/elicitation-and-collaboration/); [KCS v6, Article State](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/040/010/030).

**Situação no Contexto:** a matriz RACI cobre quem aprova, mas não descreve avaliação de impacto nos documentos dependentes. Os campos de revisão são inconsistentes entre modelos.

**Evidências:**
- [src/content/docs/governanca/papeis.mdx:43](../src/content/docs/governanca/papeis.mdx#L43) `| Atualizar conteúdo de negócio | **R** | **A** | C | I |`
- [public/downloads/template-kpi.yaml:19](../public/downloads/template-kpi.yaml#L19) `last_reviewed: null`
- [public/downloads/template-politica.yaml:49](../public/downloads/template-politica.yaml#L49) `review_trigger: null`
- [public/downloads/template-casos-teste.yaml:39](../public/downloads/template-casos-teste.yaml#L39) `revalidation_triggers: []`
- [src/content/docs/metodo/limites.mdx:36](../src/content/docs/metodo/limites.mdx#L36) `registre o que dispara uma revisão (uma data, um evento, uma nova versão da fonte);`

**Recomendação:** fluxo curto em papeis.mdx: pedido, avaliação de impacto (listar dependentes via `related_documents` e `depends_on_versions`), aprovação, publicação, aviso. Padronizar `last_reviewed`, `next_review` e `review_triggers` em todos os modelos. Usar as perguntas feitas pelos usuários como sinal de demanda para priorizar revisões.

### PV-09 · Versão imutável em três níveis

**Confiança:** alta.

**O que é:** no SemVer, uma versão publicada não pode mudar (item 3); PATCH corrige, MINOR acrescenta sem quebrar, MAJOR quebra. O ODCS separa a versão do padrão (`apiVersion`) da versão do contrato. O dbt cria versão nova quando há quebra de contrato.

**Fontes:** [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html); [ODCS, fundamentos](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/fundamentals.md); [dbt, model versions](https://docs.getdbt.com/docs/mesh/govern/model-versions).

**Situação no Contexto:** o critério "o resultado muda?" é bom, mas correção de texto mantém a mesma versão, o que contradiz a garantia de que duas versões nunca compartilham ID. O esquema tem dois níveis, e os modelos não dizem qual versão de esquema seguem.

**Evidências:**
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:90](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L90) `| Só o texto, nada muda no resultado (erro de digitação, link) | Mesma versão | Corrigir uma palavra |`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:29](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L29) `duas versões nunca compartilham o mesmo ID`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:86](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L86) `**alguém que aplicar a regra nova chega a um resultado diferente em algum caso?**`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:34](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L34) `0.1 para o primeiro rascunho; 1.0 para a primeira versão aprovada.`

**Recomendação:** manter o critério pelo resultado e passar a três níveis: PATCH editorial, MINOR esclarecimento sem mudança de resultado, MAJOR quando o resultado muda, id novo quando o objeto medido muda. Declarar que versão aprovada é imutável e acrescentar `template_version` a cada modelo.

### PV-10 · Vigência bitemporal

**Confiança:** alta.

**O que é:** o modelo bitemporal separa quando o fato vale (vigência) de quando a organização o registrou. O histórico de registro permite responder "o que pensávamos em tal data", o que importa em mudanças retroativas.

**Fontes:** [Martin Fowler, Bitemporal History](https://martinfowler.com/articles/bitemporal-history.html).

**Situação no Contexto:** o intervalo de vigência resolve o tempo de vigência. Já `version_date` é definido de forma diferente em duas páginas e não há campo para registro ou aprovação. O exemplo da política tem um caso retroativo, e só conceito e indicador guardam cópias integrais das versões antigas.

**Evidências:**
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:35](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L35) `` | Data desta versão | `version_date` | O dia em que esta versão foi escrita ou aprovada | ``
- [src/content/docs/metodo/identificacao-versoes.mdx:18](../src/content/docs/metodo/identificacao-versoes.mdx#L18) `Quando esta versão foi emitida ou confirmada; não é necessariamente a data de aplicação`
- [src/content/docs/metodo/identificacao-versoes.mdx:93](../src/content/docs/metodo/identificacao-versoes.mdx#L93) `Em caso de efeito retroativo, isso precisa ser declarado e confirmado explicitamente.`
- [src/content/docs/templates/politica.mdx:65](../src/content/docs/templates/politica.mdx#L65) `O conflito foi resolvido em 14/08, depois da despesa, mas a resolução não criou regra nova: confirmou a que já valia desde 01/07.`
- [src/content/docs/metodo/identificacao-versoes.mdx:87](../src/content/docs/metodo/identificacao-versoes.mdx#L87) `No portal, só conceito e KPI guardam **cópias integrais** das versões antigas.`

**Recomendação:** manter `valid_from`/`valid_to`; trocar `version_date` por `recorded_at` e `approved_at`, com uma tabela das três datas (vigência da regra, vigência do registro, registro e aprovação). Exigir cópia integral de toda versão aprovada em todos os tipos. Usar o caso de 10/08 e 14/08 da política como exemplo de pergunta bitemporal.

### PV-11 · Ponteiro para a versão seguinte e descontinuação

**Confiança:** alta.

**O que é:** nos ADRs, a decisão revertida fica no histórico marcada como substituída e aponta para a nova. No dbt, `deprecation_date` comunica prazo de migração e gera avisos; para modelos versionados ou com contrato imposto, impede apagar antes da data. O ODCS dá como exemplos de status proposed, draft, active, deprecated e retired.

**Fontes:** [Nygard, Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions); [dbt, deprecation_date](https://docs.getdbt.com/reference/resource-properties/deprecation_date); [ODCS, fundamentos](https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/fundamentals.md).

**Situação no Contexto:** só existe o ponteiro para trás. A versão histórica continua `approved` e não aponta para a sucessora.

**Evidências:**
- [src/content/docs/metodo/identificacao-versoes.mdx:22](../src/content/docs/metodo/identificacao-versoes.mdx#L22) `` `supersedes_revision` aponta para a versão anterior. ``
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:6](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L6) `status: approved`

**Recomendação:** acrescentar `superseded_by_revision` e `deprecation_date`, e separar estado de aprovação de estado de vigência (por exemplo `approval: approved`, `lifecycle: superseded`). Ver também GC-03.

### PV-12 · ADR para desempates e decisões do framework

**Confiança:** alta.

**O que é:** um ADR é um registro curto e numerado de uma única decisão, com título, contexto, decisão, status e consequências; quando a decisão muda, o antigo fica marcado como substituído.

**Fontes:** [Nygard, Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

**Situação no Contexto:** a página de papéis manda registrar conflitos sem formato, e as decisões do próprio Contexto estão numa tabela sem data, status nem consequências.

**Evidências:**
- [src/content/docs/governanca/papeis.mdx:49](../src/content/docs/governanca/papeis.mdx#L49) `Registre o conflito, a origem, o impacto e o responsável pelo desempate.`
- [src/content/docs/referencias/index.mdx:48](../src/content/docs/referencias/index.mdx#L48) `| Decisão original do Contexto | Inspiração | Adaptação e consequência |`

**Recomendação:** mini-modelo "Registro de decisão" (contexto, opções, decisão, quem decidiu, vigência, consequências, substitui e substituído por) para desempates entre fontes. Migrar a tabela de rastreabilidade para ADRs numerados no repositório.

### PV-13 · Changelog (Keep a Changelog 2.0.0)

**Confiança:** alta.

**O que é:** um changelog curado para pessoas, com Unreleased, entradas datadas (mais recente primeiro), grupos Added, Changed, Deprecated, Removed, Fixed e Security, marcação de mudança incompatível e esquema de versão declarado. A 2.0.0 orienta sobre changelogs redigidos por IA com instruções em AGENTS.md. O changelog do ODCS mostra o padrão aplicado a uma especificação de metadados.

**Fontes:** [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/); [ODCS, CHANGELOG](https://github.com/bitol-io/open-data-contract-standard/blob/main/CHANGELOG.md).

**Situação no Contexto:** o pacote tem versão 0.4.0, mas não há CHANGELOG na raiz, os modelos não trazem versão de esquema e não há registro público de mudanças nos modelos.

**Evidências:**
- [package.json:4](../package.json#L4) `"version": "0.4.0",`
- [src/content/docs/referencias/index.mdx:56](../src/content/docs/referencias/index.mdx#L56) `| Datar e versionar todo documento | Prática comum de controle de documentos; KCS sobre evolução do conteúdo |`

**Recomendação:** criar CHANGELOG.md no formato 2.0.0, com marcação **Breaking:** para renomeações de campos, e mostrar no portal a versão dos modelos com link para o changelog.

### PV-14 · Perguntas verificadas com várias formulações

**Confiança:** alta.

**O que é:** o Verified Query Repository do Snowflake guarda pergunta, SQL, quem verificou, quando e se a pergunta serve de sugestão inicial. O Databricks recomenda de duas a quatro formulações por pergunta nos benchmarks.

**Fontes:** [Snowflake, Verified Query Repository](https://docs.snowflake.com/en/user-guide/views-semantic/verified-query-repository); [Databricks, monitorar Genie](https://docs.databricks.com/aws/en/genie-agents/monitor).

**Situação no Contexto:** `depends_on_versions` e `answer | clarify | abstain` são pontos fortes. Faltam formulações alternativas e a marcação de perguntas de porta de entrada.

**Evidências:**
- [public/downloads/template-casos-teste.yaml:25](../public/downloads/template-casos-teste.yaml#L25) `depends_on_versions: {}`
- [public/downloads/template-casos-teste.yaml:31](../public/downloads/template-casos-teste.yaml#L31) `expected_behavior: null  # answer | clarify | abstain`

**Recomendação:** acrescentar `phrasings: []` e `onboarding: true|false`, e ligar cada pergunta ao `revision_id` usado, para que uma mudança MAJOR num indicador dispare a revalidação das perguntas dependentes. Converge com CS-02, CS-09 e EM-05.

### PV-15 · Manter a adaptação honesta de DMN

**Confiança:** alta.

**O que é:** o DMN 1.6 (setembro de 2026) combina notação gráfica das dependências entre decisões, conhecimento e dados de entrada com tabelas de decisão executáveis.

**Fontes:** [OMG, DMN 1.6](https://www.omg.org/spec/DMN/1.6).

**Situação no Contexto:** sem problema grave; o portal declara o modelo simplificado. Falta só ligar as entradas da decisão aos documentos de origem.

**Evidências:**
- [src/content/docs/templates/decisao.mdx:82](../src/content/docs/templates/decisao.mdx#L82) `O modelo é **simplificado e autoral**: não usa a notação DMN nem sua semântica de execução`
- [public/downloads/template-decisao.yaml:27](../public/downloads/template-decisao.yaml#L27) `required_inputs: []`

**Recomendação:** manter; opcionalmente transformar `required_inputs` em itens `{name, source_document}`.

### Não verificado nesta frente

- Se o intervalo semiaberto do Contexto coincide com a semântica de períodos do SQL:2011 (o texto da norma não foi consultado).
- Técnicas de descoberta do BABOK Guide v3 (acesso restrito).
- Conteúdo do modelo SECI no artigo de 2000 (só metadados lidos) e críticas acadêmicas ao SECI.
- Se o Databricks recomenda reavaliar benchmarks após cada mudança.
- Data de aprovação do ODCS v3.2.0.
- Se a ISO 22400-2 dá base para faixa esperada ou linha de base de volume (não dá: Range é limite lógico; volume esperado é extensão proposta).
- Afirmações de terceiros sobre o Keep a Changelog 2.0.0.
- Boas práticas de árvore de indicadores vindas de fornecedores sem especificação primária.
- Poppy, UCP e WebMCP ficaram fora do escopo desta frente.

## Frente 5 · Experiência para público misto

Documentação, linguagem simples, exemplos trabalhados, modelos, consistência visual no Starlight e arquitetura da informação.

### UX-01 · Compasso do Diátaxis

**Confiança:** alta.

**O que é:** o Diátaxis separa tutorial, guia prático, referência e explicação. O compasso classifica cada trecho com duas perguntas (ação ou cognição; aquisição ou aplicação) e vale para frases ou documentos inteiros.

**Fontes:** [Diátaxis](https://diataxis.fr/); [Diátaxis, compasso](https://diataxis.fr/compass/).

**Situação no Contexto:** o projeto cita o Diátaxis, mas cada página de modelo junta explicação, guia, referência e tutorial. No menu, "Comece por uma tarefa" junta tutorial, guia de revisão e índice; "Guias" inclui uma página que é explicação.

**Evidências:**
- [src/content/docs/metodo/visao-geral.mdx:42](../src/content/docs/metodo/visao-geral.mdx#L42) `o [Diátaxis](https://diataxis.fr/), para organizar a documentação pelo que o leitor precisa fazer`
- [astro.config.mjs:46](../astro.config.mjs#L46) `{ label: 'Comece por uma tarefa', items: ['fundamentos/comece-em-5-minutos', 'validacao/checklist', 'templates'] },`
- [astro.config.mjs:47](../astro.config.mjs#L47) `{ label: 'Guias', items: ['metodo/elicitar', 'metodo/identificacao-versoes'] },`
- [src/content/docs/metodo/identificacao-versoes.mdx:2](../src/content/docs/metodo/identificacao-versoes.mdx#L2) `title: Versões e vigência`
- [src/content/docs/templates/kpi.mdx:50](../src/content/docs/templates/kpi.mdx#L50) `## Teste você`

**Recomendação:** passar cada página pelo compasso. Opção enxuta: página de modelo como guia prático com a referência recolhida, e "O problema" e "Teste você" numa trilha de aprendizado por domínio. Se a mistura for proposital, declarar o formato híbrido e manter sempre a mesma ordem e os mesmos rótulos. Renomear os grupos do menu pela necessidade do leitor: Aprender, Fazer, Consultar, Entender.

### UX-02 · Guia de estilo em linguagem simples

**Confiança:** alta.

**O que é:** a ISO 24495-1:2023 traz princípios de linguagem simples válidos também para escrita técnica. A Lei 15.263/2025 define linguagem simples (art. 4) como técnicas para "encontrar a informação, compreendê-la e usá-la" e lista no art. 5 frases curtas em ordem direta, palavras comuns, jargão explicado no texto, nome completo antes da sigla e teste com o público. A lei vale para a administração pública; aqui é referência em português, não obrigação.

**Fontes:** [ISO 24495-1:2023](https://www.iso.org/standard/78907.html); [Lei 15.263/2025](https://planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15263.htm).

**Situação no Contexto:** não há guia de estilo nem referência a linguagem simples nas referências. Estrangeirismos e siglas aparecem como rótulos principais sem explicação, inclusive em caixa alta.

**Evidências:**
- [src/content/docs/templates/dataset.mdx:2](../src/content/docs/templates/dataset.mdx#L2) `title: Dataset`
- [src/components/TemplateFinder.astro:22](../src/components/TemplateFinder.astro#L22) `<p class="finder-eyebrow">ESCOLHA POR TAREFA · SEM CONHECER YAML OU IA</p>`
- [src/components/ExampleDoc.astro:106](../src/components/ExampleDoc.astro#L106) `<TabItem label="YAML">`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:3](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L3) `description: O que significam null, status, id, versão e os outros campos dos modelos, em linguagem simples.`

**Recomendação:** guia de estilo curto no repositório citando a ISO 24495-1 e o art. 5 da lei: tamanho máximo de frase, glossário de termos aceitos (KPI, dataset e YAML explicados na primeira menção), sem caixa alta em rótulos e regra para títulos (por exemplo "Tabela e seus campos (dataset)"). Incluir no ciclo de revisão um teste com 3 a 5 pessoas não técnicas. O vocabulário do contrato editorial é a base natural desse guia.

### UX-03 · Exemplos trabalhados e exemplos com etapas apagadas

**Confiança:** média (os estudos são de domínios bem estruturados; aplicar à escrita de documentação é extrapolação).

**O que é:** Sweller e Cooper (1985) mostraram que iniciantes que estudam exemplos resolvidos resolvem depois problemas de mesma estrutura com menos tempo e menos erros. Renkl e Atkinson propõem apagar etapas aos poucos, do exemplo completo ao problema, o que favoreceu a transferência próxima; somar perguntas que pedem o princípio de cada etapa teve efeito médio a grande também na transferência distante.

**Fontes:** [Sweller e Cooper (1985)](https://doi.org/10.1207/s1532690xci0201_3); [Renkl e Atkinson (2003)](https://doi.org/10.1207/s15326985ep3801_3); [Atkinson, Renkl e Merrill (2003)](https://doi.org/10.1037/0022-0663.95.4.774); [Renkl, Atkinson e Maier (2000)](https://escholarship.org/uc/item/81b9j9hs).

**Situação no Contexto:** o par de exemplos é justificado como decisão própria, sem base pedagógica. A ordem é com lacunas primeiro e completo depois, e as lacunas são perguntas em aberto, não etapas apagadas para o leitor completar. O resumo do modelo vem antes dos exemplos e termina no download do modelo em branco. Na página o exemplo completo aparece em abas legíveis, mas o download do exemplo completo só existe em YAML.

**Evidências:**
- [src/content/docs/referencias/index.mdx:57](../src/content/docs/referencias/index.mdx#L57) `| Mostrar o exemplo completo, já aprovado | Decisão própria | Par de exemplos por tipo: com lacunas e completo |`
- [src/content/docs/templates/kpi.mdx:13](../src/content/docs/templates/kpi.mdx#L13) `<TemplateStart kind="kpi" />`
- [src/content/docs/templates/kpi.mdx:40](../src/content/docs/templates/kpi.mdx#L40) `<ExampleDoc file="exemplo-kpi-lacunas.yaml" />`
- [src/content/docs/templates/kpi.mdx:44](../src/content/docs/templates/kpi.mdx#L44) `<ExampleDoc file="exemplo-kpi-completo.yaml" />`
- [src/components/TemplateStart.astro:86](../src/components/TemplateStart.astro#L86) `<a href={base + 'downloads/template-' + kind + '.md'} download>`
- [src/components/ExampleDoc.astro:114](../src/components/ExampleDoc.astro#L114) `download>Baixar YAML`
- [src/components/TemplateDownloads.astro:10](../src/components/TemplateDownloads.astro#L10) `{ name: 'Exemplo com lacunas', href: 'exemplo-conceito-lacunas.yaml', format: 'YAML · nada aprovado' },`
- [public/downloads/template-kpi.md:37](../public/downloads/template-kpi.md#L37) `- Numerador (definição e critérios):`

**Recomendação:** manter o par, que mostra bem o que falta decidir, e alinhar os rótulos de download ao título da seção já usado na página ("Antes e depois da decisão"). Acrescentar uma sequência: (1) exemplo completo comentado em .md, com "por que este campo" em cada seção; (2) o mesmo exemplo com 2 ou 3 campos apagados, resposta recolhida e uma pergunta sobre a regra por trás de cada campo; (3) modelo em branco. Citar os estudos nas referências no lugar de "Decisão própria", registrando a extrapolação.

### UX-04 · Guia de preenchimento por modelo

**Confiança:** média.

**O que é:** o The Good Docs Project publica cada template com um guia que explica como preencher cada seção; o guia de concept traz exemplos breves, não um documento completo preenchido.

**Fontes:** [The Good Docs Project, guias](https://www.thegooddocsproject.dev/template); [The Good Docs Project, concept](https://www.thegooddocsproject.dev/template/concept).

**Situação no Contexto:** os modelos .md trazem só os nomes dos campos, sem orientação ao lado. Só o modelo de indicador numera as seções, e ele repete o bloco de perguntas em aberto.

**Evidências:**
- [public/downloads/template-kpi.md:26](../public/downloads/template-kpi.md#L26) `## 1. Definição de negócio`
- [public/downloads/template-kpi.md:63](../public/downloads/template-kpi.md#L63) `## 8. Perguntas ainda em aberto`
- [public/downloads/template-kpi.md:66](../public/downloads/template-kpi.md#L66) `## Perguntas em aberto`

**Recomendação:** esqueleto comum aos 10 modelos (Identificação, Para que serve, conteúdo do tipo, Perguntas em aberto, Histórico), sem a duplicação do indicador. Publicar cada modelo com seu guia de preenchimento e, indo além do Good Docs, uma linha "Exemplo Aurora:" em itálico em cada campo, que o usuário apaga depois.

### UX-05 · Entrada pela pergunta de negócio

**Confiança:** alta (inferência de design a partir das fontes, não recomendação explícita delas).

**O que é:** o Diátaxis organiza guias em torno da tarefa e da meta de quem lê. Para o Contexto, a tarefa inicial é a pergunta de negócio que a IA vai responder; dela saem indicador, tabelas, junções e limites. O teste com o público, da Lei 15.263, reforça partir de perguntas reais.

**Fontes:** [Diátaxis](https://diataxis.fr/); [Lei 15.263/2025](https://planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15263.htm).

**Situação no Contexto:** as perguntas de referência são a última camada e o último item do grupo de dados. O exercício de 5 minutos usa um caso de RH, enquanto a página inicial fala de conversão. Uma busca por GA4, GTM, tag plan, tagueamento e "zerad" em `src/content/docs` não encontrou nada.

**Evidências:**
- [src/content/docs/dados/visao-geral.mdx:29](../src/content/docs/dados/visao-geral.mdx#L29) `Quais perguntas o acervo deve conseguir responder?`
- [astro.config.mjs:53](../astro.config.mjs#L53) `'templates/relacionamento', 'templates/dashboard', 'templates/casos-teste'`
- [src/content/docs/metodo/oito-dimensoes.mdx:27](../src/content/docs/metodo/oito-dimensoes.mdx#L27) `| Objetivo | Finalidade, pergunta de negócio, decisão apoiada |`
- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:12](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L12) `Imagine que a equipe de RH da Aurora diz:`
- [src/components/LandingHero.astro:21](../src/components/LandingHero.astro#L21) `Considere clientes ativos e calcule a conversão.`

**Recomendação:** quarta entrada na página inicial, "Comece por uma pergunta de negócio", com roteiro de quais modelos a pergunta exige. Exemplo trabalhado: "quais eventos do tag plan estão zerados?" exige regra de raridade, janela histórica e granularidade por operação, e leva a dataset, indicador e perguntas de referência. Dois exercícios de 5 minutos (negócio e dados). Ensinar a formular a pergunta (unidade, período, recorte, comparação) antes de documentar. Converge com PV-01.

### UX-06 · Fonte única para rótulos

**Confiança:** alta.

**O que é:** information scent é a estimativa que o leitor faz do valor de uma página antes de clicar, a partir do rótulo, do entorno e do que já sabe. Rótulos claros e consistentes com o destino deixam a estimativa mais forte.

**Fontes:** [NN/g, Information Scent](https://www.nngroup.com/articles/information-scent/).

**Situação no Contexto:** a configuração adota a regra de que o menu usa o título da página, mas os cartões da página inicial não seguem a regra. O seletor de modelos e a tabela logo abaixo descrevem o mesmo modelo com palavras diferentes, e as descrições vivem em três lugares.

**Evidências:**
- [astro.config.mjs:43](../astro.config.mjs#L43) `// Sem rótulos próprios: o menu mostra o título da página, então os dois nunca divergem.`
- [src/components/PrincipleTiles.astro:12](../src/components/PrincipleTiles.astro#L12) `title: 'Revisar o que já está escrito',`
- [src/components/PrincipleTiles.astro:15](../src/components/PrincipleTiles.astro#L15) `href: 'validacao/checklist/',`
- [src/content/docs/validacao/checklist.mdx:2](../src/content/docs/validacao/checklist.mdx#L2) `title: Revisar e entregar`
- [src/components/TemplateFinder.astro:4](../src/components/TemplateFinder.astro#L4) `label: 'Descrever como um trabalho é executado'`
- [src/content/docs/templates/index.mdx:17](../src/content/docs/templates/index.mdx#L17) `| Descrever as etapas de um trabalho | [Processo](processo/)`
- [src/components/TemplateStart.astro:14](../src/components/TemplateStart.astro#L14) `processo: {`

**Recomendação:** juntar os metadados de cada modelo num único arquivo de dados ou content collection, lido pelos três componentes e pela tabela, e estender aos cartões da página inicial a regra que já vale para o menu.

**Observação no portal:** a divergência "Revisar o que já está escrito" para a página "Revisar e entregar" foi confirmada na página inicial publicada em 17/11/2026.

### UX-07 · Card sorting e tree testing

**Confiança:** média.

**O que é:** no card sorting, participantes agrupam e nomeiam cartões, revelando o modelo mental do público; o tree testing avalia uma arquitetura existente. A NN/g recomenda de 30 a 50 cartões e pelo menos 15 participantes; acima de 50 cartões, surge uma categoria "Diversos".

**Fontes:** [NN/g, Card Sorting](https://www.nngroup.com/articles/card-sorting-definition/).

**Situação no Contexto:** os grupos do menu foram definidos pelo autor, sem registro de validação com usuários. Há 26 páginas em `src/content/docs`.

**Evidências:**
- [astro.config.mjs:48](../astro.config.mjs#L48) `{ label: 'Documentos do negócio', collapsed: true, items: [`
- [astro.config.mjs:58](../astro.config.mjs#L58) `{ label: 'Consulta', collapsed: true, items: [`

**Recomendação:** card sorting aberto e remoto com os 26 títulos e pelo menos 15 pessoas do público misto; depois tree testing com 5 a 8 tarefas reais (por exemplo "onde documento que um evento só dispara na operação B?"). Registrar o resultado como decisão (PV-12).

### UX-08 · Divulgação progressiva em dois níveis

**Confiança:** média.

**O que é:** mostrar primeiro o essencial melhora aprendizado, eficiência e taxa de erro. A NN/g diz que mais de dois níveis costuma ter baixa usabilidade e que o caminho para o nível seguinte precisa de rótulo claro.

**Fontes:** [NN/g, Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/).

**Situação no Contexto:** a aba YAML recolhida já aplica o princípio, mas o resumo do modelo cria três H2 e a comparação "antes e depois" cria um H3, o que infla o sumário. O índice mostra o seletor e logo abaixo uma tabela com os mesmos 10 itens.

**Evidências:**
- [src/components/TemplateStart.astro:69](../src/components/TemplateStart.astro#L69) `<h2>Quando usar</h2>`
- [src/components/TemplateStart.astro:77](../src/components/TemplateStart.astro#L77) `<h2>O que ter em mãos</h2>`
- [src/components/BeforeAfter.astro:4](../src/components/BeforeAfter.astro#L4) `<h3>Taxa de conversão</h3>`
- [src/content/docs/templates/index.mdx:10](../src/content/docs/templates/index.mdx#L10) `<TemplateFinder />`
- [src/content/docs/templates/index.mdx:14](../src/content/docs/templates/index.mdx#L14) `| O que você precisa fazer | Como preencher | Modelo em texto |`

**Recomendação:** usar negrito ou lista de definições em vez de H2 e H3 dentro dos componentes de resumo; manter no índice uma única forma de escolher o modelo; recolher fundamentação e histórico; limitar a página de modelo a um nível extra de detalhe.

### UX-09 · Componentes nativos do Starlight e CSS controlado

**Confiança:** alta.

**O que é:** o Starlight oferece Card e CardGrid, Steps, Aside e outros, que seguem o tema. A documentação recomenda personalizar por variáveis `--sl-*`, explica as cascade layers e observa que CSS fora de layer sobrepõe os estilos padrão.

**Fontes:** [Starlight, componentes](https://starlight.astro.build/components/using-components/); [Starlight, Steps](https://starlight.astro.build/components/steps/); [Starlight, Cards](https://starlight.astro.build/components/cards/); [Starlight, Asides](https://starlight.astro.build/components/asides/); [Starlight, CSS](https://starlight.astro.build/guides/css-and-tailwind/).

**Situação no Contexto:** só Code, Tabs e TabItem vêm do Starlight; cartões, resumo e comparações são componentes próprios. O exercício de 5 minutos usa títulos numerados em vez de Steps; avisos `:::` aparecem em só 2 páginas. O `custom.css` tem 936 linhas, 44 linhas com `!important` (47 ocorrências), 48 cores hexadecimais distintas, nenhum `@layer` e comentários de rodadas em inglês e português.

**Evidências:**
- [src/components/ExampleDoc.astro:11](../src/components/ExampleDoc.astro#L11) `import { Code, Tabs, TabItem } from '@astrojs/starlight/components';`
- [src/components/PrincipleTiles.astro:28](../src/components/PrincipleTiles.astro#L28) `<nav class="principle-tiles task-paths" aria-label="Escolha o que você quer fazer">`
- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:10](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L10) `## 1. Escolha uma frase que sua equipe usa`
- [src/styles/custom.css:52](../src/styles/custom.css#L52) `.cta-primary {color:#fff!important;background:#205a46}`
- [src/styles/custom.css:122](../src/styles/custom.css#L122) `/* v0.2: choice assistant and portable template library */`
- [src/styles/custom.css:289](../src/styles/custom.css#L289) `/* Checkpoint A: task-first navigation without a new application layer. */`
- [src/styles/custom.css:792](../src/styles/custom.css#L792) `/* Segunda rodada: cartão de exemplo com abas.`

**Recomendação:** inventariar os 14 componentes e trocar pelos nativos onde houver equivalente (cartões da página inicial por CardGrid com LinkCard, exercício de 5 minutos por Steps, ressalvas por Aside, estados por Badge). Manter próprios só onde há valor específico (ExampleDoc, JoinDiagram). Reorganizar o CSS em `@layer`, com tokens e nenhuma cor fixa fora de `:root`, agrupado por componente e com comentários numa só língua.

### Não verificado nesta frente

- Os quatro princípios da ISO 24495-1 (só o resumo oficial foi lido).
- Efeito de reversão pela expertise (Kalyuga et al., 2003), relevante para público misto, sem fonte primária lida.
- Guia oficial de linguagem simples do gov.br.
- Acessibilidade (contraste, foco) e teste em celular no portal publicado.

## Frente 6 · Governança e catálogos

Como catálogos e plataformas de governança (Unity Catalog, Knowledge Catalog, DataHub, OpenMetadata, Atlan, Collibra) estruturam termos de negócio e onde o Contexto se encaixa: como camada de descoberta e autoria versionada antes do catálogo.

### GC-01 · Separar quem mantém de quem responde pela definição

**Confiança:** alta.

**O que é:** no glossário da DAMA UK, o data owner tem autoridade para dizer que uma definição é a apropriada, e o data steward a mantém em nome dele. A revisão de 2024 do DMBOK 2.0 define o data owner como a pessoa de negócio que responde pelas decisões de um domínio. O Collibra separa Owner, Business Steward, Technical Steward e Subject Matter Expert.

**Fontes:** [DAMA, revisão do DMBOK](https://dama.org/dama-dmbok-revision/); [DAMA UK, glossário](https://www.dama-uk.org/pages/glossary); [Collibra, resource roles](https://productresources.collibra.com/docs/collibra/latest/Content/Settings/RolesAndPermissions/Roles/ResourceRoles/to_resource-roles.htm).

**Situação no Contexto:** `owner` no Contexto significa "mantém o documento", que no DAMA é o steward; quem tem autoridade é `approver`. Exportar `owner` para o campo owner de um catálogo dá autoridade a quem só mantém. Nenhum arquivo em `src/` cita DAMA ou steward.

**Evidências:**
- [src/content/docs/governanca/papeis.mdx:14](../src/content/docs/governanca/papeis.mdx#L14) `| Responsável | Mantém o documento: registra mudanças, versões e perguntas em aberto |`
- [src/content/docs/governanca/papeis.mdx:15](../src/content/docs/governanca/papeis.mdx#L15) `| Quem aprova | Confirma definições e aprova o documento no domínio |`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:32](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L32) `` | Responsável | `owner` | O cargo ou a área que responde pelo conteúdo. Não o nome de uma pessoa, que muda | ``
- [src/content/docs/governanca/papeis.mdx:57](../src/content/docs/governanca/papeis.mdx#L57) `[ISO 30401](https://www.iso.org/standard/68683.html) e [KCS: Roles and Competencies]`

**Recomendação:** antes da v1 do esquema, escolher: (a) renomear para `steward` (mantém) e `owner` (aprova); ou (b) manter os nomes e publicar em papeis.mdx uma tabela de equivalência Contexto, DAMA e catálogos, dizendo que `approver` é o data owner e `owner` é o steward. Nos dois casos, citar o DMBOK e a DAMA UK.

### GC-02 · Certificação com prazo e recertificação

**Confiança:** alta.

**O que é:** o PR #18392 do OpenMetadata (2024) define prazos por nível de certificação (P60D para Bronze e Silver, P30D para Gold). O tutorial do Knowledge Catalog cria um aspect de governança com "Last Review Date". A Databricks recomenda automatizar certificação e obsolescência por uso, idade e responsável.

**Fontes:** [OpenMetadata, PR #18392](https://github.com/open-metadata/OpenMetadata/pull/18392); [Knowledge Catalog, governança básica](https://docs.cloud.google.com/dataplex/docs/build-foundational-data-governance); [Databricks, certificar ou depreciar](https://docs.databricks.com/aws/en/data-governance/unity-catalog/certify-deprecate-data).

**Situação no Contexto:** `last_reviewed` existe em 3 dos 10 modelos, nenhum tem prazo de revisão e o validador não confere presença nem idade da revisão.

**Evidências:**
- [public/downloads/template-kpi.yaml:19](../public/downloads/template-kpi.yaml#L19) `last_reviewed: null`
- [public/downloads/template-dataset.yaml:7](../public/downloads/template-dataset.yaml#L7) `status: draft                # draft | pending_approval | approved | deprecated`
- [scripts/validate_content.py:163](../scripts/validate_content.py#L163) `for key in ("owner", "approver", "source_of_truth", "valid_from", "version_date"):`

**Recomendação:** `last_reviewed` em todos os modelos e `review_interval` (duração ISO 8601, como P90D) ou `next_review`. Ensinar no checklist que documento aprovado com revisão vencida deve ser tratado como "aprovado, revisão atrasada" e checar isso no validador. Confirmar o comportamento atual do OpenMetadata antes de citá-lo.

### GC-03 · Obsolescência com ponteiro para o substituto

**Confiança:** alta.

**O que é:** no Databricks, a tag `system.certification_status = deprecated` avisa que o ativo não deve ser usado em fluxos novos e pode ser filtrada na busca. No DataHub, o estágio Deprecated e `allowedPreviousStages` restringem as transições de ciclo de vida.

**Fontes:** [Databricks, certificar ou depreciar](https://docs.databricks.com/aws/en/data-governance/unity-catalog/certify-deprecate-data); [DataHub, Business Glossary](https://docs.datahub.com/docs/glossary/business-glossary).

**Situação no Contexto:** só existe o ponteiro para trás; quando um assunto inteiro fica obsoleto, nenhum campo diz qual documento passa a valer.

**Evidências:**
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:59](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L59) `` | Obsoleto | `deprecated` | Não é mais recomendado como referência atual ``
- [scripts/validate_content.py:16](../scripts/validate_content.py#L16) `VALID_STATUSES = {"draft", "pending_approval", "approved", "deprecated"}`
- [public/downloads/template-dataset.yaml:14](../public/downloads/template-dataset.yaml#L14) `supersedes_revision: null`

**Recomendação:** `replaced_by` (id ou revision_id), obrigatório com `status: deprecated`, e `deprecation_reason`. Documentar as transições permitidas (draft, pending_approval, approved, deprecated) e checá-las no validador. Converge com PV-11.

### GC-04 · Ligar termo ao ativo físico

**Confiança:** alta.

**O que é:** no Knowledge Catalog, termos se ligam a ativos e colunas por entry links do tipo `definition`. No DataHub, termos são aplicados a entidades por URN. As Pages do Unity Catalog têm "Related assets" e "Sources", e as metric views referenciam a fonte por nome em três partes. Em todos, o vínculo é um identificador resolvível.

**Fontes:** [Knowledge Catalog, glossário](https://docs.cloud.google.com/knowledge-catalog/docs/manage-glossaries); [DataHub, Business Glossary](https://docs.datahub.com/docs/glossary/business-glossary); [Databricks, Pages](https://docs.databricks.com/aws/en/uc-semantics/pages); [Databricks, metric views YAML](https://docs.databricks.com/aws/en/uc-semantics/metric-views/yaml-reference).

**Situação no Contexto:** plataforma e fonte da verdade são texto livre, o nome físico não tem catálogo nem esquema, e o modelo de dashboard não tem URL nem identificador na ferramenta de BI.

**Evidências:**
- [public/downloads/exemplo-dataset-completo.yaml:34](../public/downloads/exemplo-dataset-completo.yaml#L34) `physical_name: demo_sessions`
- [public/downloads/exemplo-dataset-completo.yaml:35](../public/downloads/exemplo-dataset-completo.yaml#L35) `platform: SQLite (laboratório)`
- [public/downloads/exemplo-kpi-completo.yaml:16](../public/downloads/exemplo-kpi-completo.yaml#L16) `source_of_truth: "Catálogo de indicadores da Aurora, entrada KPI-AURORA-001"`
- [public/downloads/template-dashboard.yaml:37](../public/downloads/template-dashboard.yaml#L37) `official_or_exploratory: null`

**Recomendação:** bloco `asset_refs` com `system` (bigquery, databricks, ga4, gtm, looker), `qualified_name`, `url` e `catalog_urn` opcional; nos exemplos Aurora, nomes realistas de BigQuery ou Databricks e de propriedade GA4 ou contêiner GTM, ligando evento, tag e tabela. Unificar com `platform_bindings` (CS-11) e os vínculos de AG-08.

### GC-05 · YAML do repositório alimentando o catálogo

**Confiança:** alta.

**O que é:** o DataHub ingere glossário em YAML com responsáveis, id, propriedades, links e domínio, e recomenda id explícito para identificadores estáveis. No dbt, `meta` aceita qualquer par chave-valor, e `persist_docs` grava descrições como comentários no BigQuery e no Databricks. A Atlan lê `certificateStatus` em `meta.atlan.attributes` do dbt.

**Fontes:** [DataHub, ingestão de glossário](https://docs.datahub.com/docs/generated/ingestion/sources/business-glossary); [dbt, meta](https://docs.getdbt.com/reference/resource-configs/meta); [dbt, persist_docs](https://docs.getdbt.com/reference/resource-configs/persist_docs); [Atlan, certificar ativos](https://docs.atlan.com/product/capabilities/build-apps/sdks/python/how-tos/certify-assets).

**Situação no Contexto:** o portal declara corretamente que não é especificação executável, mas não oferece ponte. O id estável já é a base dela.

**Evidências:**
- [src/content/docs/templates/kpi.mdx:70](../src/content/docs/templates/kpi.mdx#L70) `Não são uma norma universal nem uma especificação executável por dbt, Cube ou Snowflake.`
- [public/downloads/exemplo-kpi-completo.yaml:2](../public/downloads/exemplo-kpi-completo.yaml#L2) `id: KPI-AURORA-001`

**Recomendação:** página "Do Contexto para o catálogo" com tabela de mapeamento, sem código obrigatório: `id` para id explícito do DataHub; conceito para descrição, comentário do Unity Catalog ou visão geral do termo; `synonyms` para sinônimos da Page ou do termo; `owner`/`approver` para steward e owners (ver GC-01); `status` para estágio de ciclo de vida ou certificação; extras para `meta` do dbt ou aspect. O Contexto é a camada de autoria; o catálogo é a de distribuição.

### GC-06 · Conhecimento modelado prevalece sobre o aprendido

**Confiança:** alta.

**O que é:** no Genie Ontology, conhecimento modelado (metric views, domínios, Pages, certificação) é tratado como mais confiável que o aprendido automaticamente de dashboards e consultas, e prevalece em conflito. O Genie One prioriza e cita a Page quando responde sobre um conceito definido nela. Rascunhos dependem de um Page manager ou curador para serem publicados. Isso confirma, em fonte primária, a tese do Contexto e o caso 2.

**Fontes:** [Databricks, Genie Ontology](https://docs.databricks.com/aws/en/genie/genie-ontology/); [Databricks, Pages](https://docs.databricks.com/aws/en/uc-semantics/pages); [Databricks, Unity Catalog semantics](https://docs.databricks.com/aws/en/uc-semantics/).

**Situação no Contexto:** a página de dados descreve o problema, mas não mostra que as plataformas já materializam a solução. As referências citam o Genie, mas não o Genie Ontology, as Pages nem a regra de precedência.

**Evidências:**
- [src/content/docs/dados/visao-geral.mdx:8](../src/content/docs/dados/visao-geral.mdx#L8) `Uma IA pode escrever SQL válido, obter linhas do banco e ainda dar uma resposta que **não corresponde ao significado adotado pela organização**.`
- [src/content/docs/referencias/index.mdx:39](../src/content/docs/referencias/index.mdx#L39) `[Databricks: Tune Genie Agent quality](https://docs.databricks.com/gcp/en/genie/add-instructions)`

**Recomendação:** citar o Genie Ontology e as Pages na página de dados como evidência externa e reforçar que só documento aprovado deve virar conhecimento modelado; rascunho não é fonte para a IA.

### GC-07 · Rascunho por IA com aprovação humana

**Confiança:** alta.

**O que é:** o Databricks gera comentários por IA, exige revisão antes de salvar e diz para não usar o modelo para classificar dados como PII. No OpenMetadata (documentação de versão SNAPSHOT), termo proposto por agente nasce como Draft e só uma pessoa aprova; a fila mostra o agente com ícone de bot. O DataHub separa ferramentas de proposta de ferramentas de aplicação direta.

**Fontes:** [Databricks, comentários gerados por IA](https://docs.databricks.com/aws/en/comments/ai-comments); [OpenMetadata, aprovação de glossário](https://docs.open-metadata.org/v2.1.x-SNAPSHOT/how-to-guides/data-governance/glossary/approval); [DataHub, Change Proposals](https://docs.datahub.com/docs/managed-datahub/change-proposals); [DataHub MCP](https://docs.datahub.com/docs/features/feature-guides/mcp).

**Situação no Contexto:** o portal diz que a engenharia não deve inventar conteúdo, mas não trata o uso de IA para redigir rascunhos a partir de planilhas, tag plans ou schemas, que é o fluxo que o público vai tentar. A matriz RACI não tem linha para isso.

**Evidências:**
- [src/content/docs/governanca/papeis.mdx:33](../src/content/docs/governanca/papeis.mdx#L33) `O engenheiro pode ajudar a estruturar o documento, mas não deve inventar o conteúdo.`
- [src/content/docs/governanca/papeis.mdx:35](../src/content/docs/governanca/papeis.mdx#L35) `## Modelo simplificado de matriz RACI`
- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:3](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L3) `description: Faça um primeiro registro de conhecimento sem programar ou entender de IA.`

**Recomendação:** regra explícita: a IA pode propor rascunhos (`status: draft`, com `drafted_by: ai` ou equivalente no histórico de versões), mas só quem aprova muda para `approved`; nunca usar IA para preencher classificação de sensibilidade. Linha "Rascunho assistido por IA" na matriz RACI.

### GC-08 · Sensibilidade e acesso

**Confiança:** média.

**O que é:** o tutorial do Knowledge Catalog cria um aspect com Data Steward (obrigatório), Data Sensitivity (Public, Internal, Confidential) e Last Review Date; a página de aspects descreve campos como "Has PII". No Databricks, tags governadas servem para classificação e controle de acesso por atributos.

**Fontes:** [Knowledge Catalog, governança básica](https://docs.cloud.google.com/dataplex/docs/build-foundational-data-governance); [Knowledge Catalog, aspects](https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata); [Databricks, governed tags](https://docs.databricks.com/aws/en/admin/governed-tags/).

**Situação no Contexto:** a governança define política de acesso, mas nenhum modelo tem campo de sensibilidade ou restrição de uso.

**Evidências:**
- [src/content/docs/governanca/papeis.mdx:16](../src/content/docs/governanca/papeis.mdx#L16) `| Governança | Resolve hierarquia de fontes e define políticas de revisão e acesso |`
- [public/downloads/template-dataset.yaml:24](../public/downloads/template-dataset.yaml#L24) `platform: null`

**Recomendação:** `access_classification` no cabeçalho comum (por exemplo público, interno, restrito, pessoal_LGPD) e `sensitivity` por coluna no dataset, sempre preenchidos por uma pessoa, com explicação em linguagem simples. Não colocar dados pessoais nos próprios valores das tags.

### GC-09 · Domínio único e hierarquia de termos

**Confiança:** média.

**O que é:** catálogos organizam termos em domínios e grupos (domínios e subdomínios no Unity Catalog; Term Groups no DataHub; categorias em até três níveis no Knowledge Catalog), separando sinônimos de termos relacionados.

**Fontes:** [Databricks, descoberta de dados](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-discovery); [DataHub, Business Glossary](https://docs.datahub.com/docs/glossary/business-glossary); [Knowledge Catalog, glossário](https://docs.cloud.google.com/knowledge-catalog/docs/manage-glossaries).

**Situação no Contexto:** sinônimos, termos relacionados e não sinônimos estão bem alinhados. Mas `domain` fica no topo do indicador e dentro de `context` no conceito, e não há termo mais amplo.

**Evidências:**
- [public/downloads/template-kpi.yaml:10](../public/downloads/template-kpi.yaml#L10) `domain: null`
- [public/downloads/template-conceito.yaml:24](../public/downloads/template-conceito.yaml#L24) `domain: null`
- [public/downloads/template-conceito.yaml:33](../public/downloads/template-conceito.yaml#L33) `not_synonyms: []`
- [src/content/docs/referencias/index.mdx:21](../src/content/docs/referencias/index.mdx#L21) `Nosso glossário não é serialização formal SKOS`

**Recomendação:** `domain` no cabeçalho comum, com valores controlados num arquivo de domínios; `broader_term` opcional no conceito; manter `not_synonyms` como diferencial.

### GC-10 · DCAT 3 e schema.org como referência

**Confiança:** média.

**O que é:** o DCAT 3 (W3C Recommendation, 22/08/2024) tem `dcat:version` e `dcat:previousVersion` (subpropriedade de `prov:wasRevisionOf`) e prevê perfis com campos mínimos. O schema.org Dataset cobre descoberta pública.

**Fontes:** [W3C, DCAT 3](https://www.w3.org/TR/vocab-dcat-3/); [schema.org, Dataset](https://schema.org/Dataset).

**Situação no Contexto:** o portal cita DCMI, SKOS e PROV-O, mas não o DCAT, embora `version` e `supersedes_revision` correspondam a propriedades dele.

**Evidências:**
- [src/content/docs/metodo/identificacao-versoes.mdx:98](../src/content/docs/metodo/identificacao-versoes.mdx#L98) `[W3C PROV-O](https://www.w3.org/TR/prov-o/): proveniência, revisões e atribuições.`
- [src/content/docs/referencias/index.mdx:20](../src/content/docs/referencias/index.mdx#L20) `| [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) | Propriedades e identificação de documentos | YAML de exemplo não é schema DCMI |`

**Recomendação:** citar o DCAT 3 nas referências como base do modelo de versão, com a ressalva de que o YAML não é RDF. schema.org só para quem publica dados abertos.

### Não verificado nesta frente

- Conteúdo literal dos capítulos de glossário e stewardship do DAMA-DMBOK2; só a página de revisão e o glossário da DAMA UK foram lidos.
- Status e data do DMBOK 3.0.
- Classificações PII e Tier do OpenMetadata como metadado de governança.
- Status GA de Pages e metric views no Databricks (não marcados como Beta, mas sem GA explícito).
- Se os prazos de certificação do OpenMetadata (P30D, P60D) continuam iguais na documentação atual.
- Se o id explícito do DataHub sobrevive a renomeações (a página fala só de mover na hierarquia).
- Servidores MCP oficiais de Collibra, Atlan e Knowledge Catalog.
- Afirmação da Atlan de que certificados "decaem" (vem de blog, não de documentação).
- Formato de importação e exportação do Knowledge Catalog a partir de Git.

## Protocolos e padrões emergentes

| Nome | Maturidade | Fonte | O que preparar já |
|---|---|---|---|
| Apache Ossie (antigo Open Semantic Interchange, OSI) | Podling da Apache Incubator (renomeado em 08/07/2026). 0.1.1 lançada em 11/12/2025; 0.3.0.dev0 em rascunho, sem uso em produção; sem construto de filtro. O Snowflake cria semantic views a partir de Ossie 0.1.1 e guarda `ai_context` só como metadado | https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md ; https://github.com/open-semantic-interchange/OSI/blob/main/docs/index.md ; https://www.snowflake.com/en/blog/apache-ossie-open-semantic-interchange-incubator/ ; https://docs.snowflake.com/en/sql-reference/stored-procedures/system_create_semantic_view_from_ossie_yaml | Tabela de correspondência contra a 0.1.1 e versão alvo declarada; o que a IA precisa respeitar também em `description` |
| Open Data Contract Standard (ODCS) 3.2.0 e ODPS 1.1.0 | Aprovados (Bitol, LF AI & Data), sem mudanças incompatíveis; bloco `context` para IA, `synonyms`, `semanticType`, `enum`, `deprecated` | https://bitol.io/data-contracts-data-products-for-ai/ ; https://github.com/bitol-io/open-data-contract-standard/blob/main/CHANGELOG.md | Crosswalk de campos e citação na bibliografia; padrão `apiVersion` + `version` + `status` |
| Model Context Protocol (MCP) 2026-07-28 | Lançado para uso geral; núcleo stateless, `server/discover`, `ttlMs` e `cacheScope` obrigatórios | https://blog.modelcontextprotocol.io/posts/2026-07-28/ | URIs `id@versão`, JSON Schema por tipo e nota de design (AG-07) |
| Servidores MCP de dados (BigQuery, Databricks Genie One, GA4, Google Ads) | Variável: Genie One em GA; endpoints de workspace do Databricks em Public Preview; GA4 só leitura por padrão; Google Ads v0.0.6; estágio do BigQuery não informado | https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp ; https://docs.databricks.com/aws/en/agents/mcp-tools/genie-mcp ; https://developers.google.com/analytics/devguides/MCP ; https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server | Vínculos com nomes qualificados e comportamento esperado do dado nos modelos (AG-08, GC-04) |
| Servidores MCP de catálogos (DataHub, OpenMetadata, dbt) | Disponíveis; ferramentas remotas do dbt podem mudar sem aviso | https://docs.datahub.com/docs/features/feature-guides/mcp ; https://docs.open-metadata.org/v1.13.x/how-to-guides/mcp ; https://docs.getdbt.com/docs/dbt-ai/mcp-available-tools | Posicionar o Contexto como fonte autoral que alimenta o catálogo (GC-05) |
| Unity Catalog semantics (Pages, Genie Ontology) | Pages, metric views, domínios e certificação documentados sem Beta; Wikis e automação de tags em Beta | https://docs.databricks.com/aws/en/uc-semantics/ ; https://docs.databricks.com/aws/en/genie/genie-ontology/ | Conceitos para Pages e indicadores para metric views na página de mapeamento |
| Google Knowledge Catalog (antigo Dataplex) e agentes de dados do BigQuery | Produto renomeado, documentado | https://docs.cloud.google.com/knowledge-catalog/docs/manage-glossaries ; https://docs.cloud.google.com/dataplex/docs/data-insights-structured-data | `linked_columns` no conceito; aviso do limite de 10 termos por tabela |
| Cube `meta.ai_context` | Documentado; até 2.000 caracteres, truncamento silencioso | https://docs.cube.dev/docs/data-modeling/ai-context | Separar texto para pessoas de texto só para a IA |
| Snowflake: de Cortex Analyst para Cortex Agents | Recomendação explícita da Snowflake; orientações sobre sinônimos mudaram em fev 2026 | https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/suggested-questions-feature | Escrever instruções em linguagem natural, separadas por finalidade (CS-05) |
| llms.txt v2 | Proposta comunitária (10/08/2026), sem organismo de padronização | https://llmstxt.org/ | Plugin starlight-llms-txt em subcaminho (AG-01) |
| AGENTS.md | Formato aberto, Agentic AI Foundation (Linux Foundation) | https://agents.md/ | AGENTS.md no repositório e trecho modelo para times (AG-05) |
| Agent Skills (SKILL.md) | Especificação aberta, criada pela Anthropic | https://agentskills.io/specification | Duas skills: descoberta e consulta por versão (AG-06) |
| WebMCP | Draft Community Group Report do W3C (13/11/2026), fora do Standards Track; API declarativa retirada da especificação em 08/10/2026 pelo PR #338; origin trial a partir do Chrome 149 | https://webmachinelearning.github.io/webmcp/ ; https://github.com/webmachinelearning/webmcp/pull/338 ; https://developer.chrome.com/docs/ai/webmcp | Nada além dos JSON Schemas; acompanhar, não implementar |
| Universal Commerce Protocol (UCP) | Versões estáveis datadas; a mais recente listada é 2026-08-25 | https://ucp.dev/latest/specification/overview/index.md ; https://ucp.dev/ | Tema para times de e-commerce documentarem políticas; exige `/.well-known` (AG-11) |
| Personal Agent Protocol (Poppy), da Sierra | Anunciado em 06/10/2026, rascunho em 09/10/2026, v1.0 em 13/11/2026 | https://sierra.ai/blog/releasing-poppy ; https://personalagentprotocol.org/docs/1.0/spec | Monitorar; relevância indireta (orientações que a empresa dá ao agente visitante também precisam estar aprovadas) |
| Tag plan com observabilidade (Avo, Segment Protocols, Amplitude Observe, Snowplow SchemaVer) | Produtos maduros | https://www.avo.app/docs/data-design/avo-tracking-plan/properties ; https://amplitude.com/docs/data/validate-events | Modelo de evento com regra de negócio e raridade por operação (EM-07, EM-08) |
| Keep a Changelog 2.0.0 | Convenção publicada em 07/06/2026 | https://keepachangelog.com/en/2.0.0/ | CHANGELOG.md na raiz (PV-13) |
| NotebookLM / Gemini Notebook | Em produção; ajuda oficial usa o nome Gemini Notebook; API de Sources aceita texto e Markdown | https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en | Exemplos em .md e guia de preparação (AG-10) |
| Termos propostos por agentes com aprovação humana (OpenMetadata, DataHub) | OpenMetadata documentado só em versão SNAPSHOT; DataHub documentado | https://docs.open-metadata.org/v2.1.x-SNAPSHOT/how-to-guides/data-governance/glossary/approval ; https://docs.datahub.com/docs/managed-datahub/change-proposals | Regra de rascunho por IA (GC-07) |

Divergência entre frentes que precisa de conferência: a frente de camada semântica lista os conversores de referência do Ossie como dbt, GoodData, Polaris e Salesforce (repositório apache/ossie-converters), e a de agentes como dbt MetricFlow, Apache Polaris e Snowflake.

## Descartados na verificação

| ID | Afirmação removida ou corrigida | Motivo |
|---|---|---|
| D-01 | Mapear filtro do Contexto para `dimension.label: filter` no Ossie | O Ossie 0.3.0.dev0 não tem construto de filtro e `label` é só etiqueta de categorização |
| D-02 | Governança falta por completo nos fornecedores | Há `verified_by`, `verified_at`, tags, contatos e `config.meta`; falta o conjunto status, histórico e vigência |
| D-03 | Sinônimos genéricos como prática recomendada (confiança alta) | O guia da Snowflake de fev 2026 deixou de recomendar; rebaixado para média e restrito a jargão |
| D-04 | `is_enum` em fatos e indicadores; `verified_at` como data | `is_enum` só existe em dimensões; `verified_at` é epoch em segundos |
| D-05 | Avo oferece "Never" para propriedades de evento | Só Always e Sometimes; Never vale para propriedades de sistema |
| D-06 | Elementary alerta para falsos positivos com poucos pontos de treino | A página só diz que ignorar sazonalidade pode gerar falsos positivos |
| D-07 | SQL de referência obrigatório no Genie | É opcional, recomendado e necessário só para avaliação automática |
| D-08 | Snowflake cita erros de junção e de agregação sobre snapshot | O post cobre view pré-juntada e eixo de tempo não consecutivo; junção e snapshot vêm só do preprint |
| D-09 | Poppy teve "cerca de 5 semanas de draft" | Sem fonte |
| D-10 | A página do GA4 em developers.google.com lista `list_key_events` | A ferramenta está no README do repositório |
| D-11 | O `search` do Google Ads recebe uma string GAQL | Monta a consulta a partir de parâmetros estruturados |
| D-12 | O site agents.md lista o Claude Code como compatível | Não lista |
| D-13 | Só três modelos guardam cópia integral de versões antigas | São dois: conceito e indicador |
| D-14 | O ODCS exige SemVer no campo `version` | Dá exemplo 1.1.0, sem exigir |
| D-15 | O dbt impede remover qualquer modelo antes de `deprecation_date` | Só modelos versionados ou com contrato imposto |
| D-16 | Range da ISO 22400-2 como faixa esperada | É limite lógico superior e inferior |
| D-17 | Pacotes do The Good Docs Project alinhados ao Diátaxis | Nem a página de guias nem o guia de concept mencionam o Diátaxis |
| D-18 | NN/g diz que card sorting "não captura o contexto" | O artigo não traz isso; o limite apontado é o excesso de cartões |
| D-19 | A API WebMCP "mudou várias vezes ao longo de 2026" | Só a retirada da API declarativa em 08/10/2026 está confirmada |
| D-20 | A página de indicador publicada tem cerca de 3.000 palavras | Não foi medido |
| D-21 | O exemplo preenchido só existe em YAML | Na página aparece em abas legíveis; só o download é YAML |
| D-22 | As páginas de modelo precisam renomear a seção dos exemplos | Já usam "Antes e depois da decisão"; a recomendação vale só para os rótulos de download |
| D-23 | Papel Privacy Steward no Collibra | Não aparece na página de resource roles |
| D-24 | Classificações PII e Tier do OpenMetadata citadas pela página MCP | A página MCP não fala disso |
| D-25 | Rascunhos de Pages do Databricks só aparecem para o responsável | Page managers também os veem |
| D-26 | O portal não cita o Genie | Cita em [src/content/docs/referencias/index.mdx:39](../src/content/docs/referencias/index.mdx#L39) (`Databricks: Tune Genie Agent quality`); a lacuna é sobre Genie Ontology e Pages |

## Não coberto nesta rodada

- Nenhuma prática foi testada com usuários reais (card sorting, tree testing, teste de leitura com público não técnico).
- Build, validador e scripts do repositório não foram executados; a execução estava bloqueada nesta sessão.
- Auditoria de acessibilidade (contraste, foco, leitores de tela) e teste em celular do portal publicado.
- Compatibilidade do plugin starlight-llms-txt com Starlight 0.43 e Astro 7.
- Atribuição padrão do Meta Ads e de outras plataformas de mídia além do Google Ads.
- Servidores MCP oficiais de Collibra, Atlan e Knowledge Catalog.
- Críticas acadêmicas ao SECI, técnicas do BABOK v3 e capítulos do DMBOK2.
- Efeito de reversão pela expertise para público misto.
- Confirmação independente de qualquer número de acurácia vindo de fornecedores.

## Fontes consultadas

As fontes estão agrupadas por frente. Algumas aparecem em mais de uma frente.

### Camada semântica (CS)

- CS-S1. Snowflake: YAML specification for semantic views. https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec
- CS-S2. Snowflake: Cortex Analyst Verified Query Repository. https://docs.snowflake.com/en/user-guide/views-semantic/verified-query-repository
- CS-S3. Snowflake: Custom instructions in Cortex Analyst. https://docs.snowflake.com/en/user-guide/views-semantic/custom-instructions
- CS-S4. Snowflake: Best Practices for Creating Semantic Views for Cortex Analyst (2026-02-03). https://www.snowflake.com/en/developers/guides/best-practices-semantic-views-cortex-analyst/
- CS-S5. Snowflake: Onboarding questions in Cortex Analyst. https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/suggested-questions-feature
- CS-S6. Databricks: Metric view YAML syntax reference (2026-10-28). https://docs.databricks.com/aws/en/metric-views/data-modeling/syntax
- CS-S7. Databricks: Tune Genie Agent quality (2026-11-05). https://docs.databricks.com/aws/en/genie/add-instructions
- CS-S8. Databricks: Test and monitor a Genie Agent, benchmarks (2026-11-05). https://docs.databricks.com/aws/en/genie/benchmarks
- CS-S9. dbt: Semantic models (v1.12+). https://docs.getdbt.com/docs/build/semantic-models
- CS-S10. dbt: Ratio metrics. https://docs.getdbt.com/docs/build/ratio
- CS-S11. dbt: Conversion metrics. https://docs.getdbt.com/docs/build/conversion
- CS-S12. Apache Ossie Core Metadata Specification (0.3.0.dev0). https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md
- CS-S13. apache/ossie, repositório. https://github.com/apache/ossie
- CS-S14. Snowflake: Open Semantic Interchange Updates, Specification Now Live (2026-01-27). https://www.snowflake.com/en/blog/open-semantic-interchanges-specs-finalized/
- CS-S15. Google Cloud: Define data agent context for BigQuery data sources. https://docs.cloud.google.com/gemini/data-agents/conversational-analytics-api/data-agent-authored-context-bq
- CS-S16. Google Cloud: Best practices for configuring Conversational Analytics in Looker. https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices
- CS-S17. Google Cloud: Create and manage Explore data agents. https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-data-agents
- CS-S18. Google Cloud: Conversational Analytics in Looker overview. https://docs.cloud.google.com/looker/docs/conversational-analytics-overview
- CS-S19. Google Cloud: Manage a business glossary (Knowledge Catalog). https://docs.cloud.google.com/knowledge-catalog/docs/manage-glossaries
- CS-S20. Google Cloud: About data insights for structured data. https://docs.cloud.google.com/dataplex/docs/data-insights-structured-data
- CS-S21. Cube: AI context. https://docs.cube.dev/docs/data-modeling/ai-context
- CS-S22. Cube: Views. https://docs.cube.dev/docs/data-modeling/views
- CS-S23. Ossie docs index. https://github.com/open-semantic-interchange/OSI/blob/main/docs/index.md
- CS-S24. Cube: Joins reference. https://docs.cube.dev/reference/data-modeling/joins

### Evidência e martech (EM)

- EM-S1. Rumiantsau e Fokeev (2026), Semantic Layers for Reliable LLM-Powered Data Analytics, arXiv 2604.25149v1. https://arxiv.org/pdf/2604.25149v1
- EM-S2. Li et al., BIRD (NeurIPS 2023). https://arxiv.org/html/2305.03111
- EM-S3. Lei et al., Spider 2.0 (ICLR 2025). https://arxiv.org/abs/2411.07763
- EM-S4. Sequeda, Allemang, Jacob (2023). https://arxiv.org/abs/2311.07509
- EM-S5. BEAVER: An Enterprise Benchmark for Text-to-SQL. https://arxiv.org/abs/2409.02038
- EM-S6. Painter et al., JAMIA Open 8(1):ooaf003 (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC11806702/
- EM-S6b. Painter et al., arXiv 2406.10690v3. https://arxiv.org/html/2406.10690v3
- EM-S7. dbt Labs: Semantic Layer vs. Text-to-SQL, 2026 Benchmark Update (2026-04-07). https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026
- EM-S8. Snowflake: Cortex Analyst, Evaluating Text-to-SQL Accuracy for Real-World BI (2024-08-29). https://www.snowflake.com/en/blog/engineering/cortex-analyst-text-to-sql-accuracy-bi/
- EM-S9. Databricks: Curate an effective Genie Agent. https://docs.databricks.com/aws/en/genie-agents/best-practices
- EM-S10. Databricks: Test and monitor a Genie Agent. https://docs.databricks.com/aws/en/genie-agents/monitor
- EM-S11. Google: [GA4] Data freshness. https://support.google.com/analytics/answer/11198161?hl=en
- EM-S12. Google: [GA4] Anomaly detection. https://support.google.com/analytics/answer/9517187?hl=en
- EM-S13. Google Ads: Create conversions from Google Analytics events. https://support.google.com/google-ads/answer/2375435?hl=en
- EM-S14. Google Ads: Data discrepancies. https://support.google.com/google-ads/answer/7457111?hl=en
- EM-S15. Avo: Properties. https://www.avo.app/docs/data-design/avo-tracking-plan/properties
- EM-S16. Avo: Sources. https://www.avo.app/docs/data-design/avo-tracking-plan/define-sources-and-destinations
- EM-S17. Twilio Segment: Protocols Tracking Plan. https://www.twilio.com/docs/segment/protocols/tracking-plan/create
- EM-S18. Amplitude: Monitor your data with Observe. https://amplitude.com/docs/data/validate-events
- EM-S19. Amplitude: Planned events that never arrived. https://amplitude.com/docs/data/data-assistant-user-solutions/planned-unseen-events-audit
- EM-S20. Snowplow: Versioning schemas (SchemaVer). https://docs.snowplow.io/docs/fundamentals/schemas/versioning/
- EM-S21. Elementary: seasonality. https://docs.elementary-data.com/data-tests/anomaly-detection-configuration/seasonality
- EM-S22. Elementary: volume_anomalies. https://docs.elementary-data.com/data-tests/anomaly-detection-tests/volume-anomalies
- EM-S23. dbt: freshness config. https://docs.getdbt.com/reference/resource-configs/freshness
- EM-S24. ODCS v3.2.0: Service-Level Agreement. https://bitol-io.github.io/open-data-contract-standard/v3.2.0/service-level-agreement/
- EM-S25. Apache Ossie Core Metadata Specification. https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md
- EM-S26. WebMCP, Draft Community Group Report (2026-11-13). https://webmachinelearning.github.io/webmcp/
- EM-S27. UCP Specification overview. https://ucp.dev/latest/specification/overview/index.md
- EM-S27b. UCP, página inicial. https://ucp.dev/
- EM-S28. Sierra: Releasing Personal Agent Protocol 1.0 (2026-11-13). https://sierra.ai/blog/releasing-poppy
- EM-S28b. Personal Agent Protocol specification 1.0. https://personalagentprotocol.org/docs/1.0/spec
- EM-S29. Google for Developers: GA4 event parameters. https://developers.google.com/analytics/devguides/collection/ga4/event-parameters

### Agentes e protocolos (AG)

- AG-S1. The /llms.txt file, v2 (2026-08-10). https://llmstxt.org/
- AG-S2. AGENTS.md. https://agents.md/
- AG-S3. Agent Skills Specification. https://agentskills.io/specification
- AG-S4. MCP 2026-07-28 changelog. https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx
- AG-S5. MCP blog: The 2026-07-28 Specification. https://blog.modelcontextprotocol.io/posts/2026-07-28/
- AG-S6. MCP Server Resources (2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/server/resources
- AG-S7. MCP Prompts (2025-11-25). https://modelcontextprotocol.io/specification/2025-11-25/server/prompts
- AG-S8. Google Cloud: Use the BigQuery MCP server. https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp
- AG-S9. Databricks-provided MCPs (2026-11-13). https://docs.databricks.com/aws/en/agents/mcp-tools/built-in-mcp-services
- AG-S10. Databricks: Genie One MCP server (2026-11-12). https://docs.databricks.com/aws/en/agents/mcp-tools/genie-mcp
- AG-S11. Google for Developers: Try the Google Analytics MCP server. https://developers.google.com/analytics/devguides/MCP
- AG-S12. googleanalytics/google-analytics-mcp (v1.1.0). https://github.com/googleanalytics/google-analytics-mcp/
- AG-S13. Google Ads MCP server: Developer integration guide. https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
- AG-S14. googleads/google-ads-mcp (v0.0.6). https://github.com/googleads/google-ads-mcp
- AG-S15. WebMCP, Draft Community Group Report. https://webmachinelearning.github.io/webmcp/
- AG-S16. Chrome for Developers: WebMCP (2026-10-07). https://developer.chrome.com/docs/ai/webmcp
- AG-S17. UCP Core Concepts. http://ucp.dev/documentation/core-concepts/
- AG-S18. UCP Specification Overview. https://ucp.dev/latest/specification/overview/index.md
- AG-S19. Sierra: Introducing Personal Agent Protocol (2026-10-06). https://sierra.ai/blog/introducing-personal-agent-protocol
- AG-S20. Sierra: Sharing a draft of Personal Agent Protocol (2026-10-09). https://sierra.ai/blog/poppy
- AG-S21. Sierra: Releasing Personal Agent Protocol 1.0 (2026-11-13). https://sierra.ai/blog/releasing-poppy
- AG-S22. ODCS CHANGELOG. https://github.com/bitol-io/open-data-contract-standard/blob/main/CHANGELOG.md
- AG-S23. Bitol: Data Contracts & Data Products for AI. https://bitol.io/data-contracts-data-products-for-ai/
- AG-S24. Apache Ossie core spec. https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md
- AG-S25. Snowflake: Apache Ossie (Incubating) (2026-07-08). https://www.snowflake.com/en/blog/apache-ossie-open-semantic-interchange-incubator/
- AG-S26. Gemini Notebook Help: Add or discover new sources. https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en
- AG-S27. Gemini Notebook API: Sources. https://developers.google.com/notebook/docs/sources
- AG-S28. Microsoft Learn: RAG enrichment phase. https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-enrichment-phase
- AG-S29. Microsoft Learn: RAG chunking phase. https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase
- AG-S30. Anthropic: Contextual retrieval (2024-09-19). https://www.anthropic.com/research/contextual-retrieval
- AG-S31. starlight-llms-txt: Configuration. https://delucis.github.io/starlight-llms-txt/configuration/
- AG-S32. Chrome for Developers: WebMCP Imperative API. https://developer.chrome.com/docs/ai/webmcp/imperative-api
- AG-S33. MCP Server Tools (2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- AG-S34. Agent Skills Overview. https://agentskills.io/

### Perguntas e versionamento (PV)

- PV-S1. Basili, Caldiera, Rombach (1994), The Goal Question Metric Approach. http://www.cs.umd.edu/projects/SoftEng/ESEG/papers/gqm.pdf
- PV-S2. Corr e Stagnitto (2011), Agile Data Warehouse Design. https://books.google.com/books/about/Agile_Data_Warehouse_Design.html?id=TRWFmnv8jP0C
- PV-S3. BEAM Templates. https://modelstorming.com/templates
- PV-S4. ISO 22400-2:2014, amostra oficial. https://cdn.standards.iteh.ai/samples/54497/10e33d2a34c144558b5e3024ee5e1cb0/ISO-22400-2-2014.pdf
- PV-S5. Levers Labs: Designing Metric Trees (2024-04-08). https://www.leverslabs.com/article/designing-metric-trees
- PV-S6. Klein, Calderwood, MacGregor (1989), Critical decision method for eliciting knowledge. https://ieeexplore.ieee.org/document/31053/
- PV-S23. Klein et al. (1989), texto integral. https://www.theisrm.org/documents/Klein%20(1989)%20Critical%20Decision%20Method%20for%20Eliciting%20Knowledge.pdf
- PV-S7. Nonaka, Toyama, Konno (2000), SECI, Ba and Leadership. https://www.sciencedirect.com/science/article/pii/S0024630199001156
- PV-S8. IIBA Business Analysis Standard: Elicitation and Collaboration. https://www.iiba.org/knowledgehub/the-business-analysis-standard/5-applying-business-analysis-tasks/5-3-business-analysis-knowledge-areas/elicitation-and-collaboration/
- PV-S9. KCS v6 Technique 5.2: KCS Article State. https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/040/010/030
- PV-S10. OMG: Decision Model and Notation 1.6. https://www.omg.org/spec/DMN/1.6
- PV-S11. ODCS: Fundamentals. https://github.com/bitol-io/open-data-contract-standard/blob/main/docs/fundamentals.md
- PV-S12. ODCS CHANGELOG. https://github.com/bitol-io/open-data-contract-standard/blob/main/CHANGELOG.md
- PV-S13. Semantic Versioning 2.0.0. https://semver.org/spec/v2.0.0.html
- PV-S14. Martin Fowler: Bitemporal History (2021-04-07). https://martinfowler.com/articles/bitemporal-history.html
- PV-S15. Michael Nygard: Documenting Architecture Decisions (2011-11-15). https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- PV-S16. Keep a Changelog 2.0.0 (2026-06-07). https://keepachangelog.com/en/2.0.0/
- PV-S17. dbt: Model versions. https://docs.getdbt.com/docs/mesh/govern/model-versions
- PV-S18. dbt: deprecation_date. https://docs.getdbt.com/reference/resource-properties/deprecation_date
- PV-S19. Snowflake: Cortex Analyst Verified Query Repository. https://docs.snowflake.com/en/user-guide/views-semantic/verified-query-repository
- PV-S20. Databricks: Test and monitor a Genie Agent. https://docs.databricks.com/aws/en/genie-agents/monitor
- PV-S21. Apache Ossie (incubating). https://ossie.apache.org/
- PV-S22. Apache Ossie Core Metadata Specification. https://github.com/open-semantic-interchange/OSI/blob/main/core-spec/spec.md
- PV-S24. Snowflake: SYSTEM$CREATE_SEMANTIC_VIEW_FROM_OSSIE_YAML. https://docs.snowflake.com/en/sql-reference/stored-procedures/system_create_semantic_view_from_ossie_yaml
- PV-S25. Snowflake: Getting Started with Apache OSI. https://www.snowflake.com/en/developers/guides/getting-started-with-apache-osi/

### Público misto (UX)

- UX-S1. Diátaxis. https://diataxis.fr/
- UX-S2. Diátaxis: The compass. https://diataxis.fr/compass/
- UX-S3. ISO 24495-1:2023 Plain language. https://www.iso.org/standard/78907.html
- UX-S4. Lei nº 15.263, de 14 de novembro de 2025. https://planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15263.htm
- UX-S5. Sweller e Cooper (1985). https://doi.org/10.1207/s1532690xci0201_3
- UX-S6. Renkl e Atkinson (2003). https://doi.org/10.1207/s15326985ep3801_3
- UX-S7. Atkinson, Renkl e Merrill (2003). https://doi.org/10.1037/0022-0663.95.4.774
- UX-S8. Renkl, Atkinson e Maier (2000). https://escholarship.org/uc/item/81b9j9hs
- UX-S9. The Good Docs Project: Template guides. https://www.thegooddocsproject.dev/template
- UX-S10. The Good Docs Project: Concept template guide. https://www.thegooddocsproject.dev/template/concept
- UX-S11. NN/g: Progressive Disclosure (2006-12-03). https://www.nngroup.com/articles/progressive-disclosure/
- UX-S12. NN/g: Information Scent (2020-02-02). https://www.nngroup.com/articles/information-scent/
- UX-S13. NN/g: Card Sorting (2024-02-02). https://www.nngroup.com/articles/card-sorting-definition/
- UX-S14. Starlight: Using Components. https://starlight.astro.build/components/using-components/
- UX-S15. Starlight: Steps. https://starlight.astro.build/components/steps/
- UX-S16. Starlight: Cards. https://starlight.astro.build/components/cards/
- UX-S17. Starlight: Asides. https://starlight.astro.build/components/asides/
- UX-S18. Starlight: CSS & Styling. https://starlight.astro.build/guides/css-and-tailwind/
- UX-S19. The /llms.txt file, v2. https://llmstxt.org/
- UX-S20. WebMCP, Draft Community Group Report. https://webmachinelearning.github.io/webmcp/
- UX-S21. Portal publicado do Contexto (observado em 2026-11-17). https://edoardolobl.github.io/contexto-framework/
- UX-S22. webmachinelearning/webmcp PR #338 (2026-10-08). https://github.com/webmachinelearning/webmcp/pull/338

### Governança e catálogos (GC)

- GC-S1. Databricks: Flag data as certified or deprecated (2026-11-10). https://docs.databricks.com/aws/en/data-governance/unity-catalog/certify-deprecate-data
- GC-S2. Databricks: Unity Catalog semantics (2026-11-09). https://docs.databricks.com/aws/en/uc-semantics/
- GC-S3. Databricks: Pages (2026-11-10). https://docs.databricks.com/aws/en/uc-semantics/pages
- GC-S4. Databricks: Genie Ontology (2026-11-09). https://docs.databricks.com/aws/en/genie/genie-ontology/
- GC-S5. Databricks: AI-generated comments (2026-09-11). https://docs.databricks.com/aws/en/comments/ai-comments
- GC-S6. Databricks: Metric view YAML syntax reference (2026-10-28). https://docs.databricks.com/aws/en/uc-semantics/metric-views/yaml-reference
- GC-S7. Databricks: Governed tags (2026-11-11). https://docs.databricks.com/aws/en/admin/governed-tags/
- GC-S8. Google Cloud: Manage a business glossary. https://docs.cloud.google.com/knowledge-catalog/docs/manage-glossaries
- GC-S9. Google Cloud: Manage aspects and enrich metadata. https://docs.cloud.google.com/knowledge-catalog/docs/enrich-entries-metadata
- GC-S10. Google Cloud: Build foundational data governance. https://docs.cloud.google.com/dataplex/docs/build-foundational-data-governance
- GC-S11. DataHub: Business Glossary Guide. https://docs.datahub.com/docs/glossary/business-glossary
- GC-S12. DataHub: Business Glossary ingestion source. https://docs.datahub.com/docs/generated/ingestion/sources/business-glossary
- GC-S13. DataHub: MCP Server. https://docs.datahub.com/docs/features/feature-guides/mcp
- GC-S14. DataHub: Change Proposals. https://docs.datahub.com/docs/managed-datahub/change-proposals
- GC-S15. OpenMetadata: Glossary Approval Workflow (versão SNAPSHOT). https://docs.open-metadata.org/v2.1.x-SNAPSHOT/how-to-guides/data-governance/glossary/approval
- GC-S16. OpenMetadata: MCP Server. https://docs.open-metadata.org/v1.13.x/how-to-guides/mcp
- GC-S17. OpenMetadata PR #18392, Asset Certification (2024-10-30). https://github.com/open-metadata/OpenMetadata/pull/18392
- GC-S18. Atlan: Add certificates. https://docs.atlan.com/product/capabilities/discovery/how-tos/add-certificates
- GC-S19. Atlan: Certify assets. https://docs.atlan.com/product/capabilities/build-apps/sdks/python/how-tos/certify-assets
- GC-S20. Collibra: Resource roles (2026-04-03). https://productresources.collibra.com/docs/collibra/latest/Content/Settings/RolesAndPermissions/Roles/ResourceRoles/to_resource-roles.htm
- GC-S21. DAMA International: DAMA DMBOK Revision. https://dama.org/dama-dmbok-revision/
- GC-S22. DAMA UK: Glossary of Data Management Terms. https://www.dama-uk.org/pages/glossary
- GC-S23. dbt: persist_docs. https://docs.getdbt.com/reference/resource-configs/persist_docs
- GC-S24. dbt: meta. https://docs.getdbt.com/reference/resource-configs/meta
- GC-S25. dbt MCP: Available tools. https://docs.getdbt.com/docs/dbt-ai/mcp-available-tools
- GC-S26. W3C: Data Catalog Vocabulary (DCAT) Version 3 (2024-08-22). https://www.w3.org/TR/vocab-dcat-3/
- GC-S27. schema.org: Dataset. https://schema.org/Dataset
- GC-S28. Open Data Contract Standard, repositório. https://github.com/bitol-io/open-data-contract-standard
- GC-S29. Databricks: Data discovery in Unity Catalog (2026-11-10). https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-discovery
- GC-S30. ODCS: Team. https://bitol-io.github.io/open-data-contract-standard/latest/team/
