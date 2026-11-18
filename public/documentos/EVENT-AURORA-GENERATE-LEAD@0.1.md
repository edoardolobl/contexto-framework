---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: EVENT-AURORA-GENERATE-LEAD
schema_version: "1.1.0"
type: evento-coleta
title: "Evento generate_lead: Aurora"
version: "0.1"
revision_id: "EVENT-AURORA-GENERATE-LEAD@0.1" # versão específica; id = assunto estável
status: draft
owner: "Analytics de E-commerce (Aurora)"
approver: null
valid_from: null
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-10-06"
last_reviewed: null
review_interval: "P6M"
source_of_truth: null
supersedes_revision: null
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/EVENT-AURORA-GENERATE-LEAD@0.1.md"
intent:
  question: "Quando um dia sem generate_lead deve ser tratado como falha de coleta?"
  audience: ["Analytics de E-commerce", "Vendas de Atacado"]
  purpose: "Evitar que um dia em zero seja lido como evento quebrado sem comparar com o normal da operação"
  decisions: ["Abrir ou não uma investigação de coleta para generate_lead"]
plain_summary: "Rascunho: o evento registra o envio do formulário de atacado no site do Brasil. Ainda não se sabe quanto silêncio é normal nem se o evento existe no México."
open_questions:
  - question: "Zero no México é falha ou o evento não existe lá?"
    impact: "Sem a resposta, qualquer relatório que junte as duas operações lê a falta de dados do México como zero e acusa quebra"
    owner_to_resolve: "Analytics de E-commerce (Aurora)"
    status: unresolved
    resolution: null
  - question: "A partir de quantos dias completos seguidos em zero vale desconfiar no Brasil?"
    impact: "O formulário recebe poucos envios por dia; sem um limiar escolhido pelo time, cada analista decide na hora e dois dias em zero já viram alarme"
    owner_to_resolve: "Gerência de Analytics (Aurora)"
    status: unresolved
    resolution: null
  - question: "Em que dia um dia fica completo na tabela diária?"
    impact: "Contar o dia de hoje ou de ontem como zero confunde atraso de carga com silêncio do evento"
    owner_to_resolve: "Engenharia de Dados (Aurora)"
    status: unresolved
    resolution: null
version_history:
  - version: "0.1"
    date: "2026-10-06"
    change: "Primeiro rascunho, com gatilho e destino; comportamento esperado ainda em aberto"
    approved_by: null

context:
  instructions: "Zero em um dia não é quebra; compare com a linha de base por operação. Sem indicador aprovado, não calcule com a definição de mercado; pergunte."
  verifiedStatements: []
  constraints: []
authoritativeDefinitions: []

trigger: "Envio com sucesso do formulário de cadastro de atacado no site da Aurora"
parameters:
  - name: lead_source
    meaning: "Página ou campanha de onde a pessoa chegou ao formulário"
    example: "pagina_atacado"
    required: null
destination:
  - platform: "GA4"
    object: "Propriedade Aurora BR"
    timezone: null
    note: null
active_scopes:
  - operation: BR
    country: Brasil
    brand: Aurora
    active: true
    since: null
    reason: null
  - operation: MX
    country: México
    brand: Aurora
    active: null
    since: null
    reason: "Ninguém confirmou se o formulário de atacado existe no site do México"
expected_behavior:
  expected_frequency: "Poucos envios por dia, com dias em zero; ainda sem número"
  baseline_by_scope: []
  seasonality: null
  silence_tolerance: []
  expected_zero_conditions: []
launch_date: null
retirement_date: null
renamed_from: []
consent_requirements: null
late_arrival_window: null
deduplication_key: null
downstream_kpis: []
known_exceptions: []
validation_query: null
missing_days_policy: null
grain_note: null
data_incidents: []
disambiguation: []

related_documents: []
---

# Evento generate_lead: Aurora (EVENT-AURORA-GENERATE-LEAD@0.1)

> **Estado:** Rascunho
>
> **Vigência:** sem vigência definida
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/EVENT-AURORA-GENERATE-LEAD@0.1.md

## Pergunta que este documento responde (EVENT-AURORA-GENERATE-LEAD@0.1, sem vigência definida)

Quando um dia sem generate_lead deve ser tratado como falha de coleta?

## Em poucas palavras (EVENT-AURORA-GENERATE-LEAD@0.1, sem vigência definida)

Rascunho: o evento registra o envio do formulário de atacado no site do Brasil. Ainda não se sabe quanto silêncio é normal nem se o evento existe no México.

## Comentário (EVENT-AURORA-GENERATE-LEAD@0.1, sem vigência definida)

O rascunho já diz o que dispara o evento e onde ele chega no Brasil. O que falta é o comportamento esperado: quanto silêncio é normal, quando um dia fica completo e se o México tem o evento.

O que observar: sem a linha de base por operação, um dia em zero parece falha, e um evento que não existe no México parece quebrado.
