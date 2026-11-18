# 0022. Laboratório pequeno verificado em SQLite, sem LLM

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decidido por:** mantenedor (texto proposto pela auditoria (F1); aceito pelo [ADR 0030](./0030-decisoes-do-mantenedor-depois-das-fases.md))
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), laboratório Aurora 1 e fase F4; linha 63 de [referencias/index.mdx](../../src/content/docs/referencias/index.mdx)

## Contexto

O portal mostra um número que qualquer pessoa pode reproduzir: na amostra da Aurora, a consulta de referência retorna 25%, e a contagem por pedidos retorna 50% para outra medida. A página de referências trata o laboratório como um caso pequeno testado sem LLM. Sem decisão registrada, o laboratório pode crescer com um modelo no teste e perder a verificação por máquina.

## Decisão

Os laboratórios do portal usam uma amostra pequena em SQLite, com a consulta de referência. O validador recalcula o número (hoje 25%, com 1 de 4 sessões elegíveis), confere o texto da página e não chama nenhum LLM.

O teste verifica a conta nesses registros e nessa consulta. Ele não verifica se um modelo interpreta bem uma pergunta de produção, e a página diz isso ao leitor.

Em aberto: o tamanho máximo do laboratório. A fase F4 fixa um limite de escopo para o Lab 2.

## Alternativas consideradas

- **Alternativa A:** avaliar as respostas com um LLM como juiz. Não foi escolhida: o resultado deixa de ser reproduzível, e o preprint criticado pelo portal usou um juiz da mesma família dos modelos testados.
- **Alternativa B:** usar um banco de dados grande. Não foi escolhida: desloca o foco do portal para a engenharia de dados.
- **Alternativa C:** mostrar só o texto, sem número verificado. Não foi escolhida: perde a prova de que a conta confere com os registros.

## Consequências

- **Positivas:** o número é reproduzível e o validador acusa qualquer divergência entre o texto e a consulta.
- **Negativas:** a amostra não prova generalização. Ela mostra a diferença entre duas definições, não a taxa de acerto de um sistema.
- **Fases afetadas:** F4, com o Lab 2 recalculado em SQLite e o limite fixo de escopo.
- **Breaking:** nenhum.
