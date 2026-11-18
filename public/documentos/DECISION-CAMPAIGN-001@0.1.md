---
# Exemplo do Contexto, versão com lacunas: nada aqui foi aprovado. A Aurora é uma organização inventada.
id: DECISION-CAMPAIGN-001
schema_version: "1.1.0"
type: decisao
title: "Triagem de campanha: Aurora"
version: "0.1"
revision_id: "DECISION-CAMPAIGN-001@0.1" # versão específica; id = assunto estável
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
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/DECISION-CAMPAIGN-001@0.1.md"
intent:
  question: "Que encaminhamento deve receber um pedido de campanha?"
  audience: ["Operação de Marketing", "Revisão de Conteúdo"]
  purpose: "Expor critérios de triagem e evitar que etapas sejam confundidas com aprovação"
  decisions: ["Encaminhar cada pedido de campanha"]
plain_summary: "Rascunho: uma tabela diz se o pedido volta, vai para revisão, pede esclarecimento ou segue para aprovação; brief completo e evidência suficiente ainda não têm definição."
open_questions:
  - question: "A tabela foi aprovada pela área?"
    impact: "Sem aprovação, a tabela não pode encaminhar pedidos"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Quem decide se a evidência é suficiente?"
    impact: "Dois revisores podem classificar o mesmo material de forma diferente"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Quais campos tornam um brief completo?"
    impact: "Pedidos iguais podem ser devolvidos ou aceitos conforme quem confere"
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
  applies_when: "Pedido de campanha externa na Aurora"
  not_applicable_when: "Outro tipo de publicação"
required_inputs:
  - name: brief_complete
    allowed_values: [true, false, unknown]
    definition: "Ainda não definido: confirmar com a área quais campos são obrigatórios"
  - name: evidence_sufficient
    allowed_values: [true, false, unknown]
    definition: "Ainda não definido: confirmar quais evidências são suficientes e quem decide"
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
  - "Hipótese a confirmar: pedido com brief completo e sem evidência pode exigir linha própria; a linha atual o encaminha para revisão do responsável."
default_behavior: request_clarification
unknown_input_behavior: request_clarification
exceptions: []
tests:
  - case: "Publicação que diz 'protege o cabelo do calor até 230 °C': brief marcado como completo, nenhum ensaio anexado"
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

related_documents: [PROCESS-CAMPAIGN-001]
---

# Triagem de campanha: Aurora (DECISION-CAMPAIGN-001@0.1)

> **Estado:** Rascunho
>
> **Vigência:** sem vigência definida
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/DECISION-CAMPAIGN-001@0.1.md

## Pergunta que este documento responde (DECISION-CAMPAIGN-001@0.1, sem vigência definida)

Que encaminhamento deve receber um pedido de campanha?

## Em poucas palavras (DECISION-CAMPAIGN-001@0.1, sem vigência definida)

Rascunho: uma tabela diz se o pedido volta, vai para revisão, pede esclarecimento ou segue para aprovação; brief completo e evidência suficiente ainda não têm definição.

## Comentário (DECISION-CAMPAIGN-001@0.1, sem vigência definida)

A tabela de decisão já cobre todas as combinações de entradas, cada uma com um único resultado. O que falta é dizer o que torna um brief completo e quem decide se a evidência basta.

O que observar: a tabela pode estar certa e mesmo assim não servir. Sem a definição das entradas, dois revisores preenchem as mesmas colunas de formas diferentes.
