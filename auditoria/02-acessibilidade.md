# Acessibilidade

Data: 2026-11-17 · Commit: d08c810 · Escopo: componentes Astro em `src/components/`, `src/styles/custom.css`, `astro.config.mjs` e as páginas MDX citadas, avaliados pela leitura do código contra a WCAG 2.2 nível AA, sem renderizar o portal

## Resumo

- A base é boa: o checklist usa fieldset, legend e label; as tabelas têm caption e `th scope`; o SVG do diagrama tem `title` e `desc`; o foco visível tem 3px; e o portal respeita `prefers-reduced-motion`. Esses padrões devem virar regra para os componentes novos.
- O ponto mais sério está na ferramenta central do guia para quem não é técnico: o checklist não anuncia ao leitor de tela quantas lacunas restam, que a lista de lacunas apareceu, nem se a cópia funcionou (A11Y-01).
- A hierarquia de títulos tem saltos e repetições: o título do exemplo é um parágrafo, os `h4` aparecem sem `h3` pai, a página de revisão começa com `h3` e todas as páginas de modelo repetem três `h2` genéricos (A11Y-02, A11Y-03, A11Y-15).
- Três contrastes calculados a partir do CSS ficam abaixo do mínimo: linhas e bordas do diagrama nos dois temas (cerca de 1,2:1 a 1,95:1), o dourado do selo de rascunho no tema claro (cerca de 4,11:1) e, no limite, o checkbox no tema escuro (cerca de 3,02:1) (A11Y-05, A11Y-08, A11Y-13).
- O seletor de modelos agrupa 10 opções em dois subgrupos só visuais, e os links de ação aparecem sem aviso (A11Y-06, A11Y-07).
- Nada foi testado com leitor de tela, teclado ou navegador. Contrastes e tamanhos são estimativas pela fórmula de luminância relativa ([WCAG 2.2, relative luminance](https://www.w3.org/TR/WCAG22/#dfn-relative-luminance)).

## Pontos fortes (manter)

**1. Checklist com fieldset, legend e labels envolvendo cada checkbox.** O grupo e o nome de cada item chegam ao leitor de tela, e o clique na linha inteira amplia a área de alvo ([SC 1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html), [SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)).

- [src/components/ReadinessChecklist.astro:19](../src/components/ReadinessChecklist.astro#L19) `<legend class="sr-only">Dimensões da qualidade documental</legend>`
- [src/components/ReadinessChecklist.astro:21](../src/components/ReadinessChecklist.astro#L21) `<label class="check-row"><input type="checkbox" value={index} />`

**2. Regiões com rolagem horizontal são focáveis, têm nome e foco visível.** Tabelas largas ficam acessíveis por teclado sem perder o contexto no reflow ([SC 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [SC 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [SC 2.4.7](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)).

- [src/components/ExampleDoc.astro:96](../src/components/ExampleDoc.astro#L96) `role="region" aria-label="Histórico de mudanças do documento" tabindex="0"`
- [src/components/ExampleMeaning.astro:326](../src/components/ExampleMeaning.astro#L326) `role="region" aria-label="Tabela de decisão com rolagem horizontal" tabindex="0"`
- [src/styles/custom.css:747](../src/styles/custom.css#L747) `.example-doc__history-scroll:focus-visible {`

**3. Tabela com caption e `th scope="col"`.** O cabeçalho de colunas fica associado às células e a tabela tem título programático (SC 1.3.1).

- [src/components/ExampleDoc.astro:99](../src/components/ExampleDoc.astro#L99) `<thead><tr><th scope="col">Versão</th><th scope="col">Data</th>`
- [src/components/ExampleDoc.astro:98](../src/components/ExampleDoc.astro#L98) `<caption>Histórico de mudanças (o resumo não guarda a versão antiga completa)</caption>`

**4. SVG do diagrama com `role="img"`, `title` e `desc` em texto corrido.** O significado da relação 1:N chega a quem não vê o desenho, e a figcaption repete a regra de negócio ([SC 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)).

- [src/components/JoinDiagram.astro:23](../src/components/JoinDiagram.astro#L23) `<svg viewBox="0 0 600 280" role="img" aria-labelledby="jd-title jd-desc">`
- [src/components/JoinDiagram.astro:25](../src/components/JoinDiagram.astro#L25) `A sessão S1 tem dois pedidos confirmados, O1 e O2.`

**5. O estado nunca depende só de cor.** Rascunho e aprovado vêm escritos, e setas e ícones decorativos usam `aria-hidden`, o que evita ruído ([SC 1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), SC 1.1.1).

- [src/components/ExampleDoc.astro:52](../src/components/ExampleDoc.astro#L52) `{complete ? 'EXEMPLO COMPLETO' : 'EXEMPLO COM LACUNAS · NADA APROVADO'}`
- [src/components/ExampleDoc.astro:65](../src/components/ExampleDoc.astro#L65) `<span class="example-doc__revision-arrow" aria-hidden="true">→</span>`

**6. Foco visível forte (3px) nos controles customizados e respeito a `prefers-reduced-motion`.** Atende a intenção de SC 2.4.7 e [SC 2.4.13](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) e reduz desconforto vestibular ([SC 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)).

- [src/styles/custom.css:257](../src/styles/custom.css#L257) `outline: 3px solid var(--sl-color-accent);`
- [src/styles/custom.css:120](../src/styles/custom.css#L120) `@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}`

**7. Idioma declarado, título da página inicial preservado para leitor de tela e abas do Starlight.** A página declara pt-BR ([SC 3.1.1](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)). A abertura visual usa parágrafo, mas o `h1` da página continua disponível para leitor de tela. As abas usam o componente Tabs do Starlight, que segue o padrão ARIA de abas ([ARIA APG, Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)).

- [astro.config.mjs:36](../astro.config.mjs#L36) `locales: { root: { label: 'Português', lang: 'pt-BR' } },`
- [src/styles/custom.css:266](../src/styles/custom.css#L266) `main:has(.context-hero) > .content-panel:first-child {`
- [src/components/ExampleDoc.astro:76](../src/components/ExampleDoc.astro#L76) `<Tabs>`

**8. Seletor de modelos com região de status e estado selecionado visível por borda.** A escolha atualiza um texto anunciável, e o rádio marcado ganha borda e sombra interna além da cor do texto ([SC 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html), [SC 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)).

- [src/components/TemplateFinder.astro:38](../src/components/TemplateFinder.astro#L38) `<p data-summary role="status" aria-live="polite">`
- [src/styles/custom.css:225](../src/styles/custom.css#L225) `box-shadow: inset 0 0 0 1px var(--sl-color-accent);`

## Índice de achados

| ID | Severidade | Título |
|---|---|---|
| A11Y-01 | Média | Checklist: contagem de lacunas, lista de lacunas e "Lista copiada" não são anunciados |
| A11Y-02 | Média | ExampleDoc e ExampleMeaning: título do exemplo como `<p>` e `h4` sem `h3` pai |
| A11Y-05 | Média | JoinDiagram: linhas e bordas neutras com contraste muito baixo nos dois temas |
| A11Y-06 | Média | TemplateFinder: rótulos de grupo em `<p>` não associados aos radios |
| A11Y-08 | Média | Tom dourado do rascunho (#9a6b37) sobre #f1f2e9 não atinge 4,5:1 |
| A11Y-03 | Baixa | Página de revisão abre com `h3` antes de qualquer `h2` |
| A11Y-04 | Baixa | JoinDiagram: texto do SVG fica com cerca de 6 px em tela de celular |
| A11Y-07 | Baixa | TemplateFinder: links de ação aparecem sem aviso e o nome do landmark difere do `h2` visível |
| A11Y-09 | Baixa | Abas do ExampleDoc: aba selecionada com indicador fraco |
| A11Y-10 | Baixa | `list-style:none` em `<ol>` pode remover a semântica de lista no Safari e VoiceOver |
| A11Y-11 | Baixa | RevisionComparison: `dd` de IDs com `overflow-x:auto` sem `tabindex` |
| A11Y-12 | Baixa | Excesso de landmarks region e nomes repetidos na mesma página |
| A11Y-13 | Baixa | `accent-color` fixo #2c7956 nos checkboxes do checklist dá cerca de 3:1 no tema escuro |
| A11Y-14 | Baixa | Tamanhos de fonte muito pequenos em controles e textos de apoio |
| A11Y-15 | Baixa | TemplateStart repete três `h2` genéricos em todas as páginas de modelo |

## Achados

### A11Y-01 · Checklist: contagem de lacunas, lista de lacunas e "Lista copiada" não são anunciados

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** A única região viva é o parágrafo de feedback, que tem só três textos possíveis. Com uma ou com sete lacunas o texto é o mesmo, então a contagem nunca é falada. A lista de lacunas aparece quando o atributo `hidden` é removido e os itens são trocados, fora de qualquer região viva. O resultado da cópia é só uma troca do rótulo do botão, que volta ao original depois de 2,5 s, também sem região viva.

**Evidências:**

- [src/components/ReadinessChecklist.astro:24](../src/components/ReadinessChecklist.astro#L24) `<p class="readiness-feedback" data-feedback aria-live="polite">Marque o que o documento já responde.`
- [src/components/ReadinessChecklist.astro:53](../src/components/ReadinessChecklist.astro#L53) `'Sem marca, a dimensão vira lacuna. Leve a lista abaixo para quem responde pelo conteúdo.';`
- [src/components/ReadinessChecklist.astro:55](../src/components/ReadinessChecklist.astro#L55) `gaps.hidden = !touched || open.length === 0;`
- [src/components/ReadinessChecklist.astro:76](../src/components/ReadinessChecklist.astro#L76) `copy.textContent = 'Lista copiada';`
- [src/components/ReadinessChecklist.astro:80](../src/components/ReadinessChecklist.astro#L80) `setTimeout(() => { copy.textContent = 'Copiar lista de lacunas'; }, 2500);`

**Impacto:** Quem usa leitor de tela marca itens sem saber quantas lacunas restam nem que uma lista nova surgiu abaixo. Também não sabe se a cópia funcionou, e a mensagem some em 2,5 s. Como o texto do feedback não muda entre o primeiro e o sétimo item, alguns leitores de tela nem repetem o anúncio. É a ferramenta central do guia para o público não técnico ([SC 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)).

**Recomendação:** Incluir a contagem no texto do feedback, por exemplo "Faltam N de 8 dimensões". Usar uma região `role="status"` separada e persistente para "Lista copiada" ou "Não foi possível copiar". Não desfazer a mensagem com um timer curto. Opcional: ligar o feedback à lista de lacunas com `aria-describedby`.

**Observação no portal:** Não testado com leitor de tela real. A repetição do anúncio quando o mesmo `textContent` é reatribuído varia entre NVDA, JAWS e VoiceOver.

### A11Y-02 · ExampleDoc e ExampleMeaning: título do exemplo como `<p>` e `h4` sem `h3` pai

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O título do exemplo é um parágrafo, então o cartão de exemplo não tem cabeçalho navegável. Dentro das abas há `h4` ("Perguntas em aberto" e cada grupo do ExampleMeaning). Na página do modelo de conceito, o `h2` "Antes e depois da decisão" é seguido direto pelo ExampleDoc, sem `h3` intermediário. Essa página tem dois ExampleDoc, então os `h4` se repetem.

**Evidências:**

- [src/components/ExampleDoc.astro:53](../src/components/ExampleDoc.astro#L53) `<p class="example-doc__title">{doc.title}</p>`
- [src/components/ExampleDoc.astro:80](../src/components/ExampleDoc.astro#L80) `<h4>Perguntas em aberto ({questions.length})</h4>`
- [src/components/ExampleMeaning.astro:301](../src/components/ExampleMeaning.astro#L301) `<h4>{group.heading}</h4>`
- [src/content/docs/templates/conceito.mdx:44](../src/content/docs/templates/conceito.mdx#L44) `## Antes e depois da decisão`
- [src/content/docs/templates/conceito.mdx:48](../src/content/docs/templates/conceito.mdx#L48) `<ExampleDoc file="exemplo-conceito-lacunas.yaml" />`
- [src/content/docs/templates/conceito.mdx:52](../src/content/docs/templates/conceito.mdx#L52) `<ExampleDoc file="exemplo-conceito-completo.yaml" />`
- [src/content/docs/exemplos/analytics-integrado.mdx:110](../src/content/docs/exemplos/analytics-integrado.mdx#L110) `<ExampleDoc file="exemplo-dataset-pedidos-completo.yaml" />`

**Impacto:** Quem navega por títulos encontra um `h2` seguido de `h4` repetidos ("Definição e contexto", "Exemplos que ajudam a decidir") sem saber a qual exemplo pertencem. A estrutura pula de `h2` para `h4` ([SC 1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html), [SC 2.4.6](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html); técnica [G141](https://www.w3.org/WAI/WCAG22/Techniques/general/G141)).

**Recomendação:** Transformar o título do exemplo em `h3`, com uma prop de nível para quando o contexto pedir outro, e ajustar os `h4` internos para ficarem sempre um nível abaixo do título do cartão. Usar o título do exemplo para diferenciar os dois cartões da mesma página.

### A11Y-05 · JoinDiagram: linhas e bordas neutras com contraste muito baixo nos dois temas

**Severidade:** Média
**Confiança:** Média

**O que acontece:** As caixas e as ligações sem destaque usam `--context-line`. No tema claro é #d5ddd5, com cerca de 1,32:1 sobre o fundo #faf9f6 e 1,23:1 sobre a superfície #f1f2e9. No tema escuro é #38554a sobre #16251f, com cerca de 1,95:1. O mínimo para objetos gráficos é 3:1. As linhas que ligam S2 a O3 e S5 a O6, e as bordas das caixas, ficam quase invisíveis.

**Evidências:**

- [src/styles/custom.css:27](../src/styles/custom.css#L27) `--context-line: #d5ddd5;`
- [src/styles/custom.css:12](../src/styles/custom.css#L12) `--context-line: #38554a;`
- [src/components/JoinDiagram.astro:63](../src/components/JoinDiagram.astro#L63) `.jd-box { fill: var(--context-surface); stroke: var(--context-line); stroke-width: 1.5; }`
- [src/components/JoinDiagram.astro:65](../src/components/JoinDiagram.astro#L65) `.jd-link { stroke: var(--context-line); stroke-width: 1.5; }`

**Impacto:** Quem tem baixa visão ou usa tela com muito brilho não vê as relações S2 para O3 e S5 para O6, que são justamente os casos "cancelado" e "teste" que o exemplo quer ensinar ([SC 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)).

**Recomendação:** Criar um token de borda para componentes com pelo menos 3:1 (por exemplo #7d8f86 no claro, cerca de 3,25:1 sobre #faf9f6, e #6f8f80 no escuro, cerca de 4,5:1 sobre #16251f). Distinguir os pedidos não elegíveis também pelo tipo de traço (tracejado) ou por rótulo, não só pela espessura e pela cor.

**Observação no portal:** Razões recalculadas pela fórmula de luminância relativa a partir dos hex do CSS. São estimativas, não medições no navegador.

### A11Y-06 · TemplateFinder: rótulos de grupo em `<p>` não associados aos radios

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** Um único fieldset com a legend "Selecione uma finalidade" contém dois subgrupos ("Conhecimento do negócio" e "Dados e Analytics"). Os títulos dos subgrupos são parágrafos, e todos os radios têm o mesmo `name`. O leitor de tela anuncia só a legend geral, e a categoria nunca é falada quando um radio recebe foco.

**Evidências:**

- [src/components/TemplateFinder.astro:26](../src/components/TemplateFinder.astro#L26) `<legend>Selecione uma finalidade</legend>`
- [src/components/TemplateFinder.astro:28](../src/components/TemplateFinder.astro#L28) `<p class="finder-group">{group.label}</p>`
- [src/components/TemplateFinder.astro:31](../src/components/TemplateFinder.astro#L31) `<input type="radio" name="template-intent" value={choice.id}/>`

**Impacto:** As 10 opções chegam como um grupo plano. Quem usa leitor de tela perde a divisão entre conhecimento do negócio e dados, que o desenho visual usa para orientar o leitor ([SC 1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html), [SC 3.3.2](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html)).

**Recomendação:** Usar dois fieldset, um por grupo e cada um com sua legend, ou manter um fieldset e envolver cada subgrupo em `role="group"` com `aria-labelledby` apontando para o título do grupo.

### A11Y-08 · Tom dourado do rascunho (#9a6b37) sobre #f1f2e9 não atinge 4,5:1

**Severidade:** Média
**Confiança:** Média

**O que acontece:** No tema claro, `--context-gold` é #9a6b37 e é a cor do texto do selo de rascunho do ExampleDoc, com fonte de 0,86rem e peso 700, o que não conta como texto grande. O cartão do ExampleDoc usa a superfície #f1f2e9, sobre a qual a razão calculada é cerca de 4,11:1. Sobre o fundo #faf9f6 seria cerca de 4,4:1. No tema escuro (#e1bd81) o contraste é alto.

**Evidências:**

- [src/styles/custom.css:29](../src/styles/custom.css#L29) `--context-gold: #9a6b37;`
- [src/styles/custom.css:830](../src/styles/custom.css#L830) `color: var(--context-gold);`
- [src/styles/custom.css:808](../src/styles/custom.css#L808) `font-size: .86rem;`
- [src/styles/custom.css:274](../src/styles/custom.css#L274) `.example-doc { border: 1px solid var(--context-line); border-radius: 9px; background: var(--context-surface);`
- [src/styles/custom.css:25](../src/styles/custom.css#L25) `--context-surface: #f1f2e9;`

**Impacto:** O selo "Rascunho 0.x · nada aprovado ainda" é o sinal mais importante da honestidade do projeto sobre o estado do documento e fica abaixo do mínimo no tema claro ([SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)).

**Recomendação:** Escurecer o tom do texto no tema claro (por exemplo #86592a, cerca de 5,4:1 sobre #f1f2e9). Manter o dourado atual só para bordas e preenchimentos.

**Observação no portal:** Recalculado por luminância relativa a partir dos hex. Estimativa, não medição no navegador.

### A11Y-03 · Página de revisão abre com `h3` antes de qualquer `h2`

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** ReviewStages renderiza `h3` dentro de uma lista, e `checklist.mdx` usa o componente na linha 17, antes do primeiro `h2` da página (linha 19). A página pula de `h1` para `h3`.

**Evidências:**

- [src/components/ReviewStages.astro:33](../src/components/ReviewStages.astro#L33) `<h3>{stage.title}</h3>`
- [src/content/docs/validacao/checklist.mdx:17](../src/content/docs/validacao/checklist.mdx#L17) `<ReviewStages />`
- [src/content/docs/validacao/checklist.mdx:19](../src/content/docs/validacao/checklist.mdx#L19) `## 1. Cobertura: estão claras as oito dimensões?`

**Impacto:** Os títulos "Cobertura", "Consistência e evidências" e "Confirmação por responsável" aparecem como `h3` órfãos e depois voltam como `h2` numerados, o que confunde a navegação por títulos ([SC 1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)).

**Recomendação:** Adicionar um `h2` introdutório antes do componente (por exemplo "As três verificações") ou tornar o nível do título uma prop.

### A11Y-04 · JoinDiagram: texto do SVG fica com cerca de 6 px em tela de celular

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** O SVG tem viewBox de 600 unidades e escala proporcionalmente com `width:100%`. Os textos têm 12 e 14 unidades. Num contêiner de cerca de 270 a 290 px (viewport de 320 px menos margens), a escala fica perto de 0,45 a 0,48, e o texto aparece com algo entre 5,4 e 6,7 px CSS. Não há alternativa com rolagem nem layout empilhado.

**Evidências:**

- [src/components/JoinDiagram.astro:23](../src/components/JoinDiagram.astro#L23) `<svg viewBox="0 0 600 280" role="img" aria-labelledby="jd-title jd-desc">`
- [src/components/JoinDiagram.astro:58](../src/components/JoinDiagram.astro#L58) `.rel-diagram svg { width: 100%; height: auto; max-width: 600px; display: block; }`
- [src/components/JoinDiagram.astro:61](../src/components/JoinDiagram.astro#L61) `.jd-note { font: 12px var(--sl-font); fill: var(--context-muted); }`
- [src/components/JoinDiagram.astro:60](../src/components/JoinDiagram.astro#L60) `.jd-id { font: 700 14px var(--sl-font); fill: var(--context-ink); }`

**Impacto:** No celular, sem zoom, os rótulos S1, O1 e os status, que são o conteúdo central do exemplo, ficam ilegíveis sem pinça. Não é uma falha clara de conformidade: com zoom de 400% no desktop o texto ainda fica maior que no tamanho original, e gráficos que precisam de duas dimensões são isentos do [SC 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html). A informação também está no `desc` e na figcaption. É um problema de legibilidade para baixa visão e celular, não uma violação AA.

**Recomendação:** Oferecer uma versão em tabela ou lista (sessão, pedidos, status) visível no celular, ou colocar o SVG num contêiner rolável com largura mínima. Outra opção é aumentar as fontes e reduzir o viewBox para cerca de 360 de largura, com layout vertical.

**Observação no portal:** Cálculo teórico, não medido em navegador.

### A11Y-07 · TemplateFinder: links de ação aparecem sem aviso e o nome do landmark difere do `h2` visível

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** A região de status anuncia só o resumo. Os dois links (ver como preencher e baixar) aparecem com `actions.hidden = false` sem aviso, e os destinos mudam por JavaScript. Os links ficam fora da região viva, e a pessoa precisa descobri-los sozinha. A section também recebe um `aria-label` próprio ("Escolha um modelo pelo objetivo"), diferente do `h2` visível ("O que você precisa documentar?"), então o nome do landmark não bate com o título que a pessoa vê.

**Evidências:**

- [src/components/TemplateFinder.astro:21](../src/components/TemplateFinder.astro#L21) `<section class="template-finder" data-template-finder aria-label="Escolha um modelo pelo objetivo">`
- [src/components/TemplateFinder.astro:23](../src/components/TemplateFinder.astro#L23) `<h2>O que você precisa documentar?</h2>`
- [src/components/TemplateFinder.astro:39](../src/components/TemplateFinder.astro#L39) `<div class="finder-output__actions" data-actions hidden>`
- [src/components/TemplateFinder.astro:60](../src/components/TemplateFinder.astro#L60) `actions.hidden = false;`
- [src/components/TemplateFinder.astro:38](../src/components/TemplateFinder.astro#L38) `<p data-summary role="status" aria-live="polite">`

**Impacto:** Quem usa leitor de tela ouve o resumo, mas pode não perceber que há links logo abaixo ([SC 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)). Com JavaScript desativado, os links de ação ficam ocultos para sempre e escolher um radio não produz nada.

**Recomendação:** Incluir no texto do status algo como "Dois links disponíveis abaixo" ou colocar a ação dentro da região de status. Usar `aria-labelledby` apontando para o `h2` em vez de um `aria-label` diferente. Considerar uma alternativa sem JavaScript com uma lista simples de links.

### A11Y-09 · Abas do ExampleDoc: aba selecionada com indicador fraco

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** A aba ativa se distingue por fundo translúcido (17% da cor do texto sobre o trilho de 7%), borda de 22% e peso 750 contra 650, e o texto passa de muted para ink. No tema claro o fundo vira branco, com borda `--context-line` (cerca de 1,2:1) e sombra de 10%. Não há sublinhado nem barra sólida na cor de acento.

**Evidências:**

- [src/styles/custom.css:851](../src/styles/custom.css#L851) `background: color-mix(in srgb, var(--context-ink) 7%, transparent);`
- [src/styles/custom.css:871](../src/styles/custom.css#L871) `background: color-mix(in srgb, var(--context-ink) 17%, transparent);`
- [src/styles/custom.css:877](../src/styles/custom.css#L877) `border-color: var(--context-line);`
- [src/styles/custom.css:857](../src/styles/custom.css#L857) `box-shadow: none;`

**Impacto:** A diferença de fundo entre aba ativa e inativa fica bem abaixo de 3:1, e a troca de peso de 650 para 750 é sutil. Como vários sinais se somam (peso, cor do texto, fundo, borda e sombra), não é uma falha clara do [SC 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), mas quem tem baixa visão pode ter dificuldade para saber em qual aba está. O foco por teclado tem outline próprio na linha 881.

**Recomendação:** Adicionar um indicador de estado não cromático com 3:1, como uma barra inferior de 3px na cor de acento ou borda de acento na aba ativa. Manter o `aria-selected` do Starlight.

**Observação no portal:** Estimativa por inspeção do CSS, sem renderizar.

### A11Y-10 · `list-style:none` em `<ol>` pode remover a semântica de lista no Safari e VoiceOver

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** Duas listas ordenadas têm `list-style:none`: os passos do ExampleMeaning (`ol.example-meaning__entries`) e as etapas do ReviewStages (`ol.review-stages`). No ReviewStages o número visual é `aria-hidden`, então a ordem 1, 2, 3 só chega ao leitor de tela se a semântica de `ol` for preservada.

**Evidências:**

- [src/styles/custom.css:598](../src/styles/custom.css#L598) `list-style:none;`
- [src/styles/custom.css:691](../src/styles/custom.css#L691) `list-style: none;`
- [src/components/ExampleMeaning.astro:308](../src/components/ExampleMeaning.astro#L308) `<ol class="example-meaning__entries">`
- [src/components/ReviewStages.astro:32](../src/components/ReviewStages.astro#L32) `<span class="review-stages__number" aria-hidden="true">{stage.number}</span>`

**Impacto:** No WebKit com VoiceOver a lista pode deixar de ser anunciada como lista, e a contagem e a posição somem ([Scott O'Hara, "Fixing" Lists](https://www.scottohara.me/blog/2019/01/12/lists-and-safari.html)). Chromium e Firefox mantêm a semântica ([SC 1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)).

**Recomendação:** Adicionar `role="list"` explícito nos dois `ol` ou manter marcadores visíveis. No ReviewStages, tirar o `aria-hidden` do número ou incluir "Etapa 1" no texto acessível.

**Observação no portal:** O comportamento atual do Safari não foi verificado.

### A11Y-11 · RevisionComparison: `dd` de IDs com `overflow-x:auto` sem `tabindex`

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** Os valores de ID do assunto e de ID da versão ficam em `dd` com `white-space:nowrap` e `overflow-x:auto`. O `dd` não é focável e não tem nome. Em navegadores que não tornam contêineres roláveis focáveis automaticamente (Safari), quem usa só teclado não consegue rolar o ID longo.

**Evidências:**

- [src/components/RevisionComparison.astro:35](../src/components/RevisionComparison.astro#L35) `<div class="revision-comparison__metadata-id"><dt>ID do assunto</dt><dd><code>{doc.id}</code></dd></div>`
- [src/styles/custom.css:475](../src/styles/custom.css#L475) `.revision-comparison__metadata-id dd {`
- [src/styles/custom.css:481](../src/styles/custom.css#L481) `white-space: nowrap;`
- [src/styles/custom.css:483](../src/styles/custom.css#L483) `overflow-x: auto;`

**Impacto:** Em tela estreita, o ID cortado fica ilegível para quem usa teclado ([SC 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)). Chromium e Firefox recentes tornam contêineres roláveis focáveis por padrão, então o risco está sobretudo no Safari. Uma barra de rolagem dentro de um `dd` também é incomum para quem está começando.

**Recomendação:** Permitir quebra em pontos seguros (por exemplo `<wbr>` depois de hífen e ponto) e remover o overflow, ou aplicar `tabindex="0"`, `role="group"` e `aria-label` ao `dd` rolável.

### A11Y-12 · Excesso de landmarks region e nomes repetidos na mesma página

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** Vários componentes usam section com `aria-label`, o que cria um landmark region por bloco. Cada ExampleDoc tem até três (conteúdo em linguagem natural e perguntas em aberto na primeira aba, histórico na segunda). O conteúdo das abas inativas fica oculto, então por padrão aparecem dois por cartão. Na página de conceito há dois ExampleDoc com rótulos idênticos. O `aria-label` "Perguntas que ainda precisam de resposta" diz o mesmo que o `h4` "Perguntas em aberto" logo abaixo, com outras palavras.

**Evidências:**

- [src/components/ExampleMeaning.astro:299](../src/components/ExampleMeaning.astro#L299) `<section class="example-meaning" aria-label="Conteúdo principal do documento em linguagem natural">`
- [src/components/ExampleDoc.astro:79](../src/components/ExampleDoc.astro#L79) `<section class="example-doc__gaps" aria-label="Perguntas que ainda precisam de resposta">`
- [src/components/ExampleDoc.astro:96](../src/components/ExampleDoc.astro#L96) `role="region" aria-label="Histórico de mudanças do documento" tabindex="0"`
- [src/components/BeforeAfter.astro:1](../src/components/BeforeAfter.astro#L1) `<section class="before-after" aria-label="Comparação de exemplo de documento antes e depois">`
- [src/components/RevisionComparison.astro:30](../src/components/RevisionComparison.astro#L30) `<section class="revision-comparison" aria-label="Duas versões do mesmo documento">`
- [src/components/TemplateStart.astro:65](../src/components/TemplateStart.astro#L65) `<section class="template-start" aria-label="Resumo prático deste modelo">`

**Impacto:** A lista de landmarks do leitor de tela fica poluída e repete nomes idênticos entre os dois exemplos da página, sem dizer qual é qual. Isso reduz a utilidade dos landmarks para navegar. É uma questão de boa prática ARIA, não falha de conformidade por si só ([ARIA APG, Landmark Regions](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/)).

**Recomendação:** Reservar landmarks para regiões estruturais da página. Nos componentes, usar div ou section sem nome e confiar nos títulos. Onde o nome ficar, torná-lo único (incluindo o título do exemplo) e usar `aria-labelledby` apontando para o título visível. Manter `role="region"` só nas regiões roláveis focáveis.

### A11Y-13 · `accent-color` fixo #2c7956 nos checkboxes do checklist dá cerca de 3:1 no tema escuro

**Severidade:** Baixa
**Confiança:** Baixa

**O que acontece:** Os checkboxes do checklist usam uma cor fixa nos dois temas. Sobre a superfície escura #16251f do cartão, a razão calculada é cerca de 3,02:1, no limite. No tema claro, sobre #f1f2e9, é cerca de 4,68:1. O radio do seletor de modelos usa o token do tema e não tem esse problema.

**Evidências:**

- [src/styles/custom.css:105](../src/styles/custom.css#L105) `.check-row input{flex:0 0 auto;width:1.1rem;height:1.1rem;margin:.15rem 0 0;accent-color:#2c7956}`
- [src/styles/custom.css:229](../src/styles/custom.css#L229) `accent-color: var(--sl-color-accent);`
- [src/styles/custom.css:90](../src/styles/custom.css#L90) `.readiness{border:1px solid var(--context-line);border-radius:9px;background:var(--context-surface);`
- [src/styles/custom.css:10](../src/styles/custom.css#L10) `--context-surface: #16251f;`

**Impacto:** No tema escuro, a caixa marcada passa por pouco do 3:1 do [SC 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), e o contorno do checkbox desmarcado depende do navegador. É uma inconsistência de token, não uma falha.

**Recomendação:** Usar `var(--sl-color-accent)` também no checklist e conferir o ícone de marcação nos dois temas e em navegadores que aplicam o `accent-color` de formas diferentes.

**Observação no portal:** Recalculado por luminância relativa. A aparência real do `accent-color` varia por navegador.

### A11Y-14 · Tamanhos de fonte muito pequenos em controles e textos de apoio

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** Vários controles e textos de apoio ficam entre 11,5 e 13 px: o botão de limpar do checklist (0,76rem), o de copiar (0,8rem), a descrição de cada critério (0,79rem) e os kickers do diagrama (0,72rem).

**Evidências:**

- [src/styles/custom.css:111](../src/styles/custom.css#L111) `font-weight:700;font-size:.76rem}`
- [src/styles/custom.css:102](../src/styles/custom.css#L102) `font-weight:750;font-size:.8rem}`
- [src/styles/custom.css:108](../src/styles/custom.css#L108) `.check-row__body span{font-size:.79rem;line-height:1.5;color:var(--context-muted)}`
- [src/components/JoinDiagram.astro:72](../src/components/JoinDiagram.astro#L72) `font-size: .72rem !important;`

**Impacto:** Não viola um critério AA por si só, porque usa rem e acompanha o zoom ([SC 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)). Mas a descrição de cada critério é o texto principal do checklist, e o público inclui pessoas pouco técnicas e com baixa visão. Texto de cerca de 12,6 px na cor muted reduz a legibilidade.

**Recomendação:** Definir um mínimo de cerca de 0,875rem para texto que carrega instrução e 0,8125rem para metadados, com botões de pelo menos 0,875rem.

### A11Y-15 · TemplateStart repete três `h2` genéricos em todas as páginas de modelo

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** O resumo no topo de cada página de modelo tem três `h2` ("Quando usar", "O que você vai produzir", "O que ter em mãos") dentro de uma section com nome. Os mesmos três `h2` aparecem em todas as páginas que usam o componente e vêm antes do `h2` "O problema".

**Evidências:**

- [src/components/TemplateStart.astro:69](../src/components/TemplateStart.astro#L69) `<h2>Quando usar</h2>`
- [src/components/TemplateStart.astro:73](../src/components/TemplateStart.astro#L73) `<h2>O que você vai produzir</h2>`
- [src/components/TemplateStart.astro:77](../src/components/TemplateStart.astro#L77) `<h2>O que ter em mãos</h2>`
- [src/content/docs/templates/conceito.mdx:12](../src/content/docs/templates/conceito.mdx#L12) `<TemplateStart kind="conceito" />`
- [src/content/docs/templates/conceito.mdx:14](../src/content/docs/templates/conceito.mdx#L14) `## O problema`

**Impacto:** Na navegação por títulos e no índice lateral do Starlight, a página ganha três seções de primeiro nível antes do conteúdo, e o resumo passa a ter o mesmo peso que o conteúdo ([SC 2.4.6](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html)). Também desloca "O problema", que o contrato editorial define como a primeira parte da estrutura de uma página de tipo.

**Recomendação:** Usar `h3` sob um único `h2` ("Antes de preencher") ou transformar os três blocos numa lista de definição (`dl`). Isso também limpa o índice lateral.

## Descartados na verificação

- **prior-10 (termos em inglês sem `lang`):** o inglês em BeforeAfter e JoinDiagram é formado por identificadores técnicos em código (`pending_approval` em BeforeAfter.astro:15, `demo_sessions` em JoinDiagram.astro:26, status como `CONFIRMED` em JoinDiagram.astro:15). O [SC 3.1.2](https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html) isenta nomes próprios e termos técnicos, então não é falha AA. Fica como melhoria opcional de pronúncia: marcar `lang="en"` nos blocos YAML e nos identificadores, se desejado.

## Não coberto nesta rodada

- Nenhum teste com leitor de tela real (NVDA, JAWS, VoiceOver, TalkBack) nem com navegação por teclado ao vivo. Os comportamentos descritos vêm da leitura do código.
- Contrastes e tamanhos renderizados são estimativas calculadas pela fórmula de luminância relativa a partir dos hex do CSS. Não foram medidos em navegador nem com ferramenta.
- O HTML gerado pelo Starlight (Tabs, sidebar, busca, seletor de tema, skip link) não foi verificado. Só foi avaliado o CSS que o sobrescreve.
- As demais páginas MDX (fundamentos, método, governança, referências e sobre) não foram examinadas a fundo. Foram cobertas apenas a hierarquia de títulos e a presença de imagens e de links genéricos, por busca.
- As tabelas Markdown das MDX não foram inspecionadas quanto a cabeçalhos, overflow ou reflow em 320 px.
- LandingHero, TemplateDownloads, AnalyticsLabDownloads e SiteFooter não foram auditados por completo quanto a contraste e alvo de toque.
- Alvos de toque ([SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)) e reflow em 320 px de componentes além do JoinDiagram não foram medidos.
- O portal publicado (https://edoardolobl.github.io/contexto-framework/) não foi acessado, então a auditoria vale para o repositório no commit d08c810 e pode divergir da versão em produção.
