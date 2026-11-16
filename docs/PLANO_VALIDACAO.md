# Plano de validação com leitores — proposta para após v0.3

**Estado:** planejamento, não teste já realizado.

## Pergunta principal

O framework realmente permite que uma pessoa **experiente no assunto, mas sem familiaridade com engenharia de IA**, produza documentação mais explícita e saiba reconhecer o que ainda precisa ser decidido?

A avaliação tem que observar isso, não a capacidade de um LLM de executar SQL.

## Participantes recomendados

- Uma ou duas pessoas sem experiência em programação, mas que conheçam um processo;
- Uma ou duas pessoas analistas de Dados/BI;
- Uma pessoa de engenharia responsável por consumir documentação.

Essas quantidades são um **ponto de partida exploratório**, não uma recomendação estatística para estimar resultado populacional.

## Roteiro

### Cenário A — Regras e processos

1. Fornecer um processo fictício com termos ambíguos.
2. Pedir à pessoa participante que encontre o template apropriado sem orientação.
3. Solicitar que identifique gatilho, atores, decisões, exceções e fontes.
4. Pedir que registre pelo menos duas lacunas sem inventar respostas.
5. Verificar se ela distingue “pendente de aprovação” de “aprovado”.

### Cenário B — Analítica de dados

1. Apresentar os dados fictícios da Aurora.
2. Solicitar a definição de “sessões convertidas”.
3. Mostrar o cálculo 50% (pedidos confirmados por sessão) e perguntar se satisfaz a métrica.
4. Observar se a pessoa identifica cardinalidade e diferença de unidade.
5. Pedir que complete o template de KPI com fontes e pendências.

### Cenário C — Rubrica

1. Apresentar a frase “avaliar a qualidade da análise”.
2. Pedir critérios observáveis e exemplos de nível 2 versus nível 4.
3. Perguntar o que fazer quando não há evidência suficiente.
4. Verificar se ela evita concluir automaticamente o resultado da avaliação.

## O que coletar

- Se a pessoa encontrou o template sem assistência;
- Quais lacunas identificou e quais passaram despercebidas;
- Se anotou informações desconhecidas sem presumir respostas;
- Se distinguiu o exemplo fictício de uma regra oficial;
- Quais instruções eram incompreensíveis ou desnecessariamente técnicas;
- Onde o documento final precisaria de revisão por especialista;
- Comentários livres dos participantes.

## Critério de êxito

Não existe uma nota pré-definida nesta edição. Registre erros, dúvidas e melhorias por tarefa. A revisão editorial deve responder **qual lacuna pedagógica precisa ser corrigida**, e não apenas reunir elogios.

## Limites

Este plano não testa eficiência de RAG, confiabilidade de agentes, aderência normativa nem resultados de avaliações de emprego. Se algum material de usuário real for utilizado num teste, deve ser tratado segundo as permissões e políticas aplicáveis.
