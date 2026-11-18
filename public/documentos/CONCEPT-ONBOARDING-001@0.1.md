---
# Exemplo do Contexto, versão com lacunas: nada aqui foi aprovado. A Aurora é uma organização inventada.
id: CONCEPT-ONBOARDING-001
schema_version: "1.1.0"
type: conceito
title: "Participante ativo: programa de integração Aurora"
version: "0.1"
revision_id: "CONCEPT-ONBOARDING-001@0.1" # versão específica; id = assunto estável
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
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/CONCEPT-ONBOARDING-001@0.1.md"
intent:
  question: "Quem conta como participante ativo no programa de integração da Aurora?"
  audience: ["Coordenação de Integração"]
  purpose: "Distinguir inscrição, atividade e conclusão em relatórios"
  decisions: []
plain_summary: "Rascunho: separa quem se inscreveu, quem participa e quem concluiu, mas ainda não diz que atividade nem que período contam."
open_questions:
  - question: "Qual atividade marca uma pessoa como ativa?"
    impact: "Relatórios podem contar populações diferentes"
    owner_to_resolve: null
    status: unresolved
    resolution: null
  - question: "Qual período determina a classificação?"
    impact: "Atividade passada pode ser confundida com status atual"
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

domain: "Programa voluntário de integração: Aurora"
scope:
  applies_when: "Acompanhamento do programa"
  does_not_apply_when: "Avaliação de desempenho, contratação ou benefícios"
vocabulary:
  prefLabel: "Participante ativo"
  altLabel: []
  broader: []
  related: ["Participante inscrito", "Participante concluinte"]
  not_synonyms: ["Pessoa inscrita", "Pessoa que concluiu o programa"]
  other_domain_meanings: []
definition: null
inclusion_criteria: []
exclusion_criteria: []
examples: []
counterexamples: []
boundary_cases: []
validation:
  decisions_confirmed_by: null
  confirmation_evidence: null
  review_history: []

related_documents: []
---

# Participante ativo: programa de integração Aurora (CONCEPT-ONBOARDING-001@0.1)

> **Estado:** Rascunho
>
> **Vigência:** sem vigência definida
>
> **Domínio:** Programa voluntário de integração: Aurora
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/CONCEPT-ONBOARDING-001@0.1.md

## Pergunta que este documento responde (CONCEPT-ONBOARDING-001@0.1, sem vigência definida)

Quem conta como participante ativo no programa de integração da Aurora?

## Em poucas palavras (CONCEPT-ONBOARDING-001@0.1, sem vigência definida)

Rascunho: separa quem se inscreveu, quem participa e quem concluiu, mas ainda não diz que atividade nem que período contam.

## Comentário (CONCEPT-ONBOARDING-001@0.1, sem vigência definida)

O rascunho já separa três situações que os relatórios misturavam: inscrição, atividade e conclusão. A definição ficou em branco, porque faltavam duas respostas: que atividade marca alguém como ativo e em qual período.

O que observar: `not_synonyms` já impede o erro mais comum, tratar pessoa inscrita como participante ativo, mesmo antes de a definição existir.
