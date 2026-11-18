---
# Exemplo do Contexto, versão com lacunas: nada aqui foi aprovado. A Aurora é uma organização inventada.
id: RUBRIC-CAMPAIGN-001
schema_version: "1.1.0"
type: rubrica
title: "Rubrica de revisão de material de campanha: Aurora"
version: "0.1"
revision_id: "RUBRIC-CAMPAIGN-001@0.1" # versão específica; id = assunto estável
status: draft
owner: "Revisão de Conteúdo (Aurora)"
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
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/RUBRIC-CAMPAIGN-001@0.1.md"
intent:
  question: "Como avaliar um material de campanha antes da aprovação formal?"
  audience: ["Revisão de Conteúdo"]
  purpose: "Trocar a instrução 'avaliar clareza, veracidade e alinhamento à marca, nota de 0 a 10' por critérios que dois revisores apliquem do mesmo jeito"
  decisions: []
plain_summary: "Rascunho: quatro critérios de mesmo peso, com níveis de 0 a 4 que ainda não dizem o que observar no material."
open_questions:
  - question: "Quem aprova critérios, âncoras e pesos? Os pesos iguais são provisórios."
    impact: "Sem aprovação, a nota não pode alimentar a triagem"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "As âncoras dizem 'fonte fraca' e 'fonte adequada'. O que um revisor observa no material para separar uma da outra?"
    impact: "Dois revisores dão notas diferentes ao mesmo material"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Uma fonte sem data conta como prova?"
    impact: "Um número desatualizado pode passar como provado"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Uma restrição da oferta que aparece só no regulamento é suficiente?"
    impact: "Clientes podem ter a oferta negada sem ter sido avisados"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "A nota de alegações com prova decide a entrada 'evidência suficiente' da triagem? A partir de qual nível?"
    impact: "A triagem continua sem critério para encaminhar"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Como resolver quando dois revisores dão níveis diferentes ao mesmo critério?"
    impact: "A discordância fica sem quem decida"
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

evaluation_target: "Material de campanha externa antes da aprovação formal"
allowed_use: ["Revisão de material na etapa 3 do processo de campanha", "Calibração entre revisores"]
disallowed_use: ["Avaliar a pessoa que produziu o material", "Aprovar ou publicar automaticamente"]
criteria:
  - id: claims_with_proof
    name: "Alegações com prova"
    definition: "Números e comparações do material têm fonte"
    not_in_scope: null
    weight: 25
    expected_evidence: ["Fonte anexada"]
    anchors:
      "0": "Sem fonte"
      "1": "Fonte fraca"
      "2": "Fonte parcial"
      "3": "Fonte adequada"
      "4": "Fonte excelente"
  - id: offer_terms
    name: "Condições da oferta"
    definition: "A oferta está clara"
    not_in_scope: null
    weight: 25
    expected_evidence: [Regulamento]
    anchors:
      "0": "Oferta confusa"
      "1": "Faltam condições importantes"
      "2": "Condições parciais"
      "3": "Condições claras"
      "4": "Condições muito claras"
  - id: audience_fit
    name: "Adequação ao público"
    definition: "Fala com o público certo"
    not_in_scope: null
    weight: 25
    expected_evidence: [Brief]
    anchors:
      "0": "Público errado"
      "1": "Pouco adequado"
      "2": "Razoável"
      "3": Adequado
      "4": "Muito adequado"
  - id: brand_compliance
    name: "Conformidade com a marca"
    definition: "Segue o guia de marca"
    not_in_scope: null
    weight: 25
    expected_evidence: ["Guia de marca"]
    anchors:
      "0": "Fora da marca"
      "1": "Muitos desvios"
      "2": "Alguns desvios"
      "3": "Dentro da marca"
      "4": Exemplar
scoring:
  weight_sum: 100
  scale: [0, 1, 2, 3, 4]
  missing_evidence_behavior: not_evaluable
  not_evaluable_rule: null
  decision_threshold: null
  automatic_decision_allowed: false
human_review_required: true
calibration_examples: []
disagreement_resolution: null
privacy_and_fairness_considerations: ["Avaliar o material, nunca a pessoa que o produziu"]

related_documents: [PROCESS-CAMPAIGN-001, DECISION-CAMPAIGN-001]
---

# Rubrica de revisão de material de campanha: Aurora (RUBRIC-CAMPAIGN-001@0.1)

> **Estado:** Rascunho
>
> **Vigência:** sem vigência definida
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/RUBRIC-CAMPAIGN-001@0.1.md

## Pergunta que este documento responde (RUBRIC-CAMPAIGN-001@0.1, sem vigência definida)

Como avaliar um material de campanha antes da aprovação formal?

## Em poucas palavras (RUBRIC-CAMPAIGN-001@0.1, sem vigência definida)

Rascunho: quatro critérios de mesmo peso, com níveis de 0 a 4 que ainda não dizem o que observar no material.

## Comentário (RUBRIC-CAMPAIGN-001@0.1, sem vigência definida)

O rascunho troca uma nota de 0 a 10 por quatro critérios com cinco níveis cada. Os níveis ainda usam palavras como "fonte fraca" e "fonte adequada", que cada revisor lê de um jeito.

O que observar: um nível só ajuda quando diz o que se vê no material. As perguntas em aberto pedem exatamente isso.
