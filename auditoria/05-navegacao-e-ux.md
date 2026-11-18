# Navegação e experiência

Data: 2026-11-17 · Commit: d08c810 · Escopo: arquitetura de informação do portal (menu, pastas, paginação, links internos), página inicial, seletor de modelos, downloads e o percurso de dois visitantes típicos, com base em `astro.config.mjs`, `src/components/` e `src/content/docs/`.

## Resumo

- A porta de entrada para quem não é técnico funciona: um único botão de ação na página inicial, um tutorial curto e sem YAML ("Comece em 5 minutos", 475 palavras contadas com `wc -w` no MDX), páginas de modelo com estrutura fixa e um laboratório de dados bem interligado.
- A arquitetura de informação foi montada por acréscimo. O menu não segue os cinco movimentos do método nem os tipos Diátaxis que a própria página de método cita, e as pastas físicas (`fundamentos`, `metodo`, `validacao`) não batem com os grupos do menu. É daí que vem a sensação de colcha de retalhos.
- Nenhuma página define anterior e próximo no frontmatter, então a paginação automática herda a ordem do menu e sugere passos ilógicos. Há páginas órfãs (`metodo/visao-geral`, `fundamentos/conhecimento-tacito`) e becos sem saída (`metodo/elicitar`, `governanca/papeis`, `referencias`).
- As perguntas de negócio, que deveriam abrir o percurso, aparecem como último item de um grupo recolhido de Dados e com três nomes diferentes.
- Os dois casos reais que motivaram o projeto ficam desassistidos de formas diferentes: quem chega com o problema de tag plan e eventos zerados não encontra nenhum caminho (não há ocorrência de tag plan, GTM ou GA4 em `src/content/docs`); quem chega com o problema do indicador genérico se sai melhor, porque o seletor leva ao modelo de Indicador (KPI). Em ambos os casos a jornada termina antes de chegar à ferramenta de IA que a pessoa usa.
- Verificação: todas as citações foram conferidas no arquivo. Uma linha foi corrigida (NAV-10, `astro.config.mjs` de 20 para 21) e a justificativa de um ponto forte foi ajustada. Nenhum achado foi refutado.

## Como a análise foi feita

### Classificação Diátaxis por página

Referência do modelo: [https://diataxis.fr/](https://diataxis.fr/).

| Tipo | Páginas |
|---|---|
| Tutorial | `fundamentos/comece-em-5-minutos` (puro); `exemplos/analytics-integrado` (estudo de caso com referência embutida) |
| Guia de tarefa | `metodo/elicitar` (com YAML técnico); `validacao/checklist` (mistura guia, referência YAML e explicação) |
| Referência | `fundamentos/como-ler-os-campos`; `referencias`; `governanca/papeis` (com explicação) |
| Explicação | `dados/visao-geral`; `metodo/visao-geral` (também funciona como hub); `fundamentos/conhecimento-tacito` (com exercício); `metodo/limites` (solução de problemas) |
| Mistas | `metodo/identificacao-versoes`; `metodo/oito-dimensoes`; as 10 páginas de `templates/*` (por desenho do contrato editorial); `templates/index` (hub mais guia) |

### Dois visitantes simulados

**Visitante 1, gestora não técnica.** Entra pelo único botão, faz o exercício e trava em três pontos: a paginação a manda direto para "Revisar e entregar", que mostra YAML apesar de prometer o contrário (NAV-05, NAV-08); não existe passo de delimitar o acervo (NAV-13); a jornada termina entregando a um "engenheiro de IA", sem explicar como levar os documentos à ferramenta de IA que ela mesma usa (NAV-02).

**Visitante 2, analista com o problema tag plan x Databricks.** A página inicial não tem bloco para dados; a entrada fica num link no fim do texto (NAV-07). Todo o percurso de dados é um único caso de conversão sessão/pedido de e-commerce (NAV-01). Os conteúdos que ajudariam ("A regra muda de um lugar para outro" em `metodo/limites` e a categoria "Ambígua" em Perguntas de referência) ficam em grupos recolhidos. Quem vem com o problema do indicador genérico se sai melhor: o seletor leva ao modelo de Indicador (KPI).

## Pontos fortes (manter)

### Tutorial de entrada curto, sem YAML e com próximos passos explícitos

É o único tutorial Diátaxis puro do portal. Cabe no tempo prometido (475 palavras no MDX), não exige conhecimento técnico e termina com saídas claras. Deve ser mantido como porta principal para o público não técnico.

- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:38](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L38) `Um primeiro documento útil pode ser assim, **sem nenhum YAML**:`
- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:60](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L60) `## O que fazer depois?`
- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:66](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L66) `não precisa lê-las antes do exercício.`

### Página inicial orientada a tarefa, com um único botão de ação

O hero tem uma ação só e os três blocos descrevem situações do leitor, não nomes de modelos. Isso reduz a paralisia de escolha de quem nunca documentou nada.

