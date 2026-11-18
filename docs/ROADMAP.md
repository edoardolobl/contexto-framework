# Roadmap do Contexto

## v0.1: base técnica e editorial
- [x] Propósito, promessa e limites
- [x] Método das oito dimensões, elicitação e revisão
- [x] Modelo de KPI e exemplo
- [x] Checklist interativo e bibliografia
- [x] Publicação automatizada e validação em PR

## v0.2: documentação transversal
- [x] Seletor pedagógico de modelos
- [x] Conceitos/glossário + exemplo RH
- [x] Processos + exemplo Marketing
- [x] Regras e decisões + tabela de precedência
- [x] Políticas e referências + conflito de fontes
- [x] Passagem de conhecimento com pendências
- [x] Modelos Markdown/YAML e testes de qualidade estrutural

## v0.3: Dados e Analytics
- [x] Dataset e dicionário semântico + exemplo SQLite
- [x] Relacionamentos, cardinalidade e junções + exemplo 1:N
- [x] Dashboard e interpretação com filtros e escopo
- [x] Rubricas para entregáveis analíticos, com âncoras e revisão humana
- [x] Perguntas de negócio respondíveis, ambíguas e não respondíveis
- [x] Estudo de caso integrado de KPI, dataset, dashboard e rubrica
- [x] SQL sintético reproduzível + teste automatizado independente de LLM
- [x] Validação de todas as famílias de modelos e arquivos
- [x] Fundamentação bibliográfica e ressalvas ampliadas
- [ ] Revisão visual manual e testes de acessibilidade com pessoas

## v0.4: correções da auditoria independente (16/11/2026)
- [x] Links da biblioteca, título único por página, estados alinhados
- [x] Licenças MIT (código) e CC BY 4.0 (conteúdo), autoria e página de créditos
- [x] Versão, data da versão e histórico de versões em todos os modelos e exemplos
- [x] Par de exemplos por tipo: com lacunas e completo com aprovação fictícia
- [x] Modelos Markdown sem bloco YAML; páginas leem os exemplos dos arquivos de download
- [x] Páginas "Comece em 5 minutos", "Como ler os campos" e "Quando o método não basta"
- [x] Ressalvas do preprint e das fontes; lockfile; validação de links no HTML gerado

