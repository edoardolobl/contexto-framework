---
title: "Campos: Processo"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Processo."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Processo](../../../templates/processo/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Processo tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Escopo | `scope` | grupo de campos | Quando o processo se aplica. |
| Quando se aplica | `scope.applies_when` | texto | Situações cobertas. |
| Quando não se aplica | `scope.not_applicable_when` | texto | Situações fora do processo. |
| Gatilho | `trigger` | texto | O que dá início ao processo. |
| Pré-condições | `preconditions` | lista de textos | O que precisa existir antes do início. |
| Entradas indispensáveis | `required_inputs` | lista de textos | O que precisa chegar com o pedido. |
| Papéis | `roles` | grupo de campos | Quem responde, executa e aprova, por cargo ou área. |
| Responsável pelo processo | `roles.process_owner` | texto | Cargo ou área. |
| Quem executa | `roles.performers` | lista de textos | Cargos ou áreas. |
| Quem aprova | `roles.approvers` | lista de textos | Cargos ou áreas. |
| Etapas | `steps` | lista de grupos de campos | Uma entrada por etapa, na ordem. |
| Identificador | `steps[].id` | texto | Código curto da etapa (S01, S02). |
| Nome | `steps[].name` | texto | Nome da etapa. |
| Quem executa | `steps[].performer_role` | texto | Cargo ou área. |
| Ação | `steps[].action` | texto | O que é feito. |
| Entradas | `steps[].inputs` | lista de textos | O que a etapa recebe. |
| Evidência | `steps[].output_evidence` | texto | O registro que a etapa deixa. |
| Próxima etapa | `steps[].next_step` | texto | Para onde o pedido vai, inclusive desvios. |
| Prazo | `steps[].deadline` | texto | Quanto tempo a etapa pode esperar. |
| Quando o prazo vence | `steps[].on_deadline` | texto | O que acontece se ninguém agir. |
| Exceções | `steps[].exception_handling` | texto | Como tratar o que sai do esperado. |
| Regras de decisão | `decision_rules` | lista de textos | Identificadores das regras usadas, sem copiar o conteúdo. |
| Encerramento | `completion` | grupo de campos | Como o processo termina. |
| Critério de sucesso | `completion.success_criteria` | lista de textos | O que precisa ser verdade no fim. |
| Resultados de falha | `completion.failure_outcomes` | lista de textos | Formas de encerrar sem sucesso. |
| Registro da evidência | `completion.evidence_record` | texto | Onde a evidência fica guardada. |
| Exceções | `exceptions` | lista de textos | Situações fora do fluxo normal. |
| Escalonamento | `escalation` | texto | Para quem o pedido sobe e quando. |
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
