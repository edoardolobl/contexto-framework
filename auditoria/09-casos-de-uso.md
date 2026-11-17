# Casos reais contra o Contexto atual

Data: 2026-11-17 · Commit: d08c810 · Escopo: três casos de uso (dois relatados pelo mantenedor e um plausível) testados contra os modelos YAML, os exemplos completos, a amostra do Laboratório Aurora e as páginas do portal

## Resumo

- **Caso 1, evento raro marcado como quebrado (tag plan x Databricks): cobertura baixa.** Só há peças soltas (`comparison_baseline` no dashboard, `applies_when` no conceito, `decision_table` na decisão). Nenhum modelo registra o comportamento esperado de um evento: volume, raridade, onde ele dispara em cada operação, janela histórica e o que significa a falta de linha. Gravidade alta.
- **Caso 2, indicador calculado com a definição genérica: cobertura alta no conteúdo.** O modelo de KPI captura definição, exclusões e significados em outras áreas. Falta dizer ao agente o que fazer quando a definição falta ou não está aprovada, e ligar o indicador ao objeto físico que o agente consulta. Gravidade média.
- **Caso 3, cruzamento GA4 x mídia x BigQuery: cobertura média.** Junção, conflito entre dashboards e precedência existem. Faltam atribuição, fuso por fonte, taxonomia de campanha, junção por agregado (sem chave de linha) e divergência esperada entre plataformas. O modelo de relacionamento só tem dois lados. Gravidade alta.
- **Três padrões se repetem nos três casos:** nenhum campo é escrito para o agente; o documento não chega ao nome técnico que o agente consulta; e nenhum modelo registra o comportamento esperado do dado.
- **O gabarito já é o ponto mais forte.** As categorias responder, esclarecer e abster cobrem os três casos sem mudar o modelo.
- **O universo Aurora não consegue mostrar os casos 1 e 3.** A amostra tem um dia, um canal, duas tabelas e nenhum dado de mídia ou de evento.

### Como as ausências foram verificadas

Leitura dos modelos, exemplos e páginas listados no fim. Para sustentar o que "não existe", foram feitas duas buscas textuais em `src/content/docs`, `public/downloads` e `README.md`:

- `grep -rniE "GA4|GTM|tag plan|tagueamento|zerad|Databricks|BigQuery|Antigravity|Codex|Claude Code"`: Databricks aparece só como link de fundamentação. GA4, GTM, tag plan, tagueamento, BigQuery e os nomes das ferramentas de agente não aparecem nenhuma vez.
- Busca por `sazonal|volume|janela|linha de base|baseline|raro|por operação`: encontrou só `comparison_baseline` no dashboard e janelas de conceito ou indicador. Nada sobre volume de evento.

## Pontos fortes (manter)

