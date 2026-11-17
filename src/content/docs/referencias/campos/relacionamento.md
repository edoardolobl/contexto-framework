---
title: "Campos: Relacionamento entre tabelas"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Relacionamento entre tabelas."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Relacionamento entre tabelas](../../../templates/relacionamento/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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
| Pergunta de negócio que o documento responde | `intent.question` | Sim |
| Quem usa | `intent.audience` | Não |
| Para quê | `intent.purpose` | Não |
| Decisões que apoia | `intent.decisions` | Não |
| Em poucas palavras | `plain_summary` | Não |
| Perguntas em aberto | `open_questions` | Não |
| Histórico de versões | `version_history` | Não |

## Campos do tipo

Depois do cabeçalho, o modelo Relacionamento entre tabelas tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Tabela | `left` | grupo de campos | Uma das duas tabelas e o que uma linha representa. |
| Tabela | `left.dataset` | texto | Nome físico da tabela. |
| Granularidade | `left.grain` | texto | O que uma linha representa. |
| Tabela | `right` | grupo de campos | Uma das duas tabelas e o que uma linha representa. |
| Tabela | `right.dataset` | texto | Nome físico da tabela. |
| Granularidade | `right.grain` | texto | O que uma linha representa. |
| Chaves da junção | `join_keys` | lista de grupos de campos | Pares de colunas que ligam as duas tabelas. |
| Coluna da esquerda | `join_keys[].left` | texto | Coluna da tabela left. |
| Coluna da direita | `join_keys[].right` | texto | Coluna da tabela right. |
| Cardinalidade | `cardinality` | um destes: one_to_one, one_to_many, many_to_many | one_to_one, one_to_many ou many_to_many; um para muitos repete a linha da esquerda. |
| Cobertura | `coverage` | grupo de campos | Linhas sem par, chaves vazias e regra de tempo. |
| Linhas sem par esperadas | `coverage.unmatched_rows_expected` | sim ou não (true ou false) | true se é normal haver linha sem correspondente. |
| Chaves vazias esperadas | `coverage.null_keys_expected` | sim ou não (true ou false) | true se é normal haver chave sem valor. |
| Regra de tempo | `coverage.temporal_join_rule` | texto | Em que data o registro ligado conta. |
| Regras de uso | `usage_rules` | grupo de campos | O que a junção responde e como evitar contagem dobrada. |
| Perguntas autorizadas | `usage_rules.approved_question_classes` | lista de textos | Perguntas que a junção responde. |
| Perguntas proibidas | `usage_rules.disallowed_question_classes` | lista de textos | Perguntas que a junção responde errado. |
| Estratégia por pergunta | `usage_rules.join_strategy_by_question` | lista de textos | Como juntar para cada tipo de pergunta. |
| Riscos de duplicação | `usage_rules.duplication_risks` | lista de textos | Quando uma linha aparece mais de uma vez. |
| Cuidados antes de agregar | `usage_rules.aggregation_safeguards` | lista de textos | O que fazer antes de somar ou dividir. |
| Conferência | `validation` | grupo de campos | Casos conferidos e consulta verificada. |
| Casos conferidos | `validation.test_cases` | lista de textos | Situações conferidas com o resultado. |
| Consulta verificada | `validation.verified_query` | texto | Arquivo ou consulta que implementa a junção, se existia na data da versão. |
| Revisado por | `validation.reviewer` | texto | Cargo ou área. |
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
