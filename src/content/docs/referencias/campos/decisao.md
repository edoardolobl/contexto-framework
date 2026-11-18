---
title: "Campos: Regra e decisão"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Regra e decisão."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Regra e decisão](../../../templates/decisao/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

## Cabeçalho comum

Todo documento começa com estes campos, na mesma ordem.

| Campo | Chave | Obrigatório |
|---|---|---|
| Identificador do assunto | `id` | Sim |
| Versão do formato | `schema_version` | Não |
| Tipo de documento | `type` | Não |
| Título | `title` | Sim |
| Versão atual | `version` | Sim |
| Identificador desta versão | `revision_id` | Não |
| Estado | `status` | Sim |
| Responsável (cargo ou área) | `owner` | Sim |
| Quem aprova (cargo ou área) | `approver` | Sim |
| Vale a partir de | `valid_from` | Não |
| Primeiro dia em que já não vale | `valid_to` | Não |
| Data em que esta versão foi registrada | `recorded_at` | Não |
| Data desta versão | `version_date` | Sim |
| Última revisão | `last_reviewed` | Não |
| De quanto em quanto tempo revisar | `review_interval` | Não |
| Fonte oficial | `source_of_truth` | Não |
| Substitui qual versão? | `supersedes_revision` | Não |
| Substituída por qual versão? | `superseded_by_revision` | Não |
| Licença | `license` | Não |
| Endereço publicado | `source_url` | Não |
| Pergunta de negócio que o documento responde | `intent.question` | Sim |
| Quem usa | `intent.audience` | Não |
| Para quê | `intent.purpose` | Não |
| Decisões que apoia | `intent.decisions` | Não |
| Em poucas palavras | `plain_summary` | Não |
| Perguntas em aberto | `open_questions` | Não |
| Histórico de versões | `version_history` | Não |

## Campos do tipo

Depois do cabeçalho, o modelo Regra e decisão tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Escopo | `scope` | grupo de campos | Quando a regra se aplica. |
| Quando se aplica | `scope.applies_when` | texto | Situações em que a regra decide. |
| Quando não se aplica | `scope.not_applicable_when` | texto | Situações fora da regra. |
| Entradas | `required_inputs` | lista de grupos de campos | Cada entrada com os valores possíveis e a definição verificável. |
| Nome | `required_inputs[].name` | texto | Nome da entrada, igual ao usado na tabela. |
| Valores possíveis | `required_inputs[].allowed_values` | lista de valores livres | Lista fechada; unknown quando a entrada pode faltar. |
| Definição | `required_inputs[].definition` | texto | Como saber o valor sem depender de quem confere. |
| Resultados possíveis | `possible_outputs` | lista de textos | Todos os resultados que a tabela pode dar. |
| Tabela de decisão | `decision_table` | lista de grupos de campos | Cada linha com as condições (when) e o resultado (then); any vale para qualquer valor. |
| Condições | `decision_table[].when` | grupo de chaves livres | Valor de cada entrada, ou any. |
| Resultado | `decision_table[].then` | texto | Um dos resultados possíveis. |
| Precedência | `priority_rules` | lista de textos | O que fazer se duas linhas valerem ao mesmo tempo. |
| Resultado padrão | `default_behavior` | texto | Resultado quando nenhuma linha vale. |
| Entrada desconhecida | `unknown_input_behavior` | texto | Resultado quando falta uma entrada. |
| Exceções | `exceptions` | lista de grupos de campos | Situações fora da regra. |
| Condição | `exceptions[].condition` | texto | Quando a exceção vale. |
| Quem aprova | `exceptions[].approval_role` | texto | Cargo ou área que autoriza a exceção. |
| Evidência exigida | `exceptions[].evidence_needed` | texto | O que precisa ser anexado. |
| Testes | `tests` | lista de grupos de campos | Pedidos reais com as entradas e o resultado esperado. |
| Caso | `tests[].case` | texto | O pedido descrito como chegou. |
| Entradas | `tests[].inputs` | grupo de chaves livres | Valor de cada entrada neste caso. |
| Resultado esperado | `tests[].expected_outcome` | texto | Um dos resultados possíveis. |
| Justificativa | `tests[].reasoning` | texto | Por que este é o resultado. |
| Conflitos | `conflicts` | lista de valores livres | Conflitos com outras regras. |
| Documentos relacionados | `related_documents` | lista de textos | Identificadores de outros documentos que ajudam a ler este. |

## Para quem é técnico

Blocos opcionais, iguais em todos os modelos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Contexto para agentes (para quem é técnico) | `context` | grupo de campos | Bloco opcional, com as chaves do ODCS 3.2.0. Use só para o que não cabe nos campos estruturados; o significado continua nos campos do tipo. |
| Instrução ao agente | `context.instructions` | texto | Instrução curta em texto, até 500 caracteres. Quando preenchida, review_interval deixa de poder ficar em branco, para a instrução não envelhecer sem revisão. |
| Perguntas verificadas | `context.verifiedStatements` | lista de grupos de campos | Perguntas típicas do assunto, no formato do ODCS 3.2.0: cada item tem a pergunta e, quando já conferida por quem aprova, a resposta que um agente pode repetir sem recalcular. |
| Pergunta | `context.verifiedStatements[].question` | texto | A pergunta como alguém da área faria. |
| Resposta verificada | `context.verifiedStatements[].answer` | texto | A resposta já conferida por quem aprova. Sem ela, o item registra só a pergunta típica. |
| Limites | `context.constraints` | lista de grupos de campos | O que um agente não pode fazer com este documento, como comparar períodos de regras diferentes. Cada item segue o formato do ODCS 3.2.0. |
| Limite | `context.constraints[].constraint` | texto | Uma coisa que o agente não pode fazer, em uma frase. |
| Onde mora a regra executável (para quem é técnico) | `authoritativeDefinitions` | lista de grupos de campos | Lista opcional de lugares com a versão executável da regra (consulta SQL, metric view, filtro). O documento aponta, sem copiar o código; se a regra mudar lá, o documento precisa de nova versão. |
| Tipo | `authoritativeDefinitions[].type` | um destes: sql, metricView, filter, dashboard, document, other | sql (consulta), metricView, filter (filtro salvo), dashboard, document ou other. |
| Endereço | `authoritativeDefinitions[].url` | texto | Caminho do arquivo ou endereço onde a regra está. Arquivo citado precisa existir na data da versão. |
| Descrição | `authoritativeDefinitions[].description` | texto | O que a regra executável calcula e para qual versão do documento. |
