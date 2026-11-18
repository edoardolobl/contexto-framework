# Histórico de mudanças

Todas as mudanças relevantes do Contexto ficam registradas aqui. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o número de versão segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

Esta é a versão do **produto** (portal, método e ferramentas). Os modelos de documento terão versão própria de schema a partir da migração para Markdown com frontmatter ([ADR 0009](docs/adr/0009-versao-do-produto-separada-do-schema.md)). Mudança que quebra quem já usa os modelos aparece marcada com **Breaking:**.

## [1.0.0-rc.1] - 2026-11-17

Candidata a lançamento da 1.0. A versão 1.0 final depende do piloto de validação com pessoas ([ADR 0029](docs/adr/0029-agentes-e-prova.md), decisão 8), registrado em `docs/piloto/`.

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
- Página "Correspondência com o ODCS" no grupo Consultar.
- Contrato editorial 0.8 e ADR 0026, ambos em estado Proposto.
- Tipo Evento de coleta (F4, I-18): `schemas/evento-coleta.schema.json`, modelo `src/modelos/evento-coleta.md` com as duas instruções ao agente já preenchidas em `context.instructions` (`review_interval` P6M) e par de exemplos `EVENT-AURORA-GENERATE-LEAD` (com lacunas 0.1 e completo 1.1); núcleo curto com `trigger`, `destination` e `active_scopes`. Página "Evento de coleta" em Modelos, com a triagem em cinco passos antes de chamar um evento de quebrado (I-20) e os quatro downloads.
- Regra canônica de evento quebrado (I-19): exemplo `DECISION-AURORA-EVENTO-QUEBRADO` (tipo decisão, só o completo), com cinco entradas categóricas, 11 linhas exclusivas e 6 casos; o número de dias seguidos em zero fica no Evento de coleta, como escolha do time. Testes em `scripts/tests/test_decisao_evento.py`.
- Laboratório Aurora de eventos de coleta (Lab 2), no grupo Laboratórios: amostra `aurora-lab2-fixture.sql` (2 operações, 3 eventos, 28 dias, 1 dia incompleto, 1 incidente), consulta de referência `aurora-lab2-reference-query.sql`, gabarito `QA-AURORA-002` ("quais eventos pararam?") e exercício de duplicação depois da junção de pedidos com itens (I-23).
- `scripts/check_lab2_mensuracao.py`, com testes em `scripts/tests/test_lab2_mensuracao.py`: confere o limite fixo do Lab 2, recalcula no SQLite os números citados nas páginas e nos exemplos, aplica a regra canônica a cada evento e operação e confere o gabarito, sem chamar modelo de IA (ADR 0022). Entra em `check:content`.
- Página "Cenários de mensuração" no grupo Consultar (I-22): 15 cenários, cada um com fonte primária do Google Analytics Help ou do Google for Developers, e a ficha de reconciliação entre fontes `POLICY-AURORA-RECONCILIACAO-MIDIA`, exemplo do tipo Política (I-21).
- Protocolo do experimento do caso 1 em `docs/experimentos/caso-1.md` (com e sem documentação, pontuação pelo gabarito `QA-AURORA-002`), aguardando execução com agentes reais.
- Regras de vocabulário "linha de base" (no lugar de baseline) e "plano de mensuração" (no lugar de tag plan, permitido uma vez na página do tipo Evento de coleta).
- Contrato editorial 0.9 e ADR 0027, ambos em estado Proposto.
- Linhas "Exemplo Aurora:" nos modelos `.md` baixados (F5, AUR-13, MOD-03): o marcador `<!-- contexto:exemplo chave -->` em `src/modelos/<slug>.md` vira, no download, uma linha com o valor tirado do exemplo completo. Cada um dos 11 modelos tem de 5 a 7 linhas, sempre com `intent.question`; `gerar_downloads.py` acusa chave ausente, valor vazio, valor que é mapa, falta do exemplo completo, falta de `intent.question` e modelo com menos de 4 linhas.
- Referência de campos por tipo (ADR 0017, UX-03): `scripts/gerar_referencias.py` (`npm run gerar:referencias`) gera `src/content/docs/referencias/campos/` (11 páginas e um índice) a partir de `campos.yaml` e dos schemas; com `--check`, entra em `check:content`. O índice "Referência de campos" fica no grupo Consultar.
- `scripts/check_paginas_modelo.py`: confere em cada página de modelo a ordem do I-24 (TemplateStart, O problema com par contrastante, cinco etapas dentro de Steps, Baixe o modelo por último com o link para a referência de campos), com arquivo e linha. Entra no fim de `check:content`.
- Componentes de estudo `ParContrastante`, `EtapaDeEstudo` e `Exercicio`, com CSS em `src/styles/estudo.css`. O build falha com etapa de tipo desconhecido ou exercício sem exatamente uma opção correta ou sem explicação; a resposta aparece numa região de status só depois de conferir, e sem JavaScript o gabarito fica num `<details>`. Nada é enviado nem guardado.
- Sistema visual (ADR 0016): família IBM Plex (Sans, Serif e Mono) servida pelo próprio site com `@fontsource`, só nos pesos usados; camadas `contexto.base`, `contexto.primitivas`, `contexto.componentes` e `contexto.estudo` em arquivos próprios de `src/styles/`; primitivas `.ctx-card`, `.ctx-label` e `.ctx-button` (principal e secundário, com a mesma aparência do LinkButton); tokens de tamanho de texto e o par `--context-danger`; os neutros do Starlight (escala `--sl-color-gray-1` a `-7`, texto corrido, títulos do tema claro e linha fina) passam a ser tokens no matiz verde dos fundos, com os pares novos em `contraste.yaml` (VIS-02).
- Stylelint 18.0.0 (`npm run lint:css`, `.stylelintrc.json`): cor só como token em `:root` de `custom.css` e nenhum `!important`. `check_higiene.py` recusa bloco `<style>` em `src/components`.
- Checklist visual (`scripts/check_visual.mjs`, `npm run check:visual`, playwright-core 1.65.1, funções testadas em `scripts/visual/regras.mjs`): nos temas claro e escuro, página de modelo com até 4 telas a 1440x900, nenhuma página com estouro horizontal a 390 px, uma face IBM Plex Sans de fato carregada (lida em `document.fonts`, não em `document.fonts.check`, que aprova mesmo sem a fonte) e aplicada, sem requisição externa, e um tamanho por nível de título nos modelos, na home e em Revise e aprove. Antes de medir, espera o `html[data-theme]` do tema pedido e visita a página de novo (até duas vezes) se ele não aparecer, para não falhar por acaso sob carga. Roda no CI depois da instalação do Chromium.
- `docs/GUIA_VISUAL.md`: fontes, escalas, tokens, primitivas, par de botões, regras do Stylelint, como rodar o checklist visual, a situação dos achados A11Y de severidade média e a lista do CSS removido.
- Contrato editorial 0.10, em estado Proposto.
- Saídas para máquinas (F6): `scripts/gerar_saidas.py` e `scripts/kit.py` (`npm run gerar:saidas`), com testes em `scripts/tests/test_gerar_saidas.py`, geram os arquivos abaixo a partir das fontes; com `--check`, entram em `check:content` logo depois de `gerar_referencias.py --check` e acusam arquivo desatualizado, ausente ou órfão.
- Schemas publicados por versão em `public/schemas/1.0.0/` e `public/schemas/1.1.0/` (12 arquivos cada), com o `$id` e os `$ref` reescritos para o endereço do próprio arquivo; a fonte em `schemas/` continua com `$id` em URN (ADR 0026).
- Documentos por id e versão (AG-03, I-17): `public/documentos/<id>@<versão>.md` e `.yaml` para os 28 exemplos, mais `public/documentos/indice.json`. O `.md` traz id, versão e vigência no título e em cada subtítulo do corpo, para que um trecho cortado ainda diga de que documento e período ele é; os campos técnicos ficam no bloco do topo, sem títulos, e a página "Preparar para NotebookLM ou RAG" diz como tratar esse bloco.
- Kit para agentes (I-27): `public/downloads/kit/contexto-kit-agentes/` e o `.zip` determinístico, com AGENTS.md (índice gerado), glossário de conceitos (termos dos Conceitos, Indicadores e Eventos de coleta aprovados e de `termos` em `kit.yaml`, cada um com o id@versão de origem; gabaritos, rubricas e processos ficam fora), contratos aprovados, histórico, gabaritos, dados dos dois laboratórios e a Skill `auditar-coleta`. Rascunhos ficam de fora. Textos-fonte em `src/kit/` e configuração em `src/kit/kit.yaml`.
- `public/llms.txt`, gerado do menu por script, sem plugin (I-26).
- `scripts/enderecos.py`: endereço canônico do site, licença do conteúdo e caminhos de documentos e schemas publicados.
- Cópia congelada do schema 1.0.0 em `schemas/historico/1.0.0/`, sem alteração.
- Páginas novas em Usar com IA: "Kit para agentes", "Preparar para NotebookLM ou RAG" e "Endereços estáveis e schemas", com o componente `DocumentosPublicados`, que lê `indice.json` no build.
- `AGENTS.md` na raiz, para quem contribui com o repositório.
- Nota de design `docs/design/mcp.md` (nada implementado; versão alvo MCP 2026-07-28) e protocolo do experimento de onboarding em `docs/experimentos/onboarding.md` (com a ressalva de que testes dos contratos e da Skill coincidem com Q01 e Q02 do QA-AURORA-002, contados também à parte), aguardando execução com agentes reais.
- ADR 0028 (saídas para máquinas) e contrato editorial 0.11, ambos em estado Proposto.
- Plano de mensuração em planilha (F7, I-31): `scripts/planilha_para_evento.py`, com testes em `scripts/tests/test_planilha_para_evento.py`, converte um CSV (separador `;` ou `,`, com ou sem BOM) em rascunhos de Evento de coleta, um por evento, validados no schema 1.1.0. Cada célula vazia vira pergunta em aberto, todo rascunho ganha a pergunta de quem aprova, e quem aprova, vigência e aprovação nunca são preenchidos. Com erro, nada é escrito, e cada erro cita a linha da planilha. Uma célula entre aspas com quebra de linha (Alt+Enter no Excel) é lida inteira e conta como uma linha da planilha. Modelo `public/downloads/plano-de-mensuracao-modelo.csv` (UTF-8 com BOM, `;`, uma linha da Aurora) e página "Plano de mensuração em planilha" em Usar com IA. A ferramenta não roda no `npm run check`.
- Três Skills novas no kit para agentes (F7): `contexto-elicitar` (descoberta a partir de um caso real, que devolve só rascunho com as lacunas em `open_questions`), `contexto-consultar` (responder, pedir esclarecimento ou abster-se, pelo ADR 0021) e `importar-plano-de-mensuracao` (conversão da planilha). Testes em `scripts/tests/test_kit_skills.py` leem os textos reais.
- Manutenção a partir do uso (F7, I-29): `scripts/erros_para_perguntas.py`, com testes em `scripts/tests/test_erros_para_perguntas.py`, transforma os erros de um experimento em perguntas em aberto propostas, no formato do schema comum, para o responsável de cada documento ligado à pergunta. O relatório não altera nenhum documento, registra no cabeçalho o comando que o reproduz (com cada `--mapa`) e não roda no `npm run check`; "Revise e aprove" mostra o comando completo. Demonstração com os resultados reais do onboarding em `docs/experimentos/onboarding-perguntas-em-aberto.md` (Q03 do QA-AURORA-001, Q03 e Q06 do QA-AURORA-002).
- Kit do piloto de validação em `docs/piloto/` (MET-16, ADR 0010): protocolo, roteiro da sessão, tarefas, ficha do especialista, pré e pós-teste, folha de registro sem dado pessoal, termo de consentimento, pontuação e folha de resultados. O piloto aguarda execução. O critério do portão proposto compara o antes com o depois da mesma pessoa e com uma linha de base sem texto; a pergunta principal proposta é a Q02 no caso 1 (a tarefa pede só o `generate_lead`) e a Q01 no caso 2; a transferência (ticket médio) usa `lab2_pedidos` e `lab2_itens`, que têm receita. Critério, pergunta principal e caso de transferência estão como proposta a confirmar pelo mantenedor.
- Nota de design `docs/design/deriva.md` (I-30), sem código.
- ADR 0029 (agentes e prova) e contrato editorial 0.12, ambos em estado Proposto.
- ADR 0030, "Decisões do mantenedor depois das fases" (F8), aceito: registra as respostas do mantenedor de 17/11/2026 sobre os ADRs propostos, o contrato editorial, as correções do onboarding, a versão do produto, as chaves do ODCS, a limpeza de arquivos e a checagem visual.
- Indicador KPI-AURORA-002@1.0, receita de purchase por operação e dia, aprovado, com a consulta `aurora-lab2-receita-purchase.sql` (sem junção) no kit e nos downloads; `check_lab2_mensuracao.py` refaz R$ 500 (certo) e R$ 1.100 (depois da junção com os itens) e confere que a Q06 cita o indicador.
- Campo opcional `retroactive_validity` no cabeçalho comum (`reason` e `confirmed_by`): `check_revisions.py` só aceita `valid_from` anterior a `version_date` na primeira versão de um assunto e com a retroatividade declarada (contrato 0.13).
- Campo opcional `also_accepted` nas perguntas de negócio, com `behavior` e `condition`; `check_schemas.py` recusa um `behavior` igual ao comportamento esperado. O cartão do exemplo mostra a forma aceita.
- Lista `campos_do_tipo` em `src/data/campos.yaml`, com os rótulos de `also_accepted` e das chaves do ODCS; `check_schemas.py` confere cada rótulo contra o `title` do schema.
- `CLAUDE.md` na raiz, com a linha `@AGENTS.md`.
- Cache do navegador do checklist visual no CI (`actions/cache` v4.3.0, chave pela versão do `playwright-core`); com acerto, só as bibliotecas do sistema são instaladas.

