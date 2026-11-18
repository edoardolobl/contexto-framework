# Ficha do especialista

- **Uso:** só para o facilitador. Não entregue esta ficha à pessoa participante.
- **Estado:** aguarda execução
- **Data:** 2026-11-17

O facilitador revela um fato só quando a pessoa pergunta por ele. Os fatos vêm dos documentos aprovados citados. Se a pergunta não estiver coberta, diga que não tem a informação e que ela pode ser escrita como pergunta em aberto. Não resolva a dúvida por conta própria.

## Caso 1: evento raro tratado como quebrado

Fonte: EVENT-AURORA-GENERATE-LEAD@1.1 e DECISION-AURORA-EVENTO-QUEBRADO@1.1.

- **Operações:** o evento existe no Brasil (BR) e não está implementado no México (MX). Zero no México é o esperado, e não é quebra.
- **Dia completo:** um dia só fica completo em D+2 às 06h, no fuso da operação. Antes disso, o dia não entra na conta.
- **Falta de linha:** a tabela tem uma linha por dia, operação e evento, só quando houve disparo. Uma linha que falta pode ser zero ou falha de coleta, por isso a tabela não basta sozinha.
- **Linha de base:** é o comportamento normal do evento numa operação, medido em dias completos: média por dia, parte dos dias em zero e a maior sequência em zero. Compara-se sempre a mesma operação, nunca BR com MX.
- **Tolerância ao silêncio:** 4 dias completos seguidos em zero, na operação BR. Um dia isolado em zero não é quebra.
- **Quem aprova:** a Gerência de Analytics (Aurora) aprova a decisão e o evento. A Analytics de E-commerce é quem mantém o evento e confirma se ele está ativo na operação.
- **Exceção conhecida:** uma manutenção programada só conta como exceção com chamado aprovado pela Gerência de Analytics, com início e fim.
- **Evento novo:** sem histórico suficiente não há linha de base, e a decisão é pedir esclarecimento.

## Caso 2: taxa de sessões web convertidas

Fonte: KPI-AURORA-001@2.0 e REL-AURORA-SESSIONS-ORDERS@2.0.

- **Sessão web fora do tráfego interno:** a conta só usa sessões do canal web que não são tráfego interno. Pedidos de teste e pedidos cancelados ficam de fora.
- **Pedido confirmado:** só conta pedido com situação confirmada. Cancelado e de teste não contam.
- **Sessão conta uma vez:** uma sessão com dois pedidos confirmados conta como uma sessão convertida. Quem soma pedidos em vez de sessões chega a outra taxa.
- **Relação entre sessão e pedido:** uma sessão pode ter vários pedidos, por isso a junção repete a sessão. Para contar sessões convertidas, conte cada sessão uma vez.
- **Quem mantém e quem aprova:** o indicador é mantido pela Analytics de E-commerce e aprovado pela Gerência de E-commerce (Aurora).

## Transferência: ticket médio da loja web

Estes fatos ainda não foram conferidos num documento aprovado. Antes da primeira sessão, o mantenedor confirma cada um. Até lá, responda com a frase "a confirmar pelo mantenedor".

- **Unidade:** pedido confirmado. (a confirmar pelo mantenedor)
- **Exclusões:** pedidos cancelados e pedidos de teste ficam fora. (a confirmar pelo mantenedor)
- **Frete:** o valor não inclui o frete. (a confirmar pelo mantenedor)
- **Fuso:** America/Sao_Paulo. (a confirmar pelo mantenedor)
- **Fonte de pedidos:** no piloto, a tabela `lab2_pedidos` do laboratório de eventos, uma linha por pedido, com data, operação e receita. Ela não traz canal nem situação do pedido. A tabela `lab2_itens` tem uma linha por item: somar a receita depois de juntar as duas conta o pedido de novo para cada item. (a confirmar pelo mantenedor)
- **Devoluções:** ainda não há decisão sobre como tratar devoluções. A Controladoria é quem pode resolver. (a confirmar pelo mantenedor)

## O que o facilitador não faz

- Não dá a resposta do gabarito, nem diz se a pessoa acertou.
- Não diz qual pergunta em aberto a pessoa deveria ter registrado.
- Não lê os gabaritos, a pontuação nem os documentos da Aurora em voz alta.
- Não sugere termos, fórmulas ou responsáveis que não estejam nesta ficha.
