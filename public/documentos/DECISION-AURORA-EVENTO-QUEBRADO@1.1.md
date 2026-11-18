---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: DECISION-AURORA-EVENTO-QUEBRADO
schema_version: "1.1.0"
type: decisao
title: "Evento quebrado: Aurora"
version: "1.1"
revision_id: "DECISION-AURORA-EVENTO-QUEBRADO@1.1" # versão específica; id = assunto estável
status: approved
owner: "Analytics de E-commerce (Aurora)"
approver: "Gerência de Analytics (Aurora)"
valid_from: "2026-11-17"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-11-17"
last_reviewed: "2026-11-17"
review_interval: "P6M"
source_of_truth: "Plano de mensuração da Aurora e Evento de coleta de cada evento"
supersedes_revision: "DECISION-AURORA-EVENTO-QUEBRADO@1.0"
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/DECISION-AURORA-EVENTO-QUEBRADO@1.1.md"
intent:
  question: "Um evento sem disparos numa operação deve ser tratado como falha?"
  audience: ["Analytics de E-commerce", "Engenharia de Dados", "Gerência de Analytics"]
  purpose: "Dizer quando o silêncio de um evento vira suspeita de falha e quando é só espera, exceção ou dúvida"
  decisions: ["Abrir ou não uma investigação de evento quebrado"]
plain_summary: "Um evento só vira candidato a falha quando está no escopo, os dados do dia estão completos, não há exceção conhecida, ele costuma disparar e o silêncio durou o que o time definiu. Em qualquer dúvida, pede-se esclarecimento."
open_questions: []
version_history:
  - version: "1.1"
    date: "2026-11-17"
    change: "Acrescentados os testes do incidente de 11/11 no México; nenhuma linha da tabela mudou"
    approved_by: "Gerência de Analytics (Aurora)"
  - version: "1.0"
    date: "2026-10-13"
    change: "Primeira tabela aprovada, com cinco entradas verificáveis e seis saídas"
    approved_by: "Gerência de Analytics (Aurora)"
  - version: "0.1"
    date: "2026-10-06"
    change: "Primeiro rascunho, com lacunas registradas"
    approved_by: null

context:
  instructions: null
  verifiedStatements: []
  constraints: []
authoritativeDefinitions: []

scope:
  applies_when: "Eventos do plano de mensuração, avaliados por evento e por operação (BR e MX), depois de aplicadas as exceções conhecidas"
  not_applicable_when: "Evento fora do plano de mensuração ou operação que não o implementa"
required_inputs:
  - name: active_in_scope
    allowed_values: [true, false, unknown]
    definition: "O evento está implementado e previsto no plano de mensuração da operação (BR ou MX) avaliada. Quem confirma é Analytics de E-commerce, pelo Evento de coleta"
  - name: ingestion_complete
    allowed_values: [true, false, unknown]
    definition: "Os dados do dia avaliado terminaram de chegar à tabela de eventos da operação. Dia ainda em andamento ou com carga atrasada vale false"
  - name: known_exception_applies
    allowed_values: [true, false, unknown]
    definition: "Existe, para o evento e a operação, uma exceção conhecida registrada que cobre o período avaliado, como manutenção programada, com quem aprovou e a evidência"
  - name: expected_in_window
    allowed_values: [true, false, unknown]
    definition: "O evento costuma disparar na operação dentro da janela avaliada, pela linha de base da própria operação. Evento novo, sem histórico suficiente, vale unknown"
  - name: deviation_streak_reached
    allowed_values: [true, false, unknown]
    definition: "Dias completos seguidos abaixo da linha de base da mesma operação, no mínimo a tolerância ao silêncio registrada no Evento de coleta. O N é escolha do time e não aparece aqui"
possible_outputs: [not_active_in_scope, wait_for_complete_data, explained_by_known_exception, within_expected, failure_candidate, request_clarification]
decision_table:
  - when: {active_in_scope: false, ingestion_complete: any, known_exception_applies: any, expected_in_window: any, deviation_streak_reached: any}
    then: not_active_in_scope
  - when: {active_in_scope: unknown, ingestion_complete: any, known_exception_applies: any, expected_in_window: any, deviation_streak_reached: any}
    then: request_clarification
  - when: {active_in_scope: true, ingestion_complete: false, known_exception_applies: any, expected_in_window: any, deviation_streak_reached: any}
    then: wait_for_complete_data
  - when: {active_in_scope: true, ingestion_complete: unknown, known_exception_applies: any, expected_in_window: any, deviation_streak_reached: any}
    then: wait_for_complete_data
  - when: {active_in_scope: true, ingestion_complete: true, known_exception_applies: true, expected_in_window: any, deviation_streak_reached: any}
    then: explained_by_known_exception
  - when: {active_in_scope: true, ingestion_complete: true, known_exception_applies: unknown, expected_in_window: any, deviation_streak_reached: any}
    then: request_clarification
  - when: {active_in_scope: true, ingestion_complete: true, known_exception_applies: false, expected_in_window: false, deviation_streak_reached: any}
    then: within_expected
  - when: {active_in_scope: true, ingestion_complete: true, known_exception_applies: false, expected_in_window: unknown, deviation_streak_reached: any}
    then: request_clarification
  - when: {active_in_scope: true, ingestion_complete: true, known_exception_applies: false, expected_in_window: true, deviation_streak_reached: false}
    then: within_expected
  - when: {active_in_scope: true, ingestion_complete: true, known_exception_applies: false, expected_in_window: true, deviation_streak_reached: true}
    then: failure_candidate
  - when: {active_in_scope: true, ingestion_complete: true, known_exception_applies: false, expected_in_window: true, deviation_streak_reached: unknown}
    then: request_clarification
