---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: EVENT-AURORA-GENERATE-LEAD
schema_version: "1.1.0"
type: evento-coleta
title: "Evento generate_lead: Aurora"
version: "1.1"
revision_id: "EVENT-AURORA-GENERATE-LEAD@1.1" # versão específica; id = assunto estável
status: approved
owner: "Analytics de E-commerce (Aurora)"
approver: "Gerência de Analytics (Aurora)"
valid_from: "2026-11-17"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-11-17"
last_reviewed: "2026-11-17"
review_interval: "P6M"
source_of_truth: "Plano de mensuração da Aurora, linha generate_lead"
supersedes_revision: "EVENT-AURORA-GENERATE-LEAD@1.0"
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/EVENT-AURORA-GENERATE-LEAD@1.1.md"
intent:
  question: "Quando um dia sem generate_lead deve ser tratado como falha de coleta?"
  audience: ["Analytics de E-commerce", "Engenharia de Dados", "Vendas de Atacado"]
  purpose: "Evitar que um dia em zero seja lido como evento quebrado sem comparar com o normal da operação"
  decisions: ["Abrir ou não uma investigação de coleta para generate_lead"]
plain_summary: "O evento conta os cadastros de atacado enviados no site do Brasil, cerca de um por dia, com muitos dias em zero. No México ele não existe, então zero lá é o esperado; no Brasil, só 4 dias completos seguidos em zero levantam suspeita."
open_questions: []
version_history:
  - version: "1.1"
    date: "2026-11-17"
    change: "Linha de base da BR recalculada com os 27 dias completos de 20/10 a 15/11/2026; a tolerância ao silêncio não mudou, então nenhum resultado muda"
    approved_by: "Gerência de Analytics (Aurora)"
  - version: "1.0"
    date: "2026-10-13"
    change: "Primeira versão aprovada: México fora do escopo, prazo D+2 para o dia ficar completo e tolerância de 4 dias completos seguidos em zero na BR, com linha de base de 08/09 a 05/10/2026 sem os dias da manutenção"
    approved_by: "Gerência de Analytics (Aurora)"
  - version: "0.1"
    date: "2026-10-06"
    change: "Primeiro rascunho, com gatilho e destino; comportamento esperado ainda em aberto"
    approved_by: null

context:
  instructions: "Zero em um dia não é quebra; compare com a linha de base por operação. Sem indicador aprovado, não calcule com a definição de mercado; pergunte."
  verifiedStatements:
    - question: "Generate_lead está quebrado no México?"
      answer: "Não. O evento não está ativo no México; falta de linha ou zero lá é o esperado."
  constraints:
    - constraint: "Não somar BR e MX para comparar com a linha de base: ela é sempre por operação."
authoritativeDefinitions: []

trigger: "Envio com sucesso do formulário de cadastro de atacado no site da Aurora, depois da confirmação do servidor"
parameters:
  - name: lead_source
    meaning: "Página ou campanha de onde a pessoa chegou ao formulário"
    example: "pagina_atacado"
    required: true
  - name: value
    meaning: "Pedido mínimo de atacado informado no formulário, usado só como estimativa"
    example: 1500
    required: false
  - name: currency
    meaning: "Moeda do campo value, em código ISO 4217"
    example: "BRL"
    required: false
  - name: submission_id
    meaning: "Código único gerado a cada envio, para reconhecer disparo repetido"
    example: "f-20261103-0042"
    required: true
destination:
  - platform: "GA4"
    object: "Propriedade Aurora BR, com export diário para o BigQuery no dataset analytics_312345678 do projeto aurora-analytics"
    timezone: "America/Sao_Paulo"
    note: "As tabelas intraday do export ainda recebem dados e não contam como dia completo"
  - platform: "Databricks"
    object: "aurora_prod.tracking.eventos_diarios"
    timezone: "O da operação, America/Sao_Paulo na BR"
    note: "Uma linha por dia, operação e evento, só quando houve disparo; é a fonte da linha de base"
  - platform: "Google Tag Manager"
    object: "Contêiner GTM-AURBR01"
    timezone: "Não se aplica, porque guarda só a configuração"
    note: "Cada publicação de versão fica registrada com data e hora; é o primeiro lugar a cruzar com o início de um silêncio"
active_scopes:
  - operation: BR
    country: Brasil
    brand: Aurora
    active: true
    since: "2026-08-03"
    reason: "Formulário de atacado publicado no site do Brasil na data de lançamento"
  - operation: MX
    country: México
    brand: Aurora
    active: false
    since: null
    reason: "O site do México não tem formulário de atacado; zero ou falta de linha lá é o esperado"
