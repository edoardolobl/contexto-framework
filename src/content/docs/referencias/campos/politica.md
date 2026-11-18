---
title: "Campos: Política"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Política."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Política](../../../templates/politica/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Política tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Escopo | `scope` | grupo de campos | Quem e o que a política abrange. |
| Quem é abrangido | `scope.audiences` | lista de textos | Cargos, áreas ou grupos. |
| Atividades | `scope.activities` | lista de textos | Atividades cobertas. |
| Localidades | `scope.localities` | lista de textos | Unidades ou regiões cobertas. |
| Exclusões | `scope.exclusions` | lista de textos | O que fica fora, com a política que cobre. |
| Autoridade da política | `authority` | grupo de campos | Dados da própria política, que podem ser diferentes dos deste registro. |
| Quem emitiu | `authority.issuing_body` | texto | Cargo ou área. |
| Quem aprova a política | `authority.approver_role` | texto | Cargo ou área. |
| Versão da política | `authority.version` | texto | A versão da política em si, não a deste registro. |
| Início da vigência da política | `authority.effective_date` | data (AAAA-MM-DD) | Data em que a política passou a valer. |
| Fim da vigência da política | `authority.expiry_date` | data (AAAA-MM-DD) | Data em que a política deixa de valer, se houver. |
| Substitui | `authority.supersedes` | texto | Política anterior e o que ela dizia. |
| Obrigações | `obligations` | lista de textos | O que é obrigatório. |
| Permissões | `permissions` | lista de textos | O que é permitido. |
| Proibições | `prohibitions` | lista de textos | O que é proibido. |
| Exceções | `exceptions` | lista de grupos de campos | Situações fora da regra. |
| Condição | `exceptions[].condition` | texto | Quando a exceção vale. |
| Quem aprova | `exceptions[].approval_role` | texto | Cargo ou área que autoriza a exceção. |
| Evidência exigida | `exceptions[].evidence_needed` | texto | O que precisa ser anexado. |
| Fontes em conflito | `conflicting_sources` | lista de grupos de campos | Uma entrada por conflito; quando resolvido, com resolução, quem resolveu e a data. |
| Identificador | `conflicting_sources[].id` | texto | Código do conflito. |
| Fontes | `conflicting_sources[].sources` | lista de textos | Identificadores das fontes em conflito. |
| Descrição | `conflicting_sources[].description` | texto | O que diverge. |
| Posições | `conflicting_sources[].positions` | lista de grupos de campos | O que cada fonte diz. |
| Fonte | `conflicting_sources[].positions[].source` | texto | Onde está escrito, com data ou versão. |
| O que diz | `conflicting_sources[].positions[].says` | texto | A regra segundo esta fonte. |
| Impacto | `conflicting_sources[].impact` | texto | O que muda conforme a fonte consultada. |
| Estado | `conflicting_sources[].state` | um destes: unresolved, resolved | unresolved ou resolved. |
| Quem resolve | `conflicting_sources[].resolution_owner` | texto | Cargo ou área com autoridade. |
| Resolução | `conflicting_sources[].resolution` | texto | O que foi decidido. |
| Resolvido em | `conflicting_sources[].resolved_at` | data (AAAA-MM-DD) | Data da resolução. |
| Regra de precedência | `source_precedence_rule` | texto | Qual fonte prevalece quando duas discordam. |
| Como conferir | `how_to_verify` | texto | Onde olhar para saber se a política mudou. |
| Quando revisar | `review_trigger` | texto | O que dispara uma revisão deste registro. |
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
