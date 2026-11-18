---
# Versão histórica 1.0, arquivada e não vigente. A Aurora é uma organização inventada pelo Contexto.
id: CONCEPT-ONBOARDING-001
schema_version: "1.0.0"
type: conceito
title: "Participante ativo: programa de integração Aurora"
version: "1.0"
revision_id: "CONCEPT-ONBOARDING-001@1.0" # versão específica; id = assunto estável
status: superseded
owner: "Coordenação de Integração (Aurora)"
approver: "Gerência de Pessoas (Aurora)"
valid_from: "2026-08-03"
valid_to: "2026-09-01"       # fim exclusivo da vigência; null = sem fim documentado
recorded_at: "2026-08-03"
version_date: "2026-08-03"
last_reviewed: "2026-08-03"
review_interval: null
source_of_truth: "Manual do Programa de Integração Aurora, versão 1.0, seção 2.1"
supersedes_revision: "CONCEPT-ONBOARDING-001@0.1"
superseded_by_revision: "CONCEPT-ONBOARDING-001@2.0"
intent:
  question: null
  audience: []
  purpose: "Contar, nos relatórios do programa, quem está de fato participando"
  decisions: []
plain_summary: null
open_questions: []
version_history:
  - version: "1.0"
    date: "2026-08-03"
    change: "Primeira definição aprovada: presença em pelo menos uma atividade nos últimos 60 dias"
    approved_by: "Gerência de Pessoas (Aurora)"
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
  applies_when: "Relatórios e acompanhamento do programa de integração"
  does_not_apply_when: "Avaliação de desempenho, contratação ou benefícios"
vocabulary:
  prefLabel: "Participante ativo"
  altLabel: []
  broader: []
  related: ["Participante inscrito", "Participante em pausa", "Participante concluinte"]
  not_synonyms: ["Participante inscrito", "Participante em pausa", "Participante concluinte"]
  other_domain_meanings: ["Na folha de pagamento, 'ativo' significa vínculo de trabalho vigente. Não é o mesmo conceito."]
definition: "Pessoa inscrita no programa, que não está em pausa nem concluiu todas as atividades, e que registrou presença em pelo menos uma atividade entre 60 dias antes da data de referência do relatório e a própria data de referência, ambas incluídas."
inclusion_criteria:
  - "Inscrição confirmada no programa"
  - "Pelo menos uma presença registrada entre 60 dias antes da data de referência e a própria data"
  - "Sem afastamento registrado na data de referência e com atividades ainda por concluir"
exclusion_criteria:
  - "Inscrição sem nenhuma presença registrada: é participante inscrito"
  - "Afastamento registrado na data de referência: é participante em pausa"
  - "Todas as atividades concluídas: é participante concluinte"
examples: ["Inscrita em 01/08, presente na oficina de 20/08. Em 31/08 é participante ativa."]
counterexamples:
  - "Inscrito em 01/08, sem nenhuma presença. Em 31/08 é participante inscrito, não ativo."
  - "Presente em 20/06 e nunca mais. Em 31/08 passaram mais de 60 dias: não é ativo."
boundary_cases: ["Presença exatamente 60 dias antes da data de referência: conta como ativa."]
validation:
  decisions_confirmed_by: "Gerência de Pessoas (Aurora)"
  confirmation_evidence: "Ata de aprovação de 03/08/2026"
  review_history: ["2026-08-03: primeira definição aprovada, janela de 60 dias"]

related_documents: []
---

Esta é a versão 1.0 do conceito guardada como foi aprovada, com a janela de atividade de 60 dias. Só o formato mudou: os valores aprovados são os mesmos.

O que observar: a cópia permite responder quem era participante ativo numa data de agosto, pela regra que valia naquele dia.
