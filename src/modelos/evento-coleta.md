---
# Documentação do comportamento esperado de um evento; não configura nem corrige a coleta.
# null significa "ainda não sei" ou "ainda não decidido". Não troque null por um palpite: registre a dúvida em open_questions.
# Campos marcados (obrigatório) são o núcleo para sair do rascunho; os blocos "para quem é técnico" são opcionais.
id: null                     # (obrigatório) identificador do assunto, igual em todas as versões
schema_version: "1.0.0"      # versão do formato do arquivo; não mude
type: evento-coleta
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
review_interval: "P6M"       # de quanto em quanto tempo revisar, em ISO 8601; obrigatório porque context.instructions vem preenchido
source_of_truth: null        # onde está a versão oficial, como o plano de mensuração
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
  instructions: "Zero em um dia não é quebra; compare com a linha de base por operação. Sem indicador aprovado, não calcule com a definição de mercado; pergunte."
  verifiedStatements: []     # perguntas típicas; cada item: question e, se já conferida, answer
  constraints: []            # limites do agente; cada item: constraint
# Cada item: type (sql | metricView | filter | dashboard | document | other), url e description.
authoritativeDefinitions: [] # para quem é técnico: opcional. Onde mora a regra executável

trigger: null                # (a chave precisa existir) ação que faz o evento disparar
parameters: []               # cada item: name, meaning, example, required
destination: []              # (a chave precisa existir) cada item: platform, object, timezone, note
active_scopes: []            # (a chave precisa existir) cada item: operation, country, brand, active, since, reason
expected_behavior:
  expected_frequency: null   # ritmo normal, em palavras
  baseline_by_scope: []      # cada item: operation, window, typical_daily, zero_days_share, longest_zero_run
  seasonality: null
  silence_tolerance: []      # cada item: operation, rule; escolha do time, não regra universal
  expected_zero_conditions: [] # situações em que um dia em zero é normal
launch_date: null            # primeiro dia em produção, AAAA-MM-DD
retirement_date: null        # primeiro dia sem o evento, AAAA-MM-DD
renamed_from: []             # cada item: name, valid_from, valid_to
consent_requirements: null
late_arrival_window: null    # até quando o dia ainda recebe disparos atrasados
deduplication_key: null
downstream_kpis: []          # identificadores dos indicadores que usam o evento
known_exceptions: []         # cada item: condition, period, evidence
validation_query: null       # para quem é técnico: consulta que recalcula a contagem diária por operação
missing_days_policy: null    # o que significa um dia sem linha na tabela
grain_note: null             # o que uma linha da tabela diária representa
data_incidents: []           # cada item: start, end, description, effect_on_baseline, status
disambiguation: []           # cada item: term, means, not_to_confuse_with

related_documents: []        # identificadores de outros documentos
---

# [Nome do evento]

> **Como usar este modelo.** Os campos ficam no topo do arquivo, entre as duas linhas `---`. Responda só o que você sabe e consegue comprovar. O que não souber, deixe como `null` e anote em `open_questions`, com quem pode responder. Um campo em branco é melhor do que um palpite. Os campos marcados com **(obrigatório)** são o mínimo para sair do rascunho; os blocos marcados "para quem é técnico" são opcionais.

<!-- contexto:identificacao -->

## Para que serve
Em `intent`, escreva a pergunta de negócio que o documento responde (`question`), como alguém da área faria. Diga quem usa (`audience`), para quê (`purpose`) e quais decisões mudam conforme a resposta (`decisions`). Em `plain_summary`, explique em uma ou duas frases o que o evento conta e quando o silêncio dele é normal.

## Onde e quando dispara
Em `trigger`, descreva a ação que faz o evento disparar. Em `parameters`, as informações que seguem com cada disparo. Em `destination`, cada lugar onde os disparos ficam, com o fuso de cada um. Em `active_scopes`, uma linha por operação, país e marca, dizendo se o evento está ativo ali, desde quando e por quê. As três chaves `trigger`, `destination` e `active_scopes` precisam existir, mesmo vazias no rascunho. Registre também `launch_date`, `retirement_date` e, se o evento mudou de nome, `renamed_from`.

## Comportamento esperado
Em `expected_behavior`, diga o ritmo normal do evento (`expected_frequency`) e, para cada operação, a linha de base calculada sobre dias completos (`baseline_by_scope`): a janela, o volume típico por dia, quantos dias ficaram em zero e a maior sequência em zero. Em `silence_tolerance`, escreva a partir de quantos dias seguidos em zero o time passa a suspeitar. Esse número é escolha do time, não regra universal. Em `seasonality`, o que muda o volume de forma conhecida.

## Quando zero é normal
Em `expected_zero_conditions`, liste as situações em que um dia sem disparo não indica problema. Em `missing_days_policy`, diga o que significa um dia sem linha na tabela. Em `grain_note`, o que uma linha representa. Em `late_arrival_window`, até quando um dia ainda recebe dados atrasados; antes disso, o dia não está completo e não entra na conta. Em `known_exceptions`, os períodos já explicados, com a evidência, e em `data_incidents`, os problemas já investigados e o efeito deles na linha de base.

## Para quem é técnico (opcional)
`validation_query` guarda a consulta que recalcula a contagem diária por operação na fonte oficial. `deduplication_key` diz como reconhecer o mesmo disparo repetido, e `consent_requirements`, que autorização da pessoa o disparo exige. Em `downstream_kpis`, liste os indicadores que dependem do evento, e em `disambiguation`, os nomes parecidos que contam outra coisa.

`authoritativeDefinitions` aponta onde mora a regra executável, como o plano de mensuração ou a consulta oficial, sem copiar o código para o documento. Cada item tem `type` (`sql`, `metricView`, `filter`, `dashboard`, `document` ou `other`), `url` e `description`.

`context` segue o bloco de mesmo nome do ODCS 3.2.0. O modelo já traz em `instructions` as duas regras que valem para todo evento; por isso `review_interval` vem preenchido. `verifiedStatements` guarda as perguntas típicas do assunto, com a resposta quando quem aprova já conferiu. `constraints` guarda os limites que um agente de IA não pode ultrapassar, um por item, em `constraint`.

## Versões e vigência
A cada mudança, suba `version` e acrescente uma entrada no topo de `version_history`, com a data, o que mudou e por quê, e quem aprovou. Recalcular a linha de base com mais dias, sem mudar nenhum resultado, é versão menor; mudar a tolerância ao silêncio, que muda quando o time investiga, é versão maior. `version_date` é a data desta versão; `valid_from` e `valid_to` dizem quando o documento vale. Guarde a cópia completa de cada versão aprovada.

Em `last_reviewed`, registre a data da última revisão completa, e em `review_interval`, de quanto em quanto tempo revisar.

## Perguntas em aberto
Acrescente um item em `open_questions` para cada pergunta que ninguém decidiu, como "zero nesta operação é falha ou o evento não existe lá?". Escreva a pergunta (`question`), o que dá errado enquanto ela não tem resposta (`impact`) e quem pode resolver (`owner_to_resolve`). O estado começa em `unresolved`. Quando alguém decidir, mude `status` para `resolved` e registre em `resolution` o que foi decidido, com data e evidência. Sem perguntas em aberto, deixe `open_questions: []`.

<!-- contexto:historico -->
