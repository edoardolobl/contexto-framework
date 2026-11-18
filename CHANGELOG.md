# Histórico de mudanças

Todas as mudanças relevantes do Contexto ficam registradas aqui. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o número de versão segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

Esta é a versão do **produto** (portal, método e ferramentas). Os modelos de documento terão versão própria de schema a partir da migração para Markdown com frontmatter ([ADR 0009](docs/adr/0009-versao-do-produto-separada-do-schema.md)). Mudança que quebra quem já usa os modelos aparece marcada com **Breaking:**.

## [Não lançado]

### Adicionado

- Pasta `auditoria/` com a auditoria de 17/11/2026: achados ancorados no repositório, pesquisa de boas práticas, casos de uso, direção proposta, decisões do mantenedor, incorporações das pesquisas externas e medições de interface.
- ADRs: um por decisão do mantenedor, mais duas propostas da auditoria (0016, 0017), todos aceitos pelo mantenedor; 0016 escolhe a família IBM Plex e 0017 limita a página de modelo a 4 telas no desktop (pasta `docs/adr/`).
- `src/data/vocabulario.yaml`: fonte única do vocabulário que o validador aplica.
- `src/data/modelos.yaml`: fonte única da lista de tipos de documento, com o nível de cada um (núcleo, segundo nível, trilha complementar).
- `scripts/check_higiene.py`: recusa caracteres Unicode invisíveis, descrições de campo que só repetem o nome, versões do produto divergentes e termos do vocabulário ausentes do contrato.
- `scripts/comum.py` e testes em `scripts/tests/` (pytest).
- `npm run check`, que roda testes, validadores, build e conferência de links na mesma ordem do CI.
- Atualização automática de dependências com Dependabot (GitHub Actions, npm e pip).
- `scripts/check_contraste.py` e `src/data/contraste.yaml`: conferem o contraste dos tokens de cor de `custom.css` nos temas claro e escuro (4,5:1 para texto, 3:1 para bordas, 7:1 para o texto secundário).
- `scripts/check_html_gerado.py`: confere no site gerado um h1 por página, títulos sem pular nível, og:image e theme-color.
- `src/data/artefatos.yaml`: datas em que a consulta de referência e a amostra do laboratório Aurora passaram a existir.
- `check_revisions.py` acusa exemplo que cita registro, versão, consulta ou amostra de data posterior à sua, confere `archival_note` pela própria data e avisa (sem falhar) aprovação em fim de semana. Os validadores ganham linhas `AVISO:`, que não mudam o código de saída.
- ADRs 0018 a 0022, em estado Proposto, para as convenções do Contexto que ainda não tinham registro.
- `validate_content.py` acusa link `blob/main` ou `tree/main` do repositório que aponta para arquivo inexistente na cópia local (por exemplo, um ADR citado nas referências).
- Imagem de compartilhamento (`public/og-contexto.png`) e cor do tema do navegador para os dois temas.
- Seção "Evidência empírica" e tipo de fonte em cada linha das referências.
- Percurso em sete passos (F2): páginas novas em `percurso/` (Escreva a pergunta de negócio, Delimite o acervo, Descubra o que falta, Revise e aprove, Teste com as perguntas, Leve à sua ferramenta de IA), com a página de modelos como passo 4 e o Laboratório Aurora depois do último passo.
- Página "Modelo de AGENTS.md" no grupo Usar com IA, e trecho curto de AGENTS.md no passo 7.
- Banco de perguntas por tipo de documento no passo 1, com versão fraca, versão boa e a decisão que muda.
- Descoberta por entrevista a partir de um incidente real (adaptação do Critical Decision Method): oito famílias de perguntas, roteiro de 20 minutos e "5 porquês" só como heurística.
- Fontes únicas em `src/data/`: `percurso.yaml`, `entradas.yaml` (cinco entradas por sintoma, uma com destino provisório até a F4; sintoma repetido é recusado) e `dimensoes.yaml`; `modelos.yaml` ganha página, nome, tarefa, resumo, quando, resultado, preparar e rótulo de download.
- Componentes `NextStep` (bloco Próximo passo no fim de cada página do percurso), `PathMap`, `SymptomEntries` e `DimensionTable`, e `src/lib/dados.ts` para ler os dados.
- `scripts/check_navegacao.py`: recusa página órfã, página do percurso sem Próximo passo, YAML no percurso, modelos fora da ordem de nível, grupo Percurso diferente de `percurso.yaml`, título divergente e destino ou redirecionamento para página inexistente; avisa página sem link interno de saída. Entra em `check:content`.
- `validate_content.py` confere o nome de `modelos.yaml` com o título da página do modelo e os quatro arquivos de download de cada tipo, e aplica travessão, vocabulário e endereço antigo aos dados novos.
- ADRs 0023 (percurso em sete passos), 0024 (descoberta por incidente) e 0025 (instrução mínima ao agente), em estado Proposto.
- Protocolo de card sorting e tree test da F2 em `docs/PLANO_VALIDACAO.md`, aguardando execução.
- Regra de vocabulário "Perguntas de negócio" no lugar de "perguntas de referência" e "casos de teste" (fora da bibliografia).
- Schema 1.0 (F3): fontes únicas em `src/modelos/<slug>.md` (10 modelos) e `src/exemplos/<nome>.md` (23 exemplos, com `historico/`), em Markdown com os campos no topo do arquivo (frontmatter, ADR 0006).
- `scripts/gerar_downloads.py` (`npm run gerar:downloads`): gera os `.yaml` e os `.md` de `public/downloads` a partir das fontes, com as seções "Identificação" e "Histórico de versões" montadas automaticamente; com `--check`, só confere a sincronia e acusa arquivo desatualizado, ausente ou órfão. Entra no começo de `check:content`.
- `schemas/`: um JSON Schema 1.0.0 por tipo mais o cabeçalho comum (`$id` em URN), e `scripts/check_schemas.py`, que valida o frontmatter de cada fonte, confere a ordem do cabeçalho, o `type` igual ao nome do arquivo e o dicionário de campos. Dependência nova: `jsonschema==4.26.0`.
- `src/data/campos.yaml`: rótulos em português do cabeçalho comum, com 8 campos obrigatórios para sair do rascunho (ADR 0015).
- Cabeçalho comum em todos os tipos: `schema_version`, `superseded_by_revision`, `review_interval` (duração ISO 8601), `last_reviewed`, `intent` (pergunta de negócio, quem usa, para quê, decisões que apoia) e `plain_summary`; blocos técnicos opcionais `context` e `authoritativeDefinitions`; `recorded_at` só na cópia histórica.
- Estado `superseded` (Substituído, ADR 0005), usado pelas cópias históricas do KPI 1.0 e do Conceito 1.0, e regras novas em `check_revisions.py`: a substituída aponta a sucessora, que aponta de volta; a vigência de uma termina onde a da outra começa; `recorded_at` não é anterior à data da versão.
- Indicador com versão maior exige `history_recalculation` (`recalculate` ou `method_break`, I-14); o KPI 2.0 usa `method_break`, coerente com a resposta de Q07, e `check_analytics_fixture.py` cruza os dois.
- Modelos 0.x preservados em `public/downloads/historico/0.x/` (os 10 pares `.md` e `.yaml`, sem alteração).
- Páginas "Migração para o schema 1.0" e "Correspondência com o ODCS" no grupo Consultar.
- Contrato editorial 0.8 e ADR 0026, ambos em estado Proposto.
- Tipo Evento de coleta (F4, I-18): `schemas/evento-coleta.schema.json`, modelo `src/modelos/evento-coleta.md` com as duas instruções ao agente já preenchidas em `context.instructions` (`review_interval` P6M) e par de exemplos `EVENT-AURORA-GENERATE-LEAD` (com lacunas 0.1 e completo 1.1); núcleo curto com `trigger`, `destination` e `active_scopes`. Página "Evento de coleta" em Modelos, com a triagem em cinco passos antes de chamar um evento de quebrado (I-20) e os quatro downloads.
- Regra canônica de evento quebrado (I-19): exemplo `DECISION-AURORA-EVENTO-QUEBRADO` (tipo decisão, só o completo), com cinco entradas categóricas, 11 linhas exclusivas e 6 casos; o número de dias seguidos em zero fica no Evento de coleta, como escolha do time. Testes em `scripts/tests/test_decisao_evento.py`.
- Laboratório Aurora de eventos de coleta (Lab 2), no grupo Laboratórios: amostra `aurora-lab2-fixture.sql` (2 operações, 3 eventos, 28 dias, 1 dia incompleto, 1 incidente), consulta de referência `aurora-lab2-reference-query.sql`, gabarito `QA-AURORA-002` ("quais eventos pararam?") e exercício de duplicação depois da junção de pedidos com itens (I-23).
- `scripts/check_lab2_mensuracao.py`, com testes em `scripts/tests/test_lab2_mensuracao.py`: confere o limite fixo do Lab 2, recalcula no SQLite os números citados nas páginas e nos exemplos, aplica a regra canônica a cada evento e operação e confere o gabarito, sem chamar modelo de IA (ADR 0022). Entra em `check:content`.
- Página "Cenários de mensuração" no grupo Consultar (I-22): 15 cenários, cada um com fonte primária do Google Analytics Help ou do Google for Developers, e a ficha de reconciliação entre fontes `POLICY-AURORA-RECONCILIACAO-MIDIA`, exemplo do tipo Política (I-21).
- Protocolo do experimento do caso 1 em `docs/experimentos/caso-1.md` (com e sem documentação, pontuação pelo gabarito `QA-AURORA-002`), aguardando execução com agentes reais.
- Regras de vocabulário "linha de base" (no lugar de baseline) e "plano de mensuração" (no lugar de tag plan, permitido uma vez na página do tipo Evento de coleta).
- Contrato editorial 0.9 e ADR 0027, ambos em estado Proposto.