## Consolidação da experiência (v0.5 em construção)
- [x] Etapa A: entradas por tarefa, seleção de modelos e primeira documentação sem YAML
- [x] Etapa B: identificação, intervalos de vigência e versões históricas
- [x] Etapa C: exemplos de negócio visíveis, comparação alinhada e painel técnico único
- [x] Etapa visual: aumentar destaque e contraste do painel técnico recolhível
- [x] Etapa D: separar cobertura, consistência/evidências e confirmação pelo responsável; ficha prática para download
- [x] Etapa E: ajustes pontuais de tipografia, respiração e leitura mobile implementados; aguardando conferência visual do mantenedor
- [ ] Conferir visualmente a etapa E (tema claro/escuro, leitura mobile e seta única)
- [ ] Teste de compreensão com participantes externos (issue #4; após estabilizar os materiais)

## Antes de declarar a edição 1.0
- [ ] Pesquisar a aplicabilidade do método com leitores técnicos e não técnicos (issue #4)
- [ ] Teste com leitor de tela e em celular físico
- [ ] Revisão humana dos 11 exemplos completos, cujo conteúdo fictício foi escrito na v0.4
- [x] Nome mantido: Contexto. Sem domínio próprio por enquanto; o portal segue no GitHub Pages
- [ ] Planejar contribuições e governança de versões
- [ ] Verificação periódica de links externos

## Plano da auditoria de 17/11/2026

O plano completo está em [auditoria/10-direcao-proposta.md](../auditoria/10-direcao-proposta.md), seção 2, com as fases F0 a F7 e o critério de saída de cada uma. As decisões do mantenedor estão em [auditoria/11-decisoes.md](../auditoria/11-decisoes.md) e viram registros em [docs/adr/](adr/).

- [ ] **F0. Decisões e trilhos: concluída no branch, aguardando merge.** Entregue no branch `f0-decisoes-e-trilhos`: ADRs 0001 a 0017 aceitos pelo mantenedor em 17/11/2026 (0016: família IBM Plex; 0017: até 4 telas no desktop, passos recolhíveis e referência de campos à parte); `src/data/vocabulario.yaml` e `src/data/modelos.yaml`; CHANGELOG; versão do produto igual em package.json, README, página inicial e CHANGELOG; `npm run check` como comando único; deploy que só começa depois dos validadores; ações fixadas por SHA e Dependabot. Pelo ADR 0009, o contrato editorial tem versão própria de documento e fica fora da versão única do produto.
- [ ] **F1. Correções baratas e credibilidade: concluída no branch, aguardando merge.** Entregue no branch `f1-correcoes-e-credibilidade`, empilhado sobre o da F0:
  - Linha do tempo da Aurora coerente: nenhum exemplo cita registro, amostra, consulta ou versão de data posterior à sua; aprovações de sábado passam para a sexta anterior; a cópia histórica do KPI 1.0 volta a ser o que foi aprovado, com as notas posteriores em `archival_note`; os 10 exemplos com lacunas passam a `draft`.
  - Validadores novos ou ampliados: `check_revisions.py` lê as datas dos próprios YAML e de `src/data/artefatos.yaml` e avisa aprovação em fim de semana; `check_contraste.py` confere os pares de `src/data/contraste.yaml` (4,5:1 texto, 3:1 bordas, 7:1 texto secundário) nos dois temas; `check_html_gerado.py` confere no site gerado um h1 por página, títulos sem pular nível, og:image e theme-color.
  - Interface: h1 real na home, entradas por tarefa antes do cartão ilustrativo, tokens de cor com contraste conferido, nenhum `!important` além do de movimento reduzido, alvos de toque de 44 px no celular, retorno do checklist com contagem e região de status, grupos com nome acessível no seletor de modelos, imagem de compartilhamento.
  - Fontes: cinco tipos de fonte, seção de evidência empírica, guia Knowledge-Centered Success no lugar do KCS v6, Polanyi (1966) como origem da distinção tácito e explícito; nenhuma "Decisão própria" sem ADR (ADRs 0018 a 0022, propostos).
  - Contrato editorial 0.5 (proposto) e regra de vocabulário "modelo" no lugar de "template".
  - Pendente com o mantenedor: aceitar os ADRs 0018 a 0022 e o contrato 0.5; conferir os links para os ADRs novos depois do merge; aprovar a imagem de compartilhamento; medir de novo no navegador (UX-02, UX-05, UX-07, UX-08, UX-09) e testar o checklist e o seletor com leitor de tela; conferir na fonte primária os números de Painter et al., os papéis do guia Knowledge-Centered Success e a classificação de Polanyi; confirmar o título recuperado do KPI 1.0.
- [ ] **F2. Porta de entrada e percurso: concluída no branch, aguardando merge.** Entregue no branch `f2-porta-de-entrada`, empilhado sobre o da F1:
  - Menu em grupos (Comece aqui, Percurso, Modelos, Laboratórios, Entender, Consultar, Usar com IA) e percurso em sete passos, cada página com o bloco Próximo passo; página de modelos como passo 4; Laboratório Aurora depois do último passo; redirecionamento para cada endereço movido.
  - Tipo Perguntas de negócio no título, no menu e nos textos (ADR 0007), com banco de perguntas por tipo no passo 1; Regra e decisão (ADR 0013); checklist das oito dimensões como convenção do Contexto e fonte única em `src/data/dimensoes.yaml` (ADR 0014).
  - Descoberta por entrevista de um incidente real, instrução mínima ao agente (trecho e modelo de AGENTS.md) e home com h1 de categoria e público, promessa única e cinco entradas por sintoma.
  - Fontes únicas em `src/data/` (`modelos.yaml`, `percurso.yaml`, `entradas.yaml`, `dimensoes.yaml`) e `scripts/check_navegacao.py` (sem página órfã, sem beco sem saída no percurso, sem YAML no percurso).
  - Contrato editorial 0.7 e ADRs 0023 a 0025, propostos; protocolo de card sorting e tree test em `docs/PLANO_VALIDACAO.md`.
  - Pendente com o mantenedor: executar o card sorting (15 pessoas ou mais) e o tree test (sucesso de pelo menos 80% nas tarefas do percurso), que são o critério de saída da fase; aprovar o h1 da home, o contrato 0.7 e os ADRs 0023 a 0025; decidir o tutorial de dados de Comece aqui (página nova ou atalho para o Laboratório Aurora), que ainda não existe; confirmar os rótulos dos subgrupos de Modelos e o lugar da Rubrica; confirmar o destino provisório do sintoma do evento que parou de coletar até a F4; decidir se a F2 sobe a versão do produto (continua 0.4); conferir os links `blob/main` para os ADRs novos depois do merge.
- [ ] **F3. Schema 1.0 (MAJOR, Breaking): concluída no branch, aguardando merge.** Entregue no branch `f3-schema-1-0`, empilhado sobre o da F2:
  - Fonte única em Markdown com frontmatter (ADR 0006): 10 modelos em `src/modelos/` e 23 exemplos em `src/exemplos/`; `scripts/gerar_downloads.py` gera `public/downloads`, e `--check` confere a sincronia no CI.
  - Schema 1.0.0 (ADR 0009): 11 JSON Schemas em `schemas/` (comum mais um por tipo, `$id` em URN), validados por `scripts/check_schemas.py`; `type` igual ao slug; cabeçalho comum com `intent`, `plain_summary`, `review_interval` e `superseded_by_revision`; blocos `context` e `authoritativeDefinitions` do ODCS; vocabulário SKOS no Conceito; núcleo de 8 campos e rótulos em português em `src/data/campos.yaml` (ADR 0015).
  - Estado Substituído (ADR 0005) nas cópias históricas, com `recorded_at` (I-15) e checagem recíproca de substituição em `check_revisions.py`; regra de recálculo do Indicador (I-14) ligada à resposta de Q07.
  - Tipo Perguntas de negócio com arquivos e `type` renomeados (ADR 0007); modelos 0.x preservados em `public/downloads/historico/0.x/`; páginas "Migração para o schema 1.0" e "Correspondência com o ODCS".
  - Contrato editorial 0.8 e ADR 0026, propostos; CHANGELOG com as mudanças Breaking.
  - Adiado: seções autocontidas para RAG e NotebookLM (I-17), com id, escopo e vigência repetidos no subtítulo de cada seção. Os modelos são formulários em branco, sem id nem vigência para repetir, e os exemplos só ganham `.md` para download na F6. Entra na F6, junto da página "Preparar para NotebookLM ou RAG" (ADR 0026).
  - Pendente com o mantenedor: aprovar o ADR 0026 e o contrato 0.8; decidir se `physical_name`, `business_name`, `technical_type` e `grain` mudam na F6 (seria outro Breaking); decidir a fusão de Dataset com Relacionamento e de Decisão (ADR 0013); decidir se as versões de documento passam a MAJOR.MINOR.PATCH; testar o `.md` com campos no topo e o núcleo de 8 campos com o público não técnico; escolher o número da próxima versão do produto (continua 0.4) e a data de lançamento; aceitar que os endereços antigos `template-casos-teste.*` e `exemplo-casos-teste-*.yaml` dão 404.
- [ ] **F4. Mensuração: concluída no branch, aguardando merge.** Entregue no branch `f4-mensuracao`, empilhado sobre o da F3:
  - Tipo Evento de coleta no núcleo (I-18): schema, modelo com as duas instruções ao agente, par de exemplos `EVENT-AURORA-GENERATE-LEAD`, página com triagem em cinco passos (I-20), quatro downloads, menu, `modelos.yaml` (onze tipos) e a entrada da home sem destino provisório.
  - Regra canônica de evento quebrado (I-19) como exemplo de Regra e decisão (`DECISION-AURORA-EVENTO-QUEBRADO`), conferida por `check_decision_examples.py`, que passa a ler todos os exemplos de decisão; o limiar de dias em zero fica no Evento de coleta, como escolha do time.
  - Laboratório Aurora de eventos de coleta (Lab 2) com limite fixo (BR e MX; purchase, add_to_cart e generate_lead; 28 dias; 16/11 incompleto; um incidente em add_to_cart MX), consulta de referência, gabarito `QA-AURORA-002`, exercício de duplicação depois da junção (I-23) e o validador `check_lab2_mensuracao.py`, que refaz as contas sem avaliar modelo de IA (ADR 0022).
  - Página "Cenários de mensuração" com 15 cenários de fonte primária (I-22) e a ficha de reconciliação entre fontes como exemplo de Política (I-21).
  - Aviso de ficção na primeira linha dos `.sql` baixáveis (ADR 0012); vocabulário "linha de base" e "plano de mensuração"; contrato editorial 0.9 e ADR 0027, propostos; protocolo do experimento do caso 1 em `docs/experimentos/caso-1.md`.
  - Não medido: o tamanho da página Evento de coleta em telas de 1440x900 (limite de 4 telas do ADR 0017) ficou sem medição no navegador.
  - Fora desta fase: novas perguntas sobre volume esperado no passo "Descubra o que falta"; caso 3 completo no modelo (relacionamento com mais de dois lados, `expected_range`, `expected_divergence`); cenários de renomeação de evento e "(not set)", que ficaram de fora por falta de leitura da fonte primária.
  - Pendente com o mantenedor: rodar o experimento do caso 1 com agentes reais (Claude Code, Codex, Antigravity), registrando modelo, versão e data, que é o critério de saída da fase; aprovar o ADR 0027 e o contrato 0.9 (e, com eles, o tamanho do laboratório que o ADR 0022 deixou em aberto); confirmar os nomes de produção dos exemplos (`aurora-analytics`, `analytics_312345678`, `analytics_398765432`, `aurora_prod.tracking.eventos_diarios`, `GTM-AURBR01`, `GTM-AURMX01`); revisar os links de fonte primária dos cenários e decidir se cenários de Meta e Google Ads entram depois; decidir se a F4 sobe a versão do produto (continua 0.4); decidir as fusões de tipos do ADR 0013 (ADR 0026).
- [ ] **F5. Moldes, sequência didática e visual: concluída no branch, aguardando merge.** Entregue no branch `f5-moldes-e-visual`, empilhado sobre o da F4:
  - Moldes: linhas "Exemplo Aurora:" nos 11 modelos `.md` (de 5 a 7 por modelo, sempre com `intent.question`), geradas do exemplo completo por `gerar_downloads.py`.
  - Duas páginas por tipo (ADR 0017): a que ensina e a referência de campos gerada por `gerar_referencias.py` (11 páginas e índice no grupo Consultar), conferida no CI.
  - Sequência do I-24 nas 11 páginas de modelo: par contrastante, cinco etapas recolhíveis com Diagnóstico e Complete (I-25), Teste você com resposta antes do gabarito e modelo em branco por último; conferida por `check_paginas_modelo.py`. Medidas entre 2,98 e 3,49 telas a 1440x900, nos dois temas.
  - Sistema visual (ADR 0016): IBM Plex servida pelo site, três fundos, quatro primitivas, um par de botões, CSS em camadas, Stylelint sem cor fixa fora de `:root` e sem `!important`, nenhum `<style>` em componente; guia em `docs/GUIA_VISUAL.md`, com os cinco achados A11Y de severidade média confirmados como resolvidos antes da F5.
  - Checklist visual por PR (`check_visual.mjs`, playwright-core) a 1440 e 390 px, nos temas claro e escuro, no `npm run check` e no CI.
  - Contrato editorial 0.10, proposto.
  - Fora desta fase: os moldes com nomes de produção (ADR 0012), que dependem da confirmação dos nomes pendente desde a F4; integração do `perf.mjs` e do `consistency.mjs` da tasteskill.
  - Pendente com o mantenedor: aprovar o contrato 0.10; revisar os textos novos por tipo, em especial o par contrastante dos tipos sem número natural (Política, Processo, Conceito e Rubrica) e os enunciados de "Caso novo"; aceitar o tempo a mais no CI (instalação do Chromium e cerca de 170 medições) e decidir se quer cache do navegador; rodar de novo o `perf.mjs` e o `consistency.mjs` depois da troca de fontes; testar os exercícios e as etapas recolhíveis com leitor de tela real e celular físico; incluir a Referência de campos e as etapas recolhíveis no tree test da F2; decidir se a F5 sobe a versão do produto (continua 0.4).
- [ ] **F6. Saídas para máquinas: concluída no branch, aguardando merge.** Entregue no branch `f6-saidas-para-maquinas`, empilhado sobre o da F5, sem domínio próprio (ADR 0011):
  - Schema 1.1.0 aditivo: `license` e `source_url` opcionais no cabeçalho comum, `schema_version` 1.0.0 ou 1.1.0; 1.0.0 congelado em `schemas/historico/1.0.0/`; modelos com os dois campos em branco, exemplos vigentes com `CC-BY-4.0` e o endereço publicado e cópias históricas intactas na 1.0.0, conferidos por `check_schemas.py`.
  - `gerar_saidas.py` (`npm run gerar:saidas`, conferido em `check:content`): schemas publicados por versão com `$id` em URL, documentos por id e versão em `.md` e `.yaml` com `indice.json`, kit para agentes (pasta e `.zip` determinístico, com glossário de conceitos gerado e a Skill `auditar-coleta`) e `llms.txt` gerado do menu.
  - Páginas "Kit para agentes", "Preparar para NotebookLM ou RAG" e "Endereços estáveis e schemas" em Usar com IA; correspondência completa com ODCS 3.2.0 e Apache Ossie 0.1.1, datada e com fonte por linha.
  - `AGENTS.md` da raiz para quem contribui, nota de design MCP (`docs/design/mcp.md`), protocolo de onboarding (`docs/experimentos/onboarding.md`), ADR 0028 e contrato editorial 0.11, propostos.
  - Fora desta fase: Skills de elicitação e consulta e piloto com pessoas (F7); servidor MCP; `/.well-known`; plugin de llms.txt; página HTML por id e versão; renomear chaves com equivalente no ODCS (seria schema 2.0.0, Breaking).
  - Pendente com o mantenedor: aprovar o ADR 0028 e o contrato 0.11; rodar o experimento de onboarding com agentes reais, registrando modelo, versão e data, que é o critério de saída da fase (I-26); revisar os resumos dos termos do glossário em `src/kit/kit.yaml` com quem cuida de Analytics; reconferir na fonte primária o suporte a AGENTS.md de cada ferramenta citada, a especificação Agent Skills, o nome NotebookLM ou Gemini Notebook, a frase do Google sobre llms.txt e cada linha da correspondência (os links do Ossie apontam para a tag `osi-0.1.1-rc1`, a única publicada); decidir se o repositório ganha um `CLAUDE.md`; aceitar que os `$id` publicados ficam presos ao github.io até haver domínio próprio; revisar com quem cuida de Analytics a Skill e o AGENTS.md do kit; incluir a página Kit para agentes no tree test da F2; decidir se a F6 sobe a versão do produto (continua 0.4).
- [ ] **F7. Agentes e prova.** Piloto com pessoas, que é o portão da v1.0 (ADR 0010).

O framework documenta *como tornar o conhecimento explícito*. Não certifica agentes, RAG ou SQL gerado.
