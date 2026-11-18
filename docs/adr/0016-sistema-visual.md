# 0016. Sistema visual

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17, depois de comparar os três pares de fontes com textos do portal
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [13-ui-ux-tasteskill.md](../../auditoria/13-ui-ux-tasteskill.md), seção "O que entra no plano antes e durante a F0", primeira linha (UX-01, UX-02, UX-06, UX-08)

## Contexto

O CSS pede Inter e Georgia, mas nenhuma fonte é carregada: cada leitor vê o portal na fonte do próprio sistema (UX-01, VIS-06). Os títulos pulam níveis e têm tamanhos trocados, como um `h2` de 14,7 px ao lado de um `h2` de 35 px (UX-02). A página Indicador tem três estilos de botão para a mesma ação, baixar (UX-06), e quatro fundos diferentes, um deles o azul da nota padrão do Starlight, fora da paleta (UX-08). A home tem cores escritas direto no CSS, que não acompanham a troca de tema.

## Decisão

- **Fontes:** a família **IBM Plex**, com licença SIL Open Font License: IBM Plex Sans no texto, IBM Plex Serif nos títulos de destaque e IBM Plex Mono no YAML, nos nomes de campo e no código. Os arquivos são servidos pelo próprio site com `@font-face` (a regra de CSS que carrega uma fonte a partir de um arquivo), só com os pesos usados. Fontes não carregadas saem da pilha do CSS.
  - Motivo: uma família só cobre os três usos do portal, inclusive o YAML que aparece em quase toda página de modelo; os acentos do português são bem desenhados; o tom sóbrio combina com manter "Framework" no nome ([ADR 0008](./0008-manter-framework-no-nome.md)).
- **Escala tipográfica:** um tamanho por nível de título, de `h1` a `h5`, definido uma vez nas variáveis de tamanho do Starlight. Cartão não usa elemento de título fora da ordem; componentes recebem o nível como propriedade. Os valores ficam para depois da escolha da fonte.
- **Fundos:** três, e só três: base, superfície e inverso.
- **Botões:** um par só em todo o portal, principal e secundário. A mesma ação tem sempre a mesma aparência.
- **Cores:** só como tokens (variáveis de CSS com nome) declarados em `:root`, com os valores dos dois temas. Nenhuma cor escrita direto fora dos tokens.
- **Avisos do Starlight** (`note`, `tip`, `caution`, `danger`) recoloridos pelos tokens, sem `!important`.

## Alternativas consideradas

- **Inter com Source Serif 4:** menor mudança, porque o CSS já pede Inter, mas Inter é a fonte mais usada na web hoje (o visual de modelo pronto que a revisão com a tasteskill aponta) e não tem fonte de código da mesma família.
- **Atkinson Hyperlegible Next com Literata:** a melhor leitura para baixa visão e para textos longos, mas sem fonte de código da família e com um tom mais suave do que o pretendido.
- **Só a fonte do sistema, sem `@font-face`:** zero arquivos novos, mas a identidade continua diferente em cada sistema (UX-01).
- **Uma fonte só, sem serifa** (opção aberta em UX-01): mais simples; a proposta prefere o par para manter o destaque editorial que o portal já tenta ter.
- **Carregar as fontes de um serviço externo** (levantada na redação do ADR): cada visita faria uma requisição a terceiros, com custo de privacidade e uma dependência a mais.
- **Manter os fundos e o azul padrão do Starlight:** a nota azul continua quebrando a identidade.

## Consequências

- **Positivas:** o portal fica igual para todo leitor; títulos certos ajudam leitor de tela, sumário, busca e cortes para RAG (I-17).
- **Negativas:** arquivos de fonte aumentam o peso da página, e a Mono acrescenta um arquivo; o desempenho (hoje sem nenhuma falha) precisa ser medido de novo com `perf.mjs` depois da troca.
- **Fases afetadas:** F0 (este ADR e a captura de referência em `auditoria/evidencias-ui/`); F1 (nota azul recolorida, títulos por nível, `h1` da home, contraste do texto secundário, UX-09); F5 (tokens, quatro primitivas, checklist visual por PR).
- **Breaking:** nenhum para os modelos. Muda só a aparência do portal.
