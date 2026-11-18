---
name: contexto-elicitar
description: "Use esta Skill quando a pessoa quiser documentar um assunto de negócio ou de dados que ainda não tem documento: um indicador, um evento de coleta, uma regra, uma tabela. Ela conduz uma conversa a partir de um caso real, separa o que está confirmado, o que é só relato e o que está em aberto, e entrega um rascunho com as perguntas em aberto. Não use para aprovar ou revisar um documento, nem para responder uma pergunta de negócio com base em documentos aprovados."
license: CC-BY-4.0
---

# Descobrir o que falta: do caso real ao rascunho

Versão alvo: especificação Agent Skills, conferida em 17/11/2026. Licença: CC BY 4.0.

Esta Skill orienta o agente. Ela não garante o comportamento dele. O rascunho que ela produz é ponto de partida: quem tem autoridade ainda precisa revisar e aprovar.

## Arquivos

- [Tipos de documento](references/tipos.md): os onze tipos, quando usar cada um, o modelo e o schema publicados.
- [Perguntas por incidente](references/perguntas-por-incidente.md): as oito famílias de perguntas, o roteiro de 20 minutos e a fonte.

## Passos

1. **Escolha o tipo com a pessoa.** Use `references/tipos.md`. Se não houver uma pergunta de negócio, peça primeiro a pergunta: sem ela não dá para escolher o tipo.
2. **Peça o caso real.** Diga: "Conte o último caso em que..." e complete com algo concreto do assunto. Deixe a pessoa contar sem interromper. Depois refaça a linha do tempo com ela.
3. **Volte aos pontos de decisão.** Use as famílias de perguntas de `references/perguntas-por-incidente.md`. Não é preciso fazer todas.
4. **Separe Confirmado, Relatado e Em aberto.** Confirmado tem fonte. Relatado é o que a pessoa diz, sem fonte. Em aberto é o que ninguém sabe ou ninguém decidiu.
5. **Monte o rascunho no modelo publicado do tipo,** com `schema_version` 1.1.0, `status` draft, `version` 0.1 e `approved_by` null.
6. **Só o confirmado, com fonte, vira valor de campo.** Relato e dúvida viram `open_questions`, com `question`, `impact`, `owner_to_resolve` (null se ninguém foi indicado), `status` unresolved e `resolution` null.
7. **Entregue três coisas:** o rascunho, a lista de perguntas em aberto e o próximo passo, que é revisar e aprovar.

## Regras que não mudam

- Nunca invente responsável. O `owner` só recebe o cargo ou a área que a pessoa disser, nunca o nome de alguém.
- Nunca preencha `approver` nem qualquer aprovação.
- Nunca invente fórmula. Sem fonte, a fórmula vira pergunta em aberto.
- Nunca preencha a vigência. `valid_from` e `valid_to` ficam null, e uma data citada na conversa vira pergunta para confirmar.
- Nunca use status diferente de draft.

## Exemplo curto: o evento raro

Alguém de Analytics viu o evento da loja sem disparo no dia e concluiu que ele tinha parado. Quem acompanha o evento contou o caso, e o registro ficou assim:

| Confirmado | Relatado | Em aberto |
|---|---|---|
| O evento só está implementado numa das operações (plano de coleta vigente). | Dias sem disparo são normais para este evento, segundo quem o acompanha. | A partir de quantos dias seguidos sem disparo vale desconfiar de quebra? |
| Na tabela diária, um dia sem disparo não gera linha (dicionário do dataset). | O dia só fica completo depois da carga do dia seguinte. | Quem aprova essa regra? Ainda não identificado. |

No rascunho do Evento de coleta, a primeira linha de Confirmado vira valor de campo, com a fonte. As outras viram `open_questions`, com `owner_to_resolve` null, porque ninguém foi indicado. O próximo passo é revisar e aprovar.
