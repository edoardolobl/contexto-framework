# Incorporações das pesquisas externas

Data: 2026-11-17 · Commit: d08c810 · Escopo: o que três pesquisas externas do mantenedor (feitas com Claude, Codex e Gemini) acrescentam ao roteiro de [10-direcao-proposta.md](./10-direcao-proposta.md), já com as decisões de [11-decisoes.md](./11-decisoes.md)

> Registro de planejamento. Nenhum arquivo do portal foi alterado. As três pesquisas ficam fora do repositório; o que foi aproveitado delas está resumido aqui com a origem de cada ideia. Afirmações vindas delas ainda precisam de fonte primária antes de ir para o portal (ver "Cuidados").

## Resumo

- As três pesquisas confirmam a direção "da pergunta ao documento aprovado" e não pedem mudança de rumo.
- O ganho está no detalhe de quatro fases: F0 (duas checagens novas), F3 (campos alinhados ao ODCS e regra de recálculo), F4 (Evento de coleta completo e banco de cenários) e F5 (sequência didática com cinco degraus).
- Muda um critério de saída: o llms.txt deixa de ser a prova da F6, e o lugar dele vai para um kit mínimo para agentes.
- Três decisões novas foram tomadas (12 a 14, registradas em [11-decisoes.md](./11-decisoes.md)): núcleo de cinco tipos, oito dimensões como checklist e chaves em inglês com rótulos em português.

## Itens de interface

A revisão de UI e UX com a tasteskill 2.5.1 ([13-ui-ux-tasteskill.md](./13-ui-ux-tasteskill.md)) acrescenta, antes da F0, dois ADRs (sistema visual e tamanho máximo de página de modelo) e uma captura de referência; na F1, correções baratas de título, toque, contraste e compartilhamento; na F2, o `h1` da home; na F5, um checklist visual por PR. O limite de 4 telas por página de modelo condiciona a sequência didática do I-24.

## Origem das ideias

| Sigla | Pesquisa |
|---|---|
| CL | "Contexto: o que a evidência diz e o que mudar no guia" (pesquisa feita com Claude) |
| CX | "Pesquisa aprofundada para o projeto Contexto" (pesquisa feita com Codex) |
| GE | "Pesquisa Aplicada e Redesenho Arquitetural para o Projeto Contexto" (pesquisa feita com Gemini) |

## Incorporações por fase

### F0. Decisões e trilhos

| # | Incorporação | Origem |
|---|---|---|
| I-01 | Validador recusa caracteres Unicode invisíveis em `.md`, `.yaml`, `AGENTS.md` e `SKILL.md`, que podem esconder instruções (ataque "Rules File Backdoor", Pillar Security, 2025). | GE |
| I-02 | Validador recusa descrição de campo que só repete o nome do campo. A descrição precisa dizer regra de interpretação, tratamento de nulo ou ressalva de grão. | GE |
| I-03 | Tabela de evidências por tipo de fonte em toda página com fundamentação: norma, pesquisa revisada por pares, prática de mercado, relato de fornecedor e convenção do Contexto. Remover números de impacto sem fonte aplicável. | CX, CL |
| I-04 | ADRs para as decisões 12 a 14, além das 11 já registradas. | (decisão) |

### F2. Porta de entrada

| # | Incorporação | Origem |
|---|---|---|
| I-05 | Núcleo de entrada com cinco tipos: Indicador, Dataset com relacionamentos, Evento de coleta, Regra e decisão (inclui detecção de anomalia) e Perguntas de negócio. Conceito, Política, Processo e Dashboard ficam no segundo nível; Rubrica na trilha complementar (decisões 2 e 12). | CL, GE, CX |
| I-06 | Entradas por sintoma e por tarefa na home: "a IA calculou meu KPI errado", "como saber se um evento parou de coletar", "duas ferramentas dão números diferentes", "como documentar uma junção sem duplicar contagens", "como preparar esta fonte para um agente". | CX, CL |
| I-07 | Oito dimensões viram checklist de revisão, marcado como convenção do Contexto. Escopo, vigência, evidência e responsável passam a ser metadados comuns no cabeçalho de todo documento (decisão 13). | CX, CL, GE |
| I-08 | Página de descoberta reescrita como entrevista por incidente real (Critical Decision Method), com as oito famílias de perguntas: incidente, fronteira, contraste, pista, escopo, contrafactual, proveniência e reprodução. Inclui o roteiro de 20 minutos levando um rascunho imperfeito ao especialista. "5 porquês" só como heurística para chegar à regra. | CX, GE, CL |
| I-09 | Tipo Perguntas de negócio nasce com o banco de perguntas exemplares por tipo de documento que as três pesquisas trazem, ensinadas como perguntas que mudam uma decisão, não como questionário. | CL, CX, GE |
| I-10 | Teste com pessoas mede aprendizagem, não satisfação: rodadas de 5 a 8 participantes, pré-teste, tarefa observada, pós-teste em caso não visto e retenção. Métrica principal: "a definição escrita pelo participante fez a IA acertar o gabarito?". Complementa o card sorting e o tree test já previstos. | CL, CX, GE |

