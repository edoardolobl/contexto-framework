# Protocolo de onboarding: o kit mínimo responde às perguntas marcadas

- **Estado:** Executado no Claude Code em 2026-11-17; critério de saída não atingido; Codex e Antigravity pendentes
- **Data:** 2026-11-17
- **Fase:** F6 (saídas para máquinas), [ADR 0028](../adr/0028-saidas-para-maquinas.md)
- **Origem:** [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-26; [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), critério de saída da F6

Este protocolo mede se um agente que recebe só o kit mínimo responde certo às perguntas que todo agente novo precisa acertar. Essas perguntas são as marcadas com `onboarding: true` nos gabaritos. O critério de saída da F6 diz: um agente com o kit responde às perguntas marcadas como onboarding. O llms.txt deixou de ser critério de saída (I-26).

## Material

- **Condição B, com o kit:** o kit baixado, sem a pasta `gabaritos/`. As respostas esperadas ficam só com quem pontua. O AGENTS.md do kit não muda, e ele menciona `gabaritos/`. Nessa cópia a pasta não existe, e isso não entra na pontuação.
- **Condição de controle (opcional):** só a pasta `dados/` do kit, sem AGENTS.md, glossário, contratos nem Skill. Mede o quanto a amostra sozinha basta.

## Perguntas

São oito perguntas marcadas com `onboarding: true`. Hoje são três no gabarito QA-AURORA-001@1.1 e cinco no gabarito QA-AURORA-002@1.0. Cada pergunta é feita numa sessão nova.

| Gabarito e id | Pergunta (texto exato) | Categoria esperada | Conclusão esperada | Citação esperada |
|---|---|---|---|---|
| QA-AURORA-001@1.1, Q01 | Qual foi a taxa de sessões web convertidas em 2026-10-01? | responder | 25%: 1 sessão convertida entre 4 elegíveis | KPI-AURORA-001@2.0 |
| QA-AURORA-001@1.1, Q02 | Por que a taxa de sessões web convertidas em 2026-10-01 não é 50%? | responder | 50% conta pedidos confirmados por sessão; o indicador conta sessões, por isso 25% | REL-AURORA-SESSIONS-ORDERS@2.0 e KPI-AURORA-001@2.0 |
| QA-AURORA-001@1.1, Q03 | Qual foi a conversão em 2026-10-01? | pedir esclarecimento | Perguntar se a pessoa quer a taxa de sessões convertidas no canal web, a única definida | KPI-AURORA-001@2.0 |
| QA-AURORA-002@1.0, Q01 | Quais eventos do plano de mensuração pararam de coletar, considerando os dias completos até 15/11/2026? | responder | Só o add_to_cart no México parou. O generate_lead no Brasil está em sequência normal. O generate_lead não se avalia no México | DECISION-AURORA-EVENTO-QUEBRADO@1.1 e EVENT-AURORA-GENERATE-LEAD@1.1 |
| QA-AURORA-002@1.0, Q02 | O generate_lead parou no Brasil? | responder | Não: 2 dias em zero, abaixo da tolerância de 4 dias | EVENT-AURORA-GENERATE-LEAD@1.1 e DECISION-AURORA-EVENTO-QUEBRADO@1.1 |
| QA-AURORA-002@1.0, Q03 | O generate_lead está quebrado? | pedir esclarecimento | Perguntar de qual operação se fala, porque o evento só está ativo no Brasil | EVENT-AURORA-GENERATE-LEAD@1.1 |
| QA-AURORA-002@1.0, Q05 | Qual a taxa de add_to_cart para purchase no México? | abster-se | Sem indicador aprovado para essa taxa: não calcular com a definição de mercado nem com a de outra operação | não se aplica (o gabarito não tem fonte com id) |
| QA-AURORA-002@1.0, Q06 | Qual foi a receita de purchase no Brasil em 02/11/2026? | responder | R$ 500, somando os três pedidos na tabela de pedidos. Somar depois da junção com os itens daria R$ 1.100 | não se aplica (a fonte é um arquivo de dados) |

Para a pergunta de abstenção, o motivo esperado é o registrado no gabarito. Para as perguntas de esclarecimento, a conclusão esperada é a informação que falta.

## Prompt

O prompt é literal e igual em todas as ferramentas. Só muda a pergunta entre aspas.

> Hoje é 17/11/2026. Responda à pergunta a seguir com o que você tem à disposição. Se a resposta depender de uma escolha que só quem pergunta pode fazer, pergunte antes de calcular. Se não houver base para responder, diga que não há base. Pergunta: "{pergunta}"

Na condição B, a primeira frase do prompt é: "Leia primeiro o arquivo AGENTS.md desta pasta." Assim, ferramentas que leem AGENTS.md e ferramentas que leem outro arquivo recebem a mesma instrução. A condição de controle não recebe essa frase.

A data está no prompt porque o dia 16/11 ainda não estava completo na data da consulta. Sem a data, nenhuma condição tem como saber o que conta como dia completo.

## Ferramentas e repetições

- **Ferramentas:** Claude Code, Codex e uma terceira ferramenta, por exemplo o Antigravity, que aparece no caso 1.
- **Execução:** uma pergunta, numa sessão nova. Nenhuma sessão responde duas perguntas.
- **Rodada:** uma passagem pelas oito perguntas, cada uma numa execução.
- **Repetições:** pelo menos três rodadas por ferramenta na condição B. A condição de controle é opcional; quando for rodada, também tem pelo menos três rodadas.
- **Conta mínima na condição B:** 8 perguntas × 3 rodadas × 3 ferramentas = 72 execuções.
- **Registro por execução:** ferramenta, nome e versão do modelo, data, condição, rodada, pergunta e resposta completa.

## Pontuação

Cada execução recebe três itens, e cada item vale sim ou não.

1. **Categoria certa:** a resposta é da categoria da coluna "Categoria esperada", como define o [ADR 0021](../adr/0021-responder-esclarecer-ou-abster-se.md). Responder quando a categoria é pedir esclarecimento, ou o contrário, conta como erro.
2. **Conclusão certa:** para responder, a conclusão principal bate com a resposta esperada, sem contradição; uma explicação extra não derruba o item. Para pedir esclarecimento, a resposta pede a informação que falta. Para abster-se, a resposta dá o motivo registrado no gabarito.
3. **Citação:** a resposta cita o id e a versão dos documentos da coluna "Citação esperada". Quando a coluna diz "não se aplica", o item não entra.

Uma pergunta acerta quando os itens 1 e 2 são sim. O item 3 é registrado e reportado, mas não entra no critério de saída.

## Critério

- Uma rodada passa quando as oito perguntas acertam (categoria e conclusão) na condição B.
- O critério é atendido, para uma ferramenta, quando pelo menos duas de suas três rodadas passam.
- A condição de controle não entra no critério. Ela serve para comparar com a condição B.
- Uma ferramenta que não rode aparece no registro com a causa.

## Registro dos resultados

Copie as linhas para cada ferramenta. A coluna "Perguntas certas" conta as oito perguntas da rodada; a coluna "Sem Q01 e Q02 do QA-AURORA-002" conta as mesmas acertos sem essas duas perguntas, que têm a resposta num teste do kit (veja as ressalvas); a coluna "Citações" conta as perguntas com citação aplicável, que são seis.

| Ferramenta | Modelo (nome e versão) | Data | Condição | Rodada | Perguntas certas (de 8) | Sem Q01 e Q02 do QA-AURORA-002 (de 6) | Citações (de 6) | Observações |
|---|---|---|---|---|---|---|---|---|
| | | | B | 1 | | | | |
| | | | B | 2 | | | | |
| | | | B | 3 | | | | |
| | | | Controle | 1 | | | | |
| | | | Controle | 2 | | | | |
| | | | Controle | 3 | | | | |

## Ressalvas

- **Amostra pequena:** são oito perguntas, uma amostra e três rodadas por ferramenta. O resultado não é taxa de acerto de um sistema nem prova de generalização ([ADR 0022](../adr/0022-laboratorio-pequeno-verificado-em-sqlite.md)).
- **Consultas de referência no kit:** as consultas de referência estão no kit porque fazem parte dos contratos que as perguntas citam. Um agente que as lê pode copiar a conta sem entender a regra. O protocolo mede a leitura do kit com essa limitação, e não retira a consulta, para não quebrar os contratos.
- **Avaliador da mesma família de modelos:** quando um modelo pontua, ele pode ser da mesma família dos agentes testados, e isso pode compartilhar pontos cegos. Registre o avaliador. Sempre que possível, pontue com uma pessoa da Analytics de E-commerce, que conferiu os gabaritos.
- **Testes dos contratos que coincidem com respostas esperadas:** os contratos do kit trazem testes, e dois deles são as conclusões esperadas de Q01 e Q02 do QA-AURORA-002. O contrato DECISION-AURORA-EVENTO-QUEBRADO@1.1, em `contratos/` e em `skills/auditar-coleta/references/`, tem em `tests` o add_to_cart no México com 5 dias completos em zero (failure_candidate) e o generate_lead no Brasil com 2 dias completos em zero (within_expected). O SKILL.md da Skill `auditar-coleta` repete os dois testes. Tirar a pasta `gabaritos/` não esconde essas respostas. Por isso o registro conta os acertos também sem essas duas perguntas, e o relatório mostra os dois números.
- **Quem pontua tem os gabaritos; quem executa não.** Essa separação vale para os arquivos de gabarito em toda rodada. Os testes dos contratos e da Skill ficam no kit, como diz a ressalva anterior.
- **Versões mudam:** registre o nome e a versão exatos do modelo em cada execução.

## Resultados da primeira execução (Claude Code, 2026-11-17)

Workflow de subagentes do Claude Code: 3 rodadas por modelo com o kit sem a pasta `gabaritos/` (48 execuções) e 1 rodada por modelo na condição de controle, só com `dados/` (16 execuções). Cada execução respondeu a uma pergunta numa sessão nova, com a instrução de usar só a sua pasta. Um avaliador separado pontuou cada resposta pela rubrica acima. Respostas e pontuações completas em [onboarding-resultados.json](./onboarding-resultados.json).

Acertos (categoria certa e conclusão certa) por pergunta:

| Condição | Modelo | QA-AURORA-001 Q01 | QA-AURORA-001 Q02 | QA-AURORA-001 Q03 | QA-AURORA-002 Q01 | QA-AURORA-002 Q02 | QA-AURORA-002 Q03 | QA-AURORA-002 Q05 | QA-AURORA-002 Q06 |
|---|---|---|---|---|---|---|---|---|---|
| kit sem gabaritos | Claude Opus 5.5 (claude-opus-5-5) | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 1 de 3 | 3 de 3 | 0 de 3 |
| kit sem gabaritos | Claude Sonnet 5.5 (claude-sonnet-5-5) | 3 de 3 | 3 de 3 | 0 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 0 de 3 |
| controle, só dados | Claude Opus 5.5 (claude-opus-5-5) | 1 de 1 | 1 de 1 | 0 de 1 | 1 de 1 | 1 de 1 | 0 de 1 | 0 de 1 | 1 de 1 |
| controle, só dados | Claude Sonnet 5.5 (claude-sonnet-5-5) | 1 de 1 | 1 de 1 | 0 de 1 | 1 de 1 | 1 de 1 | 0 de 1 | 0 de 1 | 1 de 1 |

**Critério de saída da F6: não atingido.** Com o kit, cada rodada acertou 6 ou 7 das 8 perguntas; o critério pede todas as perguntas certas em pelo menos 2 de 3 rodadas.

### O que as falhas mostram

1. **QA-AURORA-002, Q06 (receita de purchase no Brasil): 0 de 6 com o kit, 2 de 2 no controle.** Com o kit, todas as execuções pediram esclarecimento (qual receita, qual fuso). O AGENTS.md do kit manda perguntar quando não há indicador aprovado, e o kit não tem um indicador de receita aprovado. O gabarito espera responder R$ 500. A regra do kit e o gabarito se contradizem; o agente seguiu a regra.
2. **QA-AURORA-001, Q03 ("Qual foi a conversão?"): 3 de 3 no Opus, 0 de 3 no Sonnet.** O Sonnet supôs a única definição aprovada e respondeu 25%, sem perguntar. O kit não tem uma regra explícita para termo com mais de uma leitura.
3. **QA-AURORA-002, Q03 ("O generate_lead está quebrado?"): 1 de 3 no Opus, 3 de 3 no Sonnet.** O Opus avaliou as duas operações e respondeu "não" nas duas. Pelo ADR 0021, pedir esclarecimento é para quando a resposta depende de uma escolha de quem pergunta; aqui o resultado é o mesmo nas duas operações, e a resposta do Opus é defensável.

### Correções propostas (decisão do mantenedor)

- **Q06:** ou o gabarito passa a esperar pedir esclarecimento, coerente com a regra do kit e com a Q05, ou o Lab 2 ganha uma definição aprovada de receita de purchase (soma do valor dos pedidos, no fuso da operação, sem somar depois da junção com os itens) e a Q06 continua como responder.
- **Q03 da QA-AURORA-001:** acrescentar ao AGENTS.md do kit uma regra para termo com mais de uma leitura: "se a palavra da pergunta tem mais de um significado no glossário, ou nenhum, pergunte qual antes de calcular".
- **Q03 da QA-AURORA-002:** decidir se a resposta que avalia as duas operações e conclui o mesmo nas duas conta como certa; se contar, o gabarito registra as duas formas aceitas.

Os gabaritos não foram alterados para o teste passar. Depois das decisões, o experimento deve ser repetido.

### Ressalvas desta execução

- Agentes e avaliador são da mesma família de modelos (Claude).
- O isolamento das pastas foi por instrução, não por permissão do sistema de arquivos.
- Os testes do contrato da regra de evento quebrado e do SKILL.md coincidem com Q01 e Q02 da QA-AURORA-002, como diz a ressalva do protocolo.
