---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: KPI-AURORA-002
schema_version: "1.1.0"
type: kpi
title: "Receita de purchase: pedidos por operação e dia"
version: "1.0"
revision_id: "KPI-AURORA-002@1.0" # versão específica; id = assunto estável
status: approved
owner: "Analytics de E-commerce (Aurora)"
approver: "Gerência de Analytics (Aurora)"
valid_from: "2026-10-01"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-11-17"
last_reviewed: "2026-11-17"
review_interval: null
source_of_truth: "Tabela de pedidos da Aurora, aurora-analytics.vendas.pedidos"
supersedes_revision: null
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/KPI-AURORA-002@1.0.md"
intent:
  question: "Quanto os pedidos confirmados de cada operação da Aurora geraram de receita em cada dia?"
  audience: ["Gerência de Analytics", "Analytics de E-commerce", "Quem testa agentes de IA"]
  purpose: "Dar um número único de receita de purchase e evitar a soma duplicada depois da junção com os itens"
  decisions: ["Conferir se a receita de um dia bate com a contagem de purchase da mesma operação"]
plain_summary: "Soma a receita dos pedidos confirmados, por operação e por dia, sempre na tabela de pedidos. Somar depois de juntar com os itens repete cada pedido uma vez por item: em 02/11/2026 na BR, o certo é R$ 500 e o errado é R$ 1.100."
open_questions: []
version_history:
  - version: "1.0"
    date: "2026-11-17"
    change: "Primeira versão aprovada, depois que a Analytics de E-commerce conferiu o cálculo contra a amostra do Laboratório Aurora 2"
    approved_by: "Gerência de Analytics (Aurora)"
  - version: "0.1"
    date: "2026-11-16"
    change: "Rascunho com a regra de somar na tabela de pedidos, depois que a amostra mostrou a soma duplicada"
    approved_by: null

context:
  instructions: null
  verifiedStatements: []
  constraints: []
authoritativeDefinitions:
  - type: sql
    url: aurora-lab2-receita-purchase.sql
    description: "Consulta SQL do laboratório que calcula a receita por operação e dia, sem junção"

domain: ecommerce
business_definition:
  concept: "Soma do valor (revenue) dos pedidos confirmados de uma operação em um dia"
  different_meanings_in_other_domains:
    - "Receita contábil: reconhecida pelo Financeiro, com outras regras de data; não usar como sinônimo"
    - "Receita depois da junção com os itens: soma errada, que repete o pedido uma vez por item"
synonyms: ["receita de purchase"]
scope:
  included_channels: [web]
  excluded_channels: []
  applicable_population: "Pedidos com estado CONFIRMED das operações BR e MX"
  exclusions: ["pedidos cancelados", "pedidos de teste"]
calculation:
  formula_description: "Soma de revenue dos pedidos CONFIRMED, agrupada por operação e por dia de order_date"
  numerator: "Soma de revenue dos pedidos confirmados da operação no dia"
  denominator: null
  unit: "moeda da operação (BRL na BR, MXN no MX)"
  granularity: "operação + dia de order_date no fuso da operação (America/Sao_Paulo na BR, America/Mexico_City no MX)"
  aggregation_rule: "Somar sempre na tabela de pedidos, nunca depois de juntar com os itens. Nunca somar operações diferentes: BRL e MXN não se misturam"
  null_handling: "Dia sem pedido confirmado tem receita 0"
  zero_denominator_policy: "Não se aplica: o indicador é uma soma, sem divisão"
history_recalculation:
  policy: null
  description: null
time:
  reference_date_field: order_date
  timezone: "Fuso da operação: America/Sao_Paulo na BR, America/Mexico_City no MX"
  reporting_window: "Diária"
  data_freshness: "Carga estática no laboratório; dia completo em D+2"
data_sources:
  authoritative_dataset: "aurora-analytics.vendas.pedidos"
  relevant_columns:
    - pedidos.order_id
    - pedidos.order_date
    - pedidos.operation
    - pedidos.revenue
  valid_join_paths: []
  source_conflicts_and_precedence: ["Se um dashboard mostrar valor diferente, vale o cálculo de aurora-lab2-receita-purchase.sql"]
validation:
  approved_examples: ["Exemplo: na BR em 02/11/2026, três pedidos (R$ 120, R$ 80 e R$ 300) somam R$ 500"]
  expected_questions_and_answers: ["Pergunta Q06 do gabarito dos eventos: a receita de purchase da BR em 02/11/2026 é R$ 500"]
  known_edge_cases:
    - "O pedido de R$ 300 tem 3 itens: depois da junção com os itens ele entra 3 vezes e a soma vira R$ 1.100"
    - "BR e MX usam moedas diferentes: nunca somar as duas operações"
  tests: []

related_documents: [QA-AURORA-002]

retroactive_validity:
  reason: "A receita de purchase já era somada na tabela de pedidos desde 01/10/2026; esta versão registra a regra em uso, e o primeiro dia citado no gabarito, 02/11/2026, fica dentro da vigência"
  confirmed_by: "Gerência de Analytics (Aurora)"
---

Na amostra do laboratório, o pedido P3 de 02/11/2026 na BR tem três itens. Somando a receita na tabela de pedidos, o dia fecha em R$ 500. Somando depois de juntar com os itens, o pedido de R$ 300 aparece três vezes e o dia sai com R$ 1.100.

A `lab2_pedidos` do laboratório espelha `aurora-analytics.vendas.pedidos` e guarda só pedidos CONFIRMED. A consulta `aurora-lab2-receita-purchase.sql` não usa JOIN, de propósito.

O que observar: a vigência começa em 01/10/2026, antes da data desta versão. Isso só é aceito porque é a primeira versão do indicador e `retroactive_validity` diz por que e quem confirmou.
