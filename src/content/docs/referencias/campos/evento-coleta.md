---
title: "Campos: Evento de coleta"
description: "Chave, valor aceito e o que escrever em cada campo do modelo Evento de coleta."
---

<!-- Arquivo gerado por scripts/gerar_referencias.py a partir dos schemas e de src/data. Não edite à mão: mude a fonte e rode python3 scripts/gerar_referencias.py. -->

Esta página lista, campo a campo, o modelo [Evento de coleta](../../../templates/evento-coleta/). Para aprender a preencher, siga a página do modelo. Para entender cada coluna da tabela, veja [como ler os campos](../../../fundamentos/como-ler-os-campos/).

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

Depois do cabeçalho, o modelo Evento de coleta tem estes campos.

| Campo | Chave | Valor | O que escrever |
|---|---|---|---|
| Gatilho | `trigger` | texto | A ação da pessoa ou do sistema que faz o evento disparar, escrita como alguém da área descreveria (por exemplo, envio com sucesso de um formulário). Em branco enquanto ninguém confirmou. |
| Parâmetros | `parameters` | lista de grupos de campos | Informações que seguem junto com cada disparo, uma por item. |
| Nome do parâmetro | `parameters[].name` | texto | Chave exatamente como chega na ferramenta de coleta, por exemplo lead_source. |
| Significado | `parameters[].meaning` | texto | O que o valor quer dizer para o negócio, sem repetir a chave. |
| Valor de amostra | `parameters[].example` | texto, número ou sim ou não (true ou false) | Um valor real ou plausível, para quem lê reconhecer o formato. |
| Sempre presente? | `parameters[].required` | sim ou não (true ou false) | true quando todo disparo precisa trazer o parâmetro; false quando pode faltar. |
| Destinos | `destination` | lista de grupos de campos | Para onde o disparo vai depois de coletado: ferramenta, tabela ou contêiner de tags. |
| Ferramenta | `destination[].platform` | texto | Sistema que recebe ou guarda o disparo, como GA4, BigQuery, Databricks ou Google Tag Manager. |
| Onde dentro da ferramenta | `destination[].object` | texto | Propriedade, dataset, tabela ou contêiner específico, com o identificador usado no sistema. |
| Fuso horário | `destination[].timezone` | texto | Fuso em que o dia é contado nesse destino; dois destinos com fusos diferentes dão totais diários diferentes. |
| Observação | `destination[].note` | texto | Detalhe que muda a leitura dos números nesse destino, como atraso de exportação. |
| Onde está ativo | `active_scopes` | lista de grupos de campos | Em que operação, país e marca o evento existe, desde quando e por quê. Zero onde o evento não está ativo é o esperado. |
| Operação | `active_scopes[].operation` | texto | Código da operação avaliada, como BR ou MX; a linha de base é sempre por operação. |
| País | `active_scopes[].country` | texto | País atendido pela operação, por extenso ou em código ISO. |
| Marca | `active_scopes[].brand` | texto | Marca ou site em que o evento foi implementado. |
| Está ativo? | `active_scopes[].active` | sim ou não (true ou false) | true quando o evento foi implementado e deve disparar nesse escopo; false quando não existe lá. |
| Ativo desde | `active_scopes[].since` | data (AAAA-MM-DD) | Primeiro dia em que o evento passou a disparar nesse escopo, no formato AAAA-MM-DD. |
| Motivo | `active_scopes[].reason` | texto | Por que o evento está ou não está ativo ali, para ninguém tratar ausência como defeito. |
| Comportamento esperado | `expected_behavior` | grupo de campos | O ritmo normal do evento por operação, medido em dias completos, e quanto silêncio o time tolera antes de investigar. |
| Frequência esperada | `expected_behavior.expected_frequency` | texto | Com que ritmo o evento costuma disparar, em palavras (por exemplo, poucas vezes por dia, com dias em zero). |
| Linha de base por operação | `expected_behavior.baseline_by_scope` | lista de grupos de campos | O que é normal em cada operação, calculado sobre uma janela de dias completos. |
| Operação | `expected_behavior.baseline_by_scope[].operation` | texto | Código da operação a que os números se referem. |
| Janela | `expected_behavior.baseline_by_scope[].window` | texto | Período de dias completos usado no cálculo, com início e fim. |
| Volume típico por dia | `expected_behavior.baseline_by_scope[].typical_daily` | texto | Média ou mediana de disparos por dia completo, com a medida usada. |
| Dias em zero | `expected_behavior.baseline_by_scope[].zero_days_share` | texto | Quantos dias da janela tiveram zero disparo, em número de dias e não só em porcentagem. |
| Maior sequência em zero | `expected_behavior.baseline_by_scope[].longest_zero_run` | texto | Maior número de dias completos seguidos sem nenhum disparo dentro da janela. |
| Sazonalidade | `expected_behavior.seasonality` | texto | Dias da semana, datas ou campanhas que mudam o volume de forma conhecida. |
| Tolerância ao silêncio | `expected_behavior.silence_tolerance` | lista de grupos de campos | A partir de quantos dias seguidos em zero o time passa a suspeitar, por operação. É escolha do time, não regra universal. |
| Operação | `expected_behavior.silence_tolerance[].operation` | texto | Código da operação a que o limiar se aplica. |
| Regra | `expected_behavior.silence_tolerance[].rule` | texto | Condição que dispara a suspeita, com o número de dias completos e quem escolheu. |
| Quando zero é normal | `expected_behavior.expected_zero_conditions` | lista de textos | Situações em que um dia sem disparo não indica problema, uma por item. |
| Data de lançamento | `launch_date` | data (AAAA-MM-DD) | Primeiro dia em que o evento disparou em produção; antes dele, zero é o esperado. |
| Data de desativação | `retirement_date` | data (AAAA-MM-DD) | Primeiro dia em que o evento deixou de existir; em branco enquanto continua em uso. |
| Nomes anteriores | `renamed_from` | lista de grupos de campos | Outros nomes que o mesmo evento já teve, com o período de cada um, para juntar séries antigas sem perder dias. |
| Nome antigo | `renamed_from[].name` | texto | Como o evento se chamava na coleta antes da troca. |
| Usado a partir de | `renamed_from[].valid_from` | data (AAAA-MM-DD) | Primeiro dia em que o nome antigo foi usado, no formato AAAA-MM-DD. |
| Usado até (sem incluir) | `renamed_from[].valid_to` | data (AAAA-MM-DD) | Primeiro dia em que o nome antigo deixou de ser usado, sem contar esse dia. |
| Consentimento exigido | `consent_requirements` | texto | Que autorização da pessoa o disparo precisa, como o modo de consentimento, e o que acontece com a contagem quando ela recusa. |
| Prazo para os dados chegarem | `late_arrival_window` | texto | Até quando um dia ainda pode receber disparos atrasados; antes desse prazo, o dia não conta como completo. |
| Chave de deduplicação | `deduplication_key` | texto | Campo ou combinação que identifica o mesmo disparo repetido, para contar uma vez só. |
| Indicadores que dependem do evento | `downstream_kpis` | lista de textos | Indicadores calculados a partir deste evento, pelo identificador quando já existe definição aprovada. |
| Exceções conhecidas | `known_exceptions` | lista de grupos de campos | Períodos ou situações já explicados em que o volume foge do normal sem ser falha. |
| Situação | `known_exceptions[].condition` | texto | O que aconteceu, como manutenção programada ou campanha fora do comum. |
| Período | `known_exceptions[].period` | texto | Dias afetados, com início e fim. |
| Evidência | `known_exceptions[].evidence` | texto | Chamado, comunicado ou registro que confirma a situação. |
| Consulta de conferência | `validation_query` | texto | Consulta SQL que recalcula a contagem diária por operação na fonte oficial, para conferir a linha de base. |
| Dia sem linha na tabela | `missing_days_policy` | texto | Como ler a falta de registro de um dia: se vale zero, se é dia incompleto ou se é falha de carga. |
| Nota sobre a granularidade | `grain_note` | texto | O que uma linha da tabela diária representa, como um dia de uma operação, para não somar coisas de níveis diferentes. |
| Incidentes nos dados | `data_incidents` | lista de grupos de campos | Problemas já investigados que distorceram a contagem, com o efeito na linha de base. |
| Início | `data_incidents[].start` | data (AAAA-MM-DD) | Primeiro dia afetado, no formato AAAA-MM-DD. |
| Fim | `data_incidents[].end` | data (AAAA-MM-DD) | Último dia afetado, no formato AAAA-MM-DD; em branco se ainda não acabou. |
| O que aconteceu | `data_incidents[].description` | texto | Causa e sintoma em uma ou duas frases. |
| Efeito na linha de base | `data_incidents[].effect_on_baseline` | texto | Se os dias afetados saíram do cálculo ou foram corrigidos, e como. |
| Situação do incidente | `data_incidents[].status` | texto | Em investigação, corrigido ou aceito, com a data da última atualização se houver. |
| Não confundir | `disambiguation` | lista de grupos de campos | Termos ou eventos parecidos que levam a contar a coisa errada. |
| Termo | `disambiguation[].term` | texto | A palavra ou nome de evento que gera confusão. |
| Quer dizer | `disambiguation[].means` | texto | O que o termo significa neste documento. |
| Não confundir com | `disambiguation[].not_to_confuse_with` | texto | O evento ou conceito parecido que conta outra coisa. |
| Documentos relacionados | `related_documents` | lista de textos | Identificadores de outros documentos que ajudam a ler este, como a regra de evento quebrado. |

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
