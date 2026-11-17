---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: REL-AURORA-SESSIONS-ORDERS
schema_version: "1.0.0"
type: relacionamento
title: "Sessões para pedidos: Aurora"
version: "2.0"
revision_id: "REL-AURORA-SESSIONS-ORDERS@2.0" # versão específica; id = assunto estável
status: approved
owner: "Engenharia de Dados (Aurora)"
approver: "Analytics de E-commerce (Aurora)"
valid_from: "2026-09-15"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-09-15"
last_reviewed: "2026-09-15"
review_interval: null
source_of_truth: "Catálogo de dados da Aurora, relacionamento sessões e pedidos"
supersedes_revision: "REL-AURORA-SESSIONS-ORDERS@1.0"
superseded_by_revision: null
intent:
  question: "Como ligar sessões e pedidos da Aurora sem contar a mesma sessão duas vezes?"
  audience: ["Analytics de E-commerce", "Engenharia de Dados"]
  purpose: "Relacionar cada pedido à sessão em que foi criado"
  decisions: []
plain_summary: "Uma sessão pode ter vários pedidos. Para contar sessões convertidas, conte cada sessão uma vez só."
open_questions: []
version_history:
  - version: "2.0"
    date: "2026-09-15"
    change: "Incluída a regra de contar sessão distinta, acompanhando a versão 2.0 do KPI-AURORA-001"
    approved_by: "Analytics de E-commerce (Aurora)"
  - version: "1.0"
    date: "2026-08-20"
    change: "Primeira versão aprovada, com chave e cardinalidade um para muitos"
    approved_by: "Analytics de E-commerce (Aurora)"
  - version: "0.1"
    date: "2026-07-20"
    change: "Primeiro rascunho, com lacunas registradas"
    approved_by: null

context:
  instructions: null
  verifiedStatements: []
  constraints: []
authoritativeDefinitions: []

left:
  dataset: demo_sessions     # DATASET-AURORA-SESSIONS
  grain: "Uma linha por sessão"
right:
  dataset: demo_orders       # DATASET-AURORA-ORDERS
  grain: "Uma linha por pedido"
join_keys:
  - left: session_id
    right: session_id
cardinality: one_to_many
coverage:
  unmatched_rows_expected: true
  null_keys_expected: false
  temporal_join_rule: "O pedido conta na data da sessão em que foi criado (session_date)"
usage_rules:
  approved_question_classes: ["Sessões elegíveis com pelo menos um pedido confirmado"]
  disallowed_question_classes: ["Contar sessões usando COUNT(*) após a junção sem tratar multiplicidade"]
  join_strategy_by_question: ["Para sessões convertidas, contar session_id distinto dos pedidos confirmados elegíveis"]
  duplication_risks: ["Uma sessão com dois pedidos confirmados aparece duas vezes na junção"]
  aggregation_safeguards: ["Deduplicar sessão convertida antes da razão por sessões elegíveis"]
validation:
  test_cases:
    - "Uma sessão com dois pedidos confirmados conta uma vez como sessão convertida"
    - "Uma sessão com somente pedido cancelado não conta como sessão convertida"
  verified_query: aurora-reference-query.sql
  reviewer: "Engenharia de Dados (Aurora)"

related_documents: [DATASET-AURORA-SESSIONS, DATASET-AURORA-ORDERS, KPI-AURORA-001]
---

A versão 2.0 acompanha a versão 2.0 do indicador: para sessões convertidas, a conta usa o identificador distinto da sessão. Sem essa regra, a junção soma a mesma sessão uma vez por pedido.

O que observar: `join_strategy_by_question` liga a escolha da junção à pergunta que ela responde, e `aggregation_safeguards` diz o que fazer antes de dividir.
