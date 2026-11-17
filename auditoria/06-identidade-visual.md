# Identidade visual

Data: 2026-11-17 · Commit: d08c810 · Escopo: sistema visual do portal (`src/styles/custom.css`, componentes em `src/components/`, uso de componentes do Starlight no conteúdo, `astro.config.mjs`, `package.json`, logo e favicon, documentação de apoio em `README.md` e `docs/`), com observações pontuais no portal publicado em https://edoardolobl.github.io/contexto-framework/

## Resumo

- Há uma boa base de tokens `--context-*` com par claro e escuro, usada pela maior parte dos componentes. É o ponto de partida certo para um sistema de design.
- O CSS cresceu por rodada de trabalho (v0.2, Checkpoint A a E, Segunda rodada) e não por componente. Não existem primitivas de cartão, rótulo, botão e aviso: cada componente reescreve o mesmo padrão com raio, espaçamento e nome de modificador próprios. Essa é a origem técnica da sensação de colcha de retalhos.
- O tema escuro não tem identidade própria completa: herda os neutros cinza azulados do Starlight, enquanto o tema claro redefine fundo, navegação e linhas em tons creme.
- A fonte Inter é declarada mas nunca carregada, e a escala tipográfica tem 36 tamanhos distintos, muitos separados por 0,01rem.
- O arquivo de estilo tem 47 usos de `!important` e seletores acoplados ao DOM interno do Starlight, o que deixa o layout frágil a atualizações da dependência.
- Não existe guia visual escrito, e a conferência visual nos dois temas segue em aberto no ROADMAP. Sem esse guia, novos blocos (agentes, skills, WebMCP) tendem a repetir o problema.

## Pontos fortes (manter)

**Paleta própria em tokens com par claro/escuro.** Superfícies, linhas, texto e dourado vêm de custom properties `--context-*` redefinidas no tema claro, e a maior parte dos componentes as usa. É a base certa para um sistema de design; falta completar.

