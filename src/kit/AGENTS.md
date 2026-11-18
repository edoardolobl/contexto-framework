# Instruções do kit Contexto para agentes

Versão alvo: formato AGENTS.md conforme agents.md, conferido em 17/11/2026.
Licença deste kit: CC BY 4.0.

Estas instruções orientam o agente. Elas não garantem que ele as siga: cada ferramenta decide como lê o arquivo e como responde.

## Onde fica cada coisa

- [Glossário](glossario.md): termos, sinônimos e o que não confundir com outro termo.
- [Contratos](contratos/): a definição aprovada de cada assunto, com id e versão atual.
- [Histórico de contratos](contratos/historico/): versões anteriores, usadas só para perguntas sobre o passado.
- [Gabaritos](gabaritos/): respostas esperadas, para conferir se o entendimento está certo.
- [Dados](dados/): a amostra do laboratório, para conferir contas. A amostra não é definição.
- [Skill auditar-coleta](skills/auditar-coleta/SKILL.md): passos para perguntas sobre evento de coleta que parou, quebrou ou está zerado.

## Arquivos do kit

<!-- contexto:kit-indice -->

## Ordem de leitura

1. Este arquivo.
2. O glossário, para os termos da pergunta.
3. O contrato do assunto, pelo id.
4. O gabarito, para conferir a resposta esperada, se a pergunta estiver nele.
5. A Skill auditar-coleta, quando a pergunta for sobre evento de coleta que parou.

## Regras

- Nunca calcule um indicador sem consultar a definição aprovada; se não houver, pergunte.
- Se o termo da pergunta não é o nome nem um sinônimo registrado de um indicador aprovado, ou serve para mais de um, mostre as opções e confirme qual antes de calcular. Um termo mais curto que o nome, como conversão para conversão web, não basta.
- Zero em um dia não é quebra; compare com a linha de base por operação.
- Use só o que está neste kit. Não complete a resposta com definição de mercado ou de outra operação.
- Só o estado approved (aprovado) vale como regra.
- draft (rascunho) e pending_approval (pendente de aprovação) são rascunho e não valem como definição.
- superseded (substituído) serve só para perguntas sobre o passado: escolha a versão cuja vigência cobre a data da pergunta.
- deprecated (obsoleto) quer dizer que o assunto deixou de valer. Diga isso.
- valid_from é o primeiro dia de vigência. valid_to é o fim exclusivo: o dia de valid_to já não conta.
- Em toda resposta, cite o id e a versão de cada documento usado, no formato id@versão.
- Termine toda resposta em um destes três desfechos:
  - Responder: há definição aprovada que cobre a pergunta.
  - Pedir esclarecimento: a pergunta é ambígua, porque falta operação, canal, período ou unidade. Mostre as opções que existem.
  - Abster-se: não há base aprovada. Diga isso e aponte quem pode resolver.
