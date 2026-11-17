# 0018. Não resolver políticas conflitantes pela data

- **Estado:** Proposto
- **Data:** 2026-11-17
- **Proposto por:** auditoria (F1)
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F1 (trocar as linhas "Decisão própria" por ADRs datados); [07-metodo-e-credibilidade.md](../../auditoria/07-metodo-e-credibilidade.md), MET-05; linha 55 de [referencias/index.mdx](../../src/content/docs/referencias/index.mdx)

## Contexto

A tabela de rastreabilidade da página de referências diz que o Contexto não resolve políticas conflitantes pela data. A inspiração dessa regra aparece como "decisão própria", apoiada na ênfase de KCS em autoridade do conteúdo. Não havia decisão registrada que sustentasse a regra, e a citação a KCS não basta para justificá-la. A auditoria pede que toda convenção do Contexto aponte para um ADR (I-03, MET-05).

## Decisão

Quando duas políticas sobre o mesmo tema divergem, o portal não escolhe a mais recente pela data de publicação, de aprovação ou de vigência. O documento registra as fontes divergentes, quem aprova e a pergunta em aberto, no campo de fontes em conflito, com o estado `unresolved`, até que a autoridade identificada resolva o caso. A data continua registrada, mas não decide sozinha qual política vale.

Em aberto: se algum caso admite a data como critério, por exemplo quando a própria autoridade declara que uma política substitui a outra.

## Alternativas consideradas

- **Alternativa A:** escolher a política mais recente. Não foi escolhida: a data não mostra se a política foi aprovada nem por quem, e um rascunho recente venceria uma política aprovada.
- **Alternativa B:** escolher a política de quem tem mais cargo. Não foi escolhida: o portal não define hierarquia entre áreas, e cargos mudam.
- **Alternativa C:** deixar o agente escolher a política que parecer mais provável. Não foi escolhida: é inventar uma regra ausente, o que o contrato editorial proíbe (regra 5).

## Consequências

- **Positivas:** uma resposta de IA não vira definição oficial só porque o texto é mais novo, e os conflitos ficam visíveis.
- **Negativas:** documentos ficam com conflitos abertos por mais tempo, até a autoridade decidir.
- **Fases afetadas:** F1 troca a citação e a linha da tabela de referências. F5 recebe o campo de fontes em conflito nos moldes de política, decisão e processo.
- **Breaking:** nenhum. A regra orienta o preenchimento, e nenhum modelo publicado precisa mudar agora.
