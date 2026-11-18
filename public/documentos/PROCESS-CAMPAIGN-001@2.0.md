---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: PROCESS-CAMPAIGN-001
schema_version: "1.1.0"
type: processo
title: "Solicitar e publicar campanha: Aurora"
version: "2.0"
revision_id: "PROCESS-CAMPAIGN-001@2.0" # versão específica; id = assunto estável
status: approved
owner: "Operação de Marketing (Aurora)"
approver: "Liderança de Marca (Aurora)"
valid_from: "2026-09-10"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-09-10"
last_reviewed: "2026-09-10"
review_interval: null
source_of_truth: "Procedimento PRC-MKT-007"
supersedes_revision: "PROCESS-CAMPAIGN-001@1.0"
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/PROCESS-CAMPAIGN-001@2.0.md"
intent:
  question: "Que caminho um pedido de campanha percorre até ser publicado?"
  audience: ["Operação de Marketing", "Revisão de Conteúdo", "Liderança de Marca"]
  purpose: "Descrever as transferências e evidências necessárias até a publicação de uma campanha externa"
  decisions: []
plain_summary: "Cinco etapas, do registro do pedido à publicação com evidência; sem decisão em 3 dias úteis, o pedido sobe à Diretoria de Marketing."
open_questions: []
version_history:
  - version: "2.0"
    date: "2026-09-10"
    change: "A publicação, que fazia parte da etapa de aprovação, virou a etapa S05, que só termina com o endereço e a data da publicação anexados. Motivo: auditoria interna encontrou publicações sem comprovante"
    approved_by: "Liderança de Marca (Aurora)"
  - version: "1.0"
    date: "2026-08-12"
    change: "Primeira versão aprovada, com quatro etapas e prazo de complementação; a última aprovava e publicava"
    approved_by: "Liderança de Marca (Aurora)"
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
  applies_when: "Campanha externa da Aurora em canais próprios ou pagos"
  not_applicable_when: "Comunicados internos não promocionais"
trigger: "Brief registrado no formulário de solicitação"
preconditions: ["Solicitante identificado e área responsável informada"]
required_inputs: [objetivo, canal, "público", "período", material]
roles:
  process_owner: "Operação de Marketing (Aurora)"
  performers: ["Operação de Marketing", "Revisão de Conteúdo"]
  approvers: ["Liderança de Marca"]
steps:
  - id: S01
    name: "Receber e registrar"
    performer_role: "Operação de Marketing"
    action: "Registrar o pedido e atribuir identificador"
    inputs: [brief]
    output_evidence: "Registro do pedido com identificador"
    next_step: S02
    exception_handling: "Pedido sem solicitante identificado é devolvido"
  - id: S02
    name: "Conferir brief"
    performer_role: "Operação de Marketing"
    action: "Verificar os cinco campos obrigatórios"
    inputs: [brief]
    output_evidence: "Lista de conferência preenchida"
    next_step: "S03 se completo; devolver ao solicitante se incompleto"
    exception_handling: "Complementação pedida por escrito; prazo de 2 dias úteis; sem resposta, o pedido é encerrado como devolvido"
  - id: S03
    name: "Aplicar regra de encaminhamento"
    performer_role: "Revisão de Conteúdo"
    action: "Aplicar a decisão DECISION-CAMPAIGN-001"
    inputs: [brief, "evidências das alegações", "avaliação pela RUBRIC-CAMPAIGN-001"]
    output_evidence: "Resultado da triagem e motivo"
    next_step: "S04 se o resultado for solicitar aprovação formal; depois de revisão responsável ou esclarecimento, o material corrigido volta a S03"
    exception_handling: "Evidência ausente ou desconhecida segue o resultado previsto na regra"
  - id: S04
    name: "Aprovação formal"
    performer_role: "Liderança de Marca"
    action: "Aprovar ou rejeitar o material revisado"
    inputs: ["material revisado", "resultado da triagem"]
    output_evidence: "Aprovação ou rejeição registrada, com motivo"
    next_step: "S05 se aprovado; encerrar como rejeitado caso contrário"
    exception_handling: "Sem decisão em 3 dias úteis, escalar à Diretoria de Marketing"
  - id: S05
    name: "Publicar e registrar evidência"
    performer_role: "Operação de Marketing"
    action: "Publicar e guardar o endereço e a data da publicação"
    inputs: ["aprovação válida"]
    output_evidence: "Endereço da publicação e data, anexados ao pedido"
    next_step: Fim
    exception_handling: "Falha de publicação é registrada e o pedido volta a S05"
decision_rules: [DECISION-CAMPAIGN-001]
completion:
  success_criteria: ["Publicação aprovada, publicada e com evidência anexada"]
  failure_outcomes: [Devolvido, Rejeitado, Cancelado]
  evidence_record: "Pedido no sistema de solicitações, com anexos"
exceptions: ["Pedido cancelado depois de aprovado: registrar o cancelamento e não publicar"]
escalation: "Diretoria de Marketing (Aurora), quando a Liderança de Marca não decidir no prazo"

related_documents: [DECISION-CAMPAIGN-001, RUBRIC-CAMPAIGN-001]
---

# Solicitar e publicar campanha: Aurora (PROCESS-CAMPAIGN-001@2.0)

> **Estado:** Aprovado
>
> **Vigência:** de 10/09/2026, sem fim previsto
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/PROCESS-CAMPAIGN-001@2.0.md

## Pergunta que este documento responde (PROCESS-CAMPAIGN-001@2.0, de 10/09/2026, sem fim previsto)

Que caminho um pedido de campanha percorre até ser publicado?

## Em poucas palavras (PROCESS-CAMPAIGN-001@2.0, de 10/09/2026, sem fim previsto)

Cinco etapas, do registro do pedido à publicação com evidência; sem decisão em 3 dias úteis, o pedido sobe à Diretoria de Marketing.

## Comentário (PROCESS-CAMPAIGN-001@2.0, de 10/09/2026, sem fim previsto)

A versão 2.0 tem cinco etapas, cada uma com quem executa, a evidência que deixa e o que acontece quando algo sai do esperado. A triagem da etapa 3 não repete a regra: aponta a decisão de encaminhamento.

O que observar: `exception_handling` e `escalation` dizem o que fazer quando o prazo vence, em vez de deixar a decisão para quem estiver de plantão.
