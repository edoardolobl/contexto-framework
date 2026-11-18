---
# Exemplo do Contexto, versão com lacunas: nada aqui foi aprovado. A Aurora é uma organização inventada.
id: DATASET-AURORA-SESSIONS
schema_version: "1.0.0"
type: dataset
title: "Sessões web e app: Aurora"
version: "0.1"
revision_id: "DATASET-AURORA-SESSIONS@0.1" # versão específica; id = assunto estável
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
  question: "O que significa cada coluna da tabela de sessões da Aurora?"
  audience: ["Analytics de E-commerce", "Engenharia de Dados"]
  purpose: "Representar sessões registradas por canal"
  decisions: []
plain_summary: "Rascunho: uma linha por sessão, com canal, data e uma marca de sessão interna; o que conta como interna ainda está em aberto."
open_questions:
  - question: "'is_internal = 1 marca o quê: testes da equipe, a rede do escritório, compras de funcionários?'"
    impact: "Sem o significado, ninguém sabe se o filtro tira só testes ou também compras reais"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Sessões internas entram na taxa de conversão? Uma compra de funcionário feita da rede do escritório conta?"
    impact: "A resposta muda o denominador e o numerador da taxa"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Quem aprova a semântica do dicionário?"
    impact: "Sem quem aprova, o dicionário não pode ser citado como fonte"
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

dataset:
  physical_name: demo_sessions
  platform: "SQLite (laboratório)"
  grain: "Uma linha por sessão"
  primary_key: session_id
  alternative_keys: []
  uniqueness_assumption: "Cada session_id representa uma única sessão"
columns:
  - physical_name: session_id
    technical_type: TEXT
    business_name: "Identificador da sessão"
    meaning: "Chave única da sessão"
    unit: null
    allowed_values: []
    sentinel_values: []
    null_meaning: "Não permitido no laboratório"
    examples: [SES-101, SES-102]
    do_not_use_for: ["Identificar pessoas"]
  - physical_name: channel
    technical_type: TEXT
    business_name: Canal
    meaning: "Plataforma em que ocorreu a sessão"
    unit: null
    allowed_values: [web, app]
    sentinel_values: []
    null_meaning: "Não permitido no laboratório"
    examples: [web, app]
    do_not_use_for: ["Inferir localização geográfica"]
  - physical_name: is_internal
    technical_type: INTEGER
    business_name: "Sessão interna"
    meaning: "1 = sessão interna. O que conta como interna ainda não foi confirmado"
    unit: null
    allowed_values: [0, 1]
    sentinel_values: []
    null_meaning: "Não permitido no laboratório"
    examples: [0, 1]
    do_not_use_for: ["Identificar a pessoa que navegou"]
  - physical_name: session_date
    technical_type: TEXT
    business_name: "Data da sessão"
    meaning: "Data de referência no formato YYYY-MM-DD"
    unit: dia
    allowed_values: []
    sentinel_values: []
    null_meaning: "Não permitido no laboratório"
    examples: ["2026-09-01"]
    do_not_use_for: ["Inferir hora local ou duração"]
time_semantics:
  reference_field: session_date
  timezone: null
  update_frequency: "Carga estática do laboratório"
  known_latency: "Não aplicável ao laboratório"
  snapshot_or_events: "Registro de sessão; não snapshot de estoque"
usage:
  authoritative_questions: ["Taxa de sessões web convertidas na amostra do laboratório"]
  invalid_aggregations: ["Contar sessões com COUNT(*) após junção 1:N sem avaliar duplicidade"]
  related_datasets: [demo_orders]
  known_caveats: ["Não extrapolar a amostra para outros períodos ou canais"]
  sample_queries: []
validation:
  checked_by: null
  checked_at: null
  evidence: []

related_documents: [KPI-AURORA-001, REL-AURORA-SESSIONS-ORDERS]
---

O dicionário já diz o que uma linha representa e quais valores cada coluna aceita. A coluna `is_internal` tem os valores certos, 0 e 1, mas ninguém sabe ainda o que o 1 marca: testes da equipe, a rede do escritório ou compras de funcionários.

O que observar: saber os valores possíveis não basta. Sem o significado, o filtro que tira sessões internas pode tirar também compras reais.