### F3. Schema 1.0 (migração para Markdown com frontmatter)

| # | Incorporação | Origem |
|---|---|---|
| I-11 | Chaves em inglês iguais às do ODCS 3.2.0 onde houver equivalente: bloco `context` com `instructions`, `verifiedStatements` e `constraints`, além de `synonyms`. Rótulos e explicações em português no Markdown e no portal (decisão 14). A nossa pesquisa confirma o bloco `context` do ODCS 3.2.0 ([08-pesquisa-boas-praticas.md](./08-pesquisa-boas-praticas.md), seção de agentes e protocolos). | CL, GE |
| I-12 | Glossário com a estrutura do SKOS: termo preferido, sinônimos, termo mais amplo, relacionados e "não confundir com" (o atual `not_synonyms`). | GE, CX, CL |
| I-13 | Três camadas separadas em todo documento: significado em linguagem humana, regra executável (SQL, metric view, filtro) e instrução ao agente. Campo que registra onde mora a versão executável. Instrução em texto só quando não há alternativa estruturada, e curta. | CL, CX, GE |
| I-14 | Toda versão maior de Indicador exige regra de recálculo do histórico (a série antiga é recalculada ou marcada como quebra de método). | CL, GE |
| I-15 | Bitemporalidade proporcional: `valid_from` e `valid_to` em todo documento; `recorded_at` só onde é preciso responder "o que sabíamos naquela data". | CX |
| I-16 | Resumo em linguagem direta ao lado de toda definição formal ("conta só pedidos pagos até sete dias após o lead"). | CX, CL |
| I-17 | Seções autocontidas para RAG e NotebookLM: id, escopo e vigência repetidos no título ou subtítulo de cada bloco; tabelas inteiras, nunca achatadas em texto. Resolve a tensão com o item de [10-direcao-proposta.md](./10-direcao-proposta.md) que concentra ressalvas numa página: cada página leva uma frase curta de ressalva e um link. | CL, GE |

### F4. Mensuração

| # | Incorporação | Origem |
|---|---|---|
| I-18 | Evento de coleta com campos de expectativa: `expected_frequency`, `active_scopes` (operação, país, marca), `expected_zero_conditions`, `launch_date`, `retirement_date`, `renamed_from` com vigência, `consent_requirements`, `late_arrival_window`, `deduplication_key`, `downstream_kpis`, `known_exceptions` e `validation_query`. | CX, CL, GE |
| I-19 | Regra canônica de evento quebrado como exemplo do tipo Regra e decisão: candidato a falha só se estiver ativo naquele escopo, com frequência esperada na janela, janela de ingestão completa e desvio da linha de base por N períodos seguidos, avaliado por operação, depois de aplicar exceções conhecidas. Limiares são escolha do time, nunca valores universais. | CX, CL |
| I-20 | Triagem de anomalia em cinco passos como tabela de decisão de exemplo: delimitar escopo, datar o início e cruzar com deploys do GTM, checar sazonalidade, cruzar fonte externa, testar o fluxo à mão. | GE |
| I-21 | Ficha de regras de reconciliação entre Meta, Google Ads, GA4, BigQuery e ERP: por que divergem por desenho (janela e modelo de atribuição, data da interação x data da conversão, view-through, fuso), qual fonte é oficial para cada decisão e qual desvio aciona investigação. Cobre o caso 3 de [09-casos-de-uso.md](./09-casos-de-uso.md). | GE, CX, CL |
| I-22 | Banco de cenários de marketing (cerca de 40 nas três pesquisas) para o Lab 2, o "Teste você" e o tipo Perguntas de negócio: consentimento, fuso, deduplicação de `purchase`, estorno, moeda, atribuição, renomeação de evento, limites de privacidade do GA4, gateways contados como Referral, tráfego interno, bots, latência de processamento e sazonalidade. | CL, CX, GE |
| I-23 | Caso de duplicação depois de junção (fan-out): receita do pedido somada depois de juntar com itens ou pontos de contato. O Lab 1 atual é pequeno demais para ensinar isso. Entra no Lab 2 sem romper o limite fixo de escopo, ou como exercício próprio. | CL, CX |