### Mudado

- **Breaking:** schema 1.0.0 (ADR 0009). A chave `type` passa a ser o slug do tipo (`metric_definition` vira `kpi`, `reference_question_set` vira `perguntas-de-negocio` e assim por diante); vários campos mudam de lugar (por exemplo `purpose` vai para `intent.purpose`, `decision_question` para `intent.question`, `vocabulary.preferred_term` para `vocabulary.prefLabel`); perguntas em aberto passam a usar `owner_to_resolve` (antes `resolution_owner`), `status` (antes `state`) e `resolution`; no KPI, `business_definition.synonyms` vira `synonyms`, no primeiro nível; os itens de `context.verifiedStatements` e `context.constraints` seguem o formato do ODCS 3.2.0, com `question` e `answer` opcional, e com `constraint`. A tabela completa está em [Migração para o schema 1.0](src/content/docs/referencias/migracao-schema-1-0.mdx), publicada no portal em Consultar.
- **Breaking:** os downloads `template-casos-teste.md`, `template-casos-teste.yaml` e `exemplo-casos-teste-*.yaml` passam a se chamar `template-perguntas-de-negocio.*` e `exemplo-perguntas-de-negocio-*.yaml` (ADR 0007). Os endereços antigos não redirecionam; os modelos antigos ficam em `historico/0.x/`.
- Os arquivos de `public/downloads` deixam de ser editados à mão: são gerados das fontes e o CI falha se estiverem fora de sincronia. O modelo `.md` baixado abre com os campos no topo.
- Os exemplos ganham pergunta de negócio e resumo em poucas palavras (I-16); o cartão do exemplo mostra o resumo, a linha "Substituída por" e só as perguntas em aberto ainda sem resposta; a comparação de versões marca a cópia antiga como substituída.
- `perguntas-de-negocio`: `questions[].intent` vira `goal`, `questions[].context` vira `assumptions`, com `phrasings`, `onboarding` e `reference_sql` opcionais; `depends_on_versions` lista todos os documentos cobertos.
- Conceito com vocabulário no padrão SKOS (`prefLabel`, `altLabel`, `broader`, `related`, `not_synonyms`); `context` passa a ser o bloco técnico do ODCS.
- Validadores: `validate_content.py` aceita `superseded`, exige que o modelo Markdown comece com frontmatter e que o exemplo completo tenha `intent.question` e `plain_summary`; `check_higiene.py` confere também `campos.yaml` e os `title` e `description` dos schemas; `check_decision_examples.py` confere o `type` e relata campo ausente como `ERRO:`; links para `historico/0.x/` passam a ser conferidos no caminho certo.
- README, "Como ler os campos", "Comece em 5 minutos", "Limites" e "Identificação e versões" descrevem o formato novo, o núcleo de 8 campos e a diferença entre Substituído e Obsoleto.
- Onze tipos de documento: Evento de coleta entra no núcleo, logo depois de Relacionamento (ADR 0013), em `modelos.yaml`, no menu, no enum de `type` do cabeçalho comum e no cartão do exemplo (`ExampleMeaning`), que também ganha rótulos em português para as entradas e saídas da regra de evento quebrado.
- A entrada da home "Um evento parece ter parado de coletar" deixa o destino provisório e passa a levar à página Evento de coleta.
- `check_decision_examples.py` lê todo `exemplo-decisao-*.yaml` em vez de uma lista fixa, relata linha da tabela sem uma entrada como `ERRO:` e, quando a regra tem `failure_candidate`, exige as cinco condições e recusa número em `allowed_values`; `validate_content.py` passa a conferir referências com o prefixo `EVENT-`.
- Os `.sql` do Lab 1 (`aurora-fixture.sql` e `aurora-reference-query.sql`) ganham o aviso de que a Aurora é inventada na primeira linha (ADR 0012), sem mudar o resultado de 25%.
- `AnalyticsLabDownloads` recebe a escolha do laboratório (`lab`), e `artefatos.yaml` registra a amostra do Lab 2 a partir de 16/11/2026.
- Revisão da F4: o link do cenário 14 para a ficha de reconciliação usa a âncora com acento, e `check_built_links.py` passa a conferir as âncoras (`#`) na página de destino, com testes em `scripts/tests/test_links_construidos.py`.
- `check_lab2_mensuracao.py` monta a partir da amostra cada linha do quadro-resumo da página do Lab 2 e as frases completas que a página, o Evento de coleta, o gabarito e a página do modelo repetem (médias, dias em zero, sequências e seus períodos, "desde 11/11"), em vez de procurar números soltos.
- As versões 1.1 do Evento de coleta `generate_lead` e da regra de evento quebrado passam de 16/11 para 17/11/2026: pela regra D+2, o dia 15/11 da linha de base e do teste do México só fica completo em 17/11.
- Protocolo do caso 1: as duas condições recebem só a tabela de eventos diários e a lista de eventos do plano por operação, sem escopo, tolerância nem marca de dia incompleto; o prompt diz a data da consulta; a pontuação compara a única pergunta feita com a Q01 do gabarito, sem colunas de esclarecer e abster-se.

