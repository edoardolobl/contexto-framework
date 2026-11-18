---
name: auditar-coleta
description: "Use esta Skill quando a pergunta for sobre um evento de coleta que parou, quebrou ou está zerado, por exemplo: o evento parou? está quebrado? ficou sem disparos? Ela confere se o evento está ativo na operação, tira da conta os dias incompletos, compara a sequência atual de dias sem disparo com a linha de base e com a tolerância registradas no Evento de coleta e aplica a regra de evento quebrado. A resposta é responder, pedir esclarecimento ou abster-se, sempre citando id e versão. Não use para perguntas sobre indicadores: para esses, consulte a definição aprovada ou pergunte."
license: CC-BY-4.0
---

# Auditar coleta: evento que parou

Versão alvo: especificação Agent Skills, conferida em 17/11/2026. Licença: CC BY 4.0.

Esta Skill orienta o agente. Ela não garante o comportamento dele. O número de dias de silêncio que vira suspeita é escolha do time e fica no Evento de coleta. Nenhum valor é universal.

## Arquivos

- `references/DECISION-AURORA-EVENTO-QUEBRADO@1.1.md`: a regra de evento quebrado, com a tabela de decisão.
- `references/EVENT-AURORA-GENERATE-LEAD@1.1.md`: um Evento de coleta completo, com a linha de base e a tolerância de cada operação.

O gerador copia os dois arquivos do kit para a pasta `references/`.

## Passos

1. **Identifique o evento e a operação.** Se a pergunta não disser a operação e o evento existir em mais de uma, pergunte qual é antes de fazer qualquer conta. Desfecho: pedir esclarecimento.
2. **Confira se o evento está ativo naquela operação.** Veja `active_scopes` no Evento de coleta. Se estiver inativo, o zero é esperado e não há quebra. Se não houver registro, pergunte.
3. **Tire da conta os dias incompletos.** Um dia só conta depois de fechar, que é D+2 às 06h no fuso da operação quando o Evento de coleta usa essa regra. Falta de linha na tabela diária é zero, mas um dia incompleto não entra na conta. Se o dia avaliado ainda não fechou, abstenha-se e diga quando a resposta sai.
4. **Meça a sequência atual e compare.** Conte os dias completos seguidos sem disparo, só na operação em questão. Compare com a linha de base da mesma operação, se o evento tem histórico suficiente, e com a tolerância ao silêncio do Evento de coleta. Verifique também se uma exceção conhecida, registrada e aprovada no Evento de coleta cobre o período.
5. **Aplique a tabela de decisão** do DECISION-AURORA-EVENTO-QUEBRADO@1.1. As cinco entradas são evento ativo no escopo, dados completos, exceção conhecida, esperado na janela e sequência atingida. Cada combinação casa com uma única linha, e a entrada desconhecida que decide o caso leva a pedir esclarecimento.
6. **Responda com o desfecho e cite id@versão.** Diga a saída da tabela, a conta (dias completos, sequência, tolerância e linha de base da operação) e cite o DECISION-AURORA-EVENTO-QUEBRADO@1.1 e o Evento de coleta usado, com a versão de cada um.

## Desfechos

| Saída da tabela | Desfecho (ADR 0021) | O que dizer |
|---|---|---|
| not_active_in_scope | Responder | O evento não está ativo nesta operação. Zero é esperado. Não é quebra. |
| wait_for_complete_data | Abster-se | O dia ainda não fechou. A resposta depende da carga completa. |
| explained_by_known_exception | Responder | Uma exceção conhecida explica o silêncio. Cite a exceção. |
| within_expected | Responder | A sequência ainda não chegou à tolerância. Não é quebra. |
| failure_candidate | Responder | Candidato a falha. É motivo para investigar, não defeito provado. |
| request_clarification | Pedir esclarecimento | Diga o que falta (operação, escopo ou histórico) e mostre as opções. |

## Depois de um candidato a falha

Quando o desfecho for failure_candidate, a triagem de cinco passos da página Evento de coleta orienta a investigação: delimitar o escopo, datar o início e cruzar com as publicações do contêiner de tags, checar a sazonalidade, cruzar com fonte externa e testar o fluxo à mão. A investigação é do time. A Skill só diz que há motivo para abri-la.

## Exemplo da própria tabela de testes

- generate_lead na operação BR, com 2 dias completos em zero e tolerância de 4 dias: within_expected.
- add_to_cart na operação MX, com 5 dias completos em zero, dados completos e evento previsto: failure_candidate.

## Regras que não mudam

- Nunca calcule um indicador sem consultar a definição aprovada; se não houver, pergunte.
- Zero em um dia não é quebra; compare com a linha de base por operação.
- Só documento aprovado vale como regra. Rascunho e documento pendente de aprovação não valem.
