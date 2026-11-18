---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: DECISION-CAMPAIGN-001
schema_version: "1.0.0"
type: decisao
title: "Triagem de campanha: Aurora"
version: "2.0"
revision_id: "DECISION-CAMPAIGN-001@2.0" # versão específica; id = assunto estável
status: approved
owner: "Revisão de Conteúdo (Aurora)"
approver: "Liderança de Marca (Aurora)"
valid_from: "2026-09-10"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-09-10"
last_reviewed: "2026-09-10"
review_interval: null
source_of_truth: "Procedimento PRC-MKT-007, anexo B"
supersedes_revision: "DECISION-CAMPAIGN-001@1.0"
superseded_by_revision: null
intent:
  question: "Que encaminhamento deve receber um pedido de campanha?"
  audience: ["Operação de Marketing", "Revisão de Conteúdo", "Liderança de Marca"]
  purpose: "Expor critérios de triagem e evitar que etapas sejam confundidas com aprovação"
  decisions: ["Encaminhar cada pedido de campanha"]
plain_summary: "Brief incompleto volta para quem pediu; sem evidência, o pedido vai para revisão; com tudo certo, segue para quem aprova; na dúvida, pede esclarecimento."
open_questions: []
version_history:
  - version: "2.0"
    date: "2026-09-10"
    change: "Evidência desconhecida deixa de seguir para revisão e passa a pedir esclarecimento ao solicitante"
    approved_by: "Liderança de Marca (Aurora)"
  - version: "1.0"
    date: "2026-08-12"
    change: "Primeira tabela aprovada, com definição de brief completo e de evidência suficiente; diferente do rascunho, evidência desconhecida seguia para revisão responsável"
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
  applies_when: "Pedido de campanha externa na Aurora"
  not_applicable_when: "Outro tipo de publicação"
required_inputs:
  - name: brief_complete
    allowed_values: [true, false, unknown]
    definition: "Os cinco campos obrigatórios estão preenchidos: objetivo, canal, público, período e material"
  - name: evidence_sufficient
    allowed_values: [true, false, unknown]
    definition: "Cada alegação verificável do material tem uma fonte anexada e datada que diz o mesmo que o material. Quem classifica é a Revisão de Conteúdo, pela RUBRIC-CAMPAIGN-001: alegações com prova em nível 3 ou 4"
possible_outputs: [complement_information, responsible_review, request_formal_approval, request_clarification]
decision_table:
  - when: {brief_complete: false, evidence_sufficient: any}
    then: complement_information
  - when: {brief_complete: true, evidence_sufficient: false}
    then: responsible_review
  - when: {brief_complete: true, evidence_sufficient: true}
    then: request_formal_approval
  - when: {brief_complete: unknown, evidence_sufficient: any}
    then: request_clarification
  - when: {brief_complete: true, evidence_sufficient: unknown}
    then: request_clarification
priority_rules:
  - "As cinco linhas são mutuamente exclusivas: cada combinação de entradas casa com uma única linha, então não há precedência a aplicar."
  - "O conflito do texto original (pedido completo, mas sem evidência) foi resolvido criando uma linha própria para esse caso."
default_behavior: request_clarification
unknown_input_behavior: request_clarification
exceptions:
  - condition: "Campanha de utilidade pública com prazo legal"
    approval_role: "Diretoria de Marketing (Aurora)"
    evidence_needed: "Autorização escrita anexada ao pedido"
tests:
  - case: "Publicação que diz 'protege o cabelo do calor até 230 °C': brief com os cinco campos, nenhum ensaio anexado"
    inputs: {brief_complete: true, evidence_sufficient: false}
    expected_outcome: responsible_review
    reasoning: "Falta evidência para seguir a solicitação"
  - case: "E-mail que diz '22% menos plástico que o frasco de 2024': brief completo; a planilha anexada, com data, diz o mesmo"
    inputs: {brief_complete: true, evidence_sufficient: true}
    expected_outcome: request_formal_approval
    reasoning: "Encaminhar a quem aprova; não publicar"
  - case: "Pedido sem o campo período; ninguém avaliou o material ainda"
    inputs: {brief_complete: false, evidence_sufficient: unknown}
    expected_outcome: complement_information
    reasoning: "Brief incompleto é devolvido, qualquer que seja o estado das evidências"
conflicts: []

related_documents: [PROCESS-CAMPAIGN-001, RUBRIC-CAMPAIGN-001]
---

A versão 2.0 mudou um caminho: evidência desconhecida deixou de seguir para revisão e passou a pedir esclarecimento a quem fez o pedido. As entradas agora têm definição verificável, e a exceção para campanha com prazo legal tem quem aprova e a evidência exigida.

O que observar: cada teste descreve um pedido real, com a frase do material, e não só uma combinação de verdadeiro e falso.