- [src/components/LandingHero.astro:11](../src/components/LandingHero.astro#L11) `` <a class="cta-primary" href={`${base}fundamentos/comece-em-5-minutos/`}> ``
- [src/components/PrincipleTiles.astro:6](../src/components/PrincipleTiles.astro#L6) `body: 'Você conhece o assunto, mas ainda não sabe como registrar regras, exceções e dúvidas.',`

### Menu sempre igual ao título e redirecionamentos para páginas fundidas

Evita divergência entre rótulo e página e preserva links antigos. Na rodada anterior foi verificado ao vivo que `/exemplos/kpi/` leva a `/templates/kpi/`.

- [astro.config.mjs:43](../astro.config.mjs#L43) `// Sem rótulos próprios: o menu mostra o título da página, então os dois nunca divergem.`
- [astro.config.mjs:9](../astro.config.mjs#L9) `// Páginas fundidas em outras (rodada 3): o endereço antigo leva ao novo.`
- [docs/CONTRATO_EDITORIAL.md:132](../docs/CONTRATO_EDITORIAL.md#L132) `` **Página fundida ganha redirecionamento** em `astro.config.mjs`, e nenhum link do portal aponta para o endereço antigo. O validador confere. ``

### Estrutura fixa e previsível nas páginas de modelo

As páginas de tipo seguem a mesma sequência (O problema, O que perguntar, Antes e depois, Teste você, Baixe o modelo). Quem aprende uma página sabe ler as outras.

- [docs/CONTRATO_EDITORIAL.md:135](../docs/CONTRATO_EDITORIAL.md#L135) `### Estrutura de uma página de tipo`
- [src/content/docs/templates/dataset.mdx:24](../src/content/docs/templates/dataset.mdx#L24) `## O que perguntar`
- [src/content/docs/templates/kpi.mdx:36](../src/content/docs/templates/kpi.mdx#L36) `## Antes e depois da decisão`

### Cartão de exemplo mostra primeiro o significado e só depois o YAML

A aba padrão é a leitura humana. O YAML fica numa aba separada, o que protege o leitor não técnico sem esconder o formato estruturado.

- [src/components/ExampleDoc.astro:77](../src/components/ExampleDoc.astro#L77) `<TabItem label="O que diz">`
- [src/components/ExampleDoc.astro:106](../src/components/ExampleDoc.astro#L106) `<TabItem label="YAML">`

### Bloco "Antes de preencher" padronizado em cada modelo

Responde quando usar, o que será produzido e o que ter em mãos, com download imediato. É a melhor microorientação de tarefa do portal.

- [src/components/TemplateStart.astro:69](../src/components/TemplateStart.astro#L69) `<h2>Quando usar</h2>`
- [src/components/TemplateStart.astro:77](../src/components/TemplateStart.astro#L77) `<h2>O que ter em mãos</h2>`

### Laboratório Aurora funciona como hub interligado de dados

Tem 12 links internos de saída (5 destinos distintos), empatado com `metodo/visao-geral` e atrás apenas de `templates/index` (24). Mostra que vários documentos ligados por identificador sustentam um único número, que é justamente a ideia de camada semântica para consultas com várias tabelas.

- [src/content/docs/exemplos/analytics-integrado.mdx:97](../src/content/docs/exemplos/analytics-integrado.mdx#L97) `O cálculo acima só é confiável porque seis documentos dizem a mesma coisa.`
- [src/content/docs/exemplos/analytics-integrado.mdx:101](../src/content/docs/exemplos/analytics-integrado.mdx#L101) `` | Indicador | `KPI-AURORA-001` | [KPI](../../templates/kpi/) | ``

### Categorias respondível, ambígua e fora da cobertura

É exatamente o raciocínio que faltou no caso real do evento raro (pedir esclarecimento ou se abster em vez de afirmar). Merece mais destaque na navegação.

- [src/content/docs/templates/casos-teste.mdx:23](../src/content/docs/templates/casos-teste.mdx#L23) `| Ambígua | Falta uma escolha que só quem pergunta pode fazer: canal, período, unidade | Pedir esclarecimento e listar as alternativas |`

## Índice de achados

| ID | Severidade | Título |
|---|---|---|
| NAV-01 | Alta | Nenhum caminho para o caso do analista com tag plan e eventos |
| NAV-02 | Alta | A jornada termina antes da IA: falta o passo de levar a documentação à ferramenta |
| NAV-03 | Alta | Perguntas de negócio, que deveriam abrir o percurso, estão no fim de um grupo recolhido e com três nomes |
| NAV-04 | Média | Menu não espelha o método de cinco movimentos nem os tipos Diátaxis, e as pastas não batem com os grupos |
| NAV-05 | Média | Paginação automática sugere próximos passos ilógicos |
| NAV-06 | Média | Becos sem saída e páginas órfãs |
| NAV-07 | Média | Página inicial sem menu e sem entrada visível para quem chega com problema de dados |
| NAV-08 | Média | A promessa "sem YAML" é quebrada logo no segundo passo do percurso não técnico |
| NAV-09 | Média | Páginas de modelo misturam quatro tipos Diátaxis, e a estrutura fixa tem variações |
| NAV-12 | Média | Referência dos campos não é alcançável de onde os campos aparecem |
| NAV-13 | Média | Falta o passo "Delimitar": ninguém ensina a planejar o acervo |
| NAV-10 | Baixa | Rótulos e endereços divergentes para a mesma escolha |
| NAV-11 | Baixa | Título "Visão geral" é ambíguo e colide com o rótulo do sumário do Starlight |
| NAV-14 | Baixa | Seletor de modelos duplica a tabela, ocupa muito espaço no celular e não oferece entrada por sintoma |
| NAV-15 | Baixa | Links de download inconsistentes: alguns forçam download, outros não |
| NAV-16 | Baixa | README classifica a rubrica como Dados, e o menu como Documentos do negócio |

## Achados

### NAV-01 · Nenhum caminho para o caso do analista com tag plan e eventos

**Severidade:** Alta

**Confiança:** Alta

**O que acontece:** Toda a trilha de Dados gira em torno de um único cenário: taxa de sessões convertidas em e-commerce. A busca por "tag plan", "plano de tags", "GTM", "GA4" ou "zerado" em `src/content/docs` não retorna nada. As perguntas que teriam evitado o falso positivo do evento raro (volume esperado, frequência histórica, granularidade por operação) não aparecem nas listas da trilha. A pergunta de frequência do modelo Dataset trata de atualização da carga, não de frequência do fenômeno. O conteúdo mais próximo está em páginas recolhidas, fora do percurso de dados.

**Evidências:**

- [src/content/docs/exemplos/analytics-integrado.mdx:12](../src/content/docs/exemplos/analytics-integrado.mdx#L12) `A loja Aurora quer documentar a **taxa de sessões web convertidas**.`
- [src/content/docs/dados/visao-geral.mdx:20](../src/content/docs/dados/visao-geral.mdx#L20) `- **Limites:** quais perguntas o dado não cobre, por canal, período ou unidade?`
- [src/content/docs/templates/dataset.mdx:33](../src/content/docs/templates/dataset.mdx#L33) `| Com que frequência atualiza, e com que atraso? | Carga diária ou estática? | Atualização |`
- [src/content/docs/metodo/limites.mdx:22](../src/content/docs/metodo/limites.mdx#L22) `A mesma palavra vale de um jeito numa unidade e de outro em outra. Um documento único esconde a diferença.`
- [astro.config.mjs:56](../astro.config.mjs#L56) `'metodo/visao-geral', 'metodo/oito-dimensoes', 'fundamentos/conhecimento-tacito', 'metodo/limites'`

**Impacto:** O analista que chega com o problema real (tag plan x Databricks, eventos zerados) não se reconhece em nenhuma página, não encontra o modelo certo e conclui que o framework serve só para indicadores de e-commerce. É o público que motivou o projeto.

**Recomendação:** Criar um segundo caso no laboratório ou uma página de cenário de mensuração (plano de tags, evento esperado por operação, linha de base histórica, regra para decidir se "zero é anomalia ou é raro"). Acrescentar ao modelo Dataset, ou a um novo modelo de evento, as perguntas de volume esperado e granularidade por operação. Ligar `metodo/limites` e a categoria "Ambígua" a partir da trilha de dados.

**Observação no portal:** Na página inicial em 390x844, o link para a trilha de dados fica em y≈2794 px, numa página de 3255 px de altura.

### NAV-02 · A jornada termina antes da IA: falta o passo de levar a documentação à ferramenta

**Severidade:** Alta

**Confiança:** Alta

**O que acontece:** O portal descreve o destino da documentação como um "engenheiro de IA" ou "quem constrói o sistema". O público descrito pelo mantenedor usa Claude Code, Codex, Antigravity ou NotebookLM diretamente. Nenhuma página ensina onde colocar os arquivos, como referenciá-los numa conversa ou num agente, nem como usar as Perguntas de referência para testar a própria ferramenta. Não há ocorrência de NotebookLM, Claude, Codex, Antigravity, AGENTS.md ou llms.txt em `src/content/docs`.

**Evidências:**

- [src/content/docs/validacao/checklist.mdx:70](../src/content/docs/validacao/checklist.mdx#L70) `Não cabe ao engenheiro de IA descobrir sozinho regras, significados ou exceções que a organização ainda não formalizou.`
- [src/content/docs/metodo/visao-geral.mdx:6](../src/content/docs/metodo/visao-geral.mdx#L6) `para que quem constrói sistemas de IA não precise adivinhar regras`
- [src/content/docs/metodo/limites.mdx:47](../src/content/docs/metodo/limites.mdx#L47) `Preencher os modelos não garante acerto de SQL, RAG ou agentes. Isso exige testes técnicos feitos por quem constrói o sistema.`
- [src/content/docs/templates/casos-teste.mdx:78](../src/content/docs/templates/casos-teste.mdx#L78) `A engenharia poderá usar essas perguntas em testes de recuperação, respostas e ferramentas.`

**Impacto:** A gestora e o analista chegam ao fim do percurso ("Revisar e entregar") sem saber o que fazer com os arquivos. Para eles, a promessa de preparar a documentação para a IA fica sem a última milha. Também falta a base de navegação para os futuros conteúdos de agentes, skills e WebMCP.

**Recomendação:** Criar um guia de tarefa "Usar a documentação com sua ferramenta de IA": organização de pastas versionadas, como citar documentos num prompt ou num arquivo de instruções, como rodar as Perguntas de referência como teste de aceitação. Posicioná-lo como último passo do percurso principal e deixá-lo como ponto de entrada da futura seção de agentes.

### NAV-03 · Perguntas de negócio, que deveriam abrir o percurso, estão no fim de um grupo recolhido e com três nomes

**Severidade:** Alta

**Confiança:** Alta

**O que acontece:** O objetivo declarado é produzir documentação a partir de perguntas de negócio. A página que trabalha perguntas (Perguntas de referência) é o último item do grupo recolhido "Dados e Analytics" e é classificada pelo seletor no grupo `dados`. O mesmo objeto tem três nomes: "Perguntas de referência" (título), "gabarito" (termo do contrato e do botão de download) e `casos-teste` (endereço). O guia "Descobrir o que falta", que traz as perguntas de investigação, só tem links externos (IIBA, KCS) e nenhum link interno de saída.

**Evidências:**

- [astro.config.mjs:53](../astro.config.mjs#L53) `'templates/relacionamento', 'templates/dashboard', 'templates/casos-teste'`
- [src/components/TemplateFinder.astro:12](../src/components/TemplateFinder.astro#L12) `{ group: 'dados', id: 'casos-teste', label: 'Definir quais perguntas podem ser respondidas'`
- [src/content/docs/templates/casos-teste.mdx:2](../src/content/docs/templates/casos-teste.mdx#L2) `title: Perguntas de referência`
- [src/components/TemplateDownloads.astro:56](../src/components/TemplateDownloads.astro#L56) `{ name: 'Modelo de gabarito', href: 'template-casos-teste.md'`
- [docs/CONTRATO_EDITORIAL.md:48](../docs/CONTRATO_EDITORIAL.md#L48) `Respostas certas de um conjunto de perguntas | gabarito`
- [src/content/docs/metodo/elicitar.mdx:44](../src/content/docs/metodo/elicitar.mdx#L44) `Este roteiro de perguntas é uma adaptação original do projeto.`

**Impacto:** O leitor não aprende a começar pela pergunta de negócio, que é a habilidade que o mantenedor quer ensinar. Quem não trabalha com dados dificilmente vê a página. Três nomes para a mesma coisa enfraquecem a credibilidade e a busca.

**Recomendação:** Promover as perguntas de negócio a etapa inicial do percurso (por exemplo: 1. escreva as perguntas que a IA deve responder; 2. descubra o que falta; 3. escolha o modelo; 4. revise; 5. teste com as perguntas). Unificar nome, título e endereço segundo o vocabulário do contrato. Tirar o modelo do grupo exclusivo de dados.

### NAV-04 · Menu não espelha o método de cinco movimentos nem os tipos Diátaxis, e as pastas não batem com os grupos

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** A página de método declara cinco movimentos e diz usar Diátaxis. O menu, porém, mistura tipos no mesmo grupo: "Comece por uma tarefa" junta tutorial, guia e hub; "Guias" tem só dois itens, embora outros guias estejam espalhados; "Consulta" junta referência, explicação e créditos. As três páginas da pasta `fundamentos` estão em três grupos diferentes (Comece por uma tarefa, Entenda o método, Consulta). O movimento "1. Delimitar" não tem página.

**Evidências:**

- [astro.config.mjs:46](../astro.config.mjs#L46) `{ label: 'Comece por uma tarefa', items: ['fundamentos/comece-em-5-minutos', 'validacao/checklist', 'templates'] },`
- [astro.config.mjs:47](../astro.config.mjs#L47) `{ label: 'Guias', items: ['metodo/elicitar', 'metodo/identificacao-versoes'] },`
- [astro.config.mjs:59](../astro.config.mjs#L59) `'fundamentos/como-ler-os-campos', 'governanca/papeis', 'referencias', 'sobre/creditos'`
- [src/content/docs/metodo/visao-geral.mdx:16](../src/content/docs/metodo/visao-geral.mdx#L16) `| **1. Delimitar** | Identificar o assunto, quem o usa e quando vale | Objetivo e escopo |`
- [src/content/docs/metodo/visao-geral.mdx:42](../src/content/docs/metodo/visao-geral.mdx#L42) `o [Diátaxis](https://diataxis.fr/), para organizar a documentação pelo que o leitor precisa fazer`

**Impacto:** O leitor não consegue formar um modelo mental do portal pela navegação. É a sensação de colcha de retalhos que o mantenedor descreve. Quem mantiver o portal no futuro também não sabe onde encaixar páginas novas (agentes, skills, WebMCP).

**Recomendação:** Redesenhar o menu em torno do percurso (os cinco movimentos como guias numerados), mais uma área de Referência (modelos, campos, papéis, bibliografia) e uma de Entender (explicações). Alinhar pastas e endereços aos grupos e registrar no contrato editorial a regra de classificação Diátaxis de cada página. Referência: [https://diataxis.fr/](https://diataxis.fr/).

### NAV-05 · Paginação automática sugere próximos passos ilógicos

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O Starlight gera anterior e próximo pela ordem do menu, e nenhuma página define `prev`, `next` ou `pagination` no frontmatter. O resultado: "Comece em 5 minutos" aponta para "Revisar e entregar"; "Encontrar um modelo" aponta para "Descobrir o que falta" (que deveria vir antes); "Rubrica de avaliação" aponta para "Por que dados precisam de contexto"; "Perguntas de referência" aponta para "Visão geral" do método.

**Evidências:**

- [astro.config.mjs:46](../astro.config.mjs#L46) `{ label: 'Comece por uma tarefa', items: ['fundamentos/comece-em-5-minutos', 'validacao/checklist', 'templates'] },`
- [astro.config.mjs:49](../astro.config.mjs#L49) `'templates/conceito', 'templates/processo', 'templates/decisao', 'templates/politica', 'templates/rubrica'`
- [astro.config.mjs:52](../astro.config.mjs#L52) `'dados/visao-geral', 'exemplos/analytics-integrado', 'templates/kpi', 'templates/dataset',`

**Impacto:** A gestora que segue o "Próximo" depois do tutorial cai numa página de revisão e entrega (1088 palavras no MDX, com YAML) antes de ter um documento. Para quem lê em sequência, a paginação contradiz o próprio bloco "O que fazer depois?".

**Recomendação:** Reordenar o menu para que a sequência linear faça sentido, ou definir `prev`/`next` no frontmatter das páginas do percurso principal e desligar a paginação nas páginas de referência. Documentação dos campos: [https://starlight.astro.build/reference/frontmatter/](https://starlight.astro.build/reference/frontmatter/).

**Observação no portal:** Links de paginação lidos no portal publicado: `comece-em-5-minutos` mostra "Próximo Revisar e entregar"; `templates/` mostra "Próximo Descobrir o que falta"; `templates/rubrica/` mostra "Próximo Por que dados precisam de contexto"; `templates/casos-teste/` mostra "Próximo Visão geral".

### NAV-06 · Becos sem saída e páginas órfãs

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Três páginas não têm nenhum link interno de saída no corpo, só links externos (`metodo/elicitar`, `governanca/papeis`, `referencias`). Duas não recebem nenhum link de outra página em `src` e só aparecem no menu recolhido "Entenda o método": `fundamentos/conhecimento-tacito` e `metodo/visao-geral`, que é justamente o hub "Onde cada peça entra". As páginas de modelo terminam em "### Fundamentação" com links externos e nenhuma delas linka "Revisar e entregar" (os únicos links para `validacao/checklist` vêm do tutorial, de `metodo/visao-geral` e da página inicial).

**Evidências:**

- [src/content/docs/metodo/elicitar.mdx:40](../src/content/docs/metodo/elicitar.mdx#L40) `Peça que quem responde pelo conteúdo confirme por escrito o resultado.`
- [src/content/docs/governanca/papeis.mdx:57](../src/content/docs/governanca/papeis.mdx#L57) `A tabela RACI é uma proposta do framework.`
- [src/content/docs/metodo/visao-geral.mdx:26](../src/content/docs/metodo/visao-geral.mdx#L26) `| Se você precisa… | Use |`
- [src/content/docs/templates/dataset.mdx:68](../src/content/docs/templates/dataset.mdx#L68) `Os nossos campos são **uma proposta**, não schemas dessas plataformas.`
- [src/content/docs/templates/conceito.mdx:85](../src/content/docs/templates/conceito.mdx#L85) `**Antes de pedir aprovação:** uma pessoa de outra área consegue explicar o termo`

**Impacto:** O ciclo preencher, revisar e entregar não se fecha pela navegação. O melhor mapa do portal fica escondido. O leitor depende do menu recolhido para continuar.

**Recomendação:** Padronizar um bloco final "Próximo passo" em todas as páginas (modelos levam a "Revisar e entregar" e ao modelo relacionado; guias levam ao modelo). Linkar `metodo/visao-geral` a partir da página inicial e do tutorial. Incluir em `metodo/elicitar` e `governanca/papeis` links para os modelos e para o checklist.

### NAV-07 · Página inicial sem menu e sem entrada visível para quem chega com problema de dados

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** A página inicial usa o template `splash` com o menu lateral escondido, então quem chega não vê a estrutura do portal. Os três blocos de tarefa são genéricos (primeiro documento, revisar, modelo). A trilha de dados aparece só como link no último parágrafo, depois dos blocos e da seção do laboratório.

**Evidências:**

- [src/content/docs/index.mdx:4](../src/content/docs/index.mdx#L4) `template: splash`
- [src/content/docs/index.mdx:6](../src/content/docs/index.mdx#L6) `hidden: true`
- [src/content/docs/index.mdx:26](../src/content/docs/index.mdx#L26) `Para trabalho com tabelas e dashboards, entre pela [trilha de Dados e Analytics](dados/visao-geral/).`
- [src/components/PrincipleTiles.astro:4](../src/components/PrincipleTiles.astro#L4) `index: '01', category: 'PRIMEIRO DOCUMENTO',`

**Impacto:** O analista (visitante 2) não encontra na primeira tela uma situação que descreva o problema dele ("a IA me deu um número que não confere"). No celular precisa rolar mais de três telas.

**Recomendação:** Acrescentar um quarto bloco por sintoma, por exemplo "A IA respondeu com dados, mas errado para o nosso contexto", levando à trilha de dados. Avaliar exibir na página inicial um mapa curto do percurso. Sobre o template: [https://starlight.astro.build/reference/frontmatter/](https://starlight.astro.build/reference/frontmatter/).

**Observação no portal:** Em 390x844 a página inicial não tem botão de menu (`starlight-menu-button` ausente). O cabeçalho só oferece busca e links sociais. O link da trilha de dados está em y≈2794 px de 3255 px.

### NAV-08 · A promessa "sem YAML" é quebrada logo no segundo passo do percurso não técnico

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** A página de revisão promete que não é preciso escrever YAML, mas ela mesma, que é o segundo item do menu e o próximo da paginação a partir do tutorial, mostra uma ficha de entrega num bloco `yaml`. O guia "Descobrir o que falta" ensina a registrar respostas num bloco YAML. A página de versões também pressupõe alguém que "passa para YAML".

**Evidências:**

- [src/content/docs/validacao/checklist.mdx:13](../src/content/docs/validacao/checklist.mdx#L13) `Não é necessário conhecer IA, escrever YAML ou usar uma ferramenta especial.`
- [src/content/docs/validacao/checklist.mdx:85](../src/content/docs/validacao/checklist.mdx#L85) `id: HANDOFF-001`
- [src/content/docs/metodo/elicitar.mdx:28](../src/content/docs/metodo/elicitar.mdx#L28) `question: "O pedido cancelado entra no indicador?"`
- [src/content/docs/metodo/identificacao-versoes.mdx:50](../src/content/docs/metodo/identificacao-versoes.mdx#L50) `` e quem passa para YAML registra o dia seguinte (`2026-09-01`) ``

**Impacto:** A gestora perde a confiança na promessa principal e conclui que o material é técnico. A mistura também viola a separação Diátaxis entre guia e referência.

**Recomendação:** Nas páginas de guia, mostrar o registro em formato de texto ou tabela (como no tutorial) e mover o YAML para uma aba ou para a referência "Como ler os campos", seguindo o padrão do `ExampleDoc`.

### NAV-09 · Páginas de modelo misturam quatro tipos Diátaxis, e a estrutura fixa tem variações

**Severidade:** Média

**Confiança:** Média

**O que acontece:** Por desenho do contrato, cada página de tipo junta explicação (O problema), guia (O que perguntar), referência (cartões, YAML, downloads) e exercício (Teste você). Duas páginas (processo e política) acrescentam "Verifique o seu documento" e outras acrescentam seções próprias (rubrica, conceito), o que quebra a previsibilidade. As maiores passam de mil palavras (processo 1310, rubrica 1190, política 1030, contadas com `wc -w` no MDX).

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:137](../docs/CONTRATO_EDITORIAL.md#L137) `1. **O problema**, com números: uma situação da Aurora em que a falta do documento custa algo visível.`
- [docs/CONTRATO_EDITORIAL.md:140](../docs/CONTRATO_EDITORIAL.md#L140) `4. **Teste você**, com as respostas escondidas.`
- [src/content/docs/templates/processo.mdx:110](../src/content/docs/templates/processo.mdx#L110) `## Verifique o seu documento`
- [src/content/docs/templates/rubrica.mdx:92](../src/content/docs/templates/rubrica.mdx#L92) `## O que uma IA revisora pode e não pode fazer`

**Impacto:** Quem volta à página só para consultar um campo ou baixar o modelo precisa atravessar a narrativa. Quem quer aprender perde o fio com as seções de referência. Não é grave para o público misto, mas cresce com cada modelo novo.

**Recomendação:** Manter o formato de exemplo trabalhado, que funciona para público não técnico. Separar a referência de campos por modelo numa subpágina ou num bloco recolhível. Padronizar "Verifique o seu documento" em todos os modelos ou em nenhum.

### NAV-12 · Referência dos campos não é alcançável de onde os campos aparecem

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** "Como ler os campos" explica `null`, estados, versão e o mínimo que um documento precisa ter. Só recebe links de duas páginas de método (`metodo/limites` e `metodo/identificacao-versoes`) e fica no grupo recolhido "Consulta". Nenhum modelo, nem o `TemplateStart`, nem a aba "Identificação e histórico" do cartão de exemplo aponta para ela.

**Evidências:**

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:8](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L8) `## O mínimo que um documento precisa ter`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:43](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L43) `Não é erro e não é zero.`
- [src/components/ExampleDoc.astro:84](../src/components/ExampleDoc.astro#L84) `<TabItem label="Identificação e histórico">`
- [astro.config.mjs:59](../astro.config.mjs#L59) `'fundamentos/como-ler-os-campos', 'governanca/papeis', 'referencias', 'sobre/creditos'`

**Impacto:** A gestora vê "Pendente de aprovação", "ID da versão" e `null` nos cartões sem um caminho para entender o que significam. A seção "O mínimo" é a melhor resposta para "por onde começo", e quase ninguém a encontra.

**Recomendação:** Linkar "Como ler os campos" a partir do `TemplateStart`, do `ExampleDoc` e de `templates/index`. Considerar mover "O mínimo que um documento precisa ter" para o percurso principal.

### NAV-13 · Falta o passo "Delimitar": ninguém ensina a planejar o acervo

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O método começa por delimitar assunto, usuários e vigência, mas o mapa "Onde cada peça entra" não tem linha para isso e não existe página correspondente. O tutorial e os próximos passos tratam sempre de um documento isolado, nunca de qual conjunto de documentos fazer primeiro para uma pergunta complexa.

**Evidências:**

- [src/content/docs/metodo/visao-geral.mdx:16](../src/content/docs/metodo/visao-geral.mdx#L16) `| **1. Delimitar** | Identificar o assunto, quem o usa e quando vale | Objetivo e escopo |`
- [src/content/docs/metodo/visao-geral.mdx:28](../src/content/docs/metodo/visao-geral.mdx#L28) `| Descobrir o que ainda não está escrito | [Descobrir o que falta](../elicitar/) |`
- [src/content/docs/templates/index.mdx:29](../src/content/docs/templates/index.mdx#L29) `Os dois documentos se ligam pelo identificador, sem repetir o conteúdo.`

**Impacto:** Para consultas complexas (várias tabelas, vários dashboards), o leitor não sabe por onde começar nem como montar o conjunto. Era exatamente a dor declarada pelo mantenedor.

**Recomendação:** Criar um guia "Planejar o acervo a partir de uma pergunta de negócio": listar as perguntas, mapear fontes e dashboards envolvidos, escolher os documentos mínimos e a ordem. Usar o Laboratório Aurora como exemplo de saída.

### NAV-10 · Rótulos e endereços divergentes para a mesma escolha

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A mesma opção tem textos diferentes no seletor, na tabela da mesma página, no bloco da página inicial e no título. Vários endereços não correspondem ao título (`validacao/checklist` para "Revisar e entregar"), e um usa o termo que o contrato proíbe no texto (`elicitar`).

**Evidências:**

- [src/components/TemplateFinder.astro:4](../src/components/TemplateFinder.astro#L4) `label: 'Descrever como um trabalho é executado'`
- [src/content/docs/templates/index.mdx:17](../src/content/docs/templates/index.mdx#L17) `| Descrever as etapas de um trabalho | [Processo](processo/) |`
- [src/components/PrincipleTiles.astro:12](../src/components/PrincipleTiles.astro#L12) `title: 'Revisar o que já está escrito',`
- [src/content/docs/validacao/checklist.mdx:2](../src/content/docs/validacao/checklist.mdx#L2) `title: Revisar e entregar`
- [docs/CONTRATO_EDITORIAL.md:50](../docs/CONTRATO_EDITORIAL.md#L50) `| Descobrir conhecimento com as pessoas | descobrir, perguntar | elicitar, fora da bibliografia |`
- [astro.config.mjs:21](../astro.config.mjs#L21) `` '/metodo/revisao-e-entrega/': `${base}/validacao/checklist/`, ``

**Impacto:** Reduz a confiança ("cliquei em X e cheguei em Y") e dificulta citar e compartilhar links estáveis, que importam para documentação versionada.

**Recomendação:** Definir um rótulo canônico por página no contrato e reutilizá-lo no seletor, na tabela e na página inicial. Planejar a troca de endereços (com redirecionamentos) para que o endereço reflita o título.

### NAV-11 · Título "Visão geral" é ambíguo e colide com o rótulo do sumário do Starlight

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A página do método se chama apenas "Visão geral", o mesmo texto que o Starlight usa como primeiro item do sumário das páginas. A pasta de dados também tem um `visao-geral`, com outro título.

**Evidências:**

- [src/content/docs/metodo/visao-geral.mdx:2](../src/content/docs/metodo/visao-geral.mdx#L2) `title: Visão geral`
- [src/content/docs/dados/visao-geral.mdx:2](../src/content/docs/dados/visao-geral.mdx#L2) `title: Por que dados precisam de contexto`

**Impacto:** Na paginação e nos resultados de busca, "Visão geral" não diz de quê. O leitor confunde a página com a âncora do topo.

**Recomendação:** Renomear para algo como "Como o método funciona" e alinhar o endereço.

**Observação no portal:** O sumário de `comece-em-5-minutos` começa com "Visão geral" (âncora do Starlight). A paginação de `templates/casos-teste/` mostra "Próximo Visão geral".

### NAV-14 · Seletor de modelos duplica a tabela, ocupa muito espaço no celular e não oferece entrada por sintoma

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** Em `templates/index`, o `TemplateFinder` repete as mesmas dez opções da tabela "Todos os modelos", com rótulos diferentes. As ações ficam escondidas até a escolha, via JavaScript. As opções são tipos de documento descritos como tarefa, sem entrada por sintoma (dois relatórios divergem, a IA usou definição genérica, evento aparece zerado).

**Evidências:**

- [src/components/TemplateFinder.astro:39](../src/components/TemplateFinder.astro#L39) `<div class="finder-output__actions" data-actions hidden>`
- [src/components/TemplateFinder.astro:24](../src/components/TemplateFinder.astro#L24) `<p>Escolha o resultado que deseja produzir. Você pode ler as orientações ou baixar imediatamente o modelo em texto simples.</p>`
- [src/content/docs/templates/index.mdx:12](../src/content/docs/templates/index.mdx#L12) `## Todos os modelos`

**Impacto:** Gera rolagem e redundância. Quem pensa no problema, e não no tipo de documento, não encontra caminho.

**Recomendação:** Manter um só mecanismo (a tabela é suficiente e funciona sem JavaScript) ou transformar o seletor numa entrada por sintoma que leva a um ou mais modelos.

**Observação no portal:** Em 390x844 o seletor mede cerca de 1359 px e a tabela "Todos os modelos" começa em y≈1802 px.

### NAV-15 · Links de download inconsistentes: alguns forçam download, outros não

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** Os componentes usam o atributo `download`, mas os links em Markdown do tutorial e da tabela de modelos não. O servidor entrega `.md` como `text/markdown` sem `Content-Disposition`, então o resultado depende do navegador (abrir texto cru ou baixar).

**Evidências:**

- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:58](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L58) `[baixar o modelo de conceito em texto simples](../../downloads/template-conceito.md)`
- [src/content/docs/templates/index.mdx:16](../src/content/docs/templates/index.mdx#L16) `[Baixar](../downloads/template-conceito.md)`
- [src/components/TemplateStart.astro:86](../src/components/TemplateStart.astro#L86) `<a href={base + 'downloads/template-' + kind + '.md'} download>`

**Impacto:** O leitor não técnico pode ver uma página de texto cru com marcações em vez de um arquivo, justamente no primeiro clique do tutorial.

**Recomendação:** Usar o mesmo componente de download em todos os pontos ou oferecer também um formato que abra direto no Google Docs ou no Word.

**Observação no portal:** HEAD em `/contexto-framework/downloads/template-conceito.md` retornou 200, `content-type: text/markdown; charset=utf-8`, sem `content-disposition`.

### NAV-16 · README classifica a rubrica como Dados, e o menu como Documentos do negócio

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** O README põe Rubricas e Perguntas de referência na "Trilha de Dados e Analytics". O menu põe a Rubrica em "Documentos do negócio" e Perguntas de referência em Dados.

**Evidências:**

- [README.md:22](../README.md#L22) `### Trilha de Dados e Analytics`
- [README.md:26](../README.md#L26) `- **Rubricas** com critérios explícitos, evidências, níveis e revisão humana;`
- [astro.config.mjs:49](../astro.config.mjs#L49) `'templates/conceito', 'templates/processo', 'templates/decisao', 'templates/politica', 'templates/rubrica'`

**Impacto:** Quem chega pelo GitHub forma um mapa diferente do portal, o que reforça a sensação de inconsistência.

**Recomendação:** Gerar a lista do README a partir da mesma estrutura do menu, ou revisá-la junto com cada mudança de navegação.

## Não coberto nesta rodada

- Lighthouse e acessibilidade (leitor de tela, ordem de foco, contraste) não foram executados.
- Tema escuro e o menu lateral móvel nas páginas internas não foram inspecionados visualmente.
- A qualidade da busca (Pagefind) para termos como "tag plan", "GA4" ou "evento" não foi testada no portal.
- O conteúdo dos arquivos em `public/downloads` (modelos `.md`/`.yaml` e roteiro de revisão) não foi lido.
- As páginas `templates/processo`, `rubrica`, `politica`, `decisao`, `kpi`, `dashboard` e `relacionamento` foram lidas só pelos títulos de seção e trechos finais, não na íntegra.
- `scripts/validate_content.py` e o build não foram executados (execução bloqueada); a contagem de links internos foi feita por grep e pode não pegar links montados em componentes.
- O diretório `auditoria/` que já existia na raiz não foi examinado.
- Links externos da Fundamentação não foram verificados.
- As observações no portal vêm da rodada anterior e não foram reproduzidas nesta verificação, que conferiu apenas o repositório.
