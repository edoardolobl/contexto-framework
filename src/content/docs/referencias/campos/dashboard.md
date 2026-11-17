---
title: "Campos: Dashboard"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Dashboard."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Dashboard](../../../templates/dashboard/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Dashboard tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Indicadores | `metrics` | lista de textos | Identificadores dos indicadores mostrados. |
| Filtros padrão | `default_filters` | grupo de chaves livres | Filtro e valor aplicados quando o dashboard abre. |
| Dimensões | `dimensions` | lista de textos | Cortes disponíveis. |
| Tempo | `time_semantics` | grupo de campos | Data, fuso, período e comparação. |
| Campo de data | `time_semantics.date_field` | texto | Coluna que decide o dia. |
| Fuso horário | `time_semantics.timezone` | texto | Fuso do fechamento do dia. |
| Período | `time_semantics.reporting_period` | texto | Período coberto. |
| Comparação | `time_semantics.comparison_baseline` | texto | Com o que o número é comparado e desde quando a comparação vale. |
| Atualização | `freshness` | grupo de campos | Frequência, latência e última conferência. |
| Frequência | `freshness.refresh_frequency` | texto | De quanto em quanto tempo atualiza. |
| Latência | `freshness.latency` | texto | Atraso esperado. |
| Conferido em | `freshness.verified_at` | data (AAAA-MM-DD) | Última data em que os números foram conferidos. |
| Oficial ou exploratório | `official_or_exploratory` | texto | Se este dashboard é a fonte oficial do indicador ou um dashboard exploratório. |
| Limitações | `known_limitations` | lista de textos | O que o dashboard não cobre e quando o número não deve apoiar uma decisão. |
| Versão de cada indicador | `metric_versions` | uma entrada por chave, cada uma com texto | Versão que o dashboard segue, por identificador do indicador. |
| Outros dashboards com outro número | `conflicting_dashboards` | lista de grupos de campos | Outro dashboard que mostra outro número para o mesmo dia, com a causa e qual vale. |
| Nome | `conflicting_dashboards[].name` | texto | Nome do outro dashboard. |
| O que mostra | `conflicting_dashboards[].shows` | texto | O número que ele mostra. |
| Causa | `conflicting_dashboards[].cause` | texto | Por que diverge. |
| Qual vale | `conflicting_dashboards[].precedence` | texto | Qual dos dois prevalece. |
| Encontrado em | `conflicting_dashboards[].found_at` | data (AAAA-MM-DD) | Data em que a divergência foi vista. |
| Perguntas de negócio | `reference_questions` | lista de textos | Identificadores dos documentos de Perguntas de negócio ligados. |
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
