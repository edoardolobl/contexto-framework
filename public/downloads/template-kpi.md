---
# MODELO DE DOCUMENTAÇÃO SEMÂNTICA DE KPI
# null significa "ainda não sei" ou "ainda não decidido". Não troque null por um palpite: registre a dúvida em open_questions.
# Exemplos e nomes de campos são convenções propostas, não um padrão universal.
# Não preencha informações desconhecidas com suposições. Use null + open_questions.
# Campos marcados (obrigatório) são o núcleo para sair do rascunho; os blocos "para quem é técnico" são opcionais.
id: null                     # (obrigatório) identificador do assunto, igual em todas as versões
schema_version: "1.0.0"      # versão do formato do arquivo; não mude
type: kpi
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

domain: null
business_definition:
  concept: null
  different_meanings_in_other_domains: []
synonyms: []                 # nomes que querem dizer exatamente a mesma coisa
scope:
  included_channels: []
  excluded_channels: []
  applicable_population: null
  exclusions: []
calculation:
  formula_description: null
  numerator: null
  denominator: null
  unit: null
  granularity: null
  aggregation_rule: null
  null_handling: null
  zero_denominator_policy: null
history_recalculation:       # obrigatório quando a versão maior muda (2.0, 3.0)
  policy: null               # recalculate | method_break
  description: null
time:
  reference_date_field: null
  timezone: null
  reporting_window: null
  data_freshness: null
data_sources:
  authoritative_dataset: null
  relevant_columns: []
  valid_join_paths: []
  source_conflicts_and_precedence: []
validation:
  approved_examples: []
  expected_questions_and_answers: []
  known_edge_cases: []
  tests: []

related_documents: []        # identificadores de outros documentos
---

# [Nome do indicador e contexto]

> **Como usar este modelo.** Os campos ficam no topo do arquivo, entre as duas linhas `---`. Responda só o que você sabe e consegue comprovar. O que não souber, deixe como `null` e anote em `open_questions`, com quem pode responder. Um campo em branco é melhor do que um palpite. Os campos marcados com **(obrigatório)** são o mínimo para sair do rascunho; os blocos marcados "para quem é técnico" são opcionais.

## Identificação

Preencha estes campos no topo do arquivo antes de escrever o resto.

| Campo | Chave no topo do arquivo | Obrigatório | O que escrever |
|---|---|---|---|
| Identificador do assunto | `id` | Sim | Código estável do assunto, igual em todas as versões, em maiúsculas com hífens (por exemplo KPI-AURORA-001). Não muda quando a regra muda. |
| Versão do formato | `schema_version` |  | Versão do formato do arquivo, hoje 1.0.0. Diz quais campos o arquivo tem e não muda quando o conteúdo muda. |
| Tipo de documento | `type` |  | Tipo de documento, igual ao nome do modelo (kpi, dataset, conceito e outros). Define quais campos vêm depois do cabeçalho. |
| Título | `title` | Sim | Nome que uma pessoa da área reconhece, com o assunto e a organização. Pode mudar entre versões sem mudar o identificador. |
| Versão atual | `version` | Sim | Número desta versão no formato MAIOR.MENOR (1.0, 1.1, 2.0). Suba o número maior quando a regra muda de sentido e o menor quando só esclarece. |
| Identificador desta versão | `revision_id` |  | Identificador e versão juntos, no formato id@versão (KPI-AURORA-001@2.0). É o que outro documento cita para apontar exatamente esta versão. |
| Estado | `status` | Sim | Um de cinco valores, draft (rascunho), pending_approval (pendente de aprovação), approved (aprovado), superseded (substituído) ou deprecated (obsoleto). Só use approved depois da confirmação por escrito de quem aprova. |
| Responsável (cargo ou área) | `owner` | Sim | Cargo ou área que mantém o documento e responde às dúvidas, nunca o nome de uma pessoa. |
| Quem aprova (cargo ou área) | `approver` | Sim | Cargo ou área com a palavra final sobre a regra. Pode ser diferente do responsável. |
| Vale a partir de | `valid_from` |  | Primeiro dia em que a regra vale, no formato AAAA-MM-DD. Pode ser depois da data desta versão; em rascunho, fica em branco. |
| Primeiro dia em que já não vale | `valid_to` |  | Dia em que a vigência acaba, sem contar esse dia. Em branco quando não há fim previsto. |
| Data em que esta versão foi registrada | `recorded_at` |  | Só na cópia de uma versão substituída. Guarda o dia do registro, para responder o que se sabia naquela data. |
| Data desta versão | `version_date` | Sim | Dia em que esta versão foi escrita ou aprovada, no formato AAAA-MM-DD. Não é o início da vigência. |
| Última revisão | `last_reviewed` |  | Último dia em que alguém conferiu o documento inteiro, mesmo sem mudar nada. Em branco se ninguém revisou ainda. |
| De quanto em quanto tempo revisar | `review_interval` |  | Prazo entre revisões em ISO 8601 (P6M são seis meses, P1Y um ano). Obrigatório quando há instrução ao agente em context.instructions. |
| Fonte oficial | `source_of_truth` |  | Sistema, documento ou tabela que vale quando duas fontes discordam. Fica em branco enquanto ninguém confirmou qual é. |
| Substitui qual versão? | `supersedes_revision` |  | Versão anterior do mesmo assunto que esta substitui, no formato id@versão. Em branco na primeira versão. |
| Substituída por qual versão? | `superseded_by_revision` |  | Só na cópia de uma versão substituída, aponta a versão que tomou o lugar dela. Em documento aprovado e em vigor, fica em branco. |
| Pergunta de negócio que o documento responde | `intent.question` | Sim | A pergunta escrita como alguém da área faria. Sem ela, o documento não sai do rascunho, porque ninguém sabe o que ele precisa responder. |
| Quem usa | `intent.audience` |  | Cargos ou áreas que leem e usam o documento. Ajuda a escolher o nível de detalhe e quem precisa saber de cada mudança. |
| Para quê | `intent.purpose` |  | Para que o documento existe, em uma frase, dizendo o problema que ele evita. |
| Decisões que apoia | `intent.decisions` |  | Decisões que mudam conforme a resposta. Se nenhuma decisão depende do documento, vale perguntar se ele é necessário. |
| Em poucas palavras | `plain_summary` |  | Uma ou duas frases em linguagem direta, ao lado da definição formal (por exemplo, conta só pedidos pagos até sete dias depois do contato). Não substitui os campos do tipo. |
| Perguntas em aberto | `open_questions` |  | Uma entrada por pergunta que ninguém decidiu, com o impacto, quem pode resolver, o estado e a resolução. Uma dúvida registrada vale mais do que um palpite. |
| Histórico de versões | `version_history` |  | Uma entrada por versão, a mais recente primeiro, com data, o que mudou na regra e quem aprovou. O resumo não substitui a cópia completa de cada versão aprovada. |

