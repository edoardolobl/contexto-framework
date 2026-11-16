---
id: null
title: null
type: relationship_semantics
status: draft
owner: null
source_of_truth: null
valid_from: null
---

# [Nome do relacionamento]

## Pergunta de negócio
- Por que precisamos associar estes datasets?
- Quando a relação não deve ser utilizada?

## Tabelas e granularidade
- Tabela A e o que uma linha representa:
- Tabela B e o que uma linha representa:
- Chave A e significado:
- Chave B e significado:

## Cardinalidade e cobertura
- Cardinalidade esperada: 1:1, 1:N ou N:N?
- Chaves órfãs ou nulas são esperadas?
- Uma junção pode multiplicar linhas?
- Quando usar INNER, LEFT ou outro join (se isso foi validado)?

## Tempo e histórico
- Relação depende de data ou versão?
- É snapshot ou entidade historizada?
- O relacionamento é válido ao longo de todo o período?

## Limites e testes
- Exemplos de registros associados corretamente:
- Contraexemplos e joins proibidos:
- Efeito na contagem e em métricas:
- Validação realizada pelo time de dados:
- Quem aprova e dúvidas pendentes:
