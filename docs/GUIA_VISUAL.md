# Guia visual do portal

Este guia descreve o sistema visual do portal Contexto: fontes, escalas, tokens de cor, as quatro primitivas, o par de botões e as regras que o CI confere. A decisão de fundo está no [ADR 0016](./adr/0016-sistema-visual.md). Quem cria ou muda um componente segue este guia; quem muda o guia muda o CSS junto.

## Onde fica cada coisa

| Arquivo | O que tem |
|---|---|
| `src/styles/custom.css` | Só tokens: o bloco `:root` (tema escuro, o padrão) e o bloco `:root[data-theme='light']`, mais a ordem das camadas. É o único arquivo com cor em hex. `scripts/check_contraste.py` lê os tokens daqui. |
| `src/styles/base.css` | Camada `contexto.base`: tipografia do corpo, conteúdo em Markdown, ajustes de elementos do Starlight e alvos de toque. |
| `src/styles/primitivas.css` | Camada `contexto.primitivas`: cartão, rótulo, botão e aviso. |
| `src/styles/componentes.css` | Camada `contexto.componentes`: um bloco por componente de `src/components`. |
| `src/styles/estudo.css` | Camada `contexto.estudo`: componentes de estudo das páginas de modelo (ParContrastante, EtapaDeEstudo, Exercicio). |
| `src/data/contraste.yaml` | Pares de cor conferidos nos dois temas. |

A ordem das camadas é declarada uma vez, no topo de `custom.css`: `@layer contexto.base, contexto.primitivas, contexto.componentes, contexto.estudo;`. Como esse CSS é carregado depois do CSS do Starlight, as camadas `contexto.*` vencem as camadas `starlight.*` sem `!important` e sem seletor mais específico. Dentro do portal, um componente vence uma primitiva, e uma primitiva vence a base.

Componente não tem bloco `<style>` próprio: todo o CSS mora em `src/styles`.

## Fontes

A família IBM Plex, com licença SIL Open Font License, servida pelo próprio site com os pacotes `@fontsource/ibm-plex-*`. Nenhuma requisição a serviço externo de fontes. O `astro.config.mjs` carrega só os pesos usados:

| Família | Uso | Pesos carregados | Token |
|---|---|---|---|
| IBM Plex Sans | Texto, títulos, botões e rótulos | 400, 600 e 700 | `--sl-font` |
| IBM Plex Serif | Título da home, slogan, frase de abertura (`.editorial-lead`) e frase do cartão da home | 600 e 400 itálico | `--context-font-serif` |
| IBM Plex Mono | YAML, código, nomes de campo e numeração | 400 e 600 | `--sl-font-mono` |

Use só esses pesos. Um peso que não está carregado (450, 650, 750 ou 800, por exemplo) faz o navegador imitar o mais próximo, e cada leitor vê uma coisa. Serifa só em itálico 400 ou em 600; corpo de texto em serifa normal não existe no portal.

## Escala de títulos

Um tamanho por nível, em qualquer largura de tela, definido uma vez em `:root`:

| Nível | Token | Tamanho |
|---|---|---|
| h1 | `--sl-text-h1` | 2.25rem |
| h2 | `--sl-text-h2` | 1.75rem |
| h3 | `--sl-text-h3` | 1.375rem |
| h4 | `--sl-text-h4` | 1.125rem |
| h5 | `--sl-text-h5` | 1rem |

Regras:

- Nenhum componente aplica `font-size` a um título. Um título dentro de um cartão tem o mesmo tamanho de um título do mesmo nível no texto. O componente recebe o nível como propriedade (como `nivel` em ExampleDoc) e escolhe o elemento, nunca o tamanho.
- Texto que parece título mas não é (nome de etapa, rótulo de cartão) usa `<p>` com classe, nunca um título fora da ordem.
- A única exceção é o `h1` da home (`.hero-title`), que fica fora de `.sl-markdown-content` e usa `--context-text-titulo-hero`.
- A regra R4 de `npm run check:visual` mede um tamanho calculado por nível, de h2 a h5, dentro de `.sl-markdown-content`.

## Escala de texto

Nada abaixo de 0.8125rem (A11Y-14). Todo tamanho de texto no CSS é um destes tokens:

| Token | Tamanho | Uso |
|---|---|---|
| `--context-text-xs` | 0.8125rem | Rótulos em maiúsculas, notas, numeração, legendas curtas |
| `--context-text-sm` | 0.875rem | Texto de cartão, tabelas, botões, metadados |
| `--context-text-base` | 1rem | Texto corrido de destaque dentro de componente |
| `--context-text-lg` | 1.125rem | Frase de apoio da home, nome do site |
| `--context-text-numero` | 1.5rem | Resultado numérico em destaque (contas do diagrama) |
| `--context-text-destaque` | de 1.125rem a 1.375rem | Frase de abertura em serifa itálica |
| `--context-text-titulo-hero` | de 2.25rem a 4rem | Só o `h1` da home |