- [src/styles/custom.css:9](../src/styles/custom.css#L9) `--context-ink: #e9f0ec;`
- [src/styles/custom.css:24](../src/styles/custom.css#L24) `--context-ink: #172c24;`
- [src/styles/custom.css:80](../src/styles/custom.css#L80) `.comparison-panel {padding:1.4rem;border:1px solid var(--context-line);border-radius:8px;background:var(--context-surface)}`

**Reuso de Tabs e Code nativos do Starlight no ExampleDoc.** O cartão de exemplo usa os componentes oficiais em vez de reinventar abas e bloco de código, e com isso herda navegação por teclado e consistência com o restante do Starlight.

- [src/components/ExampleDoc.astro:11](../src/components/ExampleDoc.astro#L11) `import { Code, Tabs, TabItem } from '@astrojs/starlight/components';`
- [src/components/ExampleDoc.astro:108](../src/components/ExampleDoc.astro#L108) `<Code code={raw} lang="yaml" title={file} />`

**Diagrama SVG que segue o tema.** O JoinDiagram pinta caixas, linhas e textos com tokens e não com cores fixas, então funciona nos dois temas sem regra extra.

- [src/components/JoinDiagram.astro:63](../src/components/JoinDiagram.astro#L63) `.jd-box { fill: var(--context-surface); stroke: var(--context-line); stroke-width: 1.5; }`
- [src/components/JoinDiagram.astro:64](../src/components/JoinDiagram.astro#L64) `.jd-box--hit { fill: var(--sl-color-accent-low); stroke: var(--sl-color-accent); stroke-width: 2; }`

**Foco visível e respeito a movimento reduzido.** Links, botões e controles próprios recebem contorno de foco, e as transições são desligadas com `prefers-reduced-motion`.

- [src/styles/custom.css:250](../src/styles/custom.css#L250) `.template-downloads a:focus-visible,`
- [src/styles/custom.css:120](../src/styles/custom.css#L120) `@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}`

**Tabelas largas com rolagem própria e focável.** O histórico rola dentro de um contêiner com `role=region` e `tabindex`, sem quebrar a página no celular. No portal, a 390px, `scrollWidth` igual a `clientWidth` nas páginas testadas.

- [src/components/ExampleDoc.astro:96](../src/components/ExampleDoc.astro#L96) `<div class="example-doc__history-scroll" role="region" aria-label="Histórico de mudanças do documento" tabindex="0">`
- [src/styles/custom.css:740](../src/styles/custom.css#L740) `.example-doc__history-scroll {`

**Algumas classes já são compartilhadas entre componentes.** `panel-kicker` é usada em BeforeAfter, RevisionComparison e ExampleDoc, e `template-downloads` é reaproveitada pelo laboratório. É o embrião das primitivas que faltam.

- [src/components/RevisionComparison.astro:32](../src/components/RevisionComparison.astro#L32) `<p class="panel-kicker">{i === 0 ? 'VERSÃO HISTÓRICA · NÃO VIGENTE' : 'VERSÃO ATUAL'}</p>`
- [src/components/AnalyticsLabDownloads.astro:10](../src/components/AnalyticsLabDownloads.astro#L10) `<div class="template-downloads" role="group" aria-label="Arquivos do laboratório Aurora">`

**Abas com `color-mix` sobre tokens.** O trilho e a aba ativa derivam do token de texto por `color-mix`, o que mantém a relação de contraste nos dois temas sem duplicar cores.

- [src/styles/custom.css:851](../src/styles/custom.css#L851) `background: color-mix(in srgb, var(--context-ink) 7%, transparent);`

**Contraste do tema escuro confortável.** Recalculado pela fórmula WCAG: texto secundário `#a8c1b5` sobre `#16251f` dá 8,31:1; acento `#addfc5` dá 10,72:1; dourado `#e1bd81` dá 8,95:1.

- [src/styles/custom.css:13](../src/styles/custom.css#L13) `--context-muted: #a8c1b5;`
- [src/styles/custom.css:10](../src/styles/custom.css#L10) `--context-surface: #16251f;`

## Índice de achados

| ID | Severidade | Título |
|---|---|---|
| VIS-01 | Alta | Não existe uma primitiva de cartão: oito ou mais variações com raio, espaçamento e modificador diferentes |
| VIS-02 | Alta | Tema escuro herda neutros cinza azulados do Starlight, tema claro tem neutros próprios |
| VIS-03 | Média | Cerca de 25 cores fixas fora dos tokens e vários verdes e dourados de marca quase iguais |
| VIS-04 | Média | Sete classes diferentes para o mesmo rótulo superior (eyebrow/kicker) |
| VIS-05 | Média | Cinco estilos de botão sem componente comum |
| VIS-06 | Média | Fonte Inter declarada mas nunca carregada |
| VIS-07 | Média | Escala tipográfica sem passos: 36 tamanhos de fonte distintos e serifa sem token |
| VIS-08 | Média | CSS organizado por rodada de trabalho e não por componente, com dois estilos de escrita |
| VIS-09 | Média | 47 usos de `!important` e seletores acoplados ao DOM interno do Starlight |
| VIS-10 | Média | Componentes próprios duplicam componentes nativos do Starlight |
| VIS-11 | Média | Hierarquia de títulos visual e semântica desalinhadas |
| VIS-12 | Média | Selo de rascunho em dourado abaixo do contraste AA no tema claro |
| VIS-20 | Média | Sem guia visual documentado e conferência visual em aberto no ROADMAP |
| VIS-13 | Baixa | Seletores sem uso e classes sem estilo |
| VIS-14 | Baixa | Regras duplicadas ou que se sobrepõem |
| VIS-15 | Baixa | Treze regras `@media` de largura com dez valores diferentes |
| VIS-16 | Baixa | Avisos e destaques com borda lateral em quatro variações, além do Aside nativo |
| VIS-17 | Baixa | Contorno de foco com espessura e afastamento diferentes |
| VIS-18 | Baixa | Recuo de `dd` diferente entre abas do mesmo cartão |
| VIS-19 | Baixa | Estratégia de estilo mista: um componente com `style` escopado, os demais no CSS global |

## Achados

### VIS-01 · Não existe uma primitiva de cartão: oito ou mais variações com raio, espaçamento e modificador diferentes

**Severidade:** Alta

**Confiança:** Alta

**O que acontece:** o mesmo padrão visual (borda `var(--context-line)`, fundo `var(--context-surface)`, destaque com borda de acento e `surface-2`) é reescrito em cada componente: `principle-tile`, `template-downloads a`, `comparison-panel`, `readiness`, `template-finder`, `example-doc`, `template-start`, `revision-comparison__card`, `review-stages__card` e `jd-count`. Os raios variam entre 7, 8, 9 e 10px, os espaçamentos internos entre valores fixos e `clamp` diferentes, e o mesmo modificador de destaque tem quatro nomes (`--after`, `--complete`, `--current`, `--right`). O arquivo tem 12 valores distintos de `border-radius`.

**Evidências:**

- [src/styles/custom.css:73](../src/styles/custom.css#L73) `border-radius:7px`
- [src/styles/custom.css:80](../src/styles/custom.css#L80) `.comparison-panel {padding:1.4rem;border:1px solid var(--context-line);border-radius:8px;background:var(--context-surface)}`
- [src/styles/custom.css:90](../src/styles/custom.css#L90) `.readiness{border:1px solid var(--context-line);border-radius:9px;background:var(--context-surface);padding:clamp(1rem,3vw,1.65rem);margin:1.7rem 0}`
- [src/styles/custom.css:169](../src/styles/custom.css#L169) `border-radius: 10px;`
- [src/styles/custom.css:81](../src/styles/custom.css#L81) `.comparison-panel--after {border-color:var(--sl-color-accent);background:var(--context-surface-2)}`
- [src/styles/custom.css:275](../src/styles/custom.css#L275) `.example-doc--complete { border-color: var(--sl-color-accent); background: var(--context-surface-2); }`
- [src/styles/custom.css:441](../src/styles/custom.css#L441) `.revision-comparison__card--current {`
- [src/components/JoinDiagram.astro:70](../src/components/JoinDiagram.astro#L70) `.jd-count--right { border-color: var(--sl-color-accent); }`

**Impacto:** cada componente novo (skills, WebMCP, agentes) tende a criar mais uma variação. O leitor percebe pequenas diferenças de canto e respiro entre páginas, o que reforça a sensação de colcha de retalhos e torna qualquer ajuste de marca caro.

**Recomendação:** criar tokens de raio e de espaçamento e uma classe base de cartão com um único modificador de destaque. Migrar `comparison-panel`, `example-doc`, `readiness`, `template-finder`, `template-start`, `revision-comparison__card`, `review-stages__card`, `principle-tile` e `jd-count` para ela, ou para Card/CardGrid do Starlight onde couber (https://starlight.astro.build/components/cards/).

**Observação no portal:** medido em /templates/kpi/ a 390px: `template-start` com raio 8px e padding 16px, `comparison-panel` 8px e 22.4px, `example-doc` 9px e 16px, links de download 7px e 16px 14.4px.

### VIS-02 · Tema escuro herda neutros cinza azulados do Starlight, tema claro tem neutros próprios

**Severidade:** Alta

**Confiança:** Alta

**O que acontece:** o bloco do tema claro redefine fundo, navegação, barra lateral e linha fina com tons creme. O bloco padrão (escuro) só redefine acentos, fonte, larguras e tokens `--context-*`, sem nenhum `--sl-color-bg`. Resultado: no escuro, cartões verdes (`#16251f`) ficam sobre o fundo padrão do Starlight, de matiz azulado. As duas identidades não são equivalentes.

**Evidências:**

- [src/styles/custom.css:20](../src/styles/custom.css#L20) `--sl-color-bg: #faf9f6;`
- [src/styles/custom.css:21](../src/styles/custom.css#L21) `--sl-color-bg-nav: #fbfaf7;`
- [src/styles/custom.css:23](../src/styles/custom.css#L23) `--sl-color-hairline-light: #e8e5dc;`
- [src/styles/custom.css:10](../src/styles/custom.css#L10) `--context-surface: #16251f;`

**Impacto:** quem usa o sistema em modo escuro vê uma marca diferente, com contraste de matiz entre verde e azul. Passa a impressão de tema não terminado e reduz a credibilidade.

**Recomendação:** definir no `:root` escuro também `--sl-color-bg`, `--sl-color-bg-nav`, `--sl-color-bg-sidebar`, `--sl-color-hairline` e, idealmente, a escala `--sl-color-gray-1..6` com matiz verde coerente com `--context-surface` (variáveis documentadas em https://starlight.astro.build/guides/css-and-tailwind/). Validar o contraste depois da troca.

**Observação no portal:** com `prefers-color-scheme: dark`, `--sl-color-bg` = `#17181c`, `--sl-color-bg-nav` = `#23262f`, `body` `rgb(23,24,28)`. Screenshot da página inicial e de /templates/kpi/ mostra cartões verdes sobre fundo cinza azulado.

### VIS-03 · Cerca de 25 cores fixas fora dos tokens e vários verdes e dourados de marca quase iguais

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** fora dos blocos de token (linhas 31 a 936) há 26 hexadecimais diretos: botão principal, botão do seletor, checkbox, ponto do eyebrow, aba ativa clara e todo o cartão visual da página inicial. Há verdes de marca diferentes (`#205a46`, `#2f745b`, `#2c7956` no CSS, `#256047` no token claro, `#214b40` no logo) e dourados diferentes (`#a27a4c`, `#e5c997`, `#e2c389`, `#8c6031` no CSS, `#d7b67b` no logo) além do token `--context-gold`. Logo e favicon também diferem no raio (`rx` 12 e 10).

**Evidências:**

- [src/styles/custom.css:52](../src/styles/custom.css#L52) `.cta-primary {color:#fff!important;background:#205a46}`
- [src/styles/custom.css:402](../src/styles/custom.css#L402) `background: #205a46;`
- [src/styles/custom.css:105](../src/styles/custom.css#L105) `accent-color:#2c7956`
- [src/styles/custom.css:229](../src/styles/custom.css#L229) `accent-color: var(--sl-color-accent);`
- [src/styles/custom.css:48](../src/styles/custom.css#L48) `.eyebrow-dot {width:8px;height:8px;display:inline-block;background:#a27a4c;border-radius:100%}`
- [src/styles/custom.css:56](../src/styles/custom.css#L56) `.context-hero__visual {background:#152820;color:#edf2e9;border:1px solid #314c3c;border-radius:8px;`
- [src/styles/custom.css:876](../src/styles/custom.css#L876) `background: #fff;`
- [src/assets/brand.svg:2](../src/assets/brand.svg#L2) `rx="12" fill="#214b40"`
- [public/favicon.svg:1](../public/favicon.svg#L1) `rx="10" fill="#214b40"`

**Impacto:** mudar a cor da marca exige caçar valores no arquivo. O checkbox (`#2c7956`) e o rádio (`var(--sl-color-accent)`) têm cores diferentes no mesmo site; no tema escuro o rádio fica verde-claro e o checkbox verde-escuro.

**Recomendação:** criar tokens de marca (cor principal, hover, dourado) com par claro/escuro, derivar o cartão visual da página inicial de tokens, unificar `accent-color` em `var(--sl-color-accent)` e alinhar logo e favicon.

**Observação no portal:** em /validacao/checklist/ no tema escuro, `accentColor` do checkbox computado como `rgb(44,121,86)`, enquanto o rádio do seletor usa o acento `#addfc5`.

### VIS-04 · Sete classes diferentes para o mesmo rótulo superior (eyebrow/kicker)

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** o rótulo pequeno acima de títulos aparece como `.eyebrow`, `.panel-kicker`, `.finder-eyebrow`, `.template-start__eyebrow`, `.tile-index`, `.jd-kicker` e `.review-stages__number`, com tamanhos de .7 a .84rem, espaçamento entre letras de .08em a .15em, cor ora acento ora muted, fonte ora sans ora mono. Só `.template-start__eyebrow` usa `text-transform`, e mesmo nele o texto já vem digitado em maiúsculas no markup, como nos demais.

**Evidências:**

- [src/styles/custom.css:47](../src/styles/custom.css#L47) `.eyebrow {display:inline-flex;align-items:center;gap:.55rem;color:var(--sl-color-accent);font-size:.8rem;letter-spacing:.15em;font-weight:800;line-height:1.3}`
- [src/styles/custom.css:82](../src/styles/custom.css#L82) `.panel-kicker {font-size:.8rem;font-weight:800;letter-spacing:.115em;color:var(--context-muted)}`
- [src/styles/custom.css:75](../src/styles/custom.css#L75) `.tile-index{font-family:var(--sl-font-mono);font-size:.7rem;letter-spacing:.09em;color:var(--context-muted)}`
- [src/styles/custom.css:175](../src/styles/custom.css#L175) `letter-spacing: .08em;`
- [src/styles/custom.css:325](../src/styles/custom.css#L325) `letter-spacing: .095em;`
- [src/styles/custom.css:326](../src/styles/custom.css#L326) `text-transform: uppercase;`
- [src/components/TemplateStart.astro:66](../src/components/TemplateStart.astro#L66) `<p class="template-start__eyebrow">ANTES DE PREENCHER</p>`
- [src/components/JoinDiagram.astro:72](../src/components/JoinDiagram.astro#L72) `.jd-kicker { font-size: .72rem !important; letter-spacing: .08em; font-weight: 700; color: var(--context-muted) !important; }`
- [src/components/BeforeAfter.astro:3](../src/components/BeforeAfter.astro#L3) `<p class="panel-kicker">ANTES · TEXTO INSUFICIENTE</p>`

**Impacto:** o olho percebe rótulos parecidos mas não iguais em cada página. Texto em caixa alta digitado no markup também dificulta reaproveitar o texto e trocar o estilo depois.

**Recomendação:** uma única classe de rótulo (com variante de cor e de fonte mono se necessário), texto em caixa normal no markup e `text-transform: uppercase` no CSS.

**Observação no portal:** em /validacao/checklist/ (escuro), `.readiness .eyebrow`: 12.8px, `letter-spacing` 1.92px, sans; `.review-stages__number`: 13.44px, mono, `letter-spacing` negativo.

### VIS-05 · Cinco estilos de botão sem componente comum

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** botões da página inicial, links de ação do TemplateStart e do seletor, botão de copiar lacunas e botão de limpar seleção têm raio (4, 5 e 6px), espaçamento interno e peso diferentes. O botão primário sólido existe duas vezes com cor fixa (`#205a46`).

**Evidências:**

- [src/styles/custom.css:50](../src/styles/custom.css#L50) `border-radius:5px;padding:.85rem 1.2rem`
- [src/styles/custom.css:102](../src/styles/custom.css#L102) `.readiness-gaps button{cursor:pointer;border:1px solid var(--sl-color-accent);border-radius:6px;padding:.5rem .85rem;`
- [src/styles/custom.css:111](../src/styles/custom.css#L111) `.readiness-footer button{cursor:pointer;border:1px solid var(--context-line);border-radius:4px;padding:.55rem .85rem;`
- [src/styles/custom.css:381](../src/styles/custom.css#L381) `padding: .68rem .9rem;`
- [src/styles/custom.css:401](../src/styles/custom.css#L401) `.finder-output__actions a:first-child {`
- [src/components/ReadinessChecklist.astro:30](../src/components/ReadinessChecklist.astro#L30) `<div class="readiness-footer"><button type="button" data-reset>Limpar seleção</button>`

**Impacto:** ações equivalentes parecem ter pesos diferentes, o que confunde o público não técnico sobre qual é a ação principal. Cada novo botão reinventa o estilo.

**Recomendação:** definir uma classe de botão com variantes primária, secundária e discreta, baseada em tokens. Avaliar o LinkButton nativo do Starlight para links de ação (https://starlight.astro.build/components/link-buttons/).

### VIS-06 · Fonte Inter declarada mas nunca carregada

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** `--sl-font` começa por Inter, mas não há `@font-face`, pacote `@fontsource` nem link de fonte no projeto (`package.json` só tem astro, `@astrojs/starlight` e yaml; `astro.config.mjs` só carrega `custom.css`). O site usa Inter apenas se ela estiver instalada no computador do leitor; nos demais cai para a fonte do sistema. Os pesos intermediários 650 e 750 usados no CSS dependem de fonte variável para ter efeito distinto.

**Evidências:**

- [src/styles/custom.css:5](../src/styles/custom.css#L5) `--sl-font: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;`
- [package.json:14](../package.json#L14) `"@astrojs/starlight": "^0.43.1",`
- [package.json:15](../package.json#L15) `"yaml": "^2.9.1"`
- [astro.config.mjs:37](../astro.config.mjs#L37) `customCss: ['./src/styles/custom.css'],`
- [src/styles/custom.css:34](../src/styles/custom.css#L34) `.sl-markdown-content h1, .sl-markdown-content h2, .sl-markdown-content h3 {font-weight:750}`

**Impacto:** a identidade tipográfica muda conforme o computador. Títulos podem perder o peso pretendido, e screenshots do mantenedor podem não representar o que o público vê.

**Recomendação:** carregar Inter variável via `@fontsource-variable/inter` importado no `customCss` (https://fontsource.org/fonts/inter/install) ou assumir explicitamente a pilha do sistema e remover Inter da declaração. Definir tokens de peso.

**Observação no portal:** no portal publicado, `document.fonts` retornou lista vazia: nenhuma fonte web carregada.

### VIS-07 · Escala tipográfica sem passos: 36 tamanhos de fonte distintos e serifa sem token

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** o arquivo tem 36 valores distintos de `font-size`, muitos separados por 0,01rem (de .79 a .92rem quase em sequência contínua). A serifa é declarada três vezes, em duas pilhas diferentes, sem token.

**Evidências:**

- [src/styles/custom.css:158](../src/styles/custom.css#L158) `.download-name { min-width: 0; font-size: .85rem;`
- [src/styles/custom.css:241](../src/styles/custom.css#L241) `font-size: .86rem;`
- [src/styles/custom.css:183](../src/styles/custom.css#L183) `font-size: .87rem;`
- [src/styles/custom.css:44](../src/styles/custom.css#L44) `font-family:Georgia,"Iowan Old Style",serif`
- [src/styles/custom.css:62](../src/styles/custom.css#L62) `font-family:Georgia,serif`
- [src/styles/custom.css:115](../src/styles/custom.css#L115) `.editorial-lead {font-family:Georgia,serif;`

**Impacto:** diferenças de 0,16px não criam hierarquia, só ruído e manutenção difícil. Sem escala, novos textos vão adicionar mais valores.

**Recomendação:** adotar uma escala curta em tokens (por exemplo .8, .875, 1, 1.125, 1.25 e 1.5rem) e um token único de fonte serifada, ou reaproveitar as variáveis `--sl-text-*` do Starlight.

### VIS-08 · CSS organizado por rodada de trabalho e não por componente, com dois estilos de escrita

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** as seções do arquivo são nomeadas por versão e checkpoint (v0.2, Checkpoint A a E, Segunda rodada), com comentários em inglês e português misturados. As linhas 31 a 120 estão compactadas em uma linha por regra; o restante é expandido. Regras do mesmo componente ficam espalhadas: `example-doc` aparece a partir das linhas 274, 568, 740, 795 e 892.

**Evidências:**

- [src/styles/custom.css:122](../src/styles/custom.css#L122) `/* v0.2: choice assistant and portable template library */`
- [src/styles/custom.css:289](../src/styles/custom.css#L289) `/* Checkpoint A: task-first navigation without a new application layer. */`
- [src/styles/custom.css:792](../src/styles/custom.css#L792) `/* Segunda rodada: cartão de exemplo com abas.`
- [src/styles/custom.css:43](../src/styles/custom.css#L43) `.context-hero {display:grid;grid-template-columns:minmax(0,1.06fr) minmax(315px,.94fr);`
- [src/styles/custom.css:274](../src/styles/custom.css#L274) `.example-doc { border: 1px solid var(--context-line); border-radius: 9px;`

**Impacto:** é a origem técnica da colcha de retalhos: cada rodada acrescenta regras no fim, sobrepondo as anteriores. Fica difícil saber qual regra vale e o que pode ser apagado.

**Recomendação:** reorganizar em camadas (`@layer tokens, base, primitives, components, overrides`) ou em arquivos por componente. Formatar todo o arquivo com Prettier/Stylelint e escrever comentários em um só idioma.

### VIS-09 · 47 usos de `!important` e seletores acoplados ao DOM interno do Starlight

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** muitas regras usam `margin 0 !important` para anular o espaçamento de fluxo do `.sl-markdown-content`. Outras dependem da estrutura interna do Starlight (`content-panel`, `starlight-tabs .tablist-wrapper`, `.tab > [role=tab]`) ou removem bordas globais. O título real da página inicial é escondido por um seletor `:has` sobre o primeiro `content-panel`.

**Evidências:**

- [src/styles/custom.css:42](../src/styles/custom.css#L42) `.content-panel {border:0}`
- [src/styles/custom.css:266](../src/styles/custom.css#L266) `main:has(.context-hero) > .content-panel:first-child {`
- [src/styles/custom.css:539](../src/styles/custom.css#L539) `/* Checkpoint C: reset Starlight's flow spacing on direct grid children.`
- [src/styles/custom.css:547](../src/styles/custom.css#L547) `margin-block: 0 !important;`
- [src/styles/custom.css:843](../src/styles/custom.css#L843) `.example-doc__tabs starlight-tabs .tablist-wrapper { overflow-x: auto; }`
- [src/styles/custom.css:904](../src/styles/custom.css#L904) `padding: 0 !important;`

**Impacto:** atualizações do Starlight (dependência em `^0.43`) podem quebrar o layout sem aviso. Cada nova regra precisa de `!important` para vencer a anterior, o que alimenta a espiral de especificidade.

**Recomendação:** envolver componentes próprios em contêiner com a classe `not-content` (onde o Starlight não aplica estilos de fluxo), usar `@layer` para controlar precedência e restringir sobrescritas do Starlight às variáveis `--sl-*` documentadas (https://starlight.astro.build/guides/css-and-tailwind/).

### VIS-10 · Componentes próprios duplicam componentes nativos do Starlight

**Severidade:** Média

**Confiança:** Média

**O que acontece:** o conteúdo não usa Card, CardGrid, LinkCard, Steps nem Badge, e usa Aside só duas vezes (sintaxe `:::`). Em vez disso, LandingHero refaz o hero que o Starlight oferece por frontmatter na página splash; PrincipleTiles e TemplateDownloads refazem CardGrid/LinkCard; ReviewStages refaz Steps ou CardGrid; os selos de versão refazem Badge; `method-note` refazia Aside.

**Evidências:**

- [src/content/docs/index.mdx:4](../src/content/docs/index.mdx#L4) `template: splash`
- [src/components/LandingHero.astro:5](../src/components/LandingHero.astro#L5) `<section class="context-hero">`
- [src/components/PrincipleTiles.astro:28](../src/components/PrincipleTiles.astro#L28) `<nav class="principle-tiles task-paths" aria-label="Escolha o que você quer fazer">`
- [src/components/TemplateDownloads.astro:72](../src/components/TemplateDownloads.astro#L72) `{files[kind].map((file) => <a href={base + 'downloads/' + file.href} download>`
- [src/components/ReviewStages.astro:30](../src/components/ReviewStages.astro#L30) `<ol class="review-stages" aria-label="Três etapas independentes de revisão documental">`
- [src/styles/custom.css:817](../src/styles/custom.css#L817) `.example-doc__revision-current,`
- [src/content/docs/templates/kpi.mdx:69](../src/content/docs/templates/kpi.mdx#L69) `:::note[Sobre os metadados]`

**Impacto:** mais CSS próprio para manter e menos consistência com temas e acessibilidade já resolvidos pelo Starlight. Quem contribuir precisa aprender um vocabulário paralelo.

**Recomendação:** avaliar caso a caso: hero via frontmatter ou LandingHero só com o cartão visual; CardGrid e LinkCard para trilhas e downloads; Steps para etapas sequenciais; Badge para estado e versão; Aside para notas (catálogo em https://starlight.astro.build/components/using-components/). Manter próprios apenas ReadinessChecklist, TemplateFinder, ExampleDoc e JoinDiagram, que têm comportamento específico.

### VIS-11 · Hierarquia de títulos visual e semântica desalinhadas

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** nas páginas de modelo, a frase de abertura em serifa grande é um parágrafo (`.editorial-lead`), enquanto o TemplateStart usa `h2` reais com .92rem. Na página inicial, o título visível é um parágrafo `.hero-title`, e o bloco que contém o `h1` real é escondido visualmente por CSS.

**Evidências:**

- [src/content/docs/templates/kpi.mdx:11](../src/content/docs/templates/kpi.mdx#L11) `<p class="editorial-lead">A fórmula pode estar certa e a pergunta de negócio, errada</p>`
- [src/components/TemplateStart.astro:69](../src/components/TemplateStart.astro#L69) `<h2>Quando usar</h2>`
- [src/styles/custom.css:339](../src/styles/custom.css#L339) `font-size: .92rem;`
- [src/components/LandingHero.astro:8](../src/components/LandingHero.astro#L8) `<p class="hero-title">Uma IA não deveria <em>adivinhar</em> como sua organização funciona.</p>`
- [src/styles/custom.css:266](../src/styles/custom.css#L266) `main:has(.context-hero) > .content-panel:first-child {`

**Impacto:** o que parece título não é, e o que é título parece rótulo. A navegação por títulos recebe uma estrutura diferente da visual, e o padrão confunde quem criar páginas novas copiando as existentes.

**Recomendação:** usar `h3` com estilo pequeno (ou `dt`/`strong`) nos blocos do TemplateStart e tratar a frase de abertura como lead. Na página inicial, preferir o hero nativo, que renderiza o `h1` visível.

**Observação no portal:** em /templates/kpi/ a 390px: `.editorial-lead` com 19.52px em Georgia; `h2` do TemplateStart com 14.72px; `h2` de markdown com 29px.

### VIS-12 · Selo de rascunho em dourado abaixo do contraste AA no tema claro

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** o selo de estado dos exemplos com lacunas usa `var(--context-gold)` como cor de texto. No tema claro, `#9a6b37` sobre a superfície do cartão `#f1f2e9` dá 4,11:1 (recalculado), abaixo de 4,5:1 exigido para texto de .86rem em peso 700 (critério 1.4.3, https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

**Evidências:**

- [src/styles/custom.css:830](../src/styles/custom.css#L830) `color: var(--context-gold);`
- [src/styles/custom.css:808](../src/styles/custom.css#L808) `font-size: .86rem;`
- [src/styles/custom.css:29](../src/styles/custom.css#L29) `--context-gold: #9a6b37;`
- [src/styles/custom.css:25](../src/styles/custom.css#L25) `--context-surface: #f1f2e9;`

**Impacto:** é justamente a informação que o método quer destacar (nada aprovado ainda) e ela fica com leitura mais difícil para pessoas com baixa visão.

**Recomendação:** escurecer o dourado claro para algo perto de `#855a2a` (5,33:1 sobre a superfície) ou usar fundo tingido com texto escuro. Incluir verificação de contraste dos tokens no CI.

### VIS-20 · Sem guia visual documentado e conferência visual em aberto no ROADMAP

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** o README só aponta `styles/` como identidade visual. O contrato editorial trata de termos e conteúdo e toca o visual apenas em regras pontuais (não depender só de cor, usar ExampleDoc), sem tokens, paleta, tipografia ou primitivas. O ROADMAP deixa em aberto a revisão visual manual e a conferência do checkpoint E nos dois temas.

**Evidências:**

- [README.md:64](../README.md#L64) `styles/              Identidade visual`
- [docs/CONTRATO_EDITORIAL.md:204](../docs/CONTRATO_EDITORIAL.md#L204) `- Não depender exclusivamente de cor para sinalizar um problema.`
- [docs/ROADMAP.md:29](../docs/ROADMAP.md#L29) `- [ ] Revisão visual manual e testes de acessibilidade com pessoas`
- [docs/ROADMAP.md:47](../docs/ROADMAP.md#L47) `- [ ] Conferir visualmente o checkpoint E (tema claro/escuro, leitura mobile e seta única)`

**Impacto:** sem referência escrita, cada rodada decide o visual no momento, e não há como revisar contribuições externas contra um padrão.

**Recomendação:** criar uma página curta de sistema visual (tokens, quatro primitivas, quando usar componente nativo do Starlight) e um checklist de PR com tema claro, escuro e 390px. Adotar Stylelint e um teste simples de regressão visual no CI.

### VIS-13 · Seletores sem uso e classes sem estilo

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** a busca em `src` (fora do `custom.css`) não encontra uso para `.cta-secondary`, `.method-note` e `.example-doc__notice`; `.example-doc .panel-note` também é morto, porque ExampleDoc não usa `panel-note` (só BeforeAfter usa, coberto por `.comparison-panel .panel-note`). No sentido inverso, `example-doc--gaps`, `comparison-panel--before` e `bridge-label` aparecem no markup sem regra própria.

**Evidências:**

- [src/styles/custom.css:54](../src/styles/custom.css#L54) `.cta-secondary {color:var(--context-ink)!important;border:1px solid var(--context-line)}`
- [src/styles/custom.css:116](../src/styles/custom.css#L116) `.method-note{border-left:3px solid var(--sl-color-accent);`
- [src/styles/custom.css:286](../src/styles/custom.css#L286) `.example-doc .panel-note { color: var(--context-muted); font-size: .85rem; }`
- [src/styles/custom.css:919](../src/styles/custom.css#L919) `.example-doc__notice { margin: 0 !important;`
- [src/components/ExampleDoc.astro:51](../src/components/ExampleDoc.astro#L51) `<section class:list={['example-doc', complete ? 'example-doc--complete' : 'example-doc--gaps']}>`

**Impacto:** ruído que dificulta entender o que está ativo e faz contribuições seguirem padrões abandonados.

**Recomendação:** remover as regras mortas e adotar Stylelint com verificação de classes não usadas (ou PurgeCSS em modo relatório) no CI.

### VIS-14 · Regras duplicadas ou que se sobrepõem

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** o mesmo seletor aparece duas vezes com valores diferentes, ou uma regra posterior torna a anterior inútil: `.example-doc__gaps ul` (284 e 670), `.example-doc__download` (285 e 920), coluna única do seletor em 720px (262) já coberta pela regra de 950px (760), movimento reduzido global (120) e específico para as abas (932). A grade de duas colunas em `.example-doc dl` atinge também listas internas e precisa ser desfeita depois (654).

**Evidências:**

- [src/styles/custom.css:284](../src/styles/custom.css#L284) `.example-doc__gaps ul { margin-top: .3rem; }`
- [src/styles/custom.css:670](../src/styles/custom.css#L670) `.example-doc__gaps ul {margin:.2rem 0 0;padding-left:1.2rem}`
- [src/styles/custom.css:285](../src/styles/custom.css#L285) `.example-doc__download { font-size: .85rem; margin-top: .8rem !important; }`
- [src/styles/custom.css:920](../src/styles/custom.css#L920) `.example-doc__download { font-size: .86rem; font-weight: 750;`
- [src/styles/custom.css:262](../src/styles/custom.css#L262) `.template-finder fieldset { grid-template-columns: 1fr; }`
- [src/styles/custom.css:761](../src/styles/custom.css#L761) `grid-template-columns: minmax(0, 1fr);`
- [src/styles/custom.css:932](../src/styles/custom.css#L932) `@media (prefers-reduced-motion: reduce) {`
- [src/styles/custom.css:277](../src/styles/custom.css#L277) `.example-doc dl { margin: .6rem 0 1rem; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 1.5rem; }`
- [src/styles/custom.css:654](../src/styles/custom.css#L654) `.example-doc .example-meaning__levels dl {display:block}`

**Impacto:** o valor efetivo depende da ordem no arquivo; mudanças em um lugar não têm efeito e geram retrabalho.

**Recomendação:** consolidar cada seletor em um único bloco por componente e escopar a grade a `.example-doc__ids` em vez de `.example-doc dl`.

### VIS-15 · Treze regras `@media` de largura com dez valores diferentes

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** há 13 regras `@media` por largura máxima, com 10 valores distintos (420, 500, 560, 640, 650, 720, 800, 820, 850 e 950px), sem tokens nem lógica comum; grades de duas ou três colunas colapsam em larguras diferentes.

**Evidências:**

- [src/styles/custom.css:119](../src/styles/custom.css#L119) `@media(max-width:640px)`
- [src/styles/custom.css:414](../src/styles/custom.css#L414) `@media (max-width: 820px) {`
- [src/styles/custom.css:535](../src/styles/custom.css#L535) `@media(max-width:800px){`
- [src/styles/custom.css:672](../src/styles/custom.css#L672) `@media(max-width:650px) {`
- [src/styles/custom.css:733](../src/styles/custom.css#L733) `@media(max-width: 850px) {`
- [src/styles/custom.css:922](../src/styles/custom.css#L922) `@media (max-width: 560px) {`

**Impacto:** entre 640 e 950px a mesma página mostra componentes vizinhos em colunas diferentes, e os testes visuais precisam cobrir muitas larguras.

**Recomendação:** padronizar em 2 ou 3 pontos alinhados aos do Starlight, ou usar grid com `auto-fit`/`minmax` (como `jd-counts` no JoinDiagram já faz) e regras `@container`.

### VIS-16 · Avisos e destaques com borda lateral em quatro variações, além do Aside nativo

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** citação, lista de lacunas do checklist, `method-note` e regra da comparação de versões usam borda esquerda de 3px com raio, fundo e cor diferentes, enquanto o conteúdo usa `:::note` e `:::caution` do Starlight em dois lugares.

**Evidências:**

- [src/styles/custom.css:37](../src/styles/custom.css#L37) `.sl-markdown-content blockquote {border-inline-start: 3px solid var(--sl-color-accent);`
- [src/styles/custom.css:96](../src/styles/custom.css#L96) `border-left:3px solid var(--context-gold);border-radius:0;`
- [src/styles/custom.css:494](../src/styles/custom.css#L494) `border-left:3px solid var(--sl-color-accent);`
- [src/content/docs/metodo/identificacao-versoes.mdx:44](../src/content/docs/metodo/identificacao-versoes.mdx#L44) `:::caution[Corrigir ou criar outro indicador?]`

**Impacto:** o leitor não aprende o que cada tipo de destaque significa (nota, atenção, lacuna, regra).

**Recomendação:** definir semântica fixa: Aside `note`/`tip`/`caution`/`danger` para avisos (https://starlight.astro.build/components/asides/), um único estilo de lacuna, `blockquote` só para citação.

### VIS-17 · Contorno de foco com espessura e afastamento diferentes

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** a maioria dos elementos usa 3px com afastamento 3px; o rolador do histórico usa 3px com 2px; rótulos do seletor e abas usam 2px com 2px. A regra está repetida em seis blocos.

**Evidências:**

- [src/styles/custom.css:257](../src/styles/custom.css#L257) `outline: 3px solid var(--sl-color-accent);`
- [src/styles/custom.css:749](../src/styles/custom.css#L749) `outline-offset: 2px;`
- [src/styles/custom.css:756](../src/styles/custom.css#L756) `outline: 2px solid var(--sl-color-accent);`
- [src/styles/custom.css:881](../src/styles/custom.css#L881) `outline: 2px solid var(--sl-color-accent);`

**Impacto:** pequena inconsistência na navegação por teclado e manutenção dispersa.

**Recomendação:** tokens de espessura e afastamento de foco aplicados por uma única regra `:where(...):focus-visible`.

### VIS-18 · Recuo de `dd` diferente entre abas do mesmo cartão

**Severidade:** Baixa

**Confiança:** Média (o padding padrão do Starlight só foi visto no portal publicado, não no código de `node_modules`)

**O que acontece:** na aba de identificação o padding de `dd` herdado do Starlight é anulado com `!important`; na aba O que diz só a margem é zerada, então o valor fica recuado em relação ao rótulo.

**Evidências:**

- [src/styles/custom.css:589](../src/styles/custom.css#L589) `.example-doc .example-meaning__facts dd {`
- [src/styles/custom.css:590](../src/styles/custom.css#L590) `margin:0;`
- [src/styles/custom.css:904](../src/styles/custom.css#L904) `.example-doc__ids dd { margin: .15rem 0 0 !important; padding: 0 !important;`

**Impacto:** duas listas de pares rótulo e valor no mesmo cartão alinham de jeitos diferentes, visível no celular.

**Recomendação:** uma primitiva de lista de definição usada nas duas abas, dentro de `.not-content` para não herdar o estilo do Starlight.

**Observação no portal:** em /templates/kpi/ (390px, escuro): `.example-meaning__facts dd` com `padding-inline-start` 16px; `.example-doc__ids dd` com 0px. Screenshot mostra valor recuado sob o rótulo.

### VIS-19 · Estratégia de estilo mista: um componente com `style` escopado, os demais no CSS global

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** JoinDiagram é o único dos 14 componentes com bloco `style` próprio (escopado pelo Astro); os outros 13 dependem de classes globais em `custom.css`.

**Evidências:**

- [src/components/JoinDiagram.astro:56](../src/components/JoinDiagram.astro#L56) `<style>`
- [src/components/JoinDiagram.astro:69](../src/components/JoinDiagram.astro#L69) `.jd-count { margin: 0 !important; border: 1px solid var(--context-line); border-radius: 8px; padding: .9rem 1rem; background: var(--context-surface); }`

**Impacto:** quem contribuir não sabe onde colocar estilo novo; `jd-count` repete o cartão do VIS-01 em outro arquivo.

**Recomendação:** escolher um padrão: tokens e primitivas globais, estilos específicos escopados em cada componente (o modelo do JoinDiagram serve para isso), com migração gradual.

## Descartados na verificação

- **VIS-R1:** hipótese de rolagem horizontal no celular descartada. Em /templates/kpi/ e /validacao/checklist/ a 390px, `scrollWidth` igual a `clientWidth` (390).
- **VIS-R2:** hipótese de contraste insuficiente no tema escuro descartada para os pares principais, recalculados nesta verificação: muted 8,31:1, acento 10,72:1, dourado 8,95:1 sobre `--context-surface`.
- **VIS-R3:** o cartão visual da página inicial com cores fixas iguais nos dois temas parece intencional (bloco escuro de ilustração) e os pares internos passam AA. O problema registrado é só a falta de tokens (VIS-03).

## Não coberto nesta rodada

- Build local e inspeção do HTML gerado (execução de npm e build bloqueada). Os padrões do Starlight citados (padding de `dd`, espaçamento de fluxo, cinzas do tema escuro) foram vistos apenas no portal publicado, não no código de `node_modules`, que não está instalado.
- Screenshots de todas as páginas. No portal foram vistas só a página inicial (desktop escuro), /templates/kpi/ (desktop claro e celular escuro) e /validacao/checklist/ (celular escuro).
- Tema claro no celular e larguras intermediárias (640 a 950px), onde os pontos de quebra divergem.
- Contraste de todos os pares de cor (só os principais foram calculados) e auditoria Lighthouse.
- Comportamento real da fonte em Windows, Android e Linux (inferido apenas pela ausência de carregamento de fonte).
- Pesquisa de literatura externa sobre sistemas de design para documentação (Exa/web) não feita nesta dimensão. Os links citados nas recomendações apontam só para a documentação oficial do Starlight, do Fontsource e da WCAG.
- Arquivos de download em `public/downloads` e scripts Python, fora do foco visual.
