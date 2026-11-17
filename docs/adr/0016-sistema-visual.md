# 0016. Sistema visual

- **Estado:** Proposto
- **Data:** 2026-11-17
- **Proposto por:** auditoria
- **Origem:** [13-ui-ux-tasteskill.md](../../auditoria/13-ui-ux-tasteskill.md), seção "O que entra no plano antes e durante a F0", primeira linha (UX-01, UX-02, UX-06, UX-08)

## Contexto

O CSS pede Inter e Georgia, mas nenhuma fonte é carregada: cada leitor vê o portal na fonte do próprio sistema (UX-01, VIS-06). Os títulos pulam níveis e têm tamanhos trocados, como um `h2` de 14,7 px ao lado de um `h2` de 35 px (UX-02). A página Indicador tem três estilos de botão para a mesma ação, baixar (UX-06), e quatro fundos diferentes, um deles o azul da nota padrão do Starlight, fora da paleta (UX-08). A home tem cores escritas direto no CSS, que não acompanham a troca de tema.

## Decisão

- **Fontes:** um par de fontes (uma para texto, uma para títulos de destaque) com licença aberta, com os arquivos servidos pelo próprio site com `@font-face` (a regra de CSS que carrega uma fonte a partir de um arquivo). Fontes não carregadas saem da pilha do CSS. A fonte ainda não foi escolhida: o mantenedor escolhe entre as opções abaixo, todas com licença SIL Open Font License, depois de conferir os acentos do português e o peso dos arquivos.
  - Inter (texto) com Source Serif 4 (destaque);
  - IBM Plex Sans com IBM Plex Serif;
  - Atkinson Hyperlegible Next (texto) com Literata (destaque).
- **Escala tipográfica:** um tamanho por nível de título, de `h1` a `h5`, definido uma vez nas variáveis de tamanho do Starlight. Cartão não usa elemento de título fora da ordem; componentes recebem o nível como propriedade. Os valores ficam para depois da escolha da fonte.
- **Fundos:** três, e só três: base, superfície e inverso.
- **Botões:** um par só em todo o portal, principal e secundário. A mesma ação tem sempre a mesma aparência.
- **Cores:** só como tokens (variáveis de CSS com nome) declarados em `:root`, com os valores dos dois temas. Nenhuma cor escrita direto fora dos tokens.
- **Avisos do Starlight** (`note`, `tip`, `caution`, `danger`) recoloridos pelos tokens, sem `!important`.

## Alternativas consideradas

- **Só a fonte do sistema, sem `@font-face`:** zero arquivos novos, mas a identidade continua diferente em cada sistema (UX-01).
- **Uma fonte só, sem serifa** (opção aberta em UX-01): mais simples; a proposta prefere o par para manter o destaque editorial que o portal já tenta ter.
- **Carregar as fontes de um serviço externo** (levantada na redação do ADR): cada visita faria uma requisição a terceiros, com custo de privacidade e uma dependência a mais.
- **Manter os fundos e o azul padrão do Starlight:** a nota azul continua quebrando a identidade.

## Consequências

- **Positivas:** o portal fica igual para todo leitor; títulos certos ajudam leitor de tela, sumário, busca e cortes para RAG (I-17).
- **Negativas:** arquivos de fonte aumentam o peso da página; o desempenho (hoje sem nenhuma falha) precisa ser medido de novo.
- **Fases afetadas:** F0 (este ADR e a captura de referência em `auditoria/evidencias-ui/`); F1 (nota azul recolorida, títulos por nível, `h1` da home, contraste do texto secundário, UX-09); F5 (tokens, quatro primitivas, checklist visual por PR).
- **Breaking:** nenhum para os modelos. Muda só a aparência do portal.
