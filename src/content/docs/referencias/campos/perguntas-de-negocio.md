---
title: "Campos: Perguntas de negócio"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Perguntas de negócio."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Perguntas de negócio](../../../templates/perguntas-de-negocio/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Perguntas de negócio tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Domínio | `domain` | texto | Assunto coberto pelas perguntas. |
| Documentos cobertos | `covered_documents` | lista de textos | Identificadores dos documentos que as respostas usam. |
| Versões em que as respostas se apoiam | `depends_on_versions` | uma entrada por chave, cada uma com texto | Versão de cada documento coberto; quando uma muda, as respostas que dependem dele são conferidas de novo. |
| Perguntas | `questions` | lista de grupos de campos | Uma entrada por pergunta. |
| Identificador | `questions[].id` | texto | Código curto da pergunta (Q01). |
| Pergunta | `questions[].question` | texto | Como alguém da área faria. |
| O que a pessoa quer saber | `questions[].goal` | texto | O objetivo por trás da pergunta. |
| O que a pergunta supõe | `questions[].assumptions` | texto | Canal, período ou filtro que a pergunta supõe. |
| Outras formas de perguntar | `questions[].phrasings` | lista de textos | Opcional: variações da mesma pergunta. |
| Pergunta de entrada | `questions[].onboarding` | sim ou não (true ou false) | Opcional: true se todo agente novo precisa acertar esta pergunta. |
| Comportamento esperado | `questions[].expected_behavior` | um destes: answer, clarify, abstain | answer (responder), clarify (pedir esclarecimento) ou abstain (não responder). |
| Outras formas aceitas | `questions[].also_accepted` | lista de grupos de campos | Opcional. Outros comportamentos que também valem, cada um com a condição que a resposta precisa cumprir. Não repete o comportamento esperado. |
| Comportamento aceito | `questions[].also_accepted[].behavior` | um destes: answer, clarify, abstain | answer (responder), clarify (pedir esclarecimento) ou abstain (não responder); diferente do comportamento esperado. |
| Condição | `questions[].also_accepted[].condition` | texto | O que a resposta precisa fazer para valer. |
| Resposta esperada | `questions[].reference_answer` | texto | A resposta conferida; null quando o comportamento é não responder. |
| Consulta da resposta | `questions[].reference_sql` | texto | Opcional, para quem é técnico: arquivo ou consulta que calcula a resposta. |
| Fontes | `questions[].required_sources` | lista de textos | Documentos e arquivos que sustentam a resposta. |
| Evidência | `questions[].evidence_description` | texto | O que a fonte mostra. |
| Ambiguidade | `questions[].ambiguity` | texto | O que falta na pergunta; obrigatório quando o comportamento é pedir esclarecimento. |
| Motivo para não responder | `questions[].reason_if_abstain` | texto | Obrigatório quando o comportamento é não responder. |
| Conferido por | `questions[].reviewed_by` | texto | Cargo ou área que conferiu a resposta. |
| Conferido em | `questions[].reviewed_at` | data (AAAA-MM-DD) | Data da conferência; não pode ser anterior aos dados usados. |
| Quando conferir de novo | `revalidation_triggers` | lista de textos | Mudanças que obrigam a conferir as respostas. |
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
