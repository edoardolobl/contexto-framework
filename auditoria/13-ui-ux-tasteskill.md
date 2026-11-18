# UI e UX medidos no navegador (tasteskill 2.5.1)

Data: 2026-11-17 · Commit: d08c810 (portal publicado em https://edoardolobl.github.io/contexto-framework/) · Escopo: revisão só de leitura da interface com as ferramentas da tasteskill 2.5.1, e o que entra no plano antes da F0

> Revisão só de leitura. Nenhum arquivo do portal foi alterado. Complementa [06-identidade-visual.md](./06-identidade-visual.md), que foi feito lendo o CSS sem renderizar; aqui as medições vêm de um navegador real.

## Resumo

- A base técnica é boa: desempenho sem nenhum FAIL (sem salto de layout, primeira pintura rápida, zero WebGL), uma família de cartões, um estilo de link, foco visível, texto alternativo e movimento reduzido respeitados.
- Quatro problemas reais aparecem nas quatro páginas medidas: **nenhuma fonte web é carregada** (a tipografia muda conforme o sistema operacional), **a hierarquia de títulos não segue os níveis**, **três estilos de botão numa mesma página** e **alvos de toque abaixo de 44 px no celular**.
- Na home, o título principal é um slogan e não diz o que o Contexto é nem para quem; no celular, o primeiro bloco ocupa quase quatro telas antes das três entradas por tarefa.
- As páginas de modelo são longas demais: a de Indicador tem 7,4 telas no desktop e 13 no celular, com 1.951 nós no DOM. A sequência didática da F5 (I-24) vai alongar ainda mais se não houver um limite de tamanho.
- Cerca de 60% dos FAIL do verificador vêm de regras de landing page (hero de uma tela, uma seção por tela, foto em toda seção) que não servem para páginas de documentação. Eles foram separados e não entram no plano.

## Como foi feito

- **Ferramentas da skill**, cada uma num Chrome sem janela:
  - `consistency.mjs` na home em 1440, 1024, 820, 768 e 390 px (mais 320 px para estouro e toque); nas páginas Indicador (`/templates/kpi/`), Modelos (`/templates/`) e Comece em 5 minutos, em modo rápido a 1440 e 390 px.
  - `shoot.mjs` para capturas de página inteira; `perf.mjs` na home e no Indicador.
- **Tipo declarado**: `service`. A skill não tem tipo para site de documentação; `service` é o tipo "não técnico" mais próximo e proíbe efeitos, cenas e fundos especiais, que é o que convém aqui.
- **Inspeção no navegador do app**, tema claro, para conferir fontes carregadas e níveis de título.
- **Evidências salvas** em [evidencias-ui/](./evidencias-ui/): capturas (tema escuro, que é o padrão do Chrome sem janela) e os relatórios JSON completos do verificador.
- **Não foi rodado**: `copy-lint.mjs` (as regras de texto da skill são escritas para inglês) e o portão final (`gate.mjs`), que existe para páginas construídas com a skill.

## Pontos fortes (manter)

| Ponto | Medição |
|---|---|
| Desempenho | `perf.mjs`: 0 FAIL na home e no Indicador; salto de layout 0,000; nenhuma requisição quebrada; nenhum WebGL. |
| Uma família de cartões e um estilo de link | `card-family`, `card-layout`, `link-styles` e `nesting` em PASS na home. |
| Acessibilidade básica | `focus-ring`, `focus-visible`, `img-alt`, `a11y-name`, `lang`, `menu-toggle` e `reduced-motion` em PASS. |
| Movimento contido | Nada aparece com a rolagem, sem parallax nem carrossel (`scroll-reveal`, `scroll-linked`, `tilt` em PASS). |
| Estrutura do Starlight | Busca, navegação lateral, sumário da página e paginação funcionam e devem continuar sendo a base. |

## Índice de achados

| ID | Severidade | Título |
|---|---|---|
| UX-01 | Alta | Nenhuma fonte web carregada; a tipografia depende do sistema |
| UX-02 | Alta | Títulos fora de nível e em tamanhos trocados |
| UX-03 | Média | Página de modelo longa demais e com modos misturados |
| UX-04 | Média | Título da home é slogan, sem categoria nem público |
| UX-05 | Média | No celular, a home leva quase quatro telas até as entradas por tarefa |
| UX-06 | Média | Três estilos de botão na mesma página |
| UX-07 | Média | Alvos de toque abaixo de 44 px no celular |
| UX-08 | Média | Superfícies e cores fora da paleta |
| UX-09 | Baixa | Contraste de texto abaixo do patamar da skill (passa no AA) |
| UX-10 | Baixa | Link compartilhado sem imagem nem cor de tema |

### UX-01 · Nenhuma fonte web carregada; a tipografia depende do sistema

**Severidade:** Alta · **Confiança:** Alta

**O que acontece:** o CSS pede Inter para o texto e Georgia para os títulos de destaque, mas nenhuma das duas é carregada. No navegador, `document.fonts` tem zero fontes carregadas. Cada leitor vê o portal na fonte do próprio sistema: SF no Mac, Segoe no Windows, Roboto no Android. O serifado da home e dos subtítulos também varia.

**Evidências:**
- [src/styles/custom.css:5](../src/styles/custom.css#L5) `--sl-font: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;`
- [src/styles/custom.css:44](../src/styles/custom.css#L44) `.context-hero__copy .hero-title {font-family:Georgia,"Iowan Old Style",serif;`
- [src/styles/custom.css:115](../src/styles/custom.css#L115) `.editorial-lead {font-family:Georgia,serif;`
- Verificador: `font-load` WARN nas quatro páginas ("Inter is asked for by the h1, the h2s and the body text but never loaded").

**Impacto:** a identidade visual não é a mesma para dois leitores. Também confirma o VIS-06.

**Recomendação:** escolher um par de fontes (ou só uma sem serifa) com licença aberta, servir os arquivos pelo próprio site com `@font-face`, e remover da pilha as fontes que não forem carregadas.

### UX-02 · Títulos fora de nível e em tamanhos trocados

**Severidade:** Alta · **Confiança:** Alta

**O que acontece:**
- Na página Indicador, os títulos dos três cartões "Antes de preencher" são `h2` com 14,7 px, enquanto as seções da página são `h2` com 35 px.
- Logo depois de um `h2` aparece um `h4`, pulando o nível 3.
- Na home não há `h1` visível: o título grande é um parágrafo de 69 px, maior que qualquer título.

**Evidências:**
- [src/components/TemplateStart.astro:69](../src/components/TemplateStart.astro#L69) `<h2>Quando usar</h2>`
- [src/components/ExampleMeaning.astro:301](../src/components/ExampleMeaning.astro#L301) `<h4>{group.heading}</h4>`
- [src/components/ExampleDoc.astro:80](../src/components/ExampleDoc.astro#L80) `<h4>Perguntas em aberto ({questions.length})</h4>`
- [src/components/LandingHero.astro:8](../src/components/LandingHero.astro#L8) `<p class="hero-title">Uma IA não deveria <em>adivinhar</em> como sua organização funciona.</p>`
- Medido no navegador (Indicador): `H2 14.72px Quando usar`, `H2 35px O problema`, `H4 16px O significado do indicador`. Verificador: `heading-scale` FAIL e `heading-order` FAIL. Captura: [kpi-390-titulos.jpg](./evidencias-ui/kpi-390-titulos.jpg).

**Impacto:** quem navega por títulos com leitor de tela encontra três "seções" que são cartões. O sumário "Nesta página" e a busca recebem uma estrutura enganosa, e documentos cortados por títulos (RAG, NotebookLM, I-17) herdam o mesmo erro.

**Recomendação:** uma escala só, com um tamanho por nível. Cartões usam um elemento que não seja título, ou um `h3` dentro da seção. Componentes recebem o nível como propriedade, em vez de fixá-lo. A home ganha um `h1` real. Complementa A11Y-02 e A11Y-15.

### UX-03 · Página de modelo longa demais e com modos misturados

**Severidade:** Média · **Confiança:** Alta

**O que acontece:** a página Indicador junta, numa rolagem só, orientação de uso, problema, perguntas, dois exemplos completos com abas, histórico de versões, exercícios, downloads, nota técnica e fundamentação.

**Evidências:**
- `perf.mjs` (Indicador): `page height 12.8 screens`, `DOM 1951 nodes`.
- `shoot.mjs`: 6.835 px a 1440 (8 telas) e 10.778 px a 390 (13 telas). Capturas: [kpi-1440-escuro.png](./evidencias-ui/kpi-1440-escuro.png), [kpi-390-escuro.png](./evidencias-ui/kpi-390-escuro.png).

**Impacto:** no celular, a pessoa não técnica perde o fio entre "o que é" e "baixe o modelo". A sequência de seis degraus do I-24 acrescenta blocos e deixa a página ainda maior.

**Recomendação:** um limite de tamanho por página de modelo, de no máximo 4 telas no desktop, e a sequência didática dividida em páginas ou passos recolhíveis (Steps e Tabs nativos do Starlight). A referência de campos fica numa página própria (Diátaxis). Isso precisa entrar no contrato editorial junto com o I-24.

### UX-04 · Título da home é slogan, sem categoria nem público

**Severidade:** Média · **Confiança:** Média (regra de texto da skill aplicada a um site de documentação)

**O que acontece:** o maior texto da primeira tela é "Uma IA não deveria adivinhar como sua organização funciona." O que o Contexto é aparece só no sobretítulo em caixa alta e no parágrafo abaixo. A primeira tela não tem nenhum dado concreto, como número de modelos, formato ou tempo.

**Evidências:**
- [src/components/LandingHero.astro:8](../src/components/LandingHero.astro#L8) (citado em UX-02).
- Verificador: `copy-headline` FAIL ("the page has no visible h1") e `copy-fact` FAIL na página Modelos ("the first screen holds no number, price, date, place, platform or genre"). Captura: [home-1440-escuro.png](./evidencias-ui/home-1440-escuro.png).

**Impacto:** quem chega por um link compartilhado precisa ler três blocos para saber se o Contexto serve para o seu problema. Isso conversa com EDI-01 e com a entrada por sintoma (I-06).

**Recomendação:** um `h1` que diga a categoria e o público, mantendo "Framework" (decisão 7). Por exemplo: "Framework para documentar dados e regras de negócio que a IA consegue usar". O slogan atual vira a frase de apoio, e entra um dado concreto, como "5 modelos com exemplo completo e gabarito". O texto final é decisão do mantenedor.

### UX-05 · No celular, a home leva quase quatro telas até as entradas por tarefa

**Severidade:** Média · **Confiança:** Alta

**O que acontece:** a 390 px, o cartão ilustrativo "O problema / Lacunas explícitas" fica empilhado abaixo do texto. O primeiro bloco termina em 3.230 px, e "O que você precisa fazer hoje?" só aparece na quarta tela. A 1440 px, o mesmo cartão é cortado pela borda inferior da primeira tela.

**Evidências:**
- Verificador: `hero-screen` FAIL a 390 ("the hero ends at 3230px on a 844px screen") e `fold-card` WARN a 1024 ("the 442x676 card starts on the first screen and runs 64px past its bottom"). Capturas: [home-390-escuro.png](./evidencias-ui/home-390-escuro.png), [home-390-hero.jpg](./evidencias-ui/home-390-hero.jpg).

**Impacto:** no celular, a ação principal fica abaixo de um cartão decorativo.

**Recomendação:** no celular, mostrar as três entradas por tarefa logo depois do texto e do botão, e levar o cartão para baixo delas ou reduzi-lo. A regra da skill de "o primeiro bloco cabe numa tela" vale aqui, na home.

### UX-06 · Três estilos de botão na mesma página

**Severidade:** Média · **Confiança:** Alta

**O que acontece:** a página Indicador tem botão cheio claro (o item ativo do menu), botão com contorno ("Baixar modelo em texto") e botão cheio escuro com contorno (os cartões de download).

**Evidências:**
- [src/components/TemplateStart.astro:86](../src/components/TemplateStart.astro#L86) `<a href={base + 'downloads/template-' + kind + '.md'} download>`
- [src/components/TemplateDownloads.astro:71](../src/components/TemplateDownloads.astro#L71) `<div class="template-downloads" role="group" aria-label="Arquivos de exemplo e template para reutilizar">`
- Verificador: `button-styles` FAIL ("3 button styles on the page").

**Impacto:** a mesma ação (baixar) aparece com duas aparências, e o leitor não sabe qual é a principal.

**Recomendação:** um par só (principal e secundário) em todo o portal. Faz parte das quatro primitivas previstas na F5 (cartão, rótulo, botão, aviso).

### UX-07 · Alvos de toque abaixo de 44 px no celular

**Severidade:** Média · **Confiança:** Alta

**O que acontece:** no celular, o título do site tem 121 x 32 px, o botão de busca 32 x 40 px, os ícones de âncora dos títulos 40 x 43 px e os links "Baixar" da página Modelos 41 x 17 px, encostados uns nos outros.

**Evidências:**
- Verificador: `tap-size` WARN nas quatro páginas e FAIL na página Modelos ("a 41x17px tap target ... 0px from the next one"). Captura: [home-390-alvo-toque.jpg](./evidencias-ui/home-390-alvo-toque.jpg).

**Impacto:** o dedo cai no alvo errado, sobretudo nos downloads, que são a ação final do percurso.

**Recomendação:** altura mínima de 44 px para links e controles fora do texto corrido, e espaço entre links de download vizinhos. Os controles do Starlight (título, busca) podem ser ajustados por CSS.

### UX-08 · Superfícies e cores fora da paleta

**Severidade:** Média · **Confiança:** Alta

**O que acontece:**
- A página Indicador usa quatro fundos lisos diferentes, um deles o azul da nota padrão do Starlight ("Sobre os metadados"), fora da paleta verde.
- A home tem cores escritas direto no CSS, fora dos tokens.

**Evidências:**
- [src/content/docs/templates/kpi.mdx:69](../src/content/docs/templates/kpi.mdx#L69) `:::note[Sobre os metadados]`
- [src/styles/custom.css:57](../src/styles/custom.css#L57) `color:#b4cbbb}`
- [src/styles/custom.css:61](../src/styles/custom.css#L61) `color:#e5c997}`
- [src/styles/custom.css:62](../src/styles/custom.css#L62) `color:#f7f2e8}`
- Verificador: `grounds` WARN ("4 flat grounds across the page (#17181c section, #16251f band x3, #20362d band x2, #171d4f band): three at most").

**Impacto:** a nota azul quebra a identidade. As cores fixas não acompanham a troca de tema e precisam ser mantidas à mão.

**Recomendação:** no máximo três fundos (base, superfície, inverso), avisos do Starlight recoloridos pelos tokens e nenhuma cor fixa fora de `:root`. Confirma VIS-01 e VIS-09.

### UX-09 · Contraste de texto abaixo do patamar da skill (passa no AA)

**Severidade:** Baixa · **Confiança:** Alta

**O que acontece:** três pares de texto corrido ficam entre 5,7:1 e 6,7:1. Isso passa no mínimo da WCAG AA (4,5:1), mas fica abaixo do patamar de 7:1 que a skill pede para texto corrido.

**Evidências:**
- Verificador: `text-contrast` FAIL: `#496152 on #e8eee4 reads 5.71:1` (cartão da home), `#a8c1b5 on #20362d reads 6.74:1` (Indicador), `#c1c3c8 on #353841 reads 6.64:1` (Comece em 5 minutos). Captura: [home-390-contraste.jpg](./evidencias-ui/home-390-contraste.jpg).

**Impacto:** leitura cansativa em telas de baixa qualidade e para quem tem baixa visão.

**Recomendação:** ajustar os tokens de texto secundário para 7:1 quando forem usados em parágrafos, deixando o cinza mais claro só para rótulos. Junto com A11Y-08 e VIS-12.

### UX-10 · Link compartilhado sem imagem nem cor de tema

**Severidade:** Baixa · **Confiança:** Alta

**O que acontece:** o `head` configurado só tem ícones, sem `og:image` nem `theme-color`.

**Evidências:**
- [astro.config.mjs:31](../astro.config.mjs#L31) `head: [`
- Verificador: `share-meta` WARN ("the head lacks og:image, theme-color").

**Impacto:** o Contexto foi feito para circular entre times, e um link colado no Slack ou no Teams aparece sem imagem.

**Recomendação:** uma imagem de compartilhamento (1200 x 630) e `theme-color` nos dois temas.

## Descartados (regra de landing page ou falso positivo)

| Verificação | Por que não entra no plano |
|---|---|
| `hero-screen`, `hero-fill`, `section-height`, `one-section`, `one-heading`, `section-air` nas páginas de documentação | A skill quer cada seção com uma ou duas telas e o primeiro bloco ocupando a tela toda. Página de documentação é texto corrido; isso só vale na home (UX-05). |
| `container-edges`, `row-lines`, `split-pair`, `label-centre` | Medem margens de landing page; o Starlight tem três colunas (menu, texto, sumário) de propósito. Na home, o cartão "fora da linha" a 768 px tem margens iguais nos dois lados quando visto na captura. |
| `no-visual`, `moment-none`, `cta`, `copy-headings` | Pedem foto, animação especial ou botão em toda seção e títulos com nome de produto. Não servem para documentação; as fotos e cenas da skill não combinam com o público e o tema. |
| `skip-link` | O link "Pular para o conteúdo" existe; o verificador procura o texto em inglês. |
| `copy-buttons` em "Pesquisar" | "Pesquisar" é verbo; a lista de verbos do verificador é em inglês. |
| `collide`, `overlap-text`, `tap-size` em "Ver resposta" | A barra fixa "Nesta página" do celular cobre o texto durante a rolagem; o conteúdo não se sobrepõe. |
| `links` para painéis de abas | Comportamento normal das abas do Starlight. |

## O que entra no plano antes e durante a F0

| Fase | Item | Achados |
|---|---|---|
| F0 | ADR de sistema visual: par de fontes servido pelo site, escala tipográfica com um tamanho por nível, três fundos, um par de botões, cores só em tokens. | UX-01, UX-02, UX-06, UX-08 |
| F0 | ADR de tamanho de página: no máximo 4 telas no desktop por página de modelo; sequência didática em passos ou páginas. | UX-03 |
| F0 | Captura de referência: guardar as capturas de [evidencias-ui/](./evidencias-ui/) como "antes" para comparar a cada fase. | todos |
| F1 | Correções baratas: `og:image` e `theme-color`, alvos de 44 px, títulos dos componentes por nível, home sem `h1` resolvida, cartão da home reposicionado no celular, nota azul recolorida, contraste de texto secundário. | UX-02, UX-05, UX-07, UX-09, UX-10 |
| F2 | `h1` da home com categoria e público, mantendo "Framework"; dado concreto na primeira tela. | UX-04 |
| F5 | Primitivas e tokens (já previstos), mais um checklist visual por PR: `consistency.mjs` em 1440 e 390, com uma lista de exceções escrita para as regras de landing page (a seção "Descartados"), e `perf.mjs` sem FAIL. | UX-01 a UX-10 |

**O que não adotar da skill:** fotografias, efeitos, cenas, "momentos" animados e uma seção por tela nas páginas de documentação. A skill é para sites comerciais; o Contexto aproveita dela o sistema (uma família por elemento), as medições e o rigor do celular.

## Não coberto nesta rodada

- Tema claro medido só em parte (pelo navegador do app); as capturas completas estão no tema escuro.
- 4 das 26 páginas medidas; as outras seguem os mesmos componentes, mas não foram percorridas.
- Texto (`copy-lint.mjs`) não foi rodado, porque as regras da skill são para inglês.
- Teste com leitor de tela e em celular físico continua pendente (ROADMAP).
