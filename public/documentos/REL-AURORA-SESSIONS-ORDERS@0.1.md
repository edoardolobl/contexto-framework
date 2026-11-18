---
# Exemplo do Contexto, versão com lacunas: nada aqui foi aprovado. A Aurora é uma organização inventada.
id: REL-AURORA-SESSIONS-ORDERS
schema_version: "1.1.0"
type: relacionamento
title: "Sessões para pedidos: Aurora"
version: "0.1"
revision_id: "REL-AURORA-SESSIONS-ORDERS@0.1" # versão específica; id = assunto estável
status: draft
owner: null
approver: null
valid_from: null
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-07-20"
last_reviewed: null
review_interval: null
source_of_truth: null
supersedes_revision: null
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/REL-AURORA-SESSIONS-ORDERS@0.1.md"
intent:
  question: "Como ligar sessões e pedidos da Aurora sem contar a mesma sessão duas vezes?"
  audience: ["Analytics de E-commerce", "Engenharia de Dados"]
  purpose: "Relacionar cada pedido à sessão em que foi criado"
  decisions: []
plain_summary: "Rascunho: cada sessão pode ter vários pedidos; ainda falta decidir se a conta usa pedidos ou sessões."
open_questions:
  - question: "Para contar sessões convertidas, conta-se cada pedido confirmado ou cada sessão distinta?"
    impact: "Uma sessão com dois pedidos conta em dobro"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Um pedido sem sessão correspondente pode existir? O que fazer com ele?"
    impact: "Pedidos podem sumir da conta ou entrar sem sessão"
    owner_to_resolve: null
    status: unresolved
    resolution: null
version_history:
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
  dataset: demo_sessions
  grain: "Uma linha por sessão"
right:
  dataset: demo_orders
  grain: "Uma linha por pedido"
join_keys:
  - left: session_id
    right: session_id
cardinality: one_to_many
coverage:
  unmatched_rows_expected: true
  null_keys_expected: false
  temporal_join_rule: null
usage_rules:
  approved_question_classes: ["Sessões elegíveis com pelo menos um pedido confirmado"]
  disallowed_question_classes: ["Contar sessões usando COUNT(*) após a junção sem tratar multiplicidade"]
  join_strategy_by_question: ["Ainda não definida: depende de contar pedido ou sessão (ver perguntas em aberto)"]
  duplication_risks: ["Uma sessão com dois pedidos confirmados aparece duas vezes na junção"]
  aggregation_safeguards: ["A definir junto com a pergunta em aberto sobre contar pedido ou sessão"]
validation:
  test_cases:
    - "Uma sessão com dois pedidos confirmados aparece duas vezes na junção"
    - "Uma sessão com somente pedido cancelado não conta como sessão convertida"
  verified_query: null
  reviewer: null

related_documents: [DATASET-AURORA-SESSIONS, KPI-AURORA-001]
---

# Sessões para pedidos: Aurora (REL-AURORA-SESSIONS-ORDERS@0.1)

> **Estado:** Rascunho
>
> **Vigência:** sem vigência definida
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/REL-AURORA-SESSIONS-ORDERS@0.1.md

## Pergunta que este documento responde (REL-AURORA-SESSIONS-ORDERS@0.1, sem vigência definida)

Como ligar sessões e pedidos da Aurora sem contar a mesma sessão duas vezes?

## Em poucas palavras (REL-AURORA-SESSIONS-ORDERS@0.1, sem vigência definida)

Rascunho: cada sessão pode ter vários pedidos; ainda falta decidir se a conta usa pedidos ou sessões.

## Comentário (REL-AURORA-SESSIONS-ORDERS@0.1, sem vigência definida)

O rascunho já tem a chave e a cardinalidade, um para muitos, e já viu o risco: uma sessão com dois pedidos confirmados aparece duas vezes depois da junção. O que falta é a regra para cada pergunta, porque ela depende de o indicador contar pedido ou sessão.

O que observar: o risco de duplicação vem registrado antes da regra que o resolve. Quem lê sabe onde pisar com cuidado.
