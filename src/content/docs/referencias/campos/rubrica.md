---
title: "Campos: Rubrica de avaliação"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Rubrica de avaliação."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Rubrica de avaliação](../../../templates/rubrica/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Rubrica de avaliação tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| O que se avalia | `evaluation_target` | texto | O trabalho avaliado, não a pessoa. |
| Usos permitidos | `allowed_use` | lista de textos | Para que a nota pode servir. |
| Usos proibidos | `disallowed_use` | lista de textos | Para que a nota não pode servir. |
| Critérios | `criteria` | lista de grupos de campos | Uma entrada por critério. |
| Identificador | `criteria[].id` | texto | Código do critério, usado na calibração. |
| Nome | `criteria[].name` | texto | Nome do critério. |
| Definição | `criteria[].definition` | texto | O que o critério avalia. |
| O que não avalia | `criteria[].not_in_scope` | texto | Para não punir o mesmo erro duas vezes. |
| Peso | `criteria[].weight` | número | Peso do critério; os pesos somam 100. |
| Evidências aceitas | `criteria[].expected_evidence` | lista de textos | O que o revisor procura. |
| Níveis | `criteria[].anchors` | grupo de campos | O que se vê no trabalho em cada nível, de 0 a 4. |
| Nível | `criteria[].anchors.0` | texto | O que se vê no trabalho neste nível. |
| Nível | `criteria[].anchors.1` | texto | O que se vê no trabalho neste nível. |
| Nível | `criteria[].anchors.2` | texto | O que se vê no trabalho neste nível. |
| Nível | `criteria[].anchors.3` | texto | O que se vê no trabalho neste nível. |
| Nível | `criteria[].anchors.4` | texto | O que se vê no trabalho neste nível. |
| Nota | `scoring` | grupo de campos | Como a nota é calculada e o que ela alimenta. |
| Soma dos pesos | `scoring.weight_sum` | número inteiro | Deve ser 100. |
| Escala | `scoring.scale` | lista de números | Níveis possíveis. |
| Fórmula | `scoring.formula` | texto | Como a nota sai dos níveis e pesos. |
| Sem evidência | `scoring.missing_evidence_behavior` | texto | not_evaluable: falta de evidência não vira zero em silêncio. |
| Critério não avaliável | `scoring.not_evaluable_rule` | texto | Como a nota é calculada sem um critério. |
| Decisão alimentada | `scoring.feeds_decision` | texto | Documento e entrada que a nota alimenta, e a partir de qual nível. |
| Limiar | `scoring.decision_threshold` | texto | Nota mínima, se houver. |
| Decisão automática | `scoring.automatic_decision_allowed` | sim ou não (true ou false) | Sempre false: uma pessoa revisa. |
| Revisão humana obrigatória | `human_review_required` | sim ou não (true ou false) | Sempre true. |
| Exemplos de calibração | `calibration_examples` | lista de grupos de campos | Trabalhos já avaliados, com nível, justificativa, nota e encaminhamento. |
| Caso | `calibration_examples[].case` | texto | O trabalho avaliado, com data. |
| Níveis | `calibration_examples[].levels` | uma entrada por chave, cada uma com número inteiro | Nível de cada critério, pelo identificador. |
| Justificativa | `calibration_examples[].justification` | uma entrada por chave, cada uma com texto | Motivo de cada nível, pelo identificador. |
| Nota | `calibration_examples[].score` | número | Nota recalculada pela fórmula. |
| Evidência suficiente | `calibration_examples[].evidence_sufficient` | sim ou não (true ou false) | Valor que a nota dá à entrada da decisão. |
| Encaminhamento | `calibration_examples[].routing` | texto | Resultado da tabela de decisão. |
| Discordância entre revisores | `disagreement_resolution` | texto | Como resolver e quem decide. |
| Privacidade e justiça | `privacy_and_fairness_considerations` | lista de textos | Cuidados com quem produziu o trabalho. |
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
