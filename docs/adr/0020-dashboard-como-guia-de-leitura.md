# 0020. Dashboard como guia de leitura ligado ao indicador

- **Estado:** Proposto
- **Data:** 2026-11-17
- **Proposto por:** auditoria (F1)
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F1 (trocar as linhas "Decisão própria" por ADRs datados); linha 60 de [referencias/index.mdx](../../src/content/docs/referencias/index.mdx)

## Contexto

Um dashboard mostra números que alguém lê e usa para decidir, mas o modelo atual não deixa claro o que cada número mede nem como interpretar uma diferença em relação ao indicador oficial. A página de referências registra a interpretação de dashboards como "decisão própria", com a ligação entre dashboard e definição do indicador inspirada no dbt. Sem uma decisão registrada, a regra fica sem origem verificável (I-03).

## Decisão

O modelo de dashboard é um **guia de leitura**, não uma definição de cálculo. Cada dashboard:

1. referencia, pelo `id`, o indicador que mostra, e nunca redefine a fórmula dele;
2. informa a fonte e a data de atualização;
3. explica como ler cada número e o que fazer quando ele diverge do indicador oficial.

O dashboard continua no segundo nível de tipos, como decidido no ADR 0013.

Em aberto: o formato exato dos campos, que segue o modelo atual e a validação com pessoas prevista no ADR 0010.

## Alternativas consideradas

- **Alternativa A:** dashboard com fórmula própria. Não foi escolhida: duplica o indicador e tende a divergir dele.
- **Alternativa B:** não documentar dashboards. Não foi escolhida: perde a pergunta sobre o que um número significa na tela.
- **Alternativa C:** tratar o dashboard como indicador. Não foi escolhida: mistura dois tipos com responsabilidades diferentes.

## Consequências

- **Positivas:** uma diferença entre o dashboard e o indicador vira um caso explicado, em vez de uma dúvida silenciosa.
- **Negativas:** o guia depende de o indicador existir e de ter sido aprovado. Dashboard sem indicador fica com a lacuna registrada.
- **Fases afetadas:** F3 (campos do modelo) e F5 (moldes e sequência didática da página de dashboard).
- **Breaking:** nenhum. O modelo de dashboard já referencia o indicador; a decisão fixa como ler essa ligação.