## Para que serve
Em `intent`, escreva a pergunta de negócio que o documento responde (`question`), como alguém da área faria. Diga quem usa (`audience`), para quê (`purpose`) e quais decisões mudam conforme a resposta (`decisions`). Em `plain_summary`, explique em uma ou duas frases, sem termos técnicos, o que o documento diz, por exemplo "conta só pedidos pagos até sete dias depois do contato".

## Definição de negócio
Em `domain`, diga a área do negócio. Em `business_definition.concept`, diga o que o indicador mede. Em `synonyms`, liste nomes que querem dizer exatamente a mesma coisa; em `business_definition.different_meanings_in_other_domains`, os nomes parecidos que medem outra coisa em outra área.

## Escopo e aplicabilidade
Em `scope`, liste os canais incluídos e excluídos, a população a que o indicador se aplica e as exclusões, como tráfego interno ou pedidos de teste. Se há situação em que a definição não deve ser usada, escreva em `exclusions`.

## Cálculo
Em `calculation`, descreva o numerador e o denominador com os critérios de cada um, a fórmula em palavras, a unidade, a granularidade e a regra para juntar períodos. Diga também como tratar ausência de dados e o que mostrar quando o denominador é zero. Diga a unidade antes da fórmula: pedidos, sessões, clientes ou itens.

## Recálculo do histórico
Quando a versão maior muda (2.0, 3.0), `history_recalculation.policy` é obrigatório: `recalculate` se a série antiga for recalculada pela regra nova, `method_break` se a série antiga fica como estava e passa a ser marcada como quebra de método. Em `description`, explique em uma frase o que isso muda para quem compara períodos.

## Convenções temporais
Em `time`, diga qual campo de data decide o dia de cada registro, o fuso horário, a janela de cálculo e de quanto em quanto tempo os dados são atualizados.

## Fontes e semântica dos dados
Em `data_sources`, diga qual dataset manda quando há divergência, as colunas usadas, as junções autorizadas (pelo identificador do documento de relacionamento) e a regra de precedência entre fontes.

## Exceções e exemplos
Em `validation`, registre exemplos aprovados de interpretação, perguntas que o documento deve permitir responder, casos-limite com o tratamento de cada um e testes, se houver.

## Para quem é técnico (opcional)
`authoritativeDefinitions` aponta onde mora a regra executável, como a consulta SQL que calcula o indicador ou a metric view do catálogo, sem copiar o código para o documento. Cada item tem `type` (`sql`, `metricView`, `filter`, `dashboard`, `document` ou `other`), `url` e `description`.

`context` segue o bloco de mesmo nome do ODCS 3.2.0. Em `instructions`, escreva só o que não cabe em nenhum campo estruturado, em até 500 caracteres; com instrução preenchida, `review_interval` passa a ser obrigatório. `verifiedStatements` guarda as perguntas típicas do assunto: cada item tem a pergunta (`question`) e, quando quem aprova já conferiu, a resposta (`answer`). `constraints` guarda os limites que um agente de IA não pode ultrapassar, um por item, em `constraint`.

## Versões e vigência
A cada mudança na regra, suba `version` e acrescente uma entrada no topo de `version_history`, com a data, o que mudou e por quê, e quem aprovou. Registre a mudança na regra, não só a edição do texto. `version_date` é a data desta versão; `valid_from` e `valid_to` dizem quando a regra vale. Guarde a cópia completa de cada versão aprovada: o histórico sozinho não permite reconstruir a regra anterior. Quando outra versão tomar o lugar desta, a cópia guardada passa a `status: superseded`, com `superseded_by_revision` e `recorded_at`.

Em `last_reviewed`, registre a data da última revisão completa, e em `review_interval`, de quanto em quanto tempo revisar.

## Perguntas em aberto
Acrescente um item em `open_questions` para cada pergunta que ninguém decidiu. Escreva a pergunta (`question`), o que dá errado enquanto ela não tem resposta (`impact`) e quem pode resolver (`owner_to_resolve`). O estado começa em `unresolved`. Quando alguém decidir, mude `status` para `resolved` e registre em `resolution` o que foi decidido, com data e evidência. Sem perguntas em aberto, deixe `open_questions: []`.

## Histórico de versões

| Versão | Data | O que mudou e por quê | Aprovado por (cargo ou área) |
|---|---|---|---|
| 0.1 |  |  |  |
