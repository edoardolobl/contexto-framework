# 0021. Responder, esclarecer ou abster-se

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decidido por:** mantenedor (texto proposto pela auditoria (F1); aceito pelo [ADR 0030](./0030-decisoes-do-mantenedor-depois-das-fases.md))
- **Origem:** [07-metodo-e-credibilidade.md](../../auditoria/07-metodo-e-credibilidade.md), MET-15; linha 62 de [referencias/index.mdx](../../src/content/docs/referencias/index.mdx)

## Contexto

A página de referências atribui a separação entre responder, esclarecer e abster-se a "Microsoft RAG, princípios de evidência". A página de avaliação de recuperação da Microsoft fala de testar casos positivos e negativos. A seção "Unaddressed queries", da preparação de RAG, sustenta a abstenção. Nenhuma delas trata de pedir esclarecimento (MET-15). A atribuição precisa ser corrigida e a decisão precisa de registro próprio.

## Decisão

Um sistema que consulta a documentação tem três saídas, e o portal as trata como distintas:

- **Responder:** há definição aprovada que cobre a pergunta, dentro do período de vigência e do escopo. A resposta cita o documento e a versão.
- **Esclarecer:** a pergunta é ambígua, porque falta unidade, período, recorte ou comparação. A saída é uma pergunta de volta, com as definições existentes como opções.
- **Abster-se:** não há cobertura, porque não existe definição, a pergunta está fora da vigência ou do escopo, ou só há rascunho. A saída diz que não há resposta aprovada e aponta a lacuna e quem pode resolvê-la.

Rascunho e documento pendente de aprovação não geram resposta como definição oficial.

A abstenção tem apoio na Microsoft (seção "Unaddressed queries"). Pedir esclarecimento é convenção do Contexto.

## Alternativas consideradas

- **Alternativa A:** responder sempre com a melhor inferência. Não foi escolhida: ensina a inventar regra, contra a regra 5 do contrato editorial.
- **Alternativa B:** juntar esclarecer e abster-se numa saída só. Não foi escolhida: perde a ação de pedir uma escolha a quem pergunta, que muitas perguntas exigem.
- **Alternativa C:** tratar a abstenção como falha do sistema. Não foi escolhida: esconde a lacuna que o documento deveria registrar.

## Consequências

- **Positivas:** a lacuna aparece como resultado, e a pergunta de volta mostra as definições existentes.
- **Negativas:** o portal não testa agentes. A decisão só se verifica num sistema que a implemente, e o usuário ganha perguntas de volta.
- **Fases afetadas:** F1 corrige a atribuição. F5 inclui perguntas de referência para casos de abstenção. F6 leva a distinção ao kit mínimo para agentes.
- **Breaking:** nenhum.