- A publicação no GitHub Pages só acontece depois que todos os validadores passam.
- O deploy não é mais cancelado no meio: uma publicação em andamento termina, e uma publicação que está na fila é substituída pela mais recente.
- Ações do GitHub fixadas por SHA; permissões de escrita só no job que publica.
- Os validadores relatam YAML vazio, quebrado ou sem campo esperado como linha `ERRO:` com o arquivo, em vez de parar com traceback, e falham quando uma busca de arquivos volta com menos itens que o mínimo esperado.
- Vocabulário e tipos de documento são validados: regra ou tipo malformado vira erro, em vez de passar em silêncio.
- `carregar_yaml` também relata data impossível e arquivo que não é UTF-8, como erro com o arquivo indicado.
- A varredura de caracteres invisíveis ficou mais ampla: formatação, controle, separadores de linha e parágrafo, seletores de variação e preenchedores que parecem vazios.
- Consolidação da experiência, etapas A a E do ROADMAP (v0.5 em construção): entradas por tarefa, identificação e intervalos de vigência, exemplos de negócio visíveis, painel técnico único, revisão em três verificações e ajustes de leitura no celular.
- Rodada 3, de 17/11/2026: portal reorganizado de 38 para 26 páginas, um termo por ideia, exemplos concretos por tipo e aviso de que a Aurora é inventada só em três lugares.
- Linha do tempo da Aurora: exemplos datados antes de 01/10/2026 não citam mais os registros da amostra, e os datados antes de 15/09/2026 não citam a consulta de referência; aprovações de sábado passam para a sexta anterior (KPI 1.0 em 14/08, dashboard 1.0 em 21/08, dataset de sessões 1.1 em 11/09), sem mudar o início da vigência.
- A cópia histórica do KPI 1.0 volta a ser o texto aprovado; as notas posteriores ficam em `archival_note`, com data própria.
- Os 10 exemplos com lacunas passam do estado `pending_approval` para `draft`.
- Modelo de KPI em Markdown com uma só seção de perguntas em aberto e sem numeração de seções.
- Página inicial com um h1 real e as entradas por tarefa antes do cartão ilustrativo, que passa a mostrar o estado "rascunho".
- Tokens de cor com contraste conferido nos dois temas, avisos e citações recoloridos só com tokens, `!important` removido (fica só o de movimento reduzido) e seletores sem uso apagados.
- Acessibilidade: retorno do checklist com a contagem de lacunas e região de status para o resultado da cópia; grupos do seletor de modelos com nome acessível; títulos dos componentes sem pular nível; diagrama de junção que não depende só da cor; alvos de toque de 44 px no celular.
- Citações: o guia Knowledge-Centered Success substitui o KCS v6; Polanyi (1966) aparece como origem da distinção entre conhecimento tácito e explícito; "Decisão própria" vira "Convenção do Contexto", com link para o ADR.
- Contrato editorial 0.5 (proposto): termo "modelo" no lugar de "template", cinco tipos de fonte, exemplo com lacunas em `draft`, aprovações em dia útil, datas de artefatos conferidas e notas de arquivamento em `archival_note`.
- Vocabulário: regra "modelo" no validador; termos em inglês do ROADMAP trocados por português.
- Menu reorganizado em grupos (Comece aqui, Percurso, Modelos, Laboratórios, Entender, Consultar, Usar com IA), com os cinco modelos do núcleo primeiro e a Rubrica na trilha complementar.
- Endereços movidos com redirecionamento direto ao destino: `/templates/casos-teste/` e `/exemplos/testes-analytics/` levam a `templates/perguntas-de-negocio/`; `/metodo/elicitar/` leva a `percurso/descubra-o-que-falta/`; `/validacao/checklist/` e `/metodo/revisao-e-entrega/` levam a `percurso/revise-e-aprove/`. Os arquivos de download e a chave `type` continuam `casos-teste` até a F3 (ADR 0007).
- Títulos: "Casos de teste" passa a "Perguntas de negócio"; Decisão passa a "Regra e decisão"; a visão geral do método passa a "Como o método funciona"; as oito dimensões passam a "Checklist das oito dimensões", apresentadas como convenção do Contexto (ADR 0014); a página de modelos passa a "Escreva com o modelo".
- Home com h1 de categoria e público, slogan como linha de apoio, promessa única como tagline, linha de fato calculada dos dados e entradas por sintoma no lugar dos cartões de princípios (`PrincipleTiles` removido).
- Seletor de modelos vira tabela estática sem JavaScript, agrupada por nível e alimentada por `modelos.yaml`; `TemplateDownloads` e `TemplateStart` leem o mesmo arquivo; `ReadinessChecklist` lê `dimensoes.yaml` e passa a se chamar "Checklist de revisão".
- Página de revisão sem YAML: a ficha de perguntas em aberto vira tabela.
- Contrato editorial 0.6 e 0.7 (propostos): promessa da seção 1.2, três perfis leitores, organização do portal em percurso e regra "Perguntas de negócio"; a 0.7 descreve Comece aqui como o menu publicado (tutorial de negócio e visão do método) e deixa o tutorial de dados em aberto. README com a mesma promessa.

