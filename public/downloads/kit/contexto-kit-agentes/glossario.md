# Glossário do kit

Este glossário é gerado dos documentos aprovados. Quando houver dúvida, vale a definição do documento citado.

## dia completo

Dia cujos dados já chegaram por inteiro. Para o generate_lead, o dia fica completo em D+2 às 06h no fuso da operação. Dia incompleto não entra na conta de dias em zero.

**Fonte:** `EVENT-AURORA-GENERATE-LEAD@1.1`

## evento quebrado

Evento do plano de mensuração que parou de coletar numa operação. Só vira candidato a falha (failure_candidate) quando está no escopo, os dados do dia estão completos, não há exceção conhecida, ele costuma disparar e o silêncio durou o que o time definiu. Candidato a falha é motivo para investigar, não defeito provado.

**Também chamado:** evento que parou de coletar

**Não confundir com:** silêncio dentro da tolerância (within_expected); evento fora do escopo da operação (not_active_in_scope)

**Fonte:** `DECISION-AURORA-EVENTO-QUEBRADO@1.1`

## generate_lead

Cadastro de atacado enviado com sucesso

**Não confundir com:** sign_up da newsletter, que registra a inscrição para receber e-mails e não é lead de atacado

**Fonte:** `EVENT-AURORA-GENERATE-LEAD@1.1`

## linha de base

Comportamento normal de um evento numa operação, medido numa janela de dias completos: média por dia, parte dos dias em zero e maior sequência em zero. O silêncio se compara com a linha de base da mesma operação.

**Não confundir com:** um dia isolado em zero, que sozinho não é quebra

**Fonte:** `EVENT-AURORA-GENERATE-LEAD@1.1`

## Participante ativo

Pessoa inscrita no programa, que não está em pausa nem concluiu todas as atividades, e que registrou presença em pelo menos uma atividade entre 30 dias antes da data de referência do relatório e a própria data de referência, ambas incluídas.

**Não confundir com:** Participante inscrito; Participante em pausa; Participante concluinte; Na folha de pagamento, 'ativo' significa vínculo de trabalho vigente. Não é o mesmo conceito.

**Fonte:** `CONCEPT-ONBOARDING-001@2.0`

## sessão convertida

Sessão do canal web, fora do tráfego interno, com pelo menos um pedido confirmado. Conta uma vez, mesmo com dois pedidos.

**Não confundir com:** pedido confirmado: uma sessão convertida pode ter mais de um

**Fonte:** `KPI-AURORA-001@2.0`

## Taxa de sessões convertidas

Proporção de sessões elegíveis que resultaram em pelo menos um pedido confirmado

**Também chamado:** conversão web

**Não confundir com:** Conversão de lead: outro indicador, não usar como sinônimo; Pedidos por sessão: era a definição da versão 1.0; hoje é outra medida, sem documento próprio

**Fonte:** `KPI-AURORA-001@2.0`

## tolerância ao silêncio

Número de dias completos seguidos em zero a partir do qual o time suspeita de falha, registrado por operação no Evento de coleta. É escolha do time, não regra universal.

**Fonte:** `EVENT-AURORA-GENERATE-LEAD@1.1`
