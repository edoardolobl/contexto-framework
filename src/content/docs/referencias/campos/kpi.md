---
title: "Campos: Indicador (KPI)"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Indicador (KPI)."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Indicador (KPI)](../../../templates/kpi/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Indicador (KPI) tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Domínio | `domain` | texto | Área do negócio em que o indicador é usado, para filtrar o acervo. |
| Definição de negócio | `business_definition` | grupo de campos | O que o indicador mede, em palavras da área, antes de qualquer fórmula. |
| O que mede | `business_definition.concept` | texto | Uma frase com a unidade contada (pedidos, sessões, clientes); é a parte que mais muda entre versões. |
| Nomes parecidos que medem outra coisa | `business_definition.different_meanings_in_other_domains` | lista de textos | Indicadores de outras áreas com nome parecido que não devem ser usados como sinônimo. |
| Sinônimos | `synonyms` | lista de textos | Nomes que querem dizer exatamente a mesma coisa. Nome parecido com outro significado vai em different_meanings_in_other_domains. |
| Escopo | `scope` | grupo de campos | A quem e a quais canais o indicador se aplica; fora disso, o número não deve ser usado. |
| Canais incluídos | `scope.included_channels` | lista de textos | Canais em que o indicador vale. |
| Canais excluídos | `scope.excluded_channels` | lista de textos | Canais em que o indicador não vale; uma pergunta sobre eles pede abstenção. |
| População | `scope.applicable_population` | texto | O que entra na conta, com os filtros (por exemplo, sessões que não são tráfego interno). |
| Exclusões | `scope.exclusions` | lista de textos | Registros que saem da conta mesmo dentro dos canais incluídos. |
| Cálculo | `calculation` | grupo de campos | Numerador, denominador e regras de agregação. A unidade vem antes da fórmula. |
| Fórmula em palavras | `calculation.formula_description` | texto | A fórmula para leitura humana, sem nomes técnicos de coluna. |
| Numerador | `calculation.numerator` | texto | O que conta em cima, com a regra de repetição (uma sessão com dois pedidos conta uma ou duas vezes). |
| Denominador | `calculation.denominator` | texto | O que conta embaixo, com os filtros. |
| Unidade | `calculation.unit` | texto | Percentual, valor em moeda, quantidade ou outra. |
| Granularidade | `calculation.granularity` | texto | O nível em que o número é calculado (dia, canal, loja). |
| Regra de agregação | `calculation.aggregation_rule` | texto | Como juntar períodos ou grupos; média de taxas costuma dar resultado errado. |
| Ausência de dados | `calculation.null_handling` | texto | Como tratar registro sem valor, sem trocar ausência por zero. |
| Denominador zero | `calculation.zero_denominator_policy` | texto | O que mostrar quando não há nada para dividir. |
| Recálculo do histórico | `history_recalculation` | grupo de campos | Obrigatório quando a versão maior muda (2.0, 3.0): diz se a série antiga é recalculada ou marcada como quebra de método. |
| Política | `history_recalculation.policy` | um destes: recalculate, method_break | recalculate (a série antiga é recalculada pela regra nova) ou method_break (fica como estava e não se compara). |
| O que muda para quem compara | `history_recalculation.description` | texto | Uma frase sobre o efeito para quem compara períodos. |
| Convenções temporais | `time` | grupo de campos | Qual data decide o dia do registro, o fuso e a atualização. |
| Campo de data de referência | `time.reference_date_field` | texto | Coluna que decide em que dia o registro conta. |
| Fuso horário | `time.timezone` | texto | Fuso usado para fechar o dia. |
| Janela | `time.reporting_window` | texto | Período de cálculo (diário, mensal). |
| Atualização | `time.data_freshness` | texto | De quanto em quanto tempo os dados chegam e com que atraso. |
| Fontes | `data_sources` | grupo de campos | De onde vêm os dados e qual fonte vale quando há divergência. |
| Dataset oficial | `data_sources.authoritative_dataset` | texto | Identificador do documento do dataset que manda quando há divergência. |
| Colunas usadas | `data_sources.relevant_columns` | lista de textos | Colunas no formato tabela.coluna. |
| Junções autorizadas | `data_sources.valid_join_paths` | lista de textos | Identificadores dos documentos de relacionamento que podem ser usados. |
| Precedência entre fontes | `data_sources.source_conflicts_and_precedence` | lista de textos | Qual fonte vale quando duas mostram números diferentes. |
| Exemplos e conferência | `validation` | grupo de campos | Casos que mostram a regra aplicada. |
| Exemplos aprovados | `validation.approved_examples` | lista de textos | Casos com números e resultado esperado. |
| Perguntas que o documento responde | `validation.expected_questions_and_answers` | lista de textos | Identificadores de Perguntas de negócio ou perguntas em texto. |
| Casos-limite | `validation.known_edge_cases` | lista de textos | Situações no limite da regra, com o tratamento de cada uma. |
| Testes | `validation.tests` | lista de textos | Testes executáveis ou descritos, quando existirem na data da versão. |
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