expected_behavior:
  expected_frequency: "Poucos envios por dia no Brasil, com dias inteiros em zero espalhados pela semana"
  baseline_by_scope:
    - operation: BR
      window: "20/10 a 15/11/2026, 27 dias completos"
      typical_daily: "média de 1,1 por dia"
      zero_days_share: "zero em 9 de 27 dias completos"
      longest_zero_run: "maior sequência em zero: 3 dias"
  seasonality: "Sem diferença clara entre dia útil e fim de semana na janela da linha de base; o volume sobe na semana em que sai o catálogo de atacado"
  silence_tolerance:
    - operation: BR
      rule: "Suspeitar a partir de 4 dias completos seguidos em zero. Escolha da Gerência de Analytics, não regra universal"
    - operation: MX
      rule: "Não se aplica: o evento não está ativo no México"
  expected_zero_conditions:
    - "Até 3 dias completos seguidos em zero no Brasil, como de 27 a 29/10/2026"
    - "Qualquer dia no México, onde o evento não existe"
    - "Qualquer dia antes de 03/08/2026, data de lançamento"
    - "Dias da manutenção programada registrada em known_exceptions"
launch_date: "2026-08-03"
retirement_date: null
renamed_from: []
consent_requirements: "Dispara só com analytics_storage concedido no modo de consentimento; quem recusa não entra na contagem, por isso o GA4 mostra menos cadastros que o sistema de vendas"
late_arrival_window: "D+2 às 06h no fuso da operação: o dia 15/11 só fica completo em 17/11 às 06h"
deduplication_key: "submission_id: dois disparos com o mesmo valor contam como um"
downstream_kpis:
  - "Taxa de cadastro de atacado: ainda sem indicador aprovado na Aurora"
known_exceptions:
  - condition: "Manutenção programada do formulário de atacado"
    period: "22/09/2026 a 24/09/2026"
    evidence: "Chamado de manutenção aprovado pela Gerência de Analytics, com início e fim"
validation_query: |
  SELECT operation, event_date, SUM(event_count) AS disparos
  FROM aurora_prod.tracking.eventos_diarios
  WHERE event_name = 'generate_lead'
    AND event_date BETWEEN '2026-10-20' AND '2026-11-15'
  GROUP BY operation, event_date
  ORDER BY operation, event_date
missing_days_policy: "A tabela diária só grava linha quando há pelo menos 1 disparo; falta de linha é zero, e dia incompleto não entra na conta"
grain_note: "Uma linha é um evento, uma operação e um dia no fuso da operação; não some linhas de operações diferentes para comparar com a linha de base"
data_incidents:
  - start: "2026-08-18"
    end: "2026-08-19"
    description: "Disparo em dobro depois da publicação da versão 12 do contêiner GTM-AURBR01: a tag do formulário ficou ligada a dois acionadores"
    effect_on_baseline: "Os dois dias ficam fora de toda linha de base"
    status: "Corrigido em 20/08/2026 com a versão 13 do contêiner"
disambiguation:
  - term: "generate_lead"
    means: "Cadastro de atacado enviado com sucesso"
    not_to_confuse_with: "sign_up da newsletter, que registra a inscrição para receber e-mails e não é lead de atacado"

related_documents: [DECISION-AURORA-EVENTO-QUEBRADO]
---

# Evento generate_lead: Aurora (EVENT-AURORA-GENERATE-LEAD@1.1)

> **Estado:** Aprovado
>
> **Vigência:** de 17/11/2026, sem fim previsto
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/EVENT-AURORA-GENERATE-LEAD@1.1.md

## Pergunta que este documento responde (EVENT-AURORA-GENERATE-LEAD@1.1, de 17/11/2026, sem fim previsto)

Quando um dia sem generate_lead deve ser tratado como falha de coleta?

## Em poucas palavras (EVENT-AURORA-GENERATE-LEAD@1.1, de 17/11/2026, sem fim previsto)

O evento conta os cadastros de atacado enviados no site do Brasil, cerca de um por dia, com muitos dias em zero. No México ele não existe, então zero lá é o esperado; no Brasil, só 4 dias completos seguidos em zero levantam suspeita.

## Comentário (EVENT-AURORA-GENERATE-LEAD@1.1, de 17/11/2026, sem fim previsto)

A versão 1.1 recalculou a linha de base da BR com os 27 dias completos de 20/10 a 15/11/2026; a tolerância de 4 dias não mudou, então nenhum resultado muda. A versão 1.0 já tinha tirado o México do escopo, o que explica a falta de linhas de lá.

O que observar: dois dias seguidos em zero no Brasil cabem no normal, porque a linha de base já teve uma sequência de 3; e nenhum indicador aprovado depende do evento, por isso o agente pergunta antes de calcular taxa de cadastro.
