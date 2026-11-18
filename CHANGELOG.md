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

### Mudado

- A publicação no GitHub Pages só acontece depois que todos os validadores passam.
- O deploy não é mais cancelado no meio: uma publicação em andamento termina, e uma publicação que está na fila é substituída pela mais recente.
- Ações do GitHub fixadas por SHA; permissões de escrita só no job que publica.
- Os validadores relatam YAML vazio, quebrado ou sem campo esperado como linha `ERRO:` com o arquivo, em vez de parar com traceback, e falham quando uma busca de arquivos volta com menos itens que o mínimo esperado.
- Vocabulário e tipos de documento são validados: regra ou tipo malformado vira erro, em vez de passar em silêncio.
- `carregar_yaml` também relata data impossível e arquivo que não é UTF-8, como erro com o arquivo indicado.
- A varredura de caracteres invisíveis ficou mais ampla: formatação, controle, separadores de linha e parágrafo, seletores de variação e preenchedores que parecem vazios.
- Consolidação da experiência, checkpoints A a E do ROADMAP (v0.5 em construção): entradas por tarefa, identificação e intervalos de vigência, exemplos de negócio visíveis, painel técnico único, revisão em três verificações e ajustes de leitura no celular.
- Rodada 3, de 17/11/2026: portal reorganizado de 38 para 26 páginas, um termo por ideia, exemplos concretos por tipo e aviso de que a Aurora é inventada só em três lugares.

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
