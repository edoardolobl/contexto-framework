# Perguntas em aberto propostas a partir dos erros do experimento

Relatório para revisão humana. Este script não altera nenhum documento. Uma proposta só entra num documento depois que o responsável por ele a revisa, e um documento aprovado só muda numa versão nova.

- Resultados: docs/experimentos/onboarding-resultados.json
- Condições: B
- Comando: `python3 scripts/erros_para_perguntas.py docs/experimentos/onboarding-resultados.json --mapa QA1=QA-AURORA-001 --mapa QA2=QA-AURORA-002 --condicao B`
- Execuções: 48
- Erros: 11

## Propostas

### QA-AURORA-001@1.1 Q03

- Pergunta: Qual foi a conversão em 2026-10-01?
- Comportamento esperado: pedir esclarecimento
- Errou em 3 de 6 execuções
- Categorias observadas: responder: 3
- Modelos: Claude Sonnet 5.5 (claude-sonnet-5-5): 3

Alvo: KPI-AURORA-001@2.0

```yaml
open_questions:
- question: A IA errou a Q03 do QA-AURORA-001@1.1 ("QA1-Q03") em 3 de 6 execuções. O que falta em KPI-AURORA-001@2.0 para a resposta esperada sair, ou o gabarito precisa mudar?
  impact: 'Resposta esperada: Falta o canal, e conversão pode significar sessões ou pedidos. Categorias observadas: responder (3).'
  owner_to_resolve: Analytics de E-commerce (Aurora)
  status: unresolved
  resolution: null
```

### QA-AURORA-002@1.0 Q03

- Pergunta: O generate_lead está quebrado?
- Comportamento esperado: pedir esclarecimento
- Errou em 2 de 6 execuções
- Categorias observadas: responder: 2
- Modelos: Claude Opus 5.5 (claude-opus-5-5): 2

Alvo: EVENT-AURORA-GENERATE-LEAD@1.1

```yaml
open_questions:
- question: A IA errou a Q03 do QA-AURORA-002@1.0 ("QA2-Q03") em 2 de 6 execuções. O que falta em EVENT-AURORA-GENERATE-LEAD@1.1 para a resposta esperada sair, ou o gabarito precisa mudar?
  impact: 'Resposta esperada: Falta a operação: o resultado muda entre Brasil e México. Categorias observadas: responder (2).'
  owner_to_resolve: Analytics de E-commerce (Aurora)
  status: unresolved
  resolution: null
```

### QA-AURORA-002@1.0 Q06

- Pergunta: Qual foi a receita de purchase no Brasil em 02/11/2026?
- Comportamento esperado: responder
- Errou em 6 de 6 execuções
- Categorias observadas: pedir esclarecimento: 6
- Modelos: Claude Opus 5.5 (claude-opus-5-5): 3, Claude Sonnet 5.5 (claude-sonnet-5-5): 3

Alvo: QA-AURORA-002@1.0

```yaml
open_questions:
- question: A IA errou a Q06 do QA-AURORA-002@1.0 ("QA2-Q06") em 6 de 6 execuções. O que falta em QA-AURORA-002@1.0 para a resposta esperada sair, ou o gabarito precisa mudar?
  impact: 'Resposta esperada: R$ 500, somando os 3 pedidos (R$ 120, R$ 80 e R$ 300) na tabela de pedidos. Somar depois de juntar com os itens dá R$ 1.100, valor errado: o pedido de R$ 300 tem 3 itens e entra 3 vezes. Categorias observadas: pedir esclarecimento (6).'
  owner_to_resolve: Analytics de E-commerce (Aurora)
  status: unresolved
  resolution: null
```
