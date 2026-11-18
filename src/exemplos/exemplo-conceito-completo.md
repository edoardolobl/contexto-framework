---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: CONCEPT-ONBOARDING-001
schema_version: "1.1.0"
type: conceito
title: "Participante ativo: programa de integração Aurora"
version: "2.0"
revision_id: "CONCEPT-ONBOARDING-001@2.0" # versão específica; id = assunto estável
status: approved
owner: "Coordenação de Integração (Aurora)"
approver: "Gerência de Pessoas (Aurora)"
valid_from: "2026-09-01"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-09-01"
last_reviewed: "2026-09-01"
review_interval: null
source_of_truth: "Manual do Programa de Integração Aurora, seção 2.1"
supersedes_revision: "CONCEPT-ONBOARDING-001@1.0"
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/CONCEPT-ONBOARDING-001@2.0.md"
intent:
  question: "Quem conta como participante ativo no programa de integração da Aurora?"
  audience: ["Coordenação de Integração", "Gerência de Pessoas"]
  purpose: "Contar, nos relatórios do programa, quem está de fato participando"
  decisions: ["Acompanhar a participação no relatório mensal do programa"]
plain_summary: "Ativo é quem se inscreveu, não está em pausa, não concluiu e foi a pelo menos uma atividade nos últimos 30 dias."
open_questions: []
version_history:
  - version: "2.0"
    date: "2026-09-01"
    change: "Janela de atividade reduzida de 60 para 30 dias, para coincidir com o relatório mensal"
    approved_by: "Gerência de Pessoas (Aurora)"
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
definition: "Pessoa inscrita no programa, que não está em pausa nem concluiu todas as atividades, e que registrou presença em pelo menos uma atividade entre 30 dias antes da data de referência do relatório e a própria data de referência, ambas incluídas."
inclusion_criteria:
  - "Inscrição confirmada no programa"
  - "Pelo menos uma presença registrada entre 30 dias antes da data de referência e a própria data"
  - "Sem afastamento registrado na data de referência e com atividades ainda por concluir"
exclusion_criteria:
  - "Inscrição sem nenhuma presença registrada: é participante inscrito"
  - "Afastamento registrado na data de referência: é participante em pausa"
  - "Todas as atividades concluídas: é participante concluinte"
examples: ["Inscrita em 01/08, presente na oficina de 20/09. Em 30/09 é participante ativa."]
counterexamples:
  - "Inscrito em 01/08, sem nenhuma presença. Em 30/09 é participante inscrito, não ativo."
  - "Presente em 20/08 e nunca mais. Em 30/09 passaram 41 dias: não é ativo."
  - "Presente em 25/09, com afastamento registrado de 28/09 até outubro. Em 30/09 é participante em pausa, não ativo."
boundary_cases: ["Presença em 31/08, exatamente 30 dias antes de 30/09: conta como ativa."]
validation:
  decisions_confirmed_by: "Gerência de Pessoas (Aurora)"
  confirmation_evidence: "Ata de aprovação de 01/09/2026"
  review_history: ["2026-09-01: janela alterada de 60 para 30 dias"]

related_documents: []
---

A versão 2.0 reduziu a janela de atividade de 60 para 30 dias, para coincidir com o relatório mensal. Nada mais mudou: critérios de inclusão, de exclusão e termos que não são sinônimos continuam iguais aos da 1.0.

O bloco `vocabulary` segue o SKOS: `prefLabel` é o termo preferido, `altLabel` lista sinônimos de fato equivalentes, `related` lista termos ligados e `not_synonyms` diz com o que não confundir. O caso-limite de 31/08 mostra que a janela inclui as duas pontas.
