---
# Exemplo do Contexto, versão com lacunas: nada aqui foi aprovado. A Aurora é uma organização inventada.
id: KPI-AURORA-001
schema_version: "1.0.0"
type: kpi
title: "Taxa de sessões convertidas: loja web Aurora"
version: "0.1"
revision_id: "KPI-AURORA-001@0.1" # versão específica; id = assunto estável
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
intent:
  question: "Que parte das visitas à loja web da Aurora termina em compra?"
  audience: ["Gerência de E-commerce", "Operação de marketing"]
  purpose: "Acompanhar o resultado do funil web"
  decisions: []
plain_summary: "Rascunho: quer mostrar quantas visitas à loja web viram compra, mas ainda não diz se a conta usa pedidos ou sessões."
open_questions:
  - question: "O numerador conta pedidos confirmados ou sessões com pelo menos um pedido confirmado?"
    impact: "Na mesma amostra, uma leitura pode dar o dobro da outra"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Qual campo de data determina o dia da sessão?"
    impact: "Sessões perto da meia-noite podem cair no dia errado"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "O que fazer quando o denominador é zero?"
    impact: "Um dia sem sessões pode virar erro ou 0% sem aviso"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Quem aprova a fonte oficial e a vigência?"
    impact: "Sem quem aprova, a definição não pode ser usada como oficial"
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

domain: ecommerce
business_definition:
  concept: "Taxa de conversão do canal web: conversões ÷ visitas"
  different_meanings_in_other_domains: ["Conversão de lead: outro indicador, não usar como sinônimo"]
synonyms: ["conversão web"]
scope:
  included_channels: [web]
  excluded_channels: [app, "loja física"]
  applicable_population: "Sessões elegíveis no canal web"
  exclusions: ["tráfego interno", "pedidos de teste", "pedidos cancelados"]
calculation:
  formula_description: "(Conversões / Sessões elegíveis) × 100; o que conta como conversão está em aberto"
  numerator: null
  denominator: "Quantidade de sessões elegíveis"
  unit: percentual
  granularity: "dia + canal web"
  aggregation_rule: "Recalcular numerador e denominador antes de agregar períodos"
  null_handling: "Não tratar ausência de registros como valor zero sem confirmar"
  zero_denominator_policy: null
time:
  reference_date_field: null
  timezone: null
  reporting_window: "Janela mensal ainda não aprovada"
  data_freshness: null
data_sources:
  authoritative_dataset: null
  relevant_columns: []
  valid_join_paths: []
  source_conflicts_and_precedence: []
validation:
  approved_examples: []
  expected_questions_and_answers: []
  known_edge_cases: ["Pedidos confirmados após fechamento do mês"]
  tests: []

related_documents: [DATASET-AURORA-SESSIONS, REL-AURORA-SESSIONS-ORDERS, DASH-AURORA-WEB]
---

Este é o indicador de conversão da loja web no primeiro rascunho, de 20/07/2026. A pergunta de negócio já está escrita, mas o numerador ficou em branco de propósito: ninguém tinha decidido se uma sessão com dois pedidos conta uma ou duas vezes. A dúvida foi para `open_questions`, com o impacto de cada leitura.

O que observar: um campo em branco com a pergunta registrada é mais útil do que uma fórmula escolhida por palpite. Quem lê sabe o que ainda não pode afirmar, e quem aprova sabe o que precisa decidir.
