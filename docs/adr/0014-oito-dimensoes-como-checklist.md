# 0014. Oito dimensões como checklist de revisão

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 13; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-07

## Contexto

As oito dimensões (significado, contexto, objetivo, regras, exceções, responsabilidade, evidência e vigência) aparecem em várias páginas e componentes, às vezes com definições diferentes (EDI-12). Nas páginas e componentes que ainda não declaram a convenção, elas aparecem como base do método, sem dizer que são uma convenção do próprio Contexto: `src/content/docs/index.mdx` (linha 26), `src/content/docs/metodo/visao-geral.mdx` (linha 18), `src/content/docs/validacao/checklist.mdx` (linha 19), `src/components/ReadinessChecklist.astro` (linha 3) e `src/components/ReviewStages.astro` (linha 11). A página `src/content/docs/metodo/oito-dimensoes.mdx` já diz que é um roteiro autoral, mas não usa a palavra convenção. Escopo, vigência e responsável também não aparecem do mesmo jeito no cabeçalho de todos os modelos (MOD-05). Esta é uma decisão nova, vinda das pesquisas externas (I-07).

## Decisão

- As oito dimensões viram um **checklist de revisão**: uma lista para conferir um documento antes de aprovar.
- O checklist é marcado como **convenção do Contexto**, e não como norma ou resultado de pesquisa.
- **Escopo, vigência, evidência e responsável** viram metadados comuns no cabeçalho de todo documento, de qualquer tipo.
- Os nomes dos campos desses quatro metadados seguem [0015](./0015-chaves-em-ingles-rotulos-em-portugues.md) e ficam definidos na F3.

## Alternativas consideradas

- **Manter as oito dimensões como estrutura dos modelos:** obriga todo documento a ter oito seções, mesmo quando uma não se aplica.
- **Tirar as oito dimensões do portal** (levantada na redação do ADR): perderia uma ferramenta útil de revisão que já está nas páginas e no componente ReadinessChecklist.

## Consequências

- **Positivas:** fundamentação honesta (convenção declarada, I-03); os quatro metadados comuns respondem às perguntas que toda IA precisa fazer.
- **Negativas:** as páginas e componentes listados no Contexto precisam ser reescritos para declarar a convenção.
- **Fases afetadas:** F2 (as dimensões passam a vir de um arquivo só, e o checklist entra na etapa "Descubra o que falta", I-07, I-08); F3 (cabeçalho comum no schema 1.0).
- **Breaking:** o cabeçalho comum acrescenta campos obrigatórios. Entra com o schema 1.0.
