---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: KPI-AURORA-001
schema_version: "1.0.0"
type: kpi
title: "Taxa de sessões convertidas: loja web Aurora"
version: "2.0"
revision_id: "KPI-AURORA-001@2.0" # versão específica; id = assunto estável
status: approved
owner: "Analytics de E-commerce (Aurora)"
approver: "Gerência de E-commerce (Aurora)"
valid_from: "2026-09-15"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-09-15"
last_reviewed: "2026-09-15"
review_interval: null
source_of_truth: "Catálogo de indicadores da Aurora, entrada KPI-AURORA-001"
supersedes_revision: "KPI-AURORA-001@1.0"
superseded_by_revision: null
intent:
  question: "Que parte das sessões da loja web da Aurora termina em pelo menos um pedido confirmado?"
  audience: ["Gerência de E-commerce", "Operação de marketing", "Analytics de E-commerce"]
  purpose: "Acompanhar o resultado do funil web"
  decisions: ["Investigar quedas de conversão no canal web"]
plain_summary: "Das sessões da loja web que não são da equipe interna, conta quantas tiveram pelo menos um pedido confirmado. Cada sessão conta uma vez, mesmo com dois pedidos."
open_questions: []
version_history:
  - version: "2.0"
    date: "2026-09-15"
    change: "O numerador passa a contar sessões únicas com pedido confirmado. Antes contava pedidos, o que inflava a taxa quando uma sessão tinha mais de um pedido"
    approved_by: "Gerência de E-commerce (Aurora)"
  - version: "1.0"
    date: "2026-08-14"
    change: "Primeira definição aprovada: pedidos confirmados divididos por sessões elegíveis"
    approved_by: "Gerência de E-commerce (Aurora)"
  - version: "0.1"
    date: "2026-07-20"
    change: "Primeiro rascunho, com lacunas registradas"
    approved_by: null

context:
  instructions: null
  verifiedStatements: []
  constraints: []
authoritativeDefinitions:
  - type: sql
    url: aurora-reference-query.sql
    description: "Consulta SQL do laboratório que calcula a versão 2.0"

domain: ecommerce
business_definition:
  concept: "Proporção de sessões elegíveis que resultaram em pelo menos um pedido confirmado"
  different_meanings_in_other_domains:
    - "Conversão de lead: outro indicador, não usar como sinônimo"
    - "Pedidos por sessão: era a definição da versão 1.0; hoje é outra medida, sem documento próprio"
synonyms: ["conversão web"]
scope:
  included_channels: [web]
  excluded_channels: [app, "loja física"]
  applicable_population: "Sessões do canal web que não são tráfego interno"
  exclusions: ["tráfego interno", "pedidos de teste", "pedidos cancelados"]
calculation:
  formula_description: "(Sessões únicas com pelo menos um pedido confirmado / Sessões elegíveis) × 100"
  numerator: "Quantidade de sessões elegíveis com pelo menos um pedido CONFIRMED. Uma sessão com dois pedidos confirmados conta uma vez"
  denominator: "Quantidade de sessões elegíveis: channel = web e is_internal = 0"
  unit: percentual
  granularity: "dia + canal web"
  aggregation_rule: "Para períodos maiores, somar numeradores e denominadores dos dias e só então dividir. Não tirar média das taxas diárias"
  null_handling: "Sessão sem pedido conta no denominador e não no numerador"
  zero_denominator_policy: "Sem sessões elegíveis, exibir 'sem dados'. Não exibir 0%"
history_recalculation:
  policy: method_break
  description: "A série calculada pela 1.0 não é recalculada. Números de antes de 15/09/2026 contam pedidos e não se comparam com os da 2.0."
time:
  reference_date_field: demo_sessions.session_date
  timezone: "Data local da loja, já gravada em session_date"
  reporting_window: "Diária"
  data_freshness: "Carga estática no laboratório"
data_sources:
  authoritative_dataset: DATASET-AURORA-SESSIONS
  relevant_columns:
    - demo_sessions.session_id
    - demo_sessions.channel
    - demo_sessions.is_internal
    - demo_sessions.session_date
    - demo_orders.session_id
    - demo_orders.status_code
  valid_join_paths: [REL-AURORA-SESSIONS-ORDERS]
  source_conflicts_and_precedence: ["Se um dashboard mostrar valor diferente, vale o cálculo de aurora-reference-query.sql"]
validation:
  approved_examples: ["Exemplo: quatro sessões elegíveis, uma convertida, resultado de 25%"]
  expected_questions_and_answers: [] # gabarito de outubro foi criado depois desta versão
  known_edge_cases:
    - "Uma sessão com dois pedidos confirmados conta uma única vez"
    - "Uma sessão com somente pedido cancelado não conta como convertida"
    - "Uma sessão com somente pedido de teste não conta como convertida"
  tests: []                  # demonstração executável de outubro está no laboratório, posterior a esta versão

related_documents: [DATASET-AURORA-SESSIONS, DATASET-AURORA-ORDERS, REL-AURORA-SESSIONS-ORDERS, DASH-AURORA-WEB]
---

A versão 2.0 trocou o numerador: deixou de contar pedidos e passou a contar sessões com pelo menos um pedido confirmado. No exemplo aprovado, com quatro sessões e dois pedidos confirmados na mesma sessão, a leitura antiga dá 50% e a nova dá 25%.

Como a versão maior mudou, `history_recalculation` diz o que acontece com a série antiga: ela não é recalculada e fica marcada como quebra de método. Comparar um número da 1.0 com um da 2.0 é comparar duas medidas diferentes.

O bloco `authoritativeDefinitions` aponta onde mora a regra executável, a consulta SQL do laboratório, sem copiar o código para dentro do documento.
