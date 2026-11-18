---
# Versão histórica 1.0, arquivada e não vigente. A Aurora é uma organização inventada pelo Contexto.
id: KPI-AURORA-001
schema_version: "1.0.0"
type: kpi
title: "Taxa de sessões convertidas: loja web Aurora"
version: "1.0"
revision_id: "KPI-AURORA-001@1.0" # versão específica; id = assunto estável
status: superseded
owner: "Analytics de E-commerce (Aurora)"
approver: "Gerência de E-commerce (Aurora)"
valid_from: "2026-08-15"
valid_to: "2026-09-15"       # fim exclusivo da vigência; null = sem fim documentado
recorded_at: "2026-08-14"
version_date: "2026-08-14"
last_reviewed: "2026-08-14"
review_interval: null
source_of_truth: "Catálogo de indicadores da Aurora, versão 1.0 de KPI-AURORA-001"
supersedes_revision: "KPI-AURORA-001@0.1"
superseded_by_revision: "KPI-AURORA-001@2.0"
intent:
  question: null
  audience: []
  purpose: "Acompanhar o resultado do funil web"
  decisions: []
plain_summary: null
open_questions: []
version_history:
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
authoritativeDefinitions: []

domain: ecommerce
business_definition:
  concept: "Relação entre número de pedidos confirmados e sessões elegíveis"
  different_meanings_in_other_domains: ["Conversão de lead: outro indicador"]
synonyms: ["conversão web"]
scope:
  included_channels: [web]
  excluded_channels: [app, "loja física"]
  applicable_population: "Sessões do canal web que não são tráfego interno"
  exclusions: ["tráfego interno", "pedidos de teste", "pedidos cancelados"]
calculation:
  formula_description: "(Pedidos confirmados elegíveis / Sessões elegíveis) × 100"
  numerator: "Quantidade de pedidos CONFIRMED associados a sessões elegíveis; dois pedidos na mesma sessão contam duas vezes"
  denominator: "Quantidade de sessões elegíveis: channel = web e is_internal = 0"
  unit: percentual
  granularity: "dia + canal web"
  aggregation_rule: "Para períodos maiores, somar numeradores e denominadores dos dias e só então dividir. Não tirar média das taxas diárias"
  null_handling: "Sessão sem pedido conta no denominador e não no numerador"
  zero_denominator_policy: "Sem sessões elegíveis, exibir 'sem dados'. Não exibir 0%"
time:
  reference_date_field: aurora-analytics.web.sessoes_web.session_date
  timezone: "Data local da loja, já gravada em session_date"
  reporting_window: "Diária"
  data_freshness: "Carga estática no laboratório"
data_sources:
  authoritative_dataset: DATASET-AURORA-SESSIONS
  relevant_columns:
    - aurora-analytics.web.sessoes_web.session_id
    - aurora-analytics.web.sessoes_web.channel
    - aurora-analytics.web.sessoes_web.is_internal
    - aurora-analytics.web.sessoes_web.session_date
    - aurora-analytics.vendas.pedidos.session_id
    - aurora-analytics.vendas.pedidos.status_code
  valid_join_paths: [REL-AURORA-SESSIONS-ORDERS]
  source_conflicts_and_precedence: []
validation:
  approved_examples: ["Exemplo: 4 sessões elegíveis e 2 pedidos confirmados, resultado de 50% sob a definição histórica"]
  expected_questions_and_answers: []
  known_edge_cases:
    - "Uma sessão com dois pedidos confirmados soma dois pedidos no numerador histórico"
    - "Pedido cancelado não entra na contagem de pedidos confirmados"
    - "Pedido de teste não entra na contagem de pedidos confirmados"
  tests: []

related_documents: [DATASET-AURORA-SESSIONS, DATASET-AURORA-ORDERS, REL-AURORA-SESSIONS-ORDERS]

archival_note:
  date: "2026-11-17"
  text: "Substituída por KPI-AURORA-001@2.0 em 15/09/2026. A consulta aurora-reference-query.sql implementa a 2.0 e não deve ser usada para reconstruir a 1.0. Em 17/11/2026 os nomes de tabela desta cópia foram corrigidos de demo_sessions e demo_orders para os nomes de produção, aurora-analytics.web.sessoes_web e aurora-analytics.vendas.pedidos (ADR 0030). A regra aprovada e os valores não mudaram: só os nomes, que eram de demonstração."
---

# Taxa de sessões convertidas: loja web Aurora (KPI-AURORA-001@1.0)

> **Estado:** Substituído
>
> **Vigência:** de 15/08/2026 até 15/09/2026, sem contar o último dia
>
> **Domínio:** ecommerce
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/KPI-AURORA-001@1.0.md

## Comentário (KPI-AURORA-001@1.0, de 15/08/2026 até 15/09/2026)

Esta é a versão 1.0 do indicador guardada como foi aprovada, com a fórmula que contava pedidos confirmados por sessão elegível. Só o formato e os nomes de tabela mudaram: os valores aprovados são os mesmos, e a `archival_note` explica a troca dos nomes.

O que observar: `status: superseded` diz que outra versão do mesmo assunto tomou o lugar desta, e `recorded_at` guarda o dia do registro. A nota em `archival_note` foi escrita depois, com data própria.