## Tokens de cor e os três fundos

Cor só como token declarado em `custom.css`, com valor em hex nos dois temas. Fora de `:root`, nenhum hex, nenhuma cor nomeada e nenhuma função de cor (o Stylelint confere).

Três fundos, e só três:

| Fundo | Token | Onde |
|---|---|---|
| Base | `--context-bg` | Fundo da página; também mapeado em `--sl-color-bg`, `--sl-color-bg-nav` e `--sl-color-bg-sidebar`, nos dois temas. Blocos dentro de um cartão (lacunas, entradas do exemplo) voltam para a base. |
| Superfície | `--context-surface` | Cartões, avisos, citações, caixas do diagrama. |
| Inverso | `--context-inverse` | Bloco escuro, igual nos dois temas. Hoje só o cartão de exemplo da home. |

A ênfase nunca é um quarto fundo: é a borda de acento (`.ctx-card--destaque`). Dentro do fundo inverso, os blocos internos se separam por borda, não por outro fundo.

Demais tokens de cor:

| Token | Papel |
|---|---|
| `--context-ink` | Texto principal |
| `--context-muted` | Texto secundário (pelo menos 7:1, UX-09) |
| `--sl-color-accent`, `--sl-color-accent-high`, `--sl-color-accent-low` | Acento verde: links, destaque, botão secundário |
| `--context-line` | Divisória e borda de cartão; também a linha fina do Starlight (`--sl-color-hairline`) |
| `--sl-color-gray-1` a `--sl-color-gray-7`, `--sl-color-text`, `--sl-color-white` (tema claro) | Neutros do Starlight (menus, sumário, metadados, títulos) no mesmo matiz verde dos fundos, sem os cinzas azulados padrão (VIS-02). `--sl-color-text` aponta para `--context-ink`; no tema claro, `--sl-color-white` (títulos) também. |
| `--context-border` | Borda de componente que precisa ser vista (pelo menos 3:1), como as caixas do diagrama |
| `--context-gold` | Borda dourada (selo de rascunho, aviso caution, lacunas) |
| `--context-gold-text` | Todo texto dourado |
| `--context-danger` | Título e borda do aviso danger |
| `--context-button-bg`, `--context-button-bg-hover`, `--context-button-text` | Botão principal, iguais nos dois temas |
| `--context-card-text`, `--context-card-label`, `--context-card-accent`, `--context-card-border` | Texto, rótulos, destaque e bordas sobre o fundo inverso |

Todo par de texto e fundo novo entra em `src/data/contraste.yaml`; `python3 scripts/check_contraste.py` confere os dois temas. Mínimos: 4.5:1 para texto, 3:1 para borda e objeto gráfico, 7:1 para o texto secundário.

## As quatro primitivas

As classes `.ctx-*` são contrato entre o CSS e os componentes. Não mude os nomes sem trocar todos os usos.

| Primitiva | Classes | Quando usar |
|---|---|---|
| Cartão | `.ctx-card` e `.ctx-card--destaque` | Um bloco que se lê sozinho: exemplo, checklist, etapa, próximo passo, entrada da home. Superfície, borda e raio. `--destaque` troca a borda pelo acento para o item que merece atenção (o exemplo completo, a versão atual). Não ponha um cartão dentro de outro. |
| Rótulo | `.ctx-label`, `.ctx-label--rascunho` e `.ctx-label--aprovado` | Estado curto de um documento, sempre com texto. `--rascunho`: texto dourado e borda tracejada. `--aprovado`: texto e borda de acento. A cor nunca é o único sinal. |
| Botão | `.ctx-button`, `.ctx-button--primary` e `.ctx-button--secondary` | Ação. Em `<button>` (copiar, limpar) use a classe; em link use o `LinkButton` do Starlight, que recebe o mesmo estilo. |
| Aviso | `Aside` do Starlight (`:::note`, `:::tip`, `:::caution`, `:::danger`) | Informação que interrompe a leitura. `note` e `tip` em verde de acento, `caution` em dourado, `danger` em `--context-danger`, todos sobre a superfície. Não crie caixa de aviso própria. |

## O par de botões

Um botão principal e um secundário em todo o portal. A mesma ação tem sempre a mesma aparência.

| Variante | Como escrever | Aparência |
|---|---|---|
| Principal | `<LinkButton variant="primary">` ou `class="ctx-button ctx-button--primary"` | Fundo `--context-button-bg`, texto `--context-button-text` |
| Secundário | `<LinkButton variant="secondary">` ou `class="ctx-button ctx-button--secondary"` | Fundo transparente, borda e texto de acento |

Os dois têm altura mínima de 44 px e foco de 3 px em acento. Use no máximo um botão principal por bloco. Navegação dentro do texto continua como link de texto ("Siga o percurso", "Próximo passo", o "Baixar" das tabelas de modelos, com alvo de 44 px).

Onde estão hoje:

- Home (LandingHero): "Comece em 5 minutos" é o principal; "Siga o percurso" é link de texto ao lado.
- Bloco "Antes de preencher" (TemplateStart): sem download; secundário "Ir para o modelo em branco", que leva à seção `#baixe-o-modelo` no fim da página (I-24), e links para a Referência de campos do modelo e para Como ler os campos.
- Arquivos do modelo (TemplateDownloads) e dos laboratórios (AnalyticsLabDownloads): o primeiro arquivo é o principal, os outros são secundários, numa grade com espaço entre os alvos.
- Exemplo (ExampleDoc) e versões (RevisionComparison): "Baixar YAML" e "Baixar versão" são secundários.
- Checklist (ReadinessChecklist): "Copiar lista de lacunas" e "Limpar seleção" são `<button class="ctx-button ctx-button--secondary">`.

## Componentes nativos do Starlight

Antes de criar um componente, use o nativo:

| Nativo | Onde | Observação |
|---|---|---|
| `LinkButton` | Botões em link | Recebe o estilo do par de botões em `primitivas.css`. |
| `Aside` | Avisos nas páginas | Os quatro tipos recoloridos pelos tokens. |
| `Tabs` e `TabItem` | Abas do ExampleDoc | Aparência nativa; nenhum seletor acoplado ao DOM interno das abas. |
| `Steps` | Etapas das páginas de modelo | Aparência nativa. |
| `Code` | YAML do ExampleDoc | Expressive Code do Starlight. |

`Badge` não é usado: o estado de um documento é o rótulo `.ctx-label`.

## Movimento

Transição e deslocamento só dentro de `@media (prefers-reduced-motion: no-preference)` (VIS-13). Quem pede movimento reduzido não recebe animação nenhuma, sem regra global com `!important`.

## Regras do Stylelint

Configuração em `.stylelintrc.json`, sem `extends`. Rode com `npm run lint:css`.

| Regra | Valor | O que impede |
|---|---|---|
| `color-no-hex` | `true` | Cor em hex fora de `custom.css` |
| `color-named` | `"never"` | Cor por nome (`red`, `white`). `transparent` e `currentColor` passam. |
| `declaration-no-important` | `true` | `!important` em qualquer arquivo de `src/styles` |
| `function-disallowed-list` | `rgb`, `rgba`, `hsl`, `hsla`, `hwb`, `lab`, `lch`, `oklab`, `oklch` | Cor escrita como função |
| Só em `custom.css`: `color-no-hex` | `null` | Libera o hex dos tokens |
| Só em `custom.css`: `selector-disallowed-list` | `/^(?!:root)/` | Qualquer seletor que não comece por `:root`, para que hex só exista em `:root` |

## Checklist visual local

`npm run check:visual` serve o `dist/` e mede quatro regras nos temas claro e escuro: R1 (página de modelo com até 4 telas de altura a 1440x900), R2 (nenhuma página com estouro horizontal a 390x844), R3 (uma face IBM Plex Sans com estado `loaded` em `document.fonts`, aplicada ao body, sem requisição externa; `document.fonts.check` não serve, porque aprova mesmo quando nenhuma face foi declarada) e R4 (um tamanho por nível de título).

Para rodar na sua máquina:

1. `npm run build` gera o `dist/`.
2. `npm run check:visual` abre as páginas num Chrome. O script procura, nesta ordem: o caminho em `CONTEXTO_CHROME`, o Chromium do `playwright-core` (se instalado) e o Google Chrome do sistema.
3. Se o Chrome do sistema não for encontrado, aponte o executável: `CONTEXTO_CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" npm run check:visual` no macOS, ou o caminho do `google-chrome` no Linux.

Antes de medir, o script espera o `html[data-theme]` do tema pedido; se ele não aparecer, visita a página de novo até duas vezes antes de registrar a falha TEMA.

O checklist do PR visual pede a página em tema claro, tema escuro e 390 px de largura.

## Achados A11Y de severidade média

Conferidos um por um contra o código final da F5.