### F5. Moldes e visual

| # | Incorporação | Origem |
|---|---|---|
| I-24 | Sequência didática de cada página de tipo: (1) par contrastante, mesma pergunta com duas definições e dois números, como o 25% x 50% da Aurora; (2) exemplo completo comentado, com perguntas de autoexplicação; (3) exemplo com erro sutil para encontrar; (4) exemplo quase pronto para completar um campo; (5) caso novo em branco; (6) "Teste você" que pede uma resposta antes de mostrar o gabarito, com explicação do erro. O modelo em branco aparece por último. O contrato editorial muda antes. | CL, CX, GE |
| I-25 | Nomes distintos para dois exercícios: "Diagnóstico" (encontre o que falta, papel do atual exemplo com lacunas) e "Complete" (preencha o campo que falta num exemplo quase pronto). | CL |

### F6. Saídas para máquinas

| # | Incorporação | Origem |
|---|---|---|
| I-26 | llms.txt rebaixado a opcional, sem critério de saída. O critério da F6 passa a ser: um agente com o kit mínimo responde às perguntas marcadas `onboarding`. | CL, CX, GE |
| I-27 | Kit mínimo para agentes, para download: `AGENTS.md` curto (onde está cada coisa, "nunca calcule indicador sem consultar a definição aprovada; se não houver, pergunte"), glossário, contratos, gabarito e uma Skill de auditoria de coleta. É o padrão do artigo da LogRocket sobre design system transposto para dados. | CL, CX, GE |
| I-28 | Documentação servida a agentes como `resources` do MCP (somente leitura, identificada por URI); consultas e validações como `tools`. Fica como nota de design, sem código. | CL, CX |

### F7 e depois

| # | Incorporação | Origem |
|---|---|---|
| I-29 | Manutenção a partir do uso (KCS): quando a IA erra uma pergunta do gabarito, isso abre uma pergunta em aberto no documento ligado a ela. Substitui a revisão só por calendário. | CL, CX, GE |
| I-30 | Script de deriva que compara os documentos com o warehouse e o contêiner GTM (colunas e eventos citados que não existem, eventos novos sem documento, vigência vencida). Depende de conexão com os sistemas do time, por isso fica depois da v1.0. | CL, GE |
| I-31 | Fluxo para quem não usa Git: tag plan em planilha com colunas iguais aos campos do Evento de coleta, convertido por uma Skill para o formato canônico. Responde ao ponto "formato de entrega para quem não é técnico" do [README.md](./README.md). | (síntese) |

## Cuidados antes de levar ao portal

- **Versão do OSI/Apache Ossie.** GE fala em "v1.0", CL em v0.1 e CX em 0.3.0.dev0. A nossa pesquisa achou 0.1.1 publicada e 0.3.0.dev0 em rascunho. Alinhar conceitos (métrica, dimensão, entidade, relacionamento), sem depender do formato.
- **Números de terceira mão.** Limiares de alerta do GA4 (25 a 30%), linha de base de 90 dias, custos do experimento da LogRocket (US$ 2,28 para US$ 1,08) e a auditoria de erros de anotação no BIRD e no Spider 2.0 vêm de blogs, segundo a própria GE. Benchmarks da dbt e da Cube são de fornecedores. Precisam de fonte primária ou ficam fora.
- **Norma de linguagem simples.** GE registra que um portal comercial de normas mostra a ABNT NBR ISO 24495-1 como cancelada. Conferir na ABNT antes de citar.
- **Agent Skills na Agentic AI Foundation** (22/10/2026). Só CX afirma; precisa de segunda fonte.
- **Pesquisas novas de abstenção** (AMBROSIA, PRACTIQ, PremiseSQL) não estavam na nossa pesquisa; PremiseSQL é preprint.
- **Datas de protocolos** mudam em semanas: reconferir MCP, WebMCP, UCP e Poppy no início da F6.

## Não coberto

- Nenhuma afirmação das três pesquisas foi reverificada uma a uma nesta rodada; só foram cruzadas com [08-pesquisa-boas-praticas.md](./08-pesquisa-boas-praticas.md) onde havia sobreposição.
- O desenho detalhado de cada campo novo e a tabela de migração continuam para a F3.
