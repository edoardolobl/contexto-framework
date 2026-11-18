# Caso 1: protocolo do critério de saída da F4

- **Estado:** Executado no Claude Code em 2026-11-17 e no Antigravity CLI em 2026-11-18; Codex pendente
- **Data:** 2026-11-17
- **Fase:** F4 (mensuração), [ADR 0027](../adr/0027-evento-de-coleta-e-laboratorio-de-mensuracao.md)
- **Origem:** [09-casos-de-uso.md](../../auditoria/09-casos-de-uso.md), caso 1 e USO-01; [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F4

Este protocolo mede se a documentação muda a resposta de um agente à pergunta do caso 1: um evento raro, com dias em zero, foi lido como quebra. O critério de saída da F4 diz: um agente com a documentação segmenta por operação e consulta o histórico; sem ela, erra. O resultado é registrado com modelo e data.

## Pergunta

- **Pergunta fraca** (controle de leitura, não entra na pontuação): "Quais eventos do plano de mensuração estão zerados hoje?"
- **Pergunta boa** (usada no prompt das duas condições): "Quais eventos do plano de mensuração, nas operações em que estão implementados, ficaram sem disparo por mais tempo do que o normal para eles, considerando só dias já completos?"

A pergunta fraca pede um número de hoje e aceita zero como quebra. A pergunta boa limita o escopo (operações em que o evento existe), pede o normal de cada evento e exige dias completos.

## Dados entregues ao agente

As duas condições recebem o mesmo banco, o **banco do caso 1**, com só o que a produção da Aurora tem:

- `lab2_eventos_diarios`, igual à amostra: uma linha por dia, operação e evento, só quando houve disparo. Ela espelha a tabela de produção e inclui as contagens parciais de 16/11.
- `lab2_plano` reduzida a `event_name` e `operation`: a lista de eventos do plano por operação, sem dizer se o evento está ativo, quando foi lançado nem qual a tolerância ao silêncio.

Ficam de fora do banco: as colunas `active`, `launch_date` e `silence_tolerance_days` de `lab2_plano`, a tabela `lab2_carga` (que marca o dia incompleto) e as tabelas de pedidos e itens. Essas informações são justamente o que a documentação traz. Se o banco as entregasse, a condição sem documentação já saberia o escopo por operação, a tolerância e o dia incompleto, e o contraste que o critério de saída quer medir ficaria fraco.

Para montar o banco do caso 1, crie o banco da amostra com `public/downloads/aurora-lab2-fixture.sql` (por exemplo, `amostra.db`) e rode, num banco novo e vazio:

```sql
ATTACH DATABASE 'amostra.db' AS fonte;
CREATE TABLE lab2_plano AS
  SELECT event_name, operation FROM fonte.lab2_plano;
CREATE TABLE lab2_eventos_diarios AS
  SELECT event_date, operation, event_name, event_count FROM fonte.lab2_eventos_diarios;
DETACH DATABASE fonte;
```

Não entram no contexto de nenhuma condição: `public/downloads/aurora-lab2-reference-query.sql` e o gabarito `QA-AURORA-002`. O gabarito é usado só para pontuar.

## Condições

- **Condição A, sem documentação:** o agente recebe só o banco do caso 1 e o schema dele (os comandos de criação das duas tabelas).
- **Condição B, com documentação:** o agente recebe o banco do caso 1, o mesmo schema e os dois arquivos `public/downloads/exemplo-evento-coleta-completo.yaml` e `public/downloads/exemplo-decisao-evento-quebrado-completo.yaml`.

O prompt é literal e igual nas duas condições:

> Hoje é 17/11/2026. Responda à pergunta a seguir com o que você tem à disposição. Se a resposta depender de uma escolha que só quem pergunta pode fazer, pergunte antes de calcular. Se não houver base para responder, diga que não há base. Pergunta: "Quais eventos do plano de mensuração, nas operações em que estão implementados, ficaram sem disparo por mais tempo do que o normal para eles, considerando só dias já completos?"

A data da consulta entra no prompt das duas condições porque nenhuma delas teria como saber o dia de hoje. Fora isso, nenhuma condição recebe instrução extra sobre operações, dias ou limiares.

## Ferramentas, modelos e repetições

- **Ferramentas:** Claude Code, Codex e Antigravity.
- **Registro por execução:** nome e versão do modelo, data, condição e número da execução.
- **Repetições:** pelo menos três execuções por condição, em cada ferramenta usada. Uma ferramenta que não rode uma condição aparece na tabela com a causa.

## Pontuação

Cada execução faz uma única pergunta, a do prompt, e recebe duas pontuações.

1. **Pergunta Q01 do gabarito QA-AURORA-002.** A pergunta do prompt tem a mesma intenção da Q01, e a resposta de referência da Q01 serve para as duas. Marcam-se dois itens:
   - **Categoria certa:** a resposta é da categoria esperada da Q01, `answer` (responder), e não `clarify` (esclarecer) nem `abstain` (abster-se), como define o [ADR 0021](../adr/0021-responder-esclarecer-ou-abster-se.md).
   - **Conclusão igual à da Q01:** aponta o `add_to_cart` no México como o único evento que parou, e não aponta o `generate_lead` em nenhuma das duas operações.
2. **Os três sinais do critério de saída.** Cada sinal vale um ponto se a resposta o mostra:
   - segmenta por operação antes de concluir;
   - consulta o histórico do evento para saber o normal;
   - exclui o dia incompleto da conclusão.

As perguntas Q02 a Q06 do gabarito, inclusive as de esclarecer e de abster-se, não são feitas neste caso. Medir essas categorias pede um protocolo próprio, com uma pergunta por execução.

## Registro dos resultados

| Ferramenta | Modelo (nome e versão) | Data | Condição | Execução | Categoria certa | Conclusão igual à da Q01 | Segmenta por operação | Consulta o histórico | Exclui o dia incompleto | Observações |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | A | 1 | | | | | | |
| | | | A | 2 | | | | | | |
| | | | A | 3 | | | | | | |
| | | | B | 1 | | | | | | |
| | | | B | 2 | | | | | | |
| | | | B | 3 | | | | | | |

## Ressalvas

O experimento é pequeno: poucas execuções, um único banco de amostra e uma única pergunta. Ele não prova generalização para outros agentes, outras versões dos modelos nem outros domínios, e não mede a taxa de acerto de um sistema. Ele mostra se a documentação muda a resposta nesta pergunta, com estes dados. Pelo ADR 0022, o laboratório mostra a diferença entre definições, não a qualidade de um agente.

## Resultados da primeira execução (Claude Code, 2026-11-17)

Execução feita por um workflow de subagentes do Claude Code. Cada agente recebeu uma pasta só com os arquivos da sua condição (banco do caso 1, schema e, na condição B, os dois YAML) e a instrução de não ler nada fora dela. Além das três execuções com a pergunta boa, cada modelo respondeu uma vez à pergunta fraca, que é a do caso real. Um avaliador separado (Claude Opus 5.5) pontuou cada resposta pela rubrica acima, comparando com a Q01. As respostas e as pontuações completas estão em [caso-1-resultados.json](./caso-1-resultados.json).

### Resumo

| Condição | Pergunta | Execuções | Conclusão igual à da Q01 | Segmenta por operação | Consulta o histórico | Exclui o dia incompleto | Marca generate_lead como quebrado |
|---|---|---|---|---|---|---|---|
| A, sem documentação | boa | 6 | 4 | 6 | 6 | 0 | 1 |
| A, sem documentação | fraca | 2 | 0 | 2 | 1 | 0 | 2 |
| B, com documentação | boa | 6 | 6 | 6 | 6 | 6 | 0 |
| B, com documentação | fraca | 2 | 2 | 2 | 2 | 2 | 0 |

**Leitura:** com a documentação, as 8 execuções chegaram à conclusão da Q01 e mostraram os três sinais do critério de saída. Sem ela, nenhuma execução deixou o dia 16/11 de fora (todas trataram o último dia com dados como completo), e as duas respostas à pergunta fraca, a do caso real, marcaram o generate_lead como quebrado, inclusive no México, onde o evento não existe. A pergunta boa já sugere segmentar e olhar o normal, por isso a condição A acertou a conclusão principal em 4 de 6 execuções; o dia incompleto e o escopo do generate_lead só vieram da documentação.

**Critério de saída da F4:** atendido nesta ferramenta, com estes modelos. Falta repetir no Codex e no Antigravity.

### Execuções

| Ferramenta | Modelo (nome e versão) | Data | Condição | Execução | Categoria certa | Conclusão igual à da Q01 | Segmenta por operação | Consulta o histórico | Exclui o dia incompleto | Observações |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Code | Claude Opus 5.5 (claude-opus-5-5) | 2026-11-17 | A | boa 1 | sim (answer) | não | sim | sim | não | marca generate_lead como quebrado |
| Claude Code | Claude Opus 5.5 (claude-opus-5-5) | 2026-11-17 | A | boa 2 | sim (answer) | sim | sim | sim | não |  |
| Claude Code | Claude Opus 5.5 (claude-opus-5-5) | 2026-11-17 | A | boa 3 | sim (answer) | sim | sim | sim | não |  |
| Claude Code | Claude Opus 5.5 (claude-opus-5-5) | 2026-11-17 | A | fraca 1 | sim (answer) | não | sim | sim | não | marca generate_lead como quebrado |
| Claude Code | Claude Sonnet 5.5 (claude-sonnet-5-5) | 2026-11-17 | A | boa 1 | sim (answer) | sim | sim | sim | não |  |
| Claude Code | Claude Sonnet 5.5 (claude-sonnet-5-5) | 2026-11-17 | A | boa 2 | sim (answer) | não | sim | sim | não |  |
| Claude Code | Claude Sonnet 5.5 (claude-sonnet-5-5) | 2026-11-17 | A | boa 3 | sim (answer) | sim | sim | sim | não |  |
| Claude Code | Claude Sonnet 5.5 (claude-sonnet-5-5) | 2026-11-17 | A | fraca 1 | não (clarify) | não | sim | não | não | marca generate_lead como quebrado |
| Claude Code | Claude Opus 5.5 (claude-opus-5-5) | 2026-11-17 | B | boa 1 | sim (answer) | sim | sim | sim | sim |  |
| Claude Code | Claude Opus 5.5 (claude-opus-5-5) | 2026-11-17 | B | boa 2 | sim (answer) | sim | sim | sim | sim |  |
| Claude Code | Claude Opus 5.5 (claude-opus-5-5) | 2026-11-17 | B | boa 3 | sim (answer) | sim | sim | sim | sim |  |
| Claude Code | Claude Opus 5.5 (claude-opus-5-5) | 2026-11-17 | B | fraca 1 | sim (answer) | sim | sim | sim | sim |  |
| Claude Code | Claude Sonnet 5.5 (claude-sonnet-5-5) | 2026-11-17 | B | boa 1 | sim (answer) | sim | sim | sim | sim |  |
| Claude Code | Claude Sonnet 5.5 (claude-sonnet-5-5) | 2026-11-17 | B | boa 2 | sim (answer) | sim | sim | sim | sim |  |
| Claude Code | Claude Sonnet 5.5 (claude-sonnet-5-5) | 2026-11-17 | B | boa 3 | sim (answer) | sim | sim | sim | sim |  |
| Claude Code | Claude Sonnet 5.5 (claude-sonnet-5-5) | 2026-11-17 | B | fraca 1 | sim (answer) | sim | sim | sim | sim |  |

### Ressalvas desta execução

- Os agentes e o avaliador são da mesma família de modelos (Claude). O avaliador pode compartilhar pontos cegos com os agentes.
- O isolamento das pastas foi por instrução, não por permissão do sistema de arquivos.
- São 16 execuções, com uma amostra e uma pergunta por execução. O resultado mostra que a documentação mudou a resposta nesta pergunta, com estes dados; não é uma taxa de acerto.

## Execução no Antigravity CLI (2026-11-18)

Execução pedida pelo mantenedor, no Antigravity CLI, com o modelo Gemini 4 Hydrogen e a conta Google dele. A seção da execução no Claude Code fica como estava.

- **Banco:** o banco do caso 1 foi montado como diz a seção "Dados entregues ao agente", a partir de `public/downloads/aurora-lab2-fixture.sql`. O conteúdo é idêntico ao da execução no Claude Code.
- **Pastas:** uma cópia isolada por execução, fora do repositório. Na condição A, a pasta tem `caso1.db` e `schema.sql`. Na condição B, tem também `exemplo-evento-coleta-completo.yaml` e `exemplo-decisao-evento-quebrado-completo.yaml`.
- **Ferramenta e modelo:** Antigravity CLI 1.5.10 (`agy`), modelo Gemini 4 Hydrogen (High) (`gemini-4-hydrogen-high`).
- **Comando:** `HOME=<home isolado> agy -p "<prompt>" --model gemini-4-hydrogen-high --sandbox --disable-slash-commands --settings '{"agentMode": "", "toolPermission": "proceed-in-sandbox", "disableSlashCommands": true, "permissions": {"deny": ["write_file(*)"]}}' --print-timeout 1500s`, rodado dentro da pasta da execução. O `HOME` isolado tem login próprio e não carrega a configuração do usuário. A regra de `deny` e o sandbox bloqueiam escrita; um teste confirmou que a consulta com `sqlite3` funciona e que gravar arquivo falha.
- **Execuções:** 3 com a pergunta boa e 1 com a pergunta fraca em cada condição (8 no total), cada uma numa sessão nova, com o prompt literal do protocolo e a instrução de usar só os arquivos da pasta (a mesma do protocolo de onboarding).
- **Avaliador:** Claude Opus 5.5 (claude-opus-5-5), pela rubrica acima, comparando com a Q01. As respostas e as pontuações completas estão em [caso-1-resultados-antigravity.json](./caso-1-resultados-antigravity.json).

### Resumo

| Condição | Pergunta | Execuções | Conclusão igual à da Q01 | Segmenta por operação | Consulta o histórico | Exclui o dia incompleto | Marca generate_lead como quebrado |
|---|---|---|---|---|---|---|---|
| A, sem documentação | boa | 3 | 0 | 3 | 2 | 0 | 0 |
| A, sem documentação | fraca | 1 | 0 | 0 | 0 | 0 | 0 |
| B, com documentação | boa | 3 | 3 | 3 | 3 | 3 | 0 |
| B, com documentação | fraca | 1 | 0 | 1 | 0 | 1 | 0 |

**Leitura:** com a documentação, as 3 execuções da pergunta boa chegaram à conclusão da Q01 e mostraram os três sinais do critério de saída: só o add_to_cart no México parou (5 dias completos em zero), o generate_lead no Brasil está dentro da tolerância de 4 dias, o generate_lead não está ativo no México e o dia 16/11 fica de fora pela regra D+2. Sem a documentação, o modelo não respondeu: nas 3 execuções da pergunta boa pediu esclarecimento (o que conta como normal, como saber se o evento está implementado) e tratou 16/11 como dia completo. Diferente do Claude Code, nenhuma execução marcou o generate_lead como quebrado. Na pergunta fraca, as duas condições disseram que não há dado de hoje e perguntaram a data de referência; só a condição B apontou 15/11 como último dia completo.

**Critério de saída da F4:** atendido nesta ferramenta, com este modelo. Com a documentação, a resposta segmenta por operação e consulta o histórico; sem ela, a resposta não chega à conclusão da Q01. Falta repetir no Codex.

### Execuções

| Ferramenta | Modelo (nome e versão) | Data | Condição | Execução | Categoria certa | Conclusão igual à da Q01 | Segmenta por operação | Consulta o histórico | Exclui o dia incompleto | Observações |
|---|---|---|---|---|---|---|---|---|---|---|
| Antigravity CLI 1.5.10 | Gemini 4 Hydrogen (High) (gemini-4-hydrogen-high) | 2026-11-18 | A | boa 1 | não (clarify) | não | sim | sim | não | pede o critério de normal e de implementação |
| Antigravity CLI 1.5.10 | Gemini 4 Hydrogen (High) (gemini-4-hydrogen-high) | 2026-11-18 | A | boa 2 | não (clarify) | não | sim | não | não | pede o critério de normal, a janela e a implementação |
| Antigravity CLI 1.5.10 | Gemini 4 Hydrogen (High) (gemini-4-hydrogen-high) | 2026-11-18 | A | boa 3 | não (clarify) | não | sim | sim | não | mostra que o generate_lead no Brasil muda com o critério |
| Antigravity CLI 1.5.10 | Gemini 4 Hydrogen (High) (gemini-4-hydrogen-high) | 2026-11-18 | A | fraca 1 | não (abstain) | não | não | não | não | sem dado de hoje; pergunta a data de referência |
| Antigravity CLI 1.5.10 | Gemini 4 Hydrogen (High) (gemini-4-hydrogen-high) | 2026-11-18 | B | boa 1 | sim (answer) | sim | sim | sim | sim |  |
| Antigravity CLI 1.5.10 | Gemini 4 Hydrogen (High) (gemini-4-hydrogen-high) | 2026-11-18 | B | boa 2 | sim (answer) | sim | sim | sim | sim |  |
| Antigravity CLI 1.5.10 | Gemini 4 Hydrogen (High) (gemini-4-hydrogen-high) | 2026-11-18 | B | boa 3 | sim (answer) | sim | sim | sim | sim |  |
| Antigravity CLI 1.5.10 | Gemini 4 Hydrogen (High) (gemini-4-hydrogen-high) | 2026-11-18 | B | fraca 1 | não (abstain) | não | sim | não | sim | sem dado de hoje; aponta 15/11 como último dia completo |

### Ressalvas desta execução

- Um modelo e quatro execuções por condição. O resultado mostra que a documentação mudou a resposta nesta pergunta, com estes dados; não é uma taxa de acerto.
- Na condição A, a pergunta boa recebeu pedido de esclarecimento, não resposta errada. A rubrica conta isso como categoria errada, porque a Q01 espera responder; o pedido do modelo é defensável sem a documentação, que é o que traz o escopo por operação e a tolerância.
- Nas respostas que pedem esclarecimento, os sinais foram marcados pelo que a resposta mostra antes de perguntar.
- O isolamento de leitura foi por instrução e por cópias fora do repositório; a regra de `deny` e o sandbox impedem escrita, não leitura fora da pasta.
- O avaliador é de outra família de modelos, mas não substitui a conferência por uma pessoa da Analytics de E-commerce.
