# Pontuação

- **Estado:** aguarda execução
- **Data:** 2026-11-17
- **Origem:** o protocolo de onboarding de [docs/experimentos/onboarding.md](../experimentos/onboarding.md), com a mesma rubrica do [ADR 0021](../adr/0021-responder-esclarecer-ou-abster-se.md)

## O que é pontuado

Cada texto escrito pela pessoa, nos três momentos (antes, depois e transferência), vai para a IA sozinho. A linha de base, só com os dados, também é pontuada. A pergunta é a do gabarito. O indicador principal responde a uma pergunta: 'a definição escrita pela pessoa fez a IA acertar o gabarito?'

## Entrada da IA

- **Caso 1:** o texto escrito, mais o banco do caso 1 descrito em [docs/experimentos/caso-1.md](../experimentos/caso-1.md), com o mesmo schema.
- **Caso 2:** o texto escrito, mais o arquivo `public/downloads/aurora-fixture.sql`.
- **Transferência:** o texto escrito, mais as tabelas `lab2_pedidos` (pedido, data, operação e receita) e `lab2_itens` (item, pedido e SKU) de `public/downloads/aurora-lab2-fixture.sql`. O arquivo do caso 2 não serve aqui, porque não tem valor de pedido.
- **Linha de base sem texto:** só os dados de cada caso, sem nenhum texto escrito. Roda uma vez antes da primeira sessão, com as mesmas perguntas, o mesmo prompt e as mesmas três execuções.
- A IA não recebe gabarito, consulta de referência, nem documento aprovado da Aurora. Nenhum desses materiais entra na sessão de pontuação.

## Prompt literal

Use este prompt em todas as execuções. Só muda o texto entre aspas, que é a pergunta do gabarito. O texto escrito pela pessoa entra como o documento que a IA tem à disposição, anexado antes do prompt.

> Hoje é 17/11/2026. Responda à pergunta a seguir com o que você tem à disposição. Se a resposta depender de uma escolha que só quem pergunta pode fazer, pergunte antes de calcular. Se não houver base para responder, diga que não há base. Pergunta: "{pergunta}"

A data fica fixa em 17/11/2026, como no protocolo, para que o gabarito continue valendo. Não troque a data pela data da sessão.

## Execuções

- Três execuções por texto, cada uma em sessão nova.
- O texto acerta a pergunta quando acerta em pelo menos 2 das 3 execuções.
- Registre a ferramenta, o modelo com nome e versão, a data e o número da execução.

## Rubrica

Cada execução recebe dois itens, e cada item vale sim ou não. Quem pontua é o avaliador.

1. **Categoria certa:** a resposta é da categoria esperada, como define o ADR 0021. Responder, esclarecer e abster-se são categorias diferentes. Responder quando deveria pedir esclarecimento, ou o contrário, conta como erro.
2. **Conclusão certa:** para responder, a conclusão principal bate com a resposta esperada, sem contradição; uma explicação extra não derruba o item. Para pedir esclarecimento, a resposta pede a informação que falta. Para abster-se, a resposta dá o motivo esperado.

Uma execução acerta quando os dois itens são sim.

## Perguntas pontuadas

| Caso | Gabarito | Pergunta | Papel | Categoria esperada | Conclusão esperada |
|---|---|---|---|---|---|
| Caso 1 | QA-AURORA-002@1.0, Q01 | Quais eventos do plano de mensuração pararam de coletar, considerando os dias completos até 15/11/2026? | Apoio | Responder | Só o add_to_cart no México parou. O generate_lead no Brasil está em sequência normal, e não se avalia no México |
| Caso 1 | QA-AURORA-002@1.0, Q02 | O generate_lead parou no Brasil? | Principal (proposta) | Responder | Não: 2 dias em zero, abaixo da tolerância de 4 dias |
| Caso 2 | QA-AURORA-001@1.1, Q01 | Qual foi a taxa de sessões web convertidas em 2026-10-01? | Principal | Responder | 25%: 1 sessão convertida entre 4 elegíveis |
| Caso 2 | QA-AURORA-001@1.1, Q02 | Por que a taxa de sessões web convertidas em 2026-10-01 não é 50%? | Apoio | Responder | 50% conta pedidos confirmados por sessão; o indicador conta sessões, por isso 25% |
| Transferência (a confirmar pelo mantenedor) | Pergunta de teste 1 | Pedido cancelado entra no ticket médio? | Conceitual | Responder | Não |
| Transferência (a confirmar pelo mantenedor) | Pergunta de teste 2 | Qual o ticket médio com devoluções? | Conceitual | Abster-se | Não há decisão sobre devoluções: não calcular e apontar quem pode resolver (a Controladoria) |
| Transferência (a confirmar pelo mantenedor) | Pergunta de teste 3 | Qual foi o ticket médio? | Conceitual | Pedir esclarecimento | Pedir o período e a operação (a tabela de pedidos tem data e operação) |

- **Gabaritos usados:** QA-AURORA-002@1.0 e QA-AURORA-001@1.1. O piloto não propõe mudança neles.
- **Fora da pontuação:** a Q03 e a Q06 dos gabaritos ficam de fora, porque dependem de decisões em aberto do experimento de onboarding.
- **Transferência:** as três perguntas de teste são uma proposta. O mantenedor confirma as respostas esperadas antes da primeira sessão, junto com os fatos da [ficha do especialista](ficha-do-especialista.md) marcados como a confirmar.

## Como o resultado entra no portão

Para cada caso, o que conta no critério do portão é a pergunta principal, comparada entre o antes e o depois da mesma pessoa e com a linha de base sem texto, como está no [README do piloto](README.md). A proposta é a Q02 no caso 1 e a Q01 no caso 2; a outra pergunta de cada caso é lida como apoio, e a transferência é lida separadamente. A tabela de cada pessoa fica na [folha de registro](folha-de-registro.md), e o resumo fica em [resultados.md](resultados.md).
