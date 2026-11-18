---
# Contrato documental. Não é avaliador automático nem motor de seleção.
# null significa "ainda não sei" ou "ainda não decidido". Não troque null por um palpite: registre a dúvida em open_questions.
# Campos marcados (obrigatório) são o núcleo para sair do rascunho; os blocos "para quem é técnico" são opcionais.
id: null                     # (obrigatório) identificador do assunto, igual em todas as versões
schema_version: "1.0.0"      # versão do formato do arquivo; não mude
type: rubrica
title: null                  # (obrigatório)
version: "0.1"               # (obrigatório) versão deste documento
revision_id: null            # versão específica: id@version; id = assunto estável
status: draft                # (obrigatório) draft | pending_approval | approved | superseded | deprecated
owner: null                  # (obrigatório) cargo ou área responsável, não o nome de uma pessoa
approver: null               # (obrigatório) cargo ou área que aprova
valid_from: null             # primeiro dia da vigência, AAAA-MM-DD
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: null           # (obrigatório) data desta versão, no formato AAAA-MM-DD
last_reviewed: null          # data da última revisão completa, AAAA-MM-DD
review_interval: null        # de quanto em quanto tempo revisar, em ISO 8601: P6M = seis meses
source_of_truth: null        # onde está a versão oficial
supersedes_revision: null    # versão que esta substitui: id@version
superseded_by_revision: null # só na cópia de uma versão substituída: id@version da sucessora
intent:
  question: null             # (obrigatório) pergunta de negócio que o documento responde
  audience: []               # quem usa: cargos ou áreas
  purpose: null              # para quê
  decisions: []              # decisões que mudam conforme a resposta
plain_summary: null          # uma ou duas frases em linguagem direta
open_questions:              # uma entrada por pergunta que ninguém decidiu
  - question: null
    impact: null             # o que dá errado enquanto ela não tem resposta
    owner_to_resolve: null   # quem pode resolver
    status: unresolved       # unresolved | resolved
    resolution: null         # o que foi decidido, com data e evidência; obrigatório quando resolved
version_history:             # uma entrada por versão, a mais recente primeiro
  - version: "0.1"
    date: null
    change: null             # o que mudou nesta versão e por quê
    approved_by: null        # cargo ou área que aprovou; null enquanto não aprovado

# Para quem é técnico: os dois blocos abaixo são opcionais.
context:                     # para quem é técnico: opcional (bloco context do ODCS 3.2.0)
  instructions: null         # instrução curta ao agente, até 500 caracteres; exige review_interval
  verifiedStatements: []     # perguntas típicas; cada item: question e, se já conferida, answer
  constraints: []            # limites do agente; cada item: constraint
# Cada item: type (sql | metricView | filter | dashboard | document | other), url e description.
authoritativeDefinitions: [] # para quem é técnico: opcional. Onde mora a regra executável

evaluation_target: null
allowed_use: []
disallowed_use: []
criteria:
  - id: null
    name: null
    definition: null
    not_in_scope: null       # o que este critério NÃO avalia, para não punir o mesmo erro duas vezes
    weight: null
    expected_evidence: []
    anchors:
      "0": null
      "1": null
      "2": null
      "3": null
      "4": null
scoring:
  weight_sum: null
  scale: [0, 1, 2, 3, 4]
  formula: null              # como a nota é calculada a partir dos níveis e pesos
  missing_evidence_behavior: not_evaluable
  not_evaluable_rule: null   # como a nota final é calculada quando um critério não pôde ser avaliado
  feeds_decision: null       # documento e entrada que a nota alimenta, e a partir de qual nível
  decision_threshold: null
  automatic_decision_allowed: false # a pontuação nunca decide sozinha; uma pessoa revisa
human_review_required: true
calibration_examples: []
disagreement_resolution: null
privacy_and_fairness_considerations: []

related_documents: []        # identificadores de outros documentos
---

# [Nome da rubrica]

> **Como usar este modelo.** Os campos ficam no topo do arquivo, entre as duas linhas `---`. Responda só o que você sabe e consegue comprovar. O que não souber, deixe como `null` e anote em `open_questions`, com quem pode responder. Um campo em branco é melhor do que um palpite. Os campos marcados com **(obrigatório)** são o mínimo para sair do rascunho; os blocos marcados "para quem é técnico" são opcionais.

<!-- contexto:identificacao -->

## Para que serve
Em `intent`, escreva a pergunta de negócio que o documento responde (`question`), como alguém da área faria. Diga quem usa (`audience`), para quê (`purpose`) e quais decisões mudam conforme a resposta (`decisions`). Em `plain_summary`, explique em uma ou duas frases, sem termos técnicos, o que o documento diz.

## O que se avalia
Em `evaluation_target`, diga o trabalho avaliado. Em `allowed_use` e `disallowed_use`, para que a nota pode e não pode servir.

## Critérios e níveis
Em `criteria`, repita um item para cada critério: identificador, nome, definição, o que o critério não avalia (`not_in_scope`), peso, evidências aceitas e o que se vê no trabalho em cada nível de 0 a 4 (`anchors`).

## Nota
Em `scoring`, diga a soma dos pesos, a escala, a fórmula da nota, o que fazer quando falta evidência ou um critério não pode ser avaliado, qual decisão a nota alimenta e a partir de qual nível. A nota nunca decide sozinha: `automatic_decision_allowed` fica `false` e `human_review_required` fica `true`.

## Calibração e cuidados
Em `calibration_examples`, registre trabalhos já avaliados, com o nível de cada critério, a justificativa, a nota e o encaminhamento. Em `disagreement_resolution`, como resolver quando dois revisores discordam. Em `privacy_and_fairness_considerations`, os cuidados com privacidade e justiça.

## Para quem é técnico (opcional)
`authoritativeDefinitions` aponta onde mora a regra executável, como o formulário de avaliação, sem copiar o código para o documento. Cada item tem `type` (`sql`, `metricView`, `filter`, `dashboard`, `document` ou `other`), `url` e `description`.

`context` segue o bloco de mesmo nome do ODCS 3.2.0. Em `instructions`, escreva só o que não cabe em nenhum campo estruturado, em até 500 caracteres; com instrução preenchida, `review_interval` passa a ser obrigatório. `verifiedStatements` guarda as perguntas típicas do assunto: cada item tem a pergunta (`question`) e, quando quem aprova já conferiu, a resposta (`answer`). `constraints` guarda os limites que um agente de IA não pode ultrapassar, um por item, em `constraint`.

## Versões e vigência
A cada mudança na regra, suba `version` e acrescente uma entrada no topo de `version_history`, com a data, o que mudou e por quê, e quem aprovou. Registre a mudança na regra, não só a edição do texto. `version_date` é a data desta versão; `valid_from` e `valid_to` dizem quando a regra vale. Guarde a cópia completa de cada versão aprovada: o histórico sozinho não permite reconstruir a regra anterior. Quando outra versão tomar o lugar desta, a cópia guardada passa a `status: superseded`, com `superseded_by_revision` e `recorded_at`.

Em `last_reviewed`, registre a data da última revisão completa, e em `review_interval`, de quanto em quanto tempo revisar.

## Perguntas em aberto
Acrescente um item em `open_questions` para cada pergunta que ninguém decidiu. Escreva a pergunta (`question`), o que dá errado enquanto ela não tem resposta (`impact`) e quem pode resolver (`owner_to_resolve`). O estado começa em `unresolved`. Quando alguém decidir, mude `status` para `resolved` e registre em `resolution` o que foi decidido, com data e evidência. Sem perguntas em aberto, deixe `open_questions: []`.

<!-- contexto:historico -->
