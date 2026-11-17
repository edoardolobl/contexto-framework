# 0008. Manter "Framework" no nome

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 7 e seção "'Framework' no nome"

## Contexto

O projeto se apresenta ora como framework, ora como método, metodologia ou guia (EDI-09). O título da home é "Contexto: Framework de Conhecimento para IA". O juiz da auditoria recomendava tirar "Framework" e adotar "guia e método abertos". O mantenedor divergiu e manteve o nome. O problema que continua é a oscilação, não a palavra.

## Decisão

- "Framework" fica no nome do Contexto.
- O mesmo nome é usado em todo lugar: README, home, contrato editorial e `<title>` das páginas.
- Logo abaixo do nome entra uma linha de apoio em linguagem simples, por exemplo "um guia para preparar o conhecimento do seu time para a IA". O texto final está em aberto.
- A promessa da seção 1.2 de [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md) continua valendo sem mudança.

## Alternativas consideradas

- **Trocar por "guia e método abertos"** (recomendação do juiz e proposta Pedagogia): descreve melhor o produto para o público não técnico, mas muda um nome que já circula.
- **"Guia e padrão de documentação"** (proposta Governança): mesma troca de nome, com o peso extra de prometer um padrão.

## Consequências

- **Positivas:** o nome que já circula continua válido; a correção de EDI-09 é uniformizar, não renomear.
- **Negativas:** "Framework" pode soar técnico para parte do público; a linha de apoio precisa compensar.
- **Fases afetadas:** F0 (este ADR; o README já usa o nome completo); F1 (mesmo nome no `<title>` das páginas e no contrato editorial, EDI-09); F2 (`h1` da home com categoria e público, mantendo "Framework", UX-04).
- **Breaking:** nenhum.
