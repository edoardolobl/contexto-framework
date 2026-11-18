---
title: "Campos: Dataset"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Dataset."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Dataset](../../../templates/dataset/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Dataset tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Tabela | `dataset` | grupo de campos | Identificação física e o que uma linha representa. |
| Nome físico | `dataset.physicalName` | texto | Nome da tabela no banco. |
| Plataforma | `dataset.platform` | texto | Onde a tabela está. |
| Granularidade | `dataset.grain` | texto | O que uma linha representa; sem isso, contagens saem erradas. |
| Chave primária | `dataset.primary_key` | texto | Coluna que identifica cada linha. |
| Chaves alternativas | `dataset.alternative_keys` | lista de textos | Outras colunas que também identificam a linha. |
| Critério de unicidade | `dataset.uniqueness_assumption` | texto | O que se supõe único e o que fazer com repetições. |
| Colunas | `columns` | lista de grupos de campos | Uma entrada por coluna. |
| Nome físico | `columns[].physicalName` | texto | Nome da coluna como está no banco. |
| Tipo técnico | `columns[].physicalType` | texto | Tipo no banco (TEXT, INTEGER). |
| Nome de negócio | `columns[].businessName` | texto | Nome que a área usa. |
| Significado | `columns[].meaning` | texto | O que o valor quer dizer, inclusive códigos. |
| Unidade | `columns[].unit` | texto | Unidade do valor, quando houver. |
| Valores permitidos | `columns[].allowed_values` | lista de valores livres | Lista fechada de valores, quando houver. |
| Códigos especiais | `columns[].sentinel_values` | lista de valores livres | Valores que significam outra coisa (como 9999 para sem data). |
| Significado do vazio | `columns[].null_meaning` | texto | O que quer dizer a coluna sem valor. |
| Exemplos | `columns[].examples` | lista de valores livres | Valores reais ou de amostra. |
| Não usar para | `columns[].do_not_use_for` | lista de textos | Usos que levam a erro. |
| Tempo | `time_semantics` | grupo de campos | Data de referência, fuso e atualização. |
| Campo de data | `time_semantics.reference_field` | texto | Coluna que decide o dia de cada linha. |
| Fuso horário | `time_semantics.timezone` | texto | Fuso da data gravada. |
| Frequência de atualização | `time_semantics.update_frequency` | texto | De quanto em quanto tempo chegam dados. |
| Atraso conhecido | `time_semantics.known_latency` | texto | Quanto tempo leva para um registro aparecer. |
| Fotografia ou eventos | `time_semantics.snapshot_or_events` | texto | Se a tabela guarda uma fotografia por data ou cada evento. |
| Uso | `usage` | grupo de campos | Perguntas que a tabela responde e armadilhas. |
| Perguntas que responde | `usage.authoritative_questions` | lista de textos | Perguntas para as quais esta tabela é a fonte oficial. |
| Agregações proibidas | `usage.invalid_aggregations` | lista de textos | Contas que dão número errado com esta tabela. |
| Datasets relacionados | `usage.related_datasets` | lista de textos | Outras tabelas usadas junto, pelo identificador quando houver documento. |
| Armadilhas conhecidas | `usage.known_caveats` | lista de textos | Ressalvas com o efeito no número. |
| Consultas de exemplo | `usage.sample_queries` | lista de textos | Arquivos ou consultas que existiam na data da versão. |
| Conferência | `validation` | grupo de campos | Quem conferiu, quando e com que evidência. |
| Conferido por | `validation.checked_by` | texto | Cargo ou área. |
| Conferido em | `validation.checked_at` | data (AAAA-MM-DD) | Data da conferência. |
| Evidência | `validation.evidence` | lista de textos | Arquivos ou registros usados na conferência. |
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
