---
name: contexto-consultar
description: "Use esta Skill quando a pergunta for sobre o que um termo, um indicador, uma regra ou um evento significa ou como se calcula, e a resposta deve vir dos documentos aprovados do kit, com id e versão. Ela fixa a data da pergunta, escolhe só os documentos que valem nessa data e termina em responder, pedir esclarecimento ou abster-se. Não use para escrever ou aprovar documentos. Para evento que parou de coletar, prefira a Skill auditar-coleta."
license: CC-BY-4.0
---

# Consultar: responder só com o que está aprovado

Versão alvo: especificação Agent Skills, conferida em 17/11/2026. Licença: CC BY 4.0.

Esta Skill orienta o agente. Ela não garante o comportamento dele. As regras abaixo vêm do AGENTS.md do kit e não o substituem.

## Passos

1. **Fixe a data de referência da pergunta.** Se faltar período, operação, canal ou unidade e a resposta mudar com isso, peça esclarecimento e mostre as opções documentadas.
2. **Ache os termos e os documentos.** Os termos estão no [glossário](../../glossario.md). Os documentos, por id, em [contratos](../../contratos/) e no [histórico de contratos](../../contratos/historico/). Se o termo da pergunta não é o nome nem um sinônimo registrado de um indicador aprovado, ou serve para mais de um, mostre as opções e confirme qual antes de calcular. Um termo mais curto que o nome, como conversão para conversão web, não basta.
3. **Filtre por estado.**
   - approved vale como regra.
   - superseded serve só para o passado, pela vigência que cobre a data da pergunta.
   - draft e pending_approval nunca valem como definição.
   - deprecated: diga que o assunto deixou de valer.
4. **Confira a vigência.** `valid_from` é inclusivo e `valid_to` é exclusivo. Se nenhuma versão cobre a data, abstenha-se.
5. **Calcule só com a fórmula aprovada.** A amostra de dados confere a conta, não define o indicador.
6. **Não resolva conflito pela data mais recente** (ADR 0018). Mostre o conflito entre as fontes e diga quem resolve.
7. **Termine em um desfecho** da tabela abaixo. Cite o id@versão e a vigência de cada documento usado.

## Desfechos (ADR 0021)

| Desfecho | Quando | O que dizer |
|---|---|---|
| Responder | Há definição aprovada que cobre a pergunta e a data. | A resposta, com id@versão e vigência de cada documento. |
| Pedir esclarecimento | A pergunta é ambígua: falta operação, canal, período ou unidade. | O que falta, com as opções que existem. |
| Abster-se | Não há base aprovada, ou nenhuma versão cobre a data, ou as fontes entram em conflito. | Que não há base, o que falta e quem pode resolver. |
