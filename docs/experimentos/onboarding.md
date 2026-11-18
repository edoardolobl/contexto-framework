# Protocolo de onboarding: o kit mínimo responde às perguntas marcadas

- **Estado:** Critério de saída atingido no Claude Code (terceira execução, 2026-11-17) e no Codex (quarta execução, 2026-11-18, depois do ajuste da Skill auditar-coleta); Antigravity pendente
- **Data:** 2026-11-17
- **Fase:** F6 (saídas para máquinas), [ADR 0028](../adr/0028-saidas-para-maquinas.md)
- **Origem:** [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-26; [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), critério de saída da F6

Este protocolo mede se um agente que recebe só o kit mínimo responde certo às perguntas que todo agente novo precisa acertar. Essas perguntas são as marcadas com `onboarding: true` nos gabaritos. O critério de saída da F6 diz: um agente com o kit responde às perguntas marcadas como onboarding. O llms.txt deixou de ser critério de saída (I-26).

## Material

- **Condição B, com o kit:** o kit baixado, sem a pasta `gabaritos/`. As respostas esperadas ficam só com quem pontua. O AGENTS.md do kit mudou em 17/11/2026 (regra do termo ambíguo, ADR 0030, depois da primeira execução); o texto atual menciona `gabaritos/`. Nessa cópia a pasta não existe, e isso não entra na pontuação.
- **Condição de controle (opcional):** só a pasta `dados/` do kit, sem AGENTS.md, glossário, contratos nem Skill. Mede o quanto a amostra sozinha basta.

## Perguntas

São oito perguntas marcadas com `onboarding: true`. Hoje são três no gabarito QA-AURORA-001@1.1 e cinco no gabarito QA-AURORA-002@1.1. Cada pergunta é feita numa sessão nova.

| Gabarito e id | Pergunta (texto exato) | Categoria esperada | Conclusão esperada | Citação esperada |
|---|---|---|---|---|
| QA-AURORA-001@1.1, Q01 | Qual foi a taxa de sessões web convertidas em 2026-10-01? | responder | 25%: 1 sessão convertida entre 4 elegíveis | KPI-AURORA-001@2.0 |
| QA-AURORA-001@1.1, Q02 | Por que a taxa de sessões web convertidas em 2026-10-01 não é 50%? | responder | 50% conta pedidos confirmados por sessão; o indicador conta sessões, por isso 25% | REL-AURORA-SESSIONS-ORDERS@2.0 e KPI-AURORA-001@2.0 |
| QA-AURORA-001@1.1, Q03 | Qual foi a conversão em 2026-10-01? | pedir esclarecimento | Perguntar se a pessoa quer a taxa de sessões convertidas no canal web, a única definida | KPI-AURORA-001@2.0 |
| QA-AURORA-002@1.1, Q01 | Quais eventos do plano de mensuração pararam de coletar, considerando os dias completos até 15/11/2026? | responder | Só o add_to_cart no México parou. O generate_lead no Brasil está em sequência normal. O generate_lead não se avalia no México | DECISION-AURORA-EVENTO-QUEBRADO@1.1 e EVENT-AURORA-GENERATE-LEAD@1.1 |
| QA-AURORA-002@1.1, Q02 | O generate_lead parou no Brasil? | responder | Não: 2 dias em zero, abaixo da tolerância de 4 dias | EVENT-AURORA-GENERATE-LEAD@1.1 e DECISION-AURORA-EVENTO-QUEBRADO@1.1 |
| QA-AURORA-002@1.1, Q03 | O generate_lead está quebrado? | pedir esclarecimento; também vale responder, se a condição for cumprida (`also_accepted`) | Perguntar de qual operação se fala, porque o evento só está ativo no Brasil. Também vale avaliar Brasil e México e dizer que no Brasil o silêncio está dentro da tolerância e que no México o evento não está ativo, sem chamar o México de quebrado nem de normal | EVENT-AURORA-GENERATE-LEAD@1.1 |
| QA-AURORA-002@1.1, Q05 | Qual a taxa de add_to_cart para purchase no México? | abster-se | Sem indicador aprovado para essa taxa: não calcular com a definição de mercado nem com a de outra operação | não se aplica (o gabarito não tem fonte com id) |
| QA-AURORA-002@1.1, Q06 | Qual foi a receita de purchase no Brasil em 02/11/2026? | responder | R$ 500, somando os três pedidos na tabela de pedidos. Somar depois da junção com os itens daria R$ 1.100 | KPI-AURORA-002@1.0 |

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

1. **Categoria certa:** a resposta é da categoria da coluna "Categoria esperada", como define o [ADR 0021](../adr/0021-responder-esclarecer-ou-abster-se.md). Quando o gabarito tem `also_accepted`, a categoria listada ali também vale, desde que a resposta cumpra a `condition` registrada. Fora isso, responder quando a categoria é pedir esclarecimento, ou o contrário, conta como erro.
2. **Conclusão certa:** para responder, a conclusão principal bate com a resposta esperada, sem contradição; uma explicação extra não derruba o item. Para pedir esclarecimento, a resposta pede a informação que falta. Para abster-se, a resposta dá o motivo registrado no gabarito.
3. **Citação:** a resposta cita o id e a versão dos documentos da coluna "Citação esperada". Quando a coluna diz "não se aplica", o item não entra.

Uma pergunta acerta quando os itens 1 e 2 são sim. O item 3 é registrado e reportado, mas não entra no critério de saída.

## Critério

- Uma rodada passa quando as oito perguntas acertam (categoria e conclusão) na condição B.
- O critério é atendido, para uma ferramenta, quando pelo menos duas de suas três rodadas passam.
- A condição de controle não entra no critério. Ela serve para comparar com a condição B.
- Uma ferramenta que não rode aparece no registro com a causa.

## Registro dos resultados

Copie as linhas para cada ferramenta. A coluna "Perguntas certas" conta as oito perguntas da rodada; a coluna "Sem Q01, Q02 e Q06 do QA-AURORA-002" conta as mesmas acertos sem essas três perguntas, que têm a resposta num contrato do kit (veja as ressalvas); a coluna "Citações" conta as perguntas com citação aplicável, que são sete.

| Ferramenta | Modelo (nome e versão) | Data | Condição | Rodada | Perguntas certas (de 8) | Sem Q01, Q02 e Q06 do QA-AURORA-002 (de 5) | Citações (de 7) | Observações |
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
- **Contratos que coincidem com respostas esperadas:** os contratos do kit trazem testes e exemplos, e três deles são as conclusões esperadas de Q01, Q02 e Q06 do QA-AURORA-002. O contrato DECISION-AURORA-EVENTO-QUEBRADO@1.1, em `contratos/` e em `skills/auditar-coleta/references/`, tem em `tests` o add_to_cart no México com 5 dias completos em zero (failure_candidate) e o generate_lead no Brasil com 2 dias completos em zero (within_expected). O SKILL.md da Skill `auditar-coleta` repete os dois testes. O contrato KPI-AURORA-002@1.0, em `contratos/`, traz o exemplo de R$ 500 certo e R$ 1.100 depois da junção, que é a resposta esperada de Q06. Tirar a pasta `gabaritos/` não esconde essas respostas. Por isso o registro conta os acertos também sem essas três perguntas, e o relatório mostra os dois números.
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


## Decisões de 17/11/2026 (ADR 0030)

Depois da primeira execução, o mantenedor decidiu como tratar as três falhas. Os gabaritos não foram afrouxados para o teste passar: cada falha virou uma mudança de regra ou de documento, e o experimento deve ser repetido com o material novo.

- **Q06 (receita de purchase):** o Lab 2 ganhou o indicador aprovado KPI-AURORA-002@1.0, com a consulta `aurora-lab2-receita-purchase.sql`. A Q06 continua como responder (R$ 500) e agora cita o indicador em `required_sources`. O gabarito sobe para QA-AURORA-002@1.1.
- **Q03 da QA-AURORA-001 (termo ambíguo):** o AGENTS.md do kit e a Skill `contexto-consultar` ganharam a regra: se o termo da pergunta não é o nome nem um sinônimo registrado de um indicador aprovado, ou serve para mais de um, o agente mostra as opções e confirma qual antes de calcular. Um termo mais curto que o nome, como conversão para conversão web, não basta.
- **Q03 da QA-AURORA-002:** o comportamento esperado continua sendo pedir esclarecimento. O gabarito passa a aceitar também a resposta que avalia Brasil e México, com a condição registrada em `also_accepted`. O campo é opcional no schema das perguntas de negócio.
- **Pontuação:** o item 1 da rubrica aceita a categoria de `also_accepted` quando a condição é cumprida. A Q06 entra entre as perguntas cuja resposta aparece num contrato do kit, junto de Q01 e Q02.
- **Próximo passo:** repetir as rodadas com o kit regenerado e registrar os resultados numa nova seção, sem alterar a seção da primeira execução.

## Resultados da segunda execução (Codex, 2026-11-17)

Repetição pedida pelo mantenedor em 17/11/2026 ("Sim, repetir agora"), depois das correções da ADR 0030. A seção da primeira execução fica como estava.

- **Material:** o kit regenerado em `public/downloads/kit/contexto-kit-agentes/`, sem a pasta `gabaritos/`, com o AGENTS.md que tem a regra do termo ambíguo e com o KPI-AURORA-002@1.0. Na condição de controle, só a pasta `dados/`.
- **Ferramenta e modelo:** Codex CLI 0.167.0, `codex exec`, modelo GPT-6.1 Sol (gpt-6.1-sol, esforço high), sandbox somente leitura, sem a configuração do usuário, sem memórias e sem sessão gravada.
- **Execuções:** 3 rodadas na condição B (24 execuções) e 1 rodada na condição de controle (8 execuções). Cada execução respondeu a uma pergunta numa sessão nova, numa cópia própria da pasta, com o prompt do protocolo e a mesma instrução da primeira execução: usar só os arquivos da pasta.
- **Avaliador:** Claude Opus 5.5 (claude-opus-5-5), pela rubrica acima. É de outra família de modelos, o que tira a ressalva de avaliador da mesma família, mas não substitui a conferência por uma pessoa da Analytics de E-commerce.
- **Por que não no Claude Code:** a repetição no Claude Code não rodou porque a sessão do Claude Code em modo não interativo estava sem login nesta máquina ("OAuth session expired"). Fica pendente, junto do Antigravity.

Respostas e pontuações completas em [onboarding-resultados-2.json](./onboarding-resultados-2.json).

Acertos (categoria certa e conclusão certa) por pergunta:

| Condição | Modelo | QA-AURORA-001 Q01 | QA-AURORA-001 Q02 | QA-AURORA-001 Q03 | QA-AURORA-002 Q01 | QA-AURORA-002 Q02 | QA-AURORA-002 Q03 | QA-AURORA-002 Q05 | QA-AURORA-002 Q06 |
|---|---|---|---|---|---|---|---|---|---|
| kit sem gabaritos | GPT-6.1 Sol (gpt-6.1-sol) | 3 de 3 | 3 de 3 | 3 de 3 | 0 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 |
| controle, só dados | GPT-6.1 Sol (gpt-6.1-sol) | 1 de 1 | 1 de 1 | 0 de 1 | 1 de 1 | 1 de 1 | 1 de 1 | 0 de 1 | 1 de 1 |

Registro por rodada, no formato da tabela do protocolo:

| Ferramenta | Modelo (nome e versão) | Data | Condição | Rodada | Perguntas certas (de 8) | Sem Q01, Q02 e Q06 do QA-AURORA-002 (de 5) | Citações (de 7) | Observações |
|---|---|---|---|---|---|---|---|---|
| Codex CLI 0.167.0 | GPT-6.1 Sol (gpt-6.1-sol), esforço high | 2026-11-17 | B | 1 | 7 | 5 | 6 | Q01 do QA-AURORA-002 pediu a operação |
| Codex CLI 0.167.0 | GPT-6.1 Sol (gpt-6.1-sol), esforço high | 2026-11-17 | B | 2 | 7 | 5 | 7 | Q01 do QA-AURORA-002 pediu a operação |
| Codex CLI 0.167.0 | GPT-6.1 Sol (gpt-6.1-sol), esforço high | 2026-11-17 | B | 3 | 7 | 5 | 6 | Q01 do QA-AURORA-002 pediu a operação |
| Codex CLI 0.167.0 | GPT-6.1 Sol (gpt-6.1-sol), esforço high | 2026-11-17 | Controle | 1 | 6 | 3 | 0 | Sem contratos, nenhuma resposta cita id; Q03 do QA-AURORA-001 respondeu sem perguntar; Q05 do QA-AURORA-002 pediu esclarecimento em vez de se abster |

**Critério de saída da F6: não atingido no Codex.** Nenhuma das três rodadas acertou as oito perguntas: todas erraram a Q01 do QA-AURORA-002.

### O que a segunda execução mostra

1. **As três correções da ADR 0030 funcionaram no Codex.** A Q06 (receita de purchase) acertou 3 de 3, com R$ 500 e citação do KPI-AURORA-002@1.0. A Q03 do QA-AURORA-001 ("Qual foi a conversão?") pediu esclarecimento em 3 de 3, citando a regra do termo ambíguo. A Q03 do QA-AURORA-002 pediu a operação em 3 de 3.
2. **Falha nova: QA-AURORA-002, Q01 ("Quais eventos do plano de mensuração pararam de coletar?"), 0 de 3 com o kit e 1 de 1 no controle.** Com o kit, todas as execuções pediram a operação. Duas citaram o passo 1 da Skill `auditar-coleta`: se a pergunta não disser a operação e o evento existir em mais de uma, perguntar antes de fazer qualquer conta. A pergunta não nomeia um evento e pede a lista de todos os eventos que pararam; o gabarito espera responder com a avaliação por operação. No Claude Code, a mesma pergunta tinha acertado 6 de 6 na primeira execução. É um conflito entre o texto da Skill e o gabarito, do mesmo tipo da Q06 na primeira execução: o agente seguiu a regra do kit.
3. **Citações:** 19 de 21 na condição B. As duas faltas são da Q01 do QA-AURORA-002, que citou só DECISION-AURORA-EVENTO-QUEBRADO@1.1.
4. **Controle:** sem AGENTS.md, o agente respondeu "Qual foi a conversão?" com 25% sem perguntar e pediu esclarecimento na taxa de add_to_cart para purchase, em vez de dizer que não há indicador aprovado. As duas perguntas dependem das regras do kit, como na primeira execução.

### Correção proposta (decisão do mantenedor)

- **Q01 do QA-AURORA-002:** limitar o passo 1 da Skill `auditar-coleta` à pergunta sobre um evento nomeado: "se a pergunta nomeia um evento sem dizer a operação, e o evento existe em mais de uma, pergunte qual". Uma pergunta sobre todos os eventos do plano se responde por evento e operação, como manda a DECISION-AURORA-EVENTO-QUEBRADO@1.1. A alternativa é o gabarito aceitar também pedir esclarecimento, o que contradiz a regra de avaliar por operação.
- O relatório de `scripts/erros_para_perguntas.py` para esta execução aponta a mesma pergunta (3 erros em 24 execuções) e propõe uma pergunta em aberto para DECISION-AURORA-EVENTO-QUEBRADO@1.1 e EVENT-AURORA-GENERATE-LEAD@1.1.

Os gabaritos e a Skill não foram alterados nesta execução. Depois da decisão sobre a Q01, o experimento deve ser repetido no Codex e no Claude Code.

### Ressalvas desta execução

- Uma ferramenta só, um modelo só e uma rodada de controle. O critério pede três ferramentas.
- O isolamento das pastas foi por instrução e por cópias fora do repositório; o sandbox do Codex impede escrita, não leitura fora da pasta.
- O arquivo de instruções globais do Codex do usuário (10 linhas, sem menção ao Contexto) continuou carregado.
- As respostas no JSON estão como o agente escreveu, inclusive com travessão em duas delas; o JSON é registro bruto e não é texto publicado.

## Terceira execução (Claude Code, 2026-11-17, depois das correções do ADR 0030)

Mesmo desenho da primeira execução (3 rodadas por modelo com o kit sem `gabaritos/` e 1 rodada de controle só com `dados/`), agora com o kit corrigido: indicador aprovado KPI-AURORA-002@1.0 para a Q06, regra de termo ambíguo no AGENTS.md e as duas formas aceitas na Q03 do QA-AURORA-002. Respostas e pontuações em [onboarding-resultados-3.json](./onboarding-resultados-3.json).

| Condição | Modelo | QA-AURORA-001 Q01 | QA-AURORA-001 Q02 | QA-AURORA-001 Q03 | QA-AURORA-002 Q01 | QA-AURORA-002 Q02 | QA-AURORA-002 Q03 | QA-AURORA-002 Q05 | QA-AURORA-002 Q06 |
|---|---|---|---|---|---|---|---|---|---|
| kit sem gabaritos | Claude Opus 5.5 (claude-opus-5-5) | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 |
| kit sem gabaritos | Claude Sonnet 5.5 (claude-sonnet-5-5) | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 |
| controle, só dados | Claude Opus 5.5 (claude-opus-5-5) | 1 de 1 | 1 de 1 | 0 de 1 | 1 de 1 | 1 de 1 | 1 de 1 | 0 de 1 | 1 de 1 |
| controle, só dados | Claude Sonnet 5.5 (claude-sonnet-5-5) | 1 de 1 | 1 de 1 | 0 de 1 | 0 de 1 | 1 de 1 | 1 de 1 | 0 de 1 | 1 de 1 |

**Critério de saída da F6: atingido no Claude Code.** Com o kit, as 6 rodadas (3 por modelo) acertaram as 8 perguntas. O controle continua errando onde a resposta depende de uma definição aprovada: o termo ambíguo (Q03 do QA-AURORA-001), a abstenção (Q05) e, no Sonnet, a pergunta dos eventos (Q01 do QA-AURORA-002).

**Ressalvas:** a resposta da Q06 está no kit, porque o contrato do KPI-AURORA-002 traz o exemplo de 02/11, como já acontecia com Q01 e Q02 do QA-AURORA-002; agentes e avaliador são da mesma família. Na segunda execução, no Codex, a Q01 do QA-AURORA-002 falhou nas três rodadas porque o passo 1 da Skill auditar-coleta manda perguntar a operação; essa mudança da Skill é decisão do mantenedor.

## Quarta execução (Codex CLI, depois do ajuste da Skill auditar-coleta)

Repetição no Codex, autorizada pelo mantenedor em 18/11/2026, depois da correção proposta na segunda execução. O passo 1 da Skill `auditar-coleta` agora separa dois casos: a pergunta sobre o plano inteiro ("quais eventos pararam?") não pede a operação e avalia cada evento em cada operação; a pergunta sobre um evento nomeado, sem a operação, só pede a operação quando o evento está ativo em mais de uma e o desfecho pode mudar de uma para outra. As seções anteriores ficam como estavam.

- **Material:** o kit em `public/downloads/kit/contexto-kit-agentes/`, sem a pasta `gabaritos/`, copiado para uma pasta temporária fora do repositório, uma cópia por execução.
- **Ferramenta e modelo:** o mesmo método da segunda execução. Codex CLI 0.167.0, modelo GPT-6.1 Sol (gpt-6.1-sol, esforço high), com o comando `codex exec --ignore-user-config --ephemeral --disable memories --disable hooks --ignore-rules -s read-only --skip-git-repo-check -m gpt-6.1-sol -c model_reasoning_effort="high" -C <pasta> -o <saída> "<prompt>"`.
- **Execuções:** só a condição B, 3 rodadas de 8 perguntas (24 execuções), cada uma numa sessão nova. Prompt literal do protocolo, com "Leia primeiro o arquivo AGENTS.md desta pasta." no início e a mesma instrução de usar só os arquivos da pasta. Sem condição de controle.
- **Avaliador:** Claude Opus 5.5 (claude-opus-5-5), pela rubrica acima, sem passar o gabarito ao agente.

Respostas e pontuações completas em [onboarding-resultados-4.json](./onboarding-resultados-4.json).

Acertos (categoria certa e conclusão certa) por pergunta:

| Condição | Modelo | QA-AURORA-001 Q01 | QA-AURORA-001 Q02 | QA-AURORA-001 Q03 | QA-AURORA-002 Q01 | QA-AURORA-002 Q02 | QA-AURORA-002 Q03 | QA-AURORA-002 Q05 | QA-AURORA-002 Q06 |
|---|---|---|---|---|---|---|---|---|---|
| kit sem gabaritos | GPT-6.1 Sol (gpt-6.1-sol) | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 | 3 de 3 |

Registro por rodada, no formato da tabela do protocolo:

| Ferramenta | Modelo (nome e versão) | Data | Condição | Rodada | Perguntas certas (de 8) | Sem Q01, Q02 e Q06 do QA-AURORA-002 (de 5) | Citações (de 7) | Observações |
|---|---|---|---|---|---|---|---|---|
| Codex CLI 0.167.0 | GPT-6.1 Sol (gpt-6.1-sol), esforço high | 2026-11-18 | B | 1 | 8 | 5 | 7 | Q03 do QA-AURORA-002 respondeu pela forma também aceita |
| Codex CLI 0.167.0 | GPT-6.1 Sol (gpt-6.1-sol), esforço high | 2026-11-18 | B | 2 | 8 | 5 | 7 | Q03 do QA-AURORA-002 respondeu pela forma também aceita |
| Codex CLI 0.167.0 | GPT-6.1 Sol (gpt-6.1-sol), esforço high | 2026-11-18 | B | 3 | 8 | 5 | 7 | Q03 do QA-AURORA-002 respondeu pela forma também aceita |

**Critério de saída da F6: atingido no Codex.** As três rodadas acertaram as oito perguntas; o critério pede pelo menos duas de três.

### O que a quarta execução mostra

1. **A Q01 do QA-AURORA-002 passou de 0 de 3 para 3 de 3.** Nenhuma execução pediu a operação. Todas responderam com uma linha por evento e operação: só o add_to_cart no México é candidato a falha (5 dias completos em zero), o generate_lead no Brasil está dentro do esperado (2 dias, tolerância de 4) e o generate_lead não está ativo no México. As três citaram DECISION-AURORA-EVENTO-QUEBRADO@1.1 e EVENT-AURORA-GENERATE-LEAD@1.1.
2. **A Q03 do QA-AURORA-002 mudou de forma.** Na segunda execução, as três pediram a operação. Agora as três avaliaram Brasil e México e disseram que no México o evento não está ativo, que é a forma registrada em `also_accepted`. O texto novo da Skill permite avaliar todas as operações quando o desfecho é o mesmo, e foi o que o agente fez.
3. **Citações:** 21 de 21.

### Ressalvas desta execução

- Uma ferramenta, um modelo e nenhuma rodada de controle. O Antigravity continua pendente.
- As respostas de Q01, Q02 e Q06 do QA-AURORA-002 aparecem nos testes e exemplos dos contratos e da Skill, como diz a ressalva do protocolo; sem essas três perguntas, as rodadas acertaram 5 de 5.
- O prompt continua com "Hoje é 17/11/2026", como no protocolo, embora a execução tenha sido em 18/11/2026.
- O isolamento foi por instrução e por cópias fora do repositório; o sandbox do Codex impede escrita, não leitura fora da pasta.
- O avaliador é de outra família de modelos, mas não substitui a conferência por uma pessoa da Analytics de E-commerce.