## [0.4.0] - 2026-11-16

### Corrigido

- Correções da auditoria independente: links da biblioteca, título único por página, estados alinhados.

### Adicionado

- Licenças MIT (código) e CC BY 4.0 (conteúdo), autoria e página de créditos.
- Versão, data da versão e histórico de versões em todos os modelos e exemplos.
- Par de exemplos por tipo: com lacunas e completo com aprovação.
- Páginas "Comece em 5 minutos", "Como ler os campos" e "Quando o método não basta".
- Lockfile e validação de links no HTML gerado.

### Mudado

- Modelos Markdown sem bloco YAML; páginas leem os exemplos dos arquivos de download.

## [0.3.0] - 2026-11-16

### Adicionado

- Trilha de Dados e Analytics: dataset, relacionamento, dashboard, rubrica e perguntas de referência.
- Laboratório Aurora com amostra SQLite e consulta verificada por teste automatizado.
- Estudo de caso integrado de indicador, dataset, dashboard e rubrica.

## [0.2.0] - 2026-11-16

### Adicionado

- Modelos de conceito, processo, decisão e política, com exemplos.
- Seletor de modelos e passagem de conhecimento com perguntas em aberto.

## [0.1.0] - 2026-11-16

### Adicionado

- Propósito, promessa e limites; método das oito dimensões; roteiro de descoberta e revisão.
- Modelo de indicador com exemplo, checklist interativo e bibliografia.
- Publicação automatizada e validação em pull request.

[Não lançado]: https://github.com/edoardolobl/contexto-framework/compare/b8d176e5cd75078a60c015dddae10d56f8187759...HEAD