| Id | Estado | Evidência |
|---|---|---|
| A11Y-01 | resolvido antes da F5 | `src/components/ReadinessChecklist.astro:26`: o retorno tem `aria-live="polite"` e a lista de lacunas aponta para ele por `aria-describedby` (`:29`); `:38` a `:40`: o retorno diz quantas dimensões faltam ("Faltam 3 de 8 dimensões"); `:32`: o resultado da cópia fica num `role="status"` persistente, e `:57` registra que não há timer que apague a mensagem. |
| A11Y-02 | resolvido antes da F5 | `src/components/ExampleDoc.astro:18` a `:23`: o nível do título vem da propriedade `nivel`, e os títulos internos ficam um nível abaixo; `:65`: o título do exemplo é um elemento de título (`Titulo`), não `<p>`; `src/components/ExampleMeaning.astro:8` a `:10`: os grupos usam o nível recebido do ExampleDoc, sem `h4` órfão. |
| A11Y-05 | resolvido antes da F5 | `src/styles/componentes.css:506` a `:510` (regras que saíram do `<style>` de JoinDiagram sem mudança): caixas e ligações usam `--context-border` e os pedidos fora da conta são tracejados; `src/data/contraste.yaml:24` a `:27` confere `--context-border` com pelo menos 3:1 sobre a base e a superfície nos dois temas. |
| A11Y-06 | resolvido antes da F5 | `src/components/TemplateFinder.astro:22` a `:38`: o seletor virou tabela estática, um `h3` por nível e uma tabela por grupo, sem rádios nem rótulos soltos. |
| A11Y-08 | resolvido antes da F5 | `src/styles/custom.css:73`: `--context-gold-text` é `#86592a` no tema claro (5,36:1 sobre a superfície); `src/data/contraste.yaml:20` a `:23` confere o texto dourado sobre a base e a superfície nos dois temas; `src/styles/primitivas.css:25` a `:29`: o selo de rascunho usa esse token no texto e `--context-gold` só na borda. |

A troca de tokens e primitivas da F5 não reabriu nenhum dos cinco: `python3 scripts/check_contraste.py` passa com os pares novos.

## CSS removido na F5

Seletores sem uso ou substituídos por primitivas e componentes nativos (VIS-09, VIS-13):

- `.before-after`, `.comparison-panel` (com `--after`, `h3`, `p`, `dl`, `dt` e `dd`) e `.panel-note`: saem com o BeforeAfter.
- `.principle-tiles`, `.principle-tile`, `.principle-tile h3 span`, `.tile-index`, `.task-paths` e `.task-paths__action`: viraram `.symptom-entries`, `.symptom-entries__tile` (com `.ctx-card`) e `.symptom-entries__action`; `.tile-index` e o `span` do título não tinham uso.
- `.cta-primary`, `.hero-actions a` e `.hero-footnote` (sem uso): o botão da home é o `LinkButton`; `.context-hero__copy > p:not(...)` virou `.hero-tagline`.
- `.template-downloads a`, `.download-icon` e `.download-name`: viraram `LinkButton` e `.template-downloads__formato`.
- `.template-start__next a` e `.template-start__next span`: viraram `LinkButton` secundário e `.template-start__next-text`.
- `.readiness-heading`, `.readiness-gaps button`, `.readiness-footer button` e `.readiness-convention`: viraram `.readiness__title` e `.ctx-button`.
- `.example-doc--complete`, `.example-doc__revision-current`, `.example-doc__revision-draft`, `.example-doc__download` e as regras genéricas `.example-doc dl`, `dt` e `dd`: viraram `.ctx-card--destaque`, `.ctx-label` e `LinkButton`.
- `.revision-comparison__card--current` e `.revision-comparison__download`: viraram `.ctx-card--destaque` e `LinkButton`.
- O controle segmentado das abas (`.example-doc__tabs [role='tablist']`, `.tab > [role='tab']` e variações, `[role='tabpanel']`): as abas voltam à aparência nativa, sem acoplamento ao DOM interno do Starlight.
- Regras duplicadas das rodadas "Checkpoint" A a E (`.example-doc__gaps`, `.example-doc__download`, o reset de grade de `.before-after`).
- `@media (prefers-reduced-motion: reduce) { * { ... !important } }` e a regra de movimento reduzido das abas.
- Regras de 44 px por seletor de atributo (`td a[href*="downloads/"]`) e por componente: o alvo agora vem do `.ctx-button`, do `LinkButton` e de `.template-finder__baixar`.
- Fundos próprios de `.starlight-aside--note` e `--tip`: o fundo vem da regra única de `.starlight-aside`.
- Tokens: `--context-surface-2`, `--context-raised`, `--context-shadow`, `--context-card-bg` (agora `--context-inverse`), `--context-card-shadow`, `--context-card-bridge`, `--context-card-rule`, `--context-card-number`, `--context-card-quote` (agora `--context-card-text`), `--context-card-problem-*`, `--context-card-chip-*` e `--context-card-solution-*`; os valores em hex de `--sl-color-bg-nav` e `--sl-color-bg-sidebar` viraram `var(--context-bg)`.

O bloco `<style>` do JoinDiagram não saiu: mudou para `componentes.css` com as mesmas regras, trocando só os tamanhos literais pelos tokens de texto.