- **O modelo de KPI descreve exatamente o problema do caso 2 e ensina a pergunta certa.**
  - [src/content/docs/templates/kpi.mdx:17](../src/content/docs/templates/kpi.mdx#L17) `O acervo tem dashboards, um schema SQL e a frase “taxa de conversão = conversões ÷ visitas”.`
  - [src/content/docs/templates/kpi.mdx:27](../src/content/docs/templates/kpi.mdx#L27) `| “Conversão” é pedido criado, pago, confirmado ou entregue? | Evento que conta no numerador | `
  - [public/downloads/exemplo-kpi-completo.yaml:36](../public/downloads/exemplo-kpi-completo.yaml#L36) `"Conversão de lead: outro indicador, não usar como sinônimo"`
  - [public/downloads/exemplo-kpi-completo.yaml:66](../public/downloads/exemplo-kpi-completo.yaml#L66) `"Se um dashboard mostrar valor diferente, vale o cálculo de aurora-reference-query.sql"`
- **O gabarito cobre responder, esclarecer e abster, e já tem exemplos de abstenção e de esclarecimento.**
  - [src/content/docs/templates/casos-teste.mdx:22](../src/content/docs/templates/casos-teste.mdx#L22) `| Respondível | As fontes cobrem significado, escopo e período | Responder com definição e evidência |`
  - [src/content/docs/templates/casos-teste.mdx:23](../src/content/docs/templates/casos-teste.mdx#L23) `| Ambígua | Falta uma escolha que só quem pergunta pode fazer: canal, período, unidade |`
  - [src/content/docs/templates/casos-teste.mdx:24](../src/content/docs/templates/casos-teste.mdx#L24) `| Fora da cobertura | As fontes não cobrem a pergunta ou a regra não foi aprovada |`
  - [public/downloads/exemplo-casos-teste-completo.yaml:109](../public/downloads/exemplo-casos-teste-completo.yaml#L109) `reason_if_abstain: "Indicador não definido na documentação"`
  - [public/downloads/exemplo-casos-teste-completo.yaml:69](../public/downloads/exemplo-casos-teste-completo.yaml#L69) `reference_answer: "Perguntar se a pessoa quer a taxa de sessões convertidas no canal web, que é a única definida. Não escolher por ela"`
- **O relacionamento registra usos proibidos e regra de data entre tabelas.**
  - [public/downloads/exemplo-relacionamento-completo.yaml:48](../public/downloads/exemplo-relacionamento-completo.yaml#L48) `"Contar sessões usando COUNT(*) após a junção sem tratar multiplicidade"`
  - [public/downloads/exemplo-relacionamento-completo.yaml:43](../public/downloads/exemplo-relacionamento-completo.yaml#L43) `temporal_join_rule: "O pedido conta na data da sessão em que foi criado (session_date)"`
- **O dashboard já tem linha de base de comparação e conflito entre dashboards com causa explicada.**
  - [public/downloads/exemplo-dashboard-completo.yaml:46](../public/downloads/exemplo-dashboard-completo.yaml#L46) `comparison_baseline: "Mesmo dia da semana anterior, somente a partir de 2026-09-15`
  - [public/downloads/exemplo-dashboard-completo.yaml:59](../public/downloads/exemplo-dashboard-completo.yaml#L59) `cause: "Continua com a fórmula da versão 1.0 do KPI-AURORA-001`
- **A orientação sobre regra que muda por unidade está certa.**
  - [src/content/docs/metodo/limites.mdx:22](../src/content/docs/metodo/limites.mdx#L22) `A mesma palavra vale de um jeito numa unidade e de outro em outra. Um documento único esconde a diferença.`
  - [src/content/docs/metodo/limites.mdx:24](../src/content/docs/metodo/limites.mdx#L24) `escreva um documento por contexto, cada um dizendo onde vale e onde não vale`
- **O portal é honesto sobre o limite da camada documental.**
  - [src/content/docs/dados/visao-geral.mdx:35](../src/content/docs/dados/visao-geral.mdx#L35) `Serve de contexto para busca, RAG e agentes, mas não obriga o modelo a seguir cada regra.`

## Índice de achados

| ID | Severidade | Título |
|---|---|---|
| USO-01 | Alta | Nenhum modelo registra o comportamento esperado de um evento de coleta |
| USO-02 | Alta | Cruzar mídia, GA4 e pedidos não tem atribuição, fuso por fonte, taxonomia de campanha nem junção por agregado |
| USO-03 | Média | Nenhum campo diz ao agente o que fazer quando a definição falta ou não está aprovada |
| USO-04 | Média | O documento não chega ao nome técnico que o agente consulta |
| USO-05 | Média | Falta faixa plausível e divergência esperada para servir de teste de sanidade |
| USO-06 | Média | O universo Aurora não consegue mostrar os casos 1 e 3 |

## Achados

### USO-01 · Nenhum modelo registra o comportamento esperado de um evento de coleta

**Severidade:** Alta

**Confiança:** Alta (leitura dos modelos e busca textual descrita no Resumo)

**O que acontece:** No caso 1, o Antigravity leu o tag plan no Google Sheets e consultou o Databricks pelo dia. O parse e o SQL estavam certos. O erro veio depois: tratou "zero hoje" como "evento quebrado". Não sabia que (a) o evento é raro e tem dias sem disparo como algo normal, (b) o evento existe numa operação e não em outra, então zero onde ele não está implementado é o esperado, e (c) numa tabela agregada um dia sem disparo costuma não ter linha, e um `LEFT JOIN` a partir do tag plan devolve nulo, que o agente leu como zero.

O conhecimento que faltava: volume típico do evento por operação e quantas vezes o zero aparece no histórico; onde o evento está implementado e onde não deve disparar; a janela de observação e o critério para concluir "parou" (por exemplo, N dias seguidos em zero); quando o dia D fica completo (atraso da coleta e da carga); e o que significa a falta de linha na tabela diária.

O Contexto tem peças que chegam perto, mas cada uma está no lugar errado ou fala de outra coisa:

| Conhecimento | Modelo e campo atual | Avaliação |
|---|---|---|
| Frequência de atualização | Dataset, `time_semantics.update_frequency` | Fala da carga da tabela, não da frequência do evento |
| Atraso | Dataset, `known_latency` | Serviria para "D completo em D+2", mas o exemplo preenchido diz que não se aplica |
| Evento ou fotografia | Dataset, `snapshot_or_events` | Não pergunta se o dia sem evento tem linha |
| Ressalvas livres | Dataset, `usage.known_caveats` | Daria para escrever a regra em texto livre, mas nada orienta a fazer isso |
| Linha de base | Dashboard, `time_semantics.comparison_baseline` | A peça mais próxima, mas fica no dashboard, não no evento nem no dataset |
| Onde vale e onde não vale | Conceito, `applies_when` e `does_not_apply_when` | Serve para "só vale na operação BR", mas o conceito é pensado para termos de negócio |
| Regra "zero é quebra?" | Decisão, `decision_question`, `decision_table`, `unknown_input_behavior` | Dá para registrar hoje, mas nenhum exemplo ou página sugere esse uso; os exemplos de decisão são de marketing e brief |
| Pergunta ambígua por recorte | Gabarito, categoria Ambígua | Cobre "pedir esclarecimento", não "separar por operação antes de concluir" |
| Descobrir diferenças por unidade | Roteiro de descoberta | Não pergunta sobre volume esperado nem sobre o significado de zero |

**Evidências:**

- [public/downloads/template-dataset.yaml:46](../public/downloads/template-dataset.yaml#L46) `update_frequency: null`
- [public/downloads/template-dataset.yaml:47](../public/downloads/template-dataset.yaml#L47) `known_latency: null`
- [public/downloads/exemplo-dataset-completo.yaml:88](../public/downloads/exemplo-dataset-completo.yaml#L88) `known_latency: "Não aplicável ao laboratório"`
- [public/downloads/template-dataset.yaml:48](../public/downloads/template-dataset.yaml#L48) `snapshot_or_events: null`
- [public/downloads/template-dataset.yaml:54](../public/downloads/template-dataset.yaml#L54) `known_caveats: []`
- [public/downloads/template-dashboard.yaml:32](../public/downloads/template-dashboard.yaml#L32) `comparison_baseline: null`
- [public/downloads/template-conceito.yaml:26](../public/downloads/template-conceito.yaml#L26) `applies_when: null`
- [public/downloads/template-conceito.yaml:27](../public/downloads/template-conceito.yaml#L27) `does_not_apply_when: null`
- [public/downloads/template-decisao.yaml:22](../public/downloads/template-decisao.yaml#L22) `decision_question: null`
- [public/downloads/template-decisao.yaml:29](../public/downloads/template-decisao.yaml#L29) `decision_table: []`
- [public/downloads/template-decisao.yaml:32](../public/downloads/template-decisao.yaml#L32) `unknown_input_behavior: null`
- [src/content/docs/templates/casos-teste.mdx:23](../src/content/docs/templates/casos-teste.mdx#L23) `Falta uma escolha que só quem pergunta pode fazer: canal, período, unidade`
- [src/content/docs/metodo/elicitar.mdx:15](../src/content/docs/metodo/elicitar.mdx#L15) `Identifique diferenças por área, canal e período.`

**Impacto:** O caso que originou o pedido do mantenedor não tem onde ser documentado de forma guiada. Quem segue o portal chega a um tag plan sem regra de silêncio, e o agente continua lendo "sem linha" como "quebrado".

**Recomendação:**

1. Criar um tipo "Evento de coleta" (uma linha do plano de mensuração ou tag plan). O seletor tem 10 tipos e nenhum de evento.
2. Dar a ele um bloco de comportamento esperado: volume típico por operação, proporção de dias em zero, janela de observação, critério de suspeita e de quebra, e quando o dia fica completo.
3. Registrar a presença por operação: onde está implementado, onde não deve disparar e desde quando.
4. Registrar a política de dia sem linha: se a falta de linha significa zero ou falta de coleta.
5. Acrescentar ao roteiro de descoberta perguntas sobre volume esperado e sobre o que significa zero.
6. Até o novo tipo existir, mostrar no portal que a regra cabe hoje no modelo de decisão (esboço A1 no Apêndice).

### USO-02 · Cruzar mídia, GA4 e pedidos não tem atribuição, fuso por fonte, taxonomia de campanha nem junção por agregado

**Severidade:** Alta

**Confiança:** Média (o caso é plausível, não relatado; as ausências foram confirmadas por leitura e pela busca textual)

**O que acontece:** No caso 3, uma gestora pergunta ao agente, ligado ao BigQuery e às APIs do Google Ads e do GA4: "Quanto custou cada pedido da campanha BF26 Search Marca em 10/11/2026?". O Google Ads mostra 18.400 cliques, 540 conversões (data do clique, janela de 30 dias, conta em America/Sao_Paulo) e custo de R$ 9.720. O GA4 (export para `aurora-analytics.analytics_312345678.events_*`) mostra 11.900 sessões com `utm_campaign = bf26_search_marca` e 214 eventos `purchase` (último clique, data do evento). O BigQuery `aurora-analytics.vendas.pedidos` tem 236 pedidos ligados às transações do GA4 por `transaction_id`, dos quais 198 CONFIRMED (31 cancelados e 7 de teste).

O agente erra em quatro pontos:

1. Usa as 540 conversões do Google Ads como pedidos: R$ 9.720 ÷ 540 = R$ 18,00. Pela regra do time, o certo é R$ 9.720 ÷ 198 = R$ 49,09.
2. Faz a junção pelo nome da campanha. No Google Ads o nome é "BF26 | Search | Marca", no GA4 é `bf26_search_marca`; metade das linhas não casa e as que sobram são somadas.
3. Trata cliques e sessões como a mesma unidade e chama a diferença de 6.500 de "perda de tracking", sem saber que a divergência é esperada (cliques repetidos, consentimento negado, rejeição antes de a tag carregar).
4. Mistura a data do clique (Google Ads) com a data do pedido (BigQuery, `created_at` em UTC), e pedidos entre 21h e 23h59 caem no dia seguinte.

O Contexto já tem chave, cardinalidade e regra temporal da junção, estratégia por pergunta, conflito entre dashboards, fuso e precedência entre fontes. Mas o modelo de relacionamento tem só dois lados, supõe chave de linha e tem um único fuso por documento. Mídia e pedido só se ligam por agregado (data + campanha), por meio de uma tabela de correspondência, e nada no portal ensina a encadear dois relacionamentos.

**Evidências:**

- [public/downloads/template-relacionamento.yaml:1](../public/downloads/template-relacionamento.yaml#L1) `# Documentação de relações; não gera um JOIN automaticamente.`
- [public/downloads/template-relacionamento.yaml:23](../public/downloads/template-relacionamento.yaml#L23) `left:`
- [public/downloads/template-relacionamento.yaml:26](../public/downloads/template-relacionamento.yaml#L26) `right:`
- [public/downloads/template-relacionamento.yaml:29](../public/downloads/template-relacionamento.yaml#L29) `join_keys: []`
- [public/downloads/template-relacionamento.yaml:30](../public/downloads/template-relacionamento.yaml#L30) `cardinality: null`
- [public/downloads/template-relacionamento.yaml:34](../public/downloads/template-relacionamento.yaml#L34) `temporal_join_rule: null`
- [public/downloads/template-relacionamento.yaml:38](../public/downloads/template-relacionamento.yaml#L38) `join_strategy_by_question: []`
- [public/downloads/template-dashboard.yaml:40](../public/downloads/template-dashboard.yaml#L40) `conflicting_dashboards:`
- [public/downloads/template-dashboard.yaml:44](../public/downloads/template-dashboard.yaml#L44) `precedence: null`
- [public/downloads/template-kpi.yaml:51](../public/downloads/template-kpi.yaml#L51) `timezone: null`
- [public/downloads/template-dataset.yaml:45](../public/downloads/template-dataset.yaml#L45) `timezone: null`
- [public/downloads/template-kpi.yaml:59](../public/downloads/template-kpi.yaml#L59) `source_conflicts_and_precedence: []`
- [src/content/docs/dados/visao-geral.mdx:17](../src/content/docs/dados/visao-geral.mdx#L17) `**Tempo:** qual data define o período, e em que fuso?`
- [src/content/docs/dados/visao-geral.mdx:19](../src/content/docs/dados/visao-geral.mdx#L19) `**Autoridade:** quando duas tabelas mostram valores diferentes, qual é a fonte oficial?`

**Impacto:** Consultas que cruzam várias tabelas e vários dashboards, o cenário que o mantenedor quer atender, ficam sem molde. O agente produz um número concreto e errado (CPA de R$ 18,00 em vez de R$ 49,09) e ainda diagnostica uma falha de tracking que não existe.

**Recomendação:**

1. Permitir relacionamento com mais de dois lados, ou ensinar a encadear dois documentos de relacionamento.
2. Aceitar junção por agregado (data + campanha) por meio de uma tabela de correspondência, além da chave de linha.
3. Criar um bloco de atribuição por fonte: modelo, janela, data base (clique ou conversão), método de contagem.
4. Registrar o fuso de cada fonte, e não um único fuso por documento.
5. Registrar a taxonomia de campanha: como `utm_campaign` corresponde ao nome na plataforma.
6. Registrar a divergência esperada entre fontes (ver USO-05).

Esboço B1 e perguntas do gabarito Q13 e Q14 no Apêndice.

### USO-03 · Nenhum campo diz ao agente o que fazer quando a definição falta ou não está aprovada

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** No caso 2, sem a definição do time no contexto, a IA usou a fórmula de mercado e devolveu um número concreto, com SQL válido, mas falso para aquele time. Exemplo plausível: ROAS calculado como receita atribuída pela plataforma dividida pelo gasto (84.000 ÷ 12.000 = 7,0), quando o time usa receita líquida confirmada no BigQuery dividida pelo gasto com taxa de agência (51.600 ÷ 13.200 = 3,9).

A regra "rascunho não vale" existe, mas está escrita para pessoas, numa página de referência. O aviso do modelo também é para quem preenche, não para quem consome. O mesmo padrão aparece nos três casos: a frase que teria evitado o erro ("compare por operação antes de concluir", "não use a definição de mercado", "não some conversões de plataformas diferentes") só caberia como texto livre em `known_caveats`, sem orientação para isso. Por fim, o portal reconhece que a camada documental não obriga o modelo, mas não ensina a pôr o documento no contexto de Claude Code, Codex ou Antigravity: a busca textual não encontrou nenhum desses nomes.

**Evidências:**

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:109](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L109) `Enquanto o estado do documento for “Rascunho” ou “Pendente de aprovação”, quem lê deve tratar tudo como ainda não confirmado.`
- [public/downloads/template-kpi.yaml:4](../public/downloads/template-kpi.yaml#L4) `# Não preencha informações desconhecidas com suposições. Use null + open_questions.`
- [public/downloads/template-dataset.yaml:54](../public/downloads/template-dataset.yaml#L54) `known_caveats: []`
- [src/content/docs/dados/visao-geral.mdx:35](../src/content/docs/dados/visao-geral.mdx#L35) `Serve de contexto para busca, RAG e agentes, mas não obriga o modelo a seguir cada regra.`
- [public/downloads/exemplo-casos-teste-completo.yaml:101](../public/downloads/exemplo-casos-teste-completo.yaml#L101) `question: "Qual foi a receita líquida em 2026-10-01?"`
- [public/downloads/exemplo-casos-teste-completo.yaml:109](../public/downloads/exemplo-casos-teste-completo.yaml#L109) `reason_if_abstain: "Indicador não definido na documentação"`

**Impacto:** Mesmo com um modelo de KPI forte, quando o documento falta ou está em rascunho o agente volta para a definição do treinamento. O gabarito testa a abstenção, mas o documento não dá ao agente a instrução que produziria essa abstenção.

**Recomendação:**

1. Criar um bloco comum `ai_instructions` em todos os modelos, separado em geração de consulta e tratamento da pergunta.
2. Incluir uma instrução padrão para definição ausente ou não aprovada ("não calcular com a definição de mercado; responder que a definição não está aprovada e citar `open_questions`").
3. Ensinar a entregar o documento ao agente (arquivo de instruções do projeto, contexto do harness), ligado a NAV-02.

Esboço A3 (bloco `ai_instructions`) e pergunta do gabarito Q12 no Apêndice.

### USO-04 · O documento não chega ao nome técnico que o agente consulta

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** `authoritative_dataset` aponta para um ID do Contexto, e no dataset a plataforma é texto livre. IDs como `DATASET-AURORA-SESSIONS` não levam a `catalog.schema.tabela` nem a um evento do GA4. Um agente ligado ao BigQuery que lê `vw_roas_diario` não tem como chegar ao indicador, e um agente ligado ao Databricks que lê a tabela de eventos não tem como chegar à regra de silêncio do caso 1.

**Evidências:**

- [public/downloads/exemplo-kpi-completo.yaml:62](../public/downloads/exemplo-kpi-completo.yaml#L62) `authoritative_dataset: "DATASET-AURORA-SESSIONS"`
- [public/downloads/template-dataset.yaml:24](../public/downloads/template-dataset.yaml#L24) `platform: null`
- [public/downloads/exemplo-dataset-completo.yaml:35](../public/downloads/exemplo-dataset-completo.yaml#L35) `platform: SQLite (laboratório)`

**Impacto:** O caminho do agente é o inverso do caminho da pessoa: ele parte da tabela ou do evento e precisa achar a definição. Sem essa ligação, a documentação existe mas não é encontrada no momento da consulta.

**Recomendação:** Criar um bloco `platform_bindings` (plataforma + objeto físico) em KPI, dataset e no futuro tipo Evento de coleta. Ver esboços A2, A3 e B1 no Apêndice.

### USO-05 · Falta faixa plausível e divergência esperada para servir de teste de sanidade

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Volume típico, raridade, divergência normal entre fontes e faixa plausível de um indicador não têm campo em nenhum modelo. Só existe `comparison_baseline`, e no dashboard. Os blocos `calculation` e `time` do modelo de KPI (linhas 39 a 53) não têm onde dizer que um ROAS de 7,0 é implausível quando o histórico fica entre 3 e 5, nem que sessões do GA4 costumam ficar entre 60% e 70% dos cliques.

**Evidências:**

- [public/downloads/template-kpi.yaml:39](../public/downloads/template-kpi.yaml#L39) `calculation:`
- [public/downloads/template-kpi.yaml:53](../public/downloads/template-kpi.yaml#L53) `data_freshness: null`
- [public/downloads/template-dashboard.yaml:32](../public/downloads/template-dashboard.yaml#L32) `comparison_baseline: null`
- [public/downloads/exemplo-dashboard-completo.yaml:46](../public/downloads/exemplo-dashboard-completo.yaml#L46) `comparison_baseline: "Mesmo dia da semana anterior, somente a partir de 2026-09-15`

**Impacto:** O agente não tem como distinguir o normal do erro. Nos casos 1 e 3, o normal (zero num dia de um evento raro, sessões abaixo dos cliques) foi tratado como falha; no caso 2, um valor fora da faixa foi reportado sem alerta.

**Recomendação:** Criar `expected_range` no KPI (faixa típica, direção, ação fora da faixa), `expected_behavior` no Evento de coleta e `expected_divergence` no relacionamento. Ver esboços A2, A3 e B1 no Apêndice.

### USO-06 · O universo Aurora não consegue mostrar os casos 1 e 3

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** A amostra tem um único dia, um canal, duas tabelas (sessões e pedidos) e nenhum dado de mídia ou de evento. O próprio dashboard de exemplo declara que não tem receita líquida. Sem histórico não há como mostrar raridade; sem mídia não há como mostrar atribuição. O caso 2 está bem coberto pelo KPI de conversão e pela Q06.

**Evidências:**

- [public/downloads/aurora-fixture.sql:3](../public/downloads/aurora-fixture.sql#L3) `-- O indicador usa só 01/10, canal web, sem sessões internas`
- [public/downloads/aurora-fixture.sql:20](../public/downloads/aurora-fixture.sql#L20) `('S1', 'web', 0, '2026-10-01'),`
- [public/downloads/aurora-fixture.sql:25](../public/downloads/aurora-fixture.sql#L25) `('S6', 'web', 0, '2026-10-01');`
- [public/downloads/aurora-fixture.sql:6](../public/downloads/aurora-fixture.sql#L6) `CREATE TABLE demo_sessions (`
- [public/downloads/aurora-fixture.sql:13](../public/downloads/aurora-fixture.sql#L13) `CREATE TABLE demo_orders (`
- [public/downloads/exemplo-dashboard-completo.yaml:55](../public/downloads/exemplo-dashboard-completo.yaml#L55) `"Não contém receita líquida nem indicadores de app"`

**Impacto:** O público do mantenedor (GTM, GA4, plataformas de mídia, BigQuery, Databricks) não encontra um exemplo que se pareça com o seu dia a dia. A busca textual não achou GA4, GTM, tag plan nem BigQuery em nenhuma página ou download.

**Recomendação:** Ampliar a Aurora com um tag plan, uma tabela diária de eventos com várias semanas e duas operações (Loja BR e Loja PT), e um dataset de mídia. Os números dos esboços A1, A2 e B1 já fecham entre si e podem servir de base.

## Apêndice: os casos em detalhe e os esboços

Os esboços abaixo são propostas. Campos marcados `# proposto` não existem hoje. Os números de cada esboço foram conferidos entre si.

### Caso 1. Evento raro marcado como quebrado

**Pergunta fraca:** "Quais eventos do tag plan estão zerados hoje?"

**Pergunta boa:** "Quais eventos do tag plan, nas operações em que estão implementados, ficaram sem disparo por mais tempo do que o normal para eles, considerando só dias já completos?"

Para responder à pergunta boa, a documentação precisa dizer, para cada evento: (1) em quais operações ele deve disparar; (2) com que frequência dispara em cada uma, nos últimos 28 dias; (3) a partir de quantos dias seguidos em zero vale desconfiar; (4) a partir de quando o dia está completo; (5) se a falta de linha na tabela é zero ou falha de coleta.

**Conta de apoio:** com média de 1,1 disparo por dia, a chance de um dia em zero é e^-1,1, cerca de 33%, ou 9 de 28 dias. Três dias seguidos em zero têm cerca de 3,7% de chance; cinco dias seguidos, cerca de 0,4%.

**Esboço A1. Versão possível hoje, só com campos do modelo de decisão:**

```yaml
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: DEC-AURORA-TRACK-001
revision_id: "DEC-AURORA-TRACK-001@1.0"
title: "Quando declarar que um evento do tag plan parou de ser coletado"
type: decision_rule
status: approved
version: "1.0"
version_date: "2026-11-03"
owner: "Analytics de E-commerce (Aurora)"
approver: "Gerência de Analytics (Aurora)"
valid_from: "2026-11-03"
decision_question: "Um evento com zero disparos num dia está quebrado?"
scope:
  applies_when: "Eventos do tag plan TAGPLAN-AURORA, nas operações em que estão implementados"
  not_applicable_when: "Operação em que o evento não está implementado; dia ainda incompleto (antes de D+2)"
required_inputs: ["dias seguidos em zero na operação", "taxa histórica de dias em zero (28 dias)", "evento implementado na operação?", "dia completo?"]
decision_table:
  - when: "evento não implementado na operação"
    outcome: "Esperado. Não é quebra"
  - when: "dia ainda não completo (antes de D+2)"
    outcome: "Sem conclusão. Esperar"
  - when: "evento raro (zero em mais de 20% dos últimos 28 dias) e menos de 3 dias seguidos em zero"
    outcome: "Normal"
  - when: "evento raro e de 3 a 4 dias seguidos em zero"
    outcome: "Suspeito. Abrir verificação manual no GTM"
  - when: "evento raro e 5 ou mais dias seguidos em zero"
    outcome: "Provável quebra. Acionar Engenharia de Tagueamento"
  - when: "evento frequente (zero em até 20% dos dias) e 1 dia completo em zero"
    outcome: "Provável quebra"
unknown_input_behavior: "Sem histórico de 28 dias, não classificar. Responder que falta linha de base"
tests:
  - case: "resgate_vale_presente, Loja BR, 2026-11-12: zero no dia, dia anterior com 2 disparos"
    inputs: {dias_em_zero: 1, taxa_zero_28d: 0.32, implementado: true, dia_completo: true}
    expected_outcome: "Normal"
    reasoning: "Evento raro: ficou em zero em 9 dos últimos 28 dias"
  - case: "resgate_vale_presente, Loja PT, 2026-11-12: zero"
    inputs: {implementado: false}
    expected_outcome: "Esperado. Não é quebra"
    reasoning: "Vale-presente não existe na operação PT"
```

**Esboço A2. Versão proposta, com o novo tipo "Evento de coleta":**

```yaml
id: EVT-AURORA-012
revision_id: "EVT-AURORA-012@1.1"
title: "Evento resgate_vale_presente"
type: tracking_event                          # proposto
status: approved
version: "1.1"
version_date: "2026-11-03"
owner: "Analytics de E-commerce (Aurora)"
approver: "Gerência de Analytics (Aurora)"
business_question: "Quantos clientes usam vale-presente para pagar?"   # proposto
trigger: "Clique em 'Aplicar vale' com retorno de sucesso da API de pagamento"
operations:                                   # proposto
  - operation: "Loja BR (aurora.com.br)"
    implemented_since: "2026-03-10"
    expected: true
  - operation: "Loja PT (aurora.pt)"
    expected: false
    reason: "Vale-presente não é vendido em Portugal"
destinations:
  - platform: "GA4, propriedade Aurora BR"
    object: "event_name = resgate_vale_presente"
  - platform: Databricks
    object: "aurora_prod.tracking.eventos_diarios"
expected_behavior:                            # proposto
  - operation: "Loja BR"
    typical_daily_volume: "média 1,1; mediana 1 (28 dias até 2026-11-02)"
    zero_days_share: "9 de 28 dias (32%)"
    seasonality: "Pico em dezembro e na semana após o Dia das Mães"
    rarity: rare
    silence_tolerance: "Suspeito após 3 dias completos seguidos em zero; provável quebra após 5"
    baseline_window: "28 dias, mesma operação"
data_completeness:                            # proposto
  complete_after: "D+2 às 06h (America/Sao_Paulo)"
  missing_row_means: "Zero disparos. A tabela diária só grava linha quando há pelo menos 1 disparo"
ai_instructions:                              # proposto
  - "Nunca declarar o evento quebrado com base num único dia"
  - "Antes de concluir, separar por operação e comparar com os últimos 28 dias da mesma operação"
  - "Zero na Loja PT é esperado; não listar como problema"
open_questions: []
related_documents: ["TAGPLAN-AURORA", "DATASET-AURORA-EVENTOS-DIARIOS", "DEC-AURORA-TRACK-001"]
```

**Pergunta do gabarito correspondente (cabe no modelo atual):**

```yaml
- id: Q11
  question: "Quais eventos do tag plan pararam de ser coletados em 2026-11-12?"
  expected_behavior: answer
  reference_answer: "Nenhum com evidência de quebra. resgate_vale_presente está em zero na Loja BR há 1 dia, o que é normal para um evento raro (zero em 32% dos dias). Na Loja PT ele não está implementado"
  required_sources: ["EVT-AURORA-012", "DEC-AURORA-TRACK-001", "DATASET-AURORA-EVENTOS-DIARIOS"]
```

### Caso 2. Indicador calculado com a definição genérica

**Conhecimento que faltava:** a definição do time (qual receita, quais exclusões, qual custo); a fonte com autoridade quando a plataforma e o warehouse divergem; uma instrução de comportamento (sem definição aprovada, não calcular com a definição de mercado); e a ligação entre o nome técnico (tabela ou view) e o documento.

**Pergunta fraca:** "Qual foi o ROAS de outubro?"

**Pergunta boa:** "Qual foi o ROAS de mídia paga da Loja BR em outubro de 2026 pela definição aprovada pela Gerência de Marketing, com receita líquida confirmada no BigQuery?"

Antes de documentar, a pessoa precisa responder: qual receita entra (bruta ou líquida, com ou sem frete, com ou sem cancelados); qual custo entra (só mídia, ou mídia mais taxas); qual fonte manda (plataforma ou warehouse); e o que a IA deve fazer se a definição não existir.

**Esboço A3. Campos atuais do modelo de KPI, mais três blocos propostos:**

```yaml
id: KPI-AURORA-014
revision_id: "KPI-AURORA-014@1.0"
title: "ROAS de mídia paga: Loja BR"
type: metric_definition
status: approved
version: "1.0"
version_date: "2026-10-06"
owner: "Performance de Mídia (Aurora)"
approver: "Gerência de Marketing (Aurora)"
valid_from: "2026-10-06"
business_definition:
  concept: "Receita líquida confirmada gerada por mídia paga para cada real investido, já com a taxa da agência"
  purpose: "Decidir realocação semanal de verba entre Google Ads e Meta Ads"
  synonyms: ["retorno sobre mídia"]
  different_meanings_in_other_domains:
    - "ROAS da plataforma (Google Ads, Meta Ads): receita atribuída pela própria plataforma, bruta, na data do clique. Não usar como este indicador"
calculation:
  numerator: "Receita líquida de pedidos CONFIRMED com origem em mídia paga: sem frete, sem impostos, sem cancelados nem trocas"
  denominator: "Gasto de mídia de Google Ads e Meta Ads mais taxa da agência (10%)"
  unit: "razão (R$ de receita por R$ investido)"
  aggregation_rule: "Somar numeradores e denominadores do período e só depois dividir"
data_sources:
  authoritative_dataset: "DATASET-AURORA-PEDIDOS-BQ"
  source_conflicts_and_precedence:
    - "Se a plataforma mostrar outro ROAS, vale o calculado sobre aurora-analytics.vendas.pedidos"
validation:
  approved_examples:
    - "Outubro de 2026: 51.600 ÷ (12.000 + 1.200) = 3,9. O Google Ads mostrava 7,0 (84.000 ÷ 12.000), com receita bruta atribuída"
platform_bindings:                       # proposto
  - platform: BigQuery
    object: "aurora-analytics.marketing.vw_roas_diario"
expected_range:                          # proposto
  typical: "3,0 a 5,0 por mês desde jan/2026"
  direction: "maior é melhor"
  out_of_range_action: "Abaixo de 2,0 ou acima de 6,0: conferir a fonte da receita antes de reportar"
ai_instructions:                         # proposto
  - "Ao calcular ROAS para a Aurora, usar só esta definição. Não usar a definição de mercado nem a da plataforma"
  - "Se este documento não estiver approved e vigente na data pedida, não calcular: responder que a definição não está aprovada e citar open_questions"
```

**Pergunta do gabarito de abstenção (cabe no modelo atual, no formato de Q06):**

```yaml
- id: Q12
  question: "Qual o CAC da Loja BR em outubro?"
  expected_behavior: abstain
  reason_if_abstain: "CAC não tem definição aprovada. Não usar a fórmula de mercado. Encaminhar a Performance de Mídia"
```

### Caso 3 (plausível). Cruzar GA4, plataforma de mídia e pedidos no BigQuery

**Conhecimento que faltava:** atribuição e data base de cada fonte; fuso de cada fonte; tabela de correspondência de campanhas (não existe chave de linha entre mídia e pedido, a junção é por agregado: data + campanha); qual fonte manda para "pedido"; e a divergência esperada entre cliques, sessões e conversões.

**Pergunta fraca:** "Quanto custou cada pedido da Black Friday?"

**Pergunta boa:** "Qual foi o custo por pedido confirmado da campanha BF26 Search Marca em 10/11/2026, com o custo do Google Ads e os pedidos confirmados do BigQuery atribuídos pelo GA4 (último clique), tudo no horário de Brasília?"

Perguntas que a documentação precisa responder antes: o que conta como "pedido" (conversão da plataforma, `purchase` do GA4 ou pedido confirmado do BigQuery); qual atribuição vale; qual data define o dia; como os nomes de campanha correspondem entre as fontes; e qual diferença entre fontes é normal.

**Esboço B1. Relacionamento com blocos propostos:**

```yaml
id: REL-AURORA-MIDIA-PEDIDOS
revision_id: "REL-AURORA-MIDIA-PEDIDOS@1.0"
title: "Custo de mídia x sessões GA4 x pedidos confirmados"
type: relationship_semantics
status: approved
version: "1.0"
version_date: "2026-11-04"
owner: "Engenharia de Dados (Aurora)"
approver: "Performance de Mídia (Aurora)"
valid_from: "2026-11-04"
business_intent: "Calcular custo por pedido confirmado por campanha e dia"
left:
  dataset: "google_ads.campaign_stats_diario"     # DATASET-AURORA-GADS
  grain: "Uma linha por campanha e dia da conta (America/Sao_Paulo)"
right:
  dataset: "vendas.pedidos via GA4 transaction_id" # DATASET-AURORA-PEDIDOS-BQ
  grain: "Uma linha por pedido; created_at em UTC"
join_keys:
  - left: "campaign_id + data (America/Sao_Paulo)"
    right: "campanha_map.campaign_id + DATE(created_at, 'America/Sao_Paulo')"
cardinality: one_to_many
coverage:
  unmatched_rows_expected: true
  temporal_join_rule: "Converter created_at de UTC para America/Sao_Paulo antes de agrupar por dia"
usage_rules:
  disallowed_question_classes:
    - "Usar conversões do Google Ads como quantidade de pedidos"
    - "Juntar por nome de campanha; usar campaign_id via campanha_map"
  join_strategy_by_question:
    - "Custo por pedido: custo do Google Ads ÷ pedidos CONFIRMED atribuídos pelo GA4 (último clique) no mesmo dia e campanha"
validation:
  test_cases:
    - "BF26 Search Marca em 2026-11-10: R$ 9.720 ÷ 198 pedidos confirmados = R$ 49,09. Com as 540 conversões do Google Ads daria R$ 18,00, que não é o indicador"
campaign_mapping:                      # proposto
  table: "aurora-analytics.marketing.campanha_map"
  rule: "utm_campaign em minúsculas, com '_' no lugar de ' | '; exemplo: 'BF26 | Search | Marca' -> bf26_search_marca"
source_attribution:                    # proposto
  - source: "Google Ads"
    counts: "conversões, todas as ações, janela de 30 dias após o clique"
    date_basis: "data do clique"
    timezone: "America/Sao_Paulo"
  - source: "GA4"
    counts: "purchase, último clique não direto"
    date_basis: "data do evento"
    timezone: "America/Sao_Paulo (fuso da propriedade)"
  - source: "BigQuery vendas.pedidos"
    counts: "pedidos; só CONFIRMED entra no indicador"
    date_basis: "created_at"
    timezone: "UTC"
expected_divergence:                   # proposto
  - "Sessões GA4 ficam entre 60% e 70% dos cliques do Google Ads (consentimento, cliques repetidos). Fora dessa faixa, verificar a tag"
  - "Conversões do Google Ads ficam acima dos pedidos confirmados: janela de 30 dias, conversões modeladas e cancelamentos"
ai_instructions:                       # proposto
  - "Ao comparar mídia e pedidos, declarar qual fonte deu cada número e não somar conversões de plataformas diferentes"
```

**Perguntas do gabarito correspondentes (cabem no modelo atual):**

```yaml
- id: Q13
  question: "Por que o Google Ads mostra 540 conversões e o BigQuery só 198 pedidos confirmados para a BF26 Search Marca em 10/11/2026?"
  expected_behavior: answer
  reference_answer: "Medem coisas diferentes: o Google Ads conta conversões na data do clique, com janela de 30 dias e modelagem; o BigQuery conta pedidos confirmados, sem cancelados nem testes, atribuídos pelo GA4. A diferença é esperada e não indica falha de tracking"
  required_sources: ["REL-AURORA-MIDIA-PEDIDOS", "KPI-AURORA-014"]
- id: Q14
  question: "Qual foi a conversão da Black Friday?"
  expected_behavior: clarify
  ambiguity: "Não diz a campanha, a fonte (plataforma, GA4 ou pedidos) nem a unidade (cliques, sessões ou pedidos)"
```

### Padrões que aparecem nos três casos

1. **O agente não tem onde ler instruções** (USO-03). Um bloco comum `ai_instructions` resolveria os três casos.
2. **O documento não chega ao nome técnico** (USO-04). Falta `platform_bindings`.
3. **Falta o comportamento esperado do dado** (USO-05).
4. **O gabarito já é o ponto mais forte.** As três categorias cobrem os três casos sem mudar o modelo. Falta usá-lo como porta de entrada: começar pela pergunta de negócio e só depois escolher os modelos (ver MET-01 e NAV-03).
5. **A Aurora não cobre os casos 1 e 3** (USO-06).

### Ligação com outros achados da auditoria

- Caso 1: MOD-01, MOD-02, MOD-08, MET-07, NAV-01, AUR-01, AUR-12.
- Caso 2: EDI-01, NAV-02, MOD-17, e as práticas de pesquisa `agent_instruction_if_missing` e vínculo com plataformas.
- Caso 3: MOD-18, MOD-19, EDI-31, e as práticas de pesquisa de atribuição, `named_filters` e relacionamento com vocabulário fixo.

### Arquivos consultados

- `public/downloads/template-kpi.yaml`, `template-dataset.yaml`, `template-dashboard.yaml`, `template-relacionamento.yaml`, `template-decisao.yaml`, `template-conceito.yaml`
- `public/downloads/exemplo-kpi-completo.yaml`, `exemplo-dashboard-completo.yaml`, `exemplo-dataset-completo.yaml`, `exemplo-relacionamento-completo.yaml`, `exemplo-casos-teste-completo.yaml`
- `public/downloads/aurora-fixture.sql`
- `src/content/docs/templates/kpi.mdx`, `src/content/docs/templates/casos-teste.mdx`
- `src/content/docs/dados/visao-geral.mdx`
- `src/content/docs/metodo/limites.mdx`, `src/content/docs/metodo/elicitar.mdx`
- `src/content/docs/fundamentos/como-ler-os-campos.mdx`

## Não coberto nesta rodada

- O caso 3 é plausível, não relatado: os números (cliques, sessões, conversões, pedidos) foram montados para fechar entre si, não vêm de uma operação real.
- As faixas dos esboços (taxa de zero acima de 20% como "raro", sessões entre 60% e 70% dos cliques, ROAS típico entre 3,0 e 5,0) são ilustrativas e precisam ser decididas pelo time de cada organização.
- Não foi testado nenhum agente de verdade (Claude Code, Codex, Antigravity) contra os esboços; a execução estava bloqueada nesta sessão.
- Não foi verificado como o portal publicado exibe os modelos e exemplos citados.
- Não foram pesquisadas fontes externas sobre semântica de eventos, atribuição ou camadas semânticas para este documento; a fundamentação está nos outros arquivos da auditoria.
- Os outros tipos do seletor (além de KPI, dataset, dashboard, relacionamento, decisão, conceito e gabarito) não foram testados contra os casos.
