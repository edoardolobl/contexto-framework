---
title: "Campos: Conceito"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Conceito."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Conceito](../../../templates/conceito/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Conceito tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Domínio | `domain` | texto | Área em que o termo tem este significado; em outra área ele pode querer dizer outra coisa. |
| Aplicabilidade | `scope` | grupo de campos | Quando a definição vale e quando não deve ser usada. |
| Quando se aplica | `scope.applies_when` | texto | Situações em que a definição deve ser usada. |
| Quando não se aplica | `scope.does_not_apply_when` | texto | Situações em que usar a definição leva a erro. |
| Vocabulário (SKOS) | `vocabulary` | grupo de campos | Termo preferido, sinônimos, termo mais amplo, relacionados e o que não confundir. |
| Termo preferido | `vocabulary.prefLabel` | texto | O nome que todos devem usar nos relatórios. |
| Sinônimos | `vocabulary.altLabel` | lista de textos | Nomes de fato equivalentes; nome só parecido vai em related ou not_synonyms. |
| Termo mais amplo | `vocabulary.broader` | lista de textos | Conceito que inclui este (por exemplo, participante inclui participante ativo). |
| Termos relacionados | `vocabulary.related` | lista de textos | Termos ligados a este que não são equivalentes. |
| Não confundir com | `vocabulary.not_synonyms` | lista de textos | Termos que parecem sinônimos e não são; o erro mais comum fica aqui. |
| Significados em outras áreas | `vocabulary.other_domain_meanings` | lista de textos | O que a mesma palavra quer dizer em outra área. |
| Definição | `definition` | texto | Definição completa, com período e condições, que permita classificar um caso sem perguntar a ninguém. |
| Critérios de inclusão | `inclusion_criteria` | lista de textos | Condições que, juntas, fazem um caso pertencer ao conceito. |
| Critérios de exclusão | `exclusion_criteria` | lista de textos | Condições que tiram um caso do conceito, com o nome do que ele passa a ser. |
| Exemplos | `examples` | lista de textos | Casos concretos que pertencem, com datas. |
| Contraexemplos | `counterexamples` | lista de textos | Casos concretos que não pertencem, com o motivo. |
| Casos-limite | `boundary_cases` | lista de textos | Casos no limite da definição e como classificá-los. |
| Confirmação | `validation` | grupo de campos | Quem confirmou o significado e com que evidência. |
| Confirmado por | `validation.decisions_confirmed_by` | texto | Cargo ou área que confirmou. |
| Evidência | `validation.confirmation_evidence` | texto | Documento que registra a confirmação, como uma ata. |
| Histórico de revisões | `validation.review_history` | lista de textos | Revisões do significado, com data. |
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
