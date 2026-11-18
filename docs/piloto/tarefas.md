# Tarefas

- **Estado:** aguarda execução
- **Data:** 2026-11-17

Este é o enunciado entregue à pessoa participante. Cada tarefa tem uma parte "antes", sem o Contexto, e uma parte "depois", com o modelo .md do tipo indicado. A tarefa 3 é só depois.

Você está num time de análise da Aurora, a loja de exemplo dos laboratórios. Os dados que você recebe são os do laboratório. Escreva o que se pede, sem consultar outras pessoas.

## Tarefa 1: caso 1, evento raro tratado como quebrado

**Situação:** alguém viu que um evento ficou vários dias sem disparar e concluiu que ele quebrou. A pergunta da equipe é: quais eventos do plano de mensuração pararam de coletar?

**Material:** o banco do caso 1, com a tabela de eventos diários e a lista de eventos do plano por operação.

**Antes (texto livre, 10 min, sem o Contexto):** escreva o documento do evento `generate_lead` que deixe a IA responder "quais eventos pararam". Escreva em texto livre, com as palavras que quiser.

**Depois (modelo .md do tipo Evento de coleta, 10 min):** escreva de novo o documento do `generate_lead`, agora no modelo .md do tipo Evento de coleta. Preencha o que você conseguir com fonte. O que ninguém decidiu vai para as perguntas em aberto, com o impacto e quem resolve.

**Entrega:** o texto da parte antes e o modelo .md da parte depois.

## Tarefa 2: caso 2, indicador calculado com a definição genérica

**Situação:** a equipe calculou a taxa de sessões web convertidas com a definição genérica de mercado, e os números não batem com a conta do time.

**Material:** o arquivo de dados do caso 2 (`aurora-fixture.sql`), com as sessões e os pedidos.

**Antes (texto livre, 10 min, sem o Contexto):** escreva a definição da taxa de sessões web convertidas que deixe a IA chegar à conta do time. Escreva em texto livre.

**Depois (modelo .md do tipo Indicador, 10 min):** escreva de novo a definição, no modelo .md do tipo Indicador, com fonte e perguntas em aberto para o que não souber decidir.

**Entrega:** o texto da parte antes e o modelo .md da parte depois.

## Tarefa 3: transferência, caso não visto no portal

**Situação:** a equipe da loja web da Aurora quer acompanhar o ticket médio. Ninguém escreveu essa definição ainda.

**Material:** as tabelas de pedidos e de itens do laboratório de eventos (`aurora-lab2-fixture.sql`). Cada pedido tem data, operação e receita; cada item aponta para o pedido.

**Depois (modelo .md do tipo Indicador, 10 min):** defina o ticket médio da loja web da Aurora no modelo .md do tipo Indicador. Use fonte para o que souber e perguntas em aberto para o que ninguém decidiu. Não invente responsável, aprovação, fórmula nem vigência.

**Entrega:** o modelo .md preenchido.

## Regras para a pessoa

- Use a ferramenta de IA que você costuma usar, quando a tarefa pedir.
- Se a informação não existe nos materiais, escreva como pergunta em aberto. Não escolha um valor para completar.
- Pode perguntar ao facilitador sobre o caso. Ele responde só o que estiver na ficha, e pode dizer que não tem a informação.
- O tempo de cada parte é o indicado. Quando ele acabar, pare de escrever.
