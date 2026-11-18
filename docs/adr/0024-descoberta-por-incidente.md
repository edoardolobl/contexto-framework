# 0024. Descoberta por incidente

- **Estado:** Proposto
- **Data:** 2026-11-17
- **Proposto por:** auditoria (F2)
- **Origem:** [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-08; [08-pesquisa-boas-praticas.md](../../auditoria/08-pesquisa-boas-praticas.md), recomendação sobre o roteiro de 8 perguntas; [07-metodo-e-credibilidade.md](../../auditoria/07-metodo-e-credibilidade.md), listas de perguntas que não se referenciam

## Contexto

A página de descoberta reúne perguntas gerais, e cada lista de perguntas do portal está solta das outras (07-metodo-e-credibilidade.md). Quem responde a perguntas gerais tende a descrever o processo ideal, não o caso que de fato aconteceu. A regra que importa costuma estar na exceção, e ela só aparece quando alguém conta uma decisão real. O método de análise de decisões críticas (Klein et al., 1989) parte de um caso real para extrair esse conhecimento tácito, e foi revisado por pares em estudos posteriores (Hoffman et al., 1998).

## Decisão

- **Ponto de partida:** a entrevista começa por um incidente real, uma situação em que a regra foi usada, ficou em dúvida ou falhou. A técnica é uma adaptação do Critical Decision Method. A adaptação é **convenção do Contexto**, não o método original, e é declarada como tal na página.
- **Oito famílias de perguntas:** incidente, fronteira, contraste, pista, escopo, contrafactual, proveniência e reprodução. Cada uma tem a pergunta operacional e a evidência esperada (regra 1 do contrato).
- **Roteiro de 20 minutos:** relato do incidente, linha do tempo, decisões tomadas e, no fim, um rascunho imperfeito da regra, levado ao especialista para correção. O rascunho não é aprovação.
- **"5 porquês"** só como heurística para chegar à regra, nunca como método de descoberta.
- **Em aberto:** a duração de cada família de perguntas. O roteiro é confirmado com pessoas pelo plano de validação (ADR 0010).

## Alternativas consideradas

- **O questionário atual de oito perguntas:** perguntas gerais respondidas de memória, sem caso real que ancore a resposta. Não foi escolhido.
- **Entrevista livre:** depende de quem conduz e deixa de cobrir fronteiras, contrastes e exceções. Não foi escolhida.
- **5 porquês como método:** tende a produzir uma causa única e uma regra limpa, quando o conhecimento real tem exceções e conflitos. Fica só como heurística.

## Consequências

- **Positivas:** as regras nascem de casos reais, com exceções e a origem de cada afirmação.
- **Negativas:** o roteiro leva mais tempo quando o caso é complexo; quem conduz precisa saber ouvir e não sugerir a resposta.
- **Fases afetadas:** F2 (a página Descubra o que falta vira entrevista por incidente, I-08). Nos modelos, as tabelas "O que perguntar" passam a apontar para esse roteiro (F5).
- **Breaking:** nenhum no formato dos modelos.

## Referências

- Klein, G. A., Calderwood, R., & MacGregor, D. (1989). Critical decision method for eliciting knowledge. *IEEE Transactions on Systems, Man, and Cybernetics*, 19(3), 462-472. https://doi.org/10.1109/21.31053
- Hoffman, R. R., Crandall, B., & Shadbolt, N. (1998). Use of the critical decision method to elicit expert knowledge: A case study in the methodology of cognitive task analysis. *Human Factors*, 40(2), 254-276. https://doi.org/10.1518/001872098779480442