### Mudado

- **Breaking:** schema 1.0.0 (ADR 0009). A chave `type` passa a ser o slug do tipo (`metric_definition` vira `kpi`, `reference_question_set` vira `perguntas-de-negocio` e assim por diante); vários campos mudam de lugar (por exemplo `purpose` vai para `intent.purpose`, `decision_question` para `intent.question`, `vocabulary.preferred_term` para `vocabulary.prefLabel`); perguntas em aberto passam a usar `owner_to_resolve` (antes `resolution_owner`), `status` (antes `state`) e `resolution`; no KPI, `business_definition.synonyms` vira `synonyms`, no primeiro nível; os itens de `context.verifiedStatements` e `context.constraints` seguem o formato do ODCS 3.2.0, com `question` e `answer` opcional, e com `constraint`. Como nenhuma versão 1.x foi publicada antes desta, não há página de migração (ADR 0030).
- **Breaking:** os downloads `template-casos-teste.md`, `template-casos-teste.yaml` e `exemplo-casos-teste-*.yaml` passam a se chamar `template-perguntas-de-negocio.*` e `exemplo-perguntas-de-negocio-*.yaml` (ADR 0007). Os endereços antigos não redirecionam; o site publicado (0.4) nunca teve os arquivos antigos dentro de `historico/0.x/`, que foram removidos (ADR 0030).
- Os arquivos de `public/downloads` deixam de ser editados à mão: são gerados das fontes e o CI falha se estiverem fora de sincronia. O modelo `.md` baixado abre com os campos no topo.
- Os exemplos ganham pergunta de negócio e resumo em poucas palavras (I-16); o cartão do exemplo mostra o resumo, a linha "Substituída por" e só as perguntas em aberto ainda sem resposta; a comparação de versões marca a cópia antiga como substituída.
- `perguntas-de-negocio`: `questions[].intent` vira `goal`, `questions[].context` vira `assumptions`, com `phrasings`, `onboarding` e `reference_sql` opcionais; `depends_on_versions` lista todos os documentos cobertos.
- Conceito com vocabulário no padrão SKOS (`prefLabel`, `altLabel`, `broader`, `related`, `not_synonyms`); `context` passa a ser o bloco técnico do ODCS.
- Validadores: `validate_content.py` aceita `superseded`, exige que o modelo Markdown comece com frontmatter e que o exemplo completo tenha `intent.question` e `plain_summary`; `check_higiene.py` confere também `campos.yaml` e os `title` e `description` dos schemas; `check_decision_examples.py` confere o `type` e relata campo ausente como `ERRO:`; links para subpastas de `historico/` passam a ser conferidos no caminho certo.
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
- As 11 páginas de modelo seguem a sequência do I-24: O problema com par contrastante (por exemplo, 25% x 50% no KPI) e "Aprenda com a Aurora" em cinco etapas recolhíveis (exemplo comentado, Diagnóstico, Complete, caso novo e Teste você, I-25), com a triagem opcional só no Evento de coleta e "Baixe o modelo" por último. Medidas no checklist visual, ficam entre 2,98 e 3,49 telas a 1440x900. `BeforeAfter` foi removido; no KPI, o aviso "Sobre os metadados" vira `Aside`.
- `TemplateStart` deixa de ter download: leva a "Baixe o modelo" e à referência de campos. `TemplateDownloads` e `AnalyticsLabDownloads` usam o primeiro arquivo como botão principal e os outros como secundários; `ExampleDoc` usa `.ctx-label` no selo de estado; o checklist de revisão usa `.ctx-button`.
- `custom.css` passa a ter só tokens e a ordem das camadas. Três fundos (`--context-bg`, `--context-surface` e `--context-inverse`); `--context-surface-2` sai e a ênfase passa a ser a borda de acento. Títulos com um tamanho por nível, sem tamanho próprio nos componentes; nenhum texto abaixo de 0.8125rem; pesos 450, 650, 750 e 800 viram 400, 600 ou 700. `contraste.yaml` confere 17 pares.
- Movimento reduzido sem `!important`: transições e transforms só existem dentro de `prefers-reduced-motion: no-preference`. O CSS do `JoinDiagram` sai do componente para `componentes.css`, e seletores sem uso foram apagados.
- `npm run check` roda, nesta ordem, os testes dos validadores (pytest e `node --test`), o Stylelint, o conteúdo, o build, os links e o checklist visual; o CI segue os mesmos passos. README atualizado.
- Schema 1.1.0 (F6, mudança aditiva, sem Breaking): `schema_version` aceita `1.0.0` ou `1.1.0`, e o cabeçalho comum ganha `license` e `source_url`, opcionais, depois de `superseded_by_revision`. Os 11 modelos passam a 1.1.0 com os dois campos em branco; os 26 exemplos vigentes passam a 1.1.0 com `license: CC-BY-4.0` e `source_url` apontando para o `.md` publicado. As duas cópias históricas (KPI 1.0 e Conceito 1.0) ficam na 1.0.0, sem os dois campos, como foram aprovadas. `check_schemas.py` confere esses valores e aceita a 1.0.0 só em cópia histórica (`superseded`, com `recorded_at`); `campos.yaml`, "Como ler os campos" e "Identificação e versões" explicam os campos novos.
- `validate_content.py` confere links relativos para arquivos de `public/` (`.json`, `.zip`, `.txt`, `.md`, `.yaml`, `.sql`, `.pdf`), recusa meia-risca junto com o travessão e passa a ler `AGENTS.md` e `src/kit/`.
- A página "Correspondência com o ODCS" passa a "Correspondência com ODCS e Ossie", com a tabela completa do cabeçalho comum e dos campos principais de Indicador, Dataset, Relacionamento e Evento de coleta, data de conferência e fonte em cada linha; o endereço não muda.
- O grupo Usar com IA passa a ter quatro páginas; "Modelo de AGENTS.md" ganha as regras de linha de base e de estados e o link para o kit; "Leve à sua ferramenta de IA" aponta o kit e a página de RAG; as referências ganham ODCS 3.2.0, Apache Ossie 0.1.1, Agent Skills, AGENTS.md, llms.txt e MCP.
- `scripts/kit.py` (F7): copia para o kit os arquivos da pasta de cada Skill além do `SKILL.md`, em ordem alfabética, e acusa colisão com referência gerada por id; exige em cada `SKILL.md` a frase "Esta Skill orienta o agente. Ela não garante o comportamento dele." e uma linha `Versão alvo:`; acusa Skill sem entrada em `src/kit/kit.yaml`; o índice do AGENTS.md gerado mostra cada Skill entre crases. `src/kit/AGENTS.md` e a Skill `auditar-coleta` não mudam.
- `public/llms.txt` descreve o kit com as quatro Skills, e `scripts/comum.py` reconhece `.csv` como arquivo publicado.
- **Breaking:** no schema 1.1.0, as chaves do dataset com equivalente direto no ODCS 3.2.0 seguem o ODCS: `physical_name` vira `physicalName`, `business_name` vira `businessName` e `technical_type` vira `physicalType` (ADR 0030). Nenhuma versão 1.x tinha sido publicada; quem tiver um dataset em 1.0.0 troca as três chaves.
- ADRs 0018 a 0029 passam a Aceito, decididos pelo mantenedor; o contrato editorial fica aprovado até a 0.12 e ganha a 0.13, aprovada pelo mantenedor; ADR 0013 (tipos separados) e ADR 0009 (versão do documento em MAJOR.MINOR) têm as perguntas em aberto fechadas pelo ADR 0030.
- Nomes de produção nos laboratórios (ADR 0012 e ADR 0030): no Lab 1, as tabelas do SQLite passam a `sessoes_web` e `pedidos`, que espelham `aurora-analytics.web.sessoes_web` e `aurora-analytics.vendas.pedidos`; amostra, consulta, dicionários, páginas, `JoinDiagram` e validadores usam os nomes novos. A cópia histórica do KPI 1.0 recebe os nomes novos e uma `archival_note` que explica a correção.
- Gabarito QA-AURORA-002 sobe para 1.1: a Q06 cita KPI-AURORA-002@1.0 e a Q03 aceita também a resposta que diz que no México o evento não está ativo. O AGENTS.md do kit e a Skill `contexto-consultar` ganham a regra do termo ambíguo (nome ou sinônimo registrado do indicador). O protocolo de onboarding atualiza a tabela e a rubrica. O experimento foi repetido no Codex (GPT-6.1 Sol, 24 execuções com o kit e 8 no controle), com resultados em `docs/experimentos/onboarding-resultados-2.json`: as três correções acertaram em todas as rodadas, e a Q01 do QA-AURORA-002 errou nas três, porque o agente seguiu o passo 1 da Skill `auditar-coleta` e pediu a operação. O critério de saída da F6 segue não atingido.
- Versão do produto 1.0.0-rc.1 em `package.json`, README e página inicial; `check_higiene.py` aceita o sufixo de pré-lançamento no CHANGELOG.
- O grupo Usar com IA passa a ter cinco páginas; "Kit para agentes" lista as quatro Skills; "Revise e aprove" ganha o passo "5. Manter a partir do uso" (usar, detectar, corrigir, validar e republicar), que completa a revisão por calendário; `docs/PLANO_VALIDACAO.md` registra o caso 1 e o onboarding já executados e aponta o piloto; `docs/design/mcp.md` fica como nota até depois da v1.0; `AGENTS.md` da raiz cita `docs/piloto/` e as duas ferramentas novas.

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

### Removido

- `public/downloads/historico/0.x/` (os modelos 0.x) e a página "Migração para o schema 1.0" (`referencias/migracao-schema-1-0`), criados durante a preparação desta versão. O site publicado (0.4) nunca teve nenhum dos dois, por isso nenhum endereço publicado passa a dar 404. Ficam os históricos de exemplo (KPI 1.0 e Conceito 1.0) e os redirecionamentos de páginas (ADR 0030).

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
