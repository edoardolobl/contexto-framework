---
# Exemplo do Contexto, versão com lacunas: nada aqui foi aprovado. A Aurora é uma organização inventada.
id: PROCESS-CAMPAIGN-001
schema_version: "1.1.0"
type: processo
title: "Solicitar e publicar campanha: Aurora"
version: "0.1"
revision_id: "PROCESS-CAMPAIGN-001@0.1" # versão específica; id = assunto estável
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
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/PROCESS-CAMPAIGN-001@0.1.md"
intent:
  question: "Que caminho um pedido de campanha percorre até ser publicado?"
  audience: ["Operação de Marketing"]
  purpose: "Descrever as transferências e evidências necessárias até a publicação"
  decisions: []
plain_summary: "Rascunho: duas etapas de conferência estão descritas; faltam quem aprova, os prazos e as exceções."
open_questions:
  - question: "Quem aprova cada tipo de conteúdo?"
    impact: "O pedido pode ir para quem não tem autoridade e voltar"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Qual é o prazo de cada etapa, e o que acontece quando ele vence?"
    impact: "Um pedido pode ficar parado sem que ninguém perceba"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Quem pode autorizar uma exceção de publicação?"
    impact: "Uma campanha com prazo legal pode ser barrada pelo fluxo normal"
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

scope:
  applies_when: "Campanha externa"
  not_applicable_when: "Comunicados internos não promocionais"
trigger: "Solicitação identificada e registrada"
preconditions: []
required_inputs: [brief, canal, objetivo, material]
roles:
  process_owner: null
  performers: ["Operação de marketing"]
  approvers: []
steps:
  - id: S01
    name: "Conferir brief"
    performer_role: "Operação de marketing"
    action: "Registrar lacunas e encaminhamento"
    inputs: [brief]
    output_evidence: "Registro de triagem"
    next_step: "S02 se completo; devolver se incompleto"
    exception_handling: "Complementação solicitada por escrito"
  - id: S02
    name: "Conferir evidências e critérios"
    performer_role: null
    action: "Aplicar decisão DECISION-CAMPAIGN-001"
    inputs: [brief, "evidências"]
    output_evidence: "Resultado da triagem"
    next_step: "Solicitar aprovação formal se elegível"
    exception_handling: "Pausar quando dados indispensáveis faltarem"
decision_rules: [DECISION-CAMPAIGN-001]
completion:
  success_criteria: ["Publicação autorizada, registrada e comprovada"]
  failure_outcomes: [Devolvido, Rejeitado, Cancelado]
  evidence_record: null
exceptions: ["Pedido cancelado depois de aprovado"]
escalation: null

related_documents: [DECISION-CAMPAIGN-001]
---

O rascunho descreve as duas primeiras conferências do pedido, mas não diz quem aprova cada tipo de conteúdo nem quanto tempo cada etapa pode esperar.

O que observar: um processo sem prazo deixa o pedido parado sem que ninguém perceba. A pergunta em aberto sobre prazos aponta esse risco.