priority_rules:
  - "As onze linhas são mutuamente exclusivas: cada combinação das cinco entradas casa com uma única linha, então não há precedência a aplicar."
  - "A ordem de leitura é escopo, dados completos, exceção conhecida, expectativa e sequência; failure_candidate só sai quando todas respondem como a linha 10."
default_behavior: request_clarification
unknown_input_behavior: request_clarification
exceptions:
  - condition: "Manutenção programada do site ou do contêiner de tags"
    approval_role: "Gerência de Analytics (Aurora)"
    evidence_needed: "Chamado de manutenção com datas de início e fim, anexado ao Evento de coleta"
tests:
  - case: "add_to_cart na operação MX, avaliado em 17/11 com dados até 15/11: 5 dias completos em zero depois da versão 48 do contêiner GTM-AURMX01"
    inputs: {active_in_scope: true, ingestion_complete: true, known_exception_applies: false, expected_in_window: true, deviation_streak_reached: true}
    expected_outcome: failure_candidate
    reasoning: "Evento previsto, dados completos, sem exceção e silêncio além da tolerância: abrir investigação, que ainda não prova defeito"
  - case: "generate_lead na operação BR: 2 dias completos em zero, com tolerância ao silêncio de 4 dias"
    inputs: {active_in_scope: true, ingestion_complete: true, known_exception_applies: false, expected_in_window: true, deviation_streak_reached: false}
    expected_outcome: within_expected
    reasoning: "A sequência ainda não chegou à tolerância registrada"
  - case: "generate_lead na operação MX, evento não implementado"
    inputs: {active_in_scope: false, ingestion_complete: true, known_exception_applies: false, expected_in_window: true, deviation_streak_reached: false}
    expected_outcome: not_active_in_scope
    reasoning: "Evento fora do escopo da operação não é avaliado"
  - case: "purchase na operação BR, avaliado em 16/11 com o dia ainda incompleto"
    inputs: {active_in_scope: true, ingestion_complete: false, known_exception_applies: false, expected_in_window: true, deviation_streak_reached: true}
    expected_outcome: wait_for_complete_data
    reasoning: "Dia incompleto não prova silêncio; esperar a carga terminar"
  - case: "generate_lead na operação BR de 22 a 24/09, com manutenção programada registrada"
    inputs: {active_in_scope: true, ingestion_complete: true, known_exception_applies: true, expected_in_window: true, deviation_streak_reached: true}
    expected_outcome: explained_by_known_exception
    reasoning: "A exceção conhecida explica o silêncio"
  - case: "Evento novo na operação BR, sem 28 dias de histórico"
    inputs: {active_in_scope: true, ingestion_complete: true, known_exception_applies: false, expected_in_window: unknown, deviation_streak_reached: unknown}
    expected_outcome: request_clarification
    reasoning: "Sem histórico não há linha de base; pedir esclarecimento a Analytics de E-commerce"
conflicts: []

related_documents: [EVENT-AURORA-GENERATE-LEAD]
---

# Evento quebrado: Aurora (DECISION-AURORA-EVENTO-QUEBRADO@1.1)

> **Estado:** Aprovado
>
> **Vigência:** de 17/11/2026, sem fim previsto
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/DECISION-AURORA-EVENTO-QUEBRADO@1.1.md

## Pergunta que este documento responde (DECISION-AURORA-EVENTO-QUEBRADO@1.1, de 17/11/2026, sem fim previsto)

Um evento sem disparos numa operação deve ser tratado como falha?

## Em poucas palavras (DECISION-AURORA-EVENTO-QUEBRADO@1.1, de 17/11/2026, sem fim previsto)

Um evento só vira candidato a falha quando está no escopo, os dados do dia estão completos, não há exceção conhecida, ele costuma disparar e o silêncio durou o que o time definiu. Em qualquer dúvida, pede-se esclarecimento.

## Comentário (DECISION-AURORA-EVENTO-QUEBRADO@1.1, de 17/11/2026, sem fim previsto)

A versão 1.1 acrescentou os testes do incidente de 11/11 no México. Nenhuma linha da tabela mudou.

O limiar de dias de silêncio não está aqui: ele é escolha do time e mora no Evento de coleta. Failure candidate quer dizer candidato a falha, isto é, motivo para investigar, e não defeito provado.
