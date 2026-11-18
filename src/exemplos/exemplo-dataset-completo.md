---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: DATASET-AURORA-SESSIONS
schema_version: "1.1.0"
type: dataset
title: "Sessões web e app: Aurora"
version: "1.2"
revision_id: "DATASET-AURORA-SESSIONS@1.2" # versão específica; id = assunto estável
status: approved
owner: "Engenharia de Dados (Aurora)"
approver: "Analytics de E-commerce (Aurora)"
valid_from: "2026-10-02"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-10-02"
last_reviewed: "2026-10-02"
review_interval: null
source_of_truth: "Catálogo de dados da Aurora, tabela aurora-analytics.web.sessoes_web"
supersedes_revision: "DATASET-AURORA-SESSIONS@1.1"
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/DATASET-AURORA-SESSIONS@1.2.md"
intent:
  question: "O que significa cada coluna da tabela de sessões da Aurora?"
  audience: ["Analytics de E-commerce", "Engenharia de Dados"]
  purpose: "Representar sessões registradas por canal"
  decisions: ["Decidir quais sessões entram na taxa de conversão web"]
plain_summary: "Uma linha por sessão. Sessões abertas na rede do escritório ficam fora da taxa de conversão; sem esse filtro, a taxa da amostra sobe de 25% para 40%."
open_questions: []
version_history:
  - version: "1.2"
    date: "2026-10-02"
    change: "Registrado o caso-limite de S3, sessão interna com pedido confirmado, e o efeito do filtro na amostra de 01/10. Nenhum resultado mudou"
    approved_by: "Analytics de E-commerce (Aurora)"
  - version: "1.1"
    date: "2026-09-11"
    change: "Documentado que session_date é data local sem hora, depois de dúvida sobre fuso no fechamento diário"
    approved_by: "Analytics de E-commerce (Aurora)"
  - version: "1.0"
    date: "2026-08-20"
    change: "Primeira versão aprovada do dicionário, com as quatro colunas"
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

dataset:
  physicalName: aurora-analytics.web.sessoes_web
  platform: "BigQuery (amostra reproduzida em SQLite)"
  grain: "Uma linha por sessão"
  primary_key: session_id
  alternative_keys: []
  uniqueness_assumption: "Cada session_id representa uma única sessão"
columns:
  - physicalName: session_id
    physicalType: TEXT
    businessName: "Identificador da sessão"
    meaning: "Chave única da sessão"
    unit: null
    allowed_values: []
    sentinel_values: []
    null_meaning: "Não permitido no laboratório"
    examples: [S1, S2]
    do_not_use_for: ["Identificar pessoas"]
  - physicalName: channel
    physicalType: TEXT
    businessName: Canal
    meaning: "Plataforma em que ocorreu a sessão"
    unit: null
    allowed_values: [web, app]
    sentinel_values: []
    null_meaning: "Não permitido no laboratório"
    examples: [web, app]
    do_not_use_for: ["Inferir localização geográfica"]
  - physicalName: is_internal
    physicalType: INTEGER
    businessName: "Sessão interna"
    meaning: "1 = sessão aberta na rede do escritório da Aurora: testes da equipe, demonstrações e compras de funcionários. 0 = qualquer outra sessão"
    unit: null
    allowed_values: [0, 1]
    sentinel_values: []
    null_meaning: "Não permitido no laboratório"
    examples: [0, 1]
    do_not_use_for: ["Identificar a pessoa que navegou"]
  - physicalName: session_date
    physicalType: TEXT
    businessName: "Data da sessão"
    meaning: "Data de referência no formato YYYY-MM-DD"
    unit: dia
    allowed_values: []
    sentinel_values: []
    null_meaning: "Não permitido no laboratório"
    examples: ["2026-09-01"]
    do_not_use_for: ["Inferir hora local ou duração"]
time_semantics:
  reference_field: session_date
  timezone: "Data local da loja, sem hora"
  update_frequency: "Carga estática do laboratório"
  known_latency: "Não aplicável ao laboratório"
  snapshot_or_events: "Registro de sessão; não snapshot de estoque"
usage:
  authoritative_questions: ["Taxa de sessões web convertidas na amostra do laboratório"]
  invalid_aggregations: ["Contar sessões com COUNT(*) após junção 1:N sem avaliar duplicidade"]
  related_datasets: [DATASET-AURORA-ORDERS]
  known_caveats:
    - "Não extrapolar a amostra para outros períodos ou canais"
    - "Caso-limite: S3 é interna e tem o pedido O4 confirmado, uma compra real de funcionário. Mesmo assim fica fora do KPI-AURORA-001, que exclui toda sessão interna. Sem esse filtro, a taxa de 01/10 passa de 25% para 40%"
  sample_queries: [aurora-reference-query.sql]
validation:
  checked_by: "Engenharia de Dados (Aurora)"
  checked_at: "2026-10-02"
  evidence: [aurora-fixture.sql]

related_documents: [KPI-AURORA-001, DATASET-AURORA-ORDERS, REL-AURORA-SESSIONS-ORDERS]
---

A versão 1.2 registrou um caso-limite: uma sessão interna com pedido confirmado, compra real de uma pessoa da equipe. Ela continua fora do indicador, que exclui toda sessão interna, e o dicionário mostra o efeito do filtro com números da amostra.

O que observar: `known_caveats` traz a taxa com e sem o filtro. Quem consulta a tabela vê na hora quanto a escolha muda o resultado.
