# 0019. Par de exemplos com lacunas e completo

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decidido por:** mantenedor (texto proposto pela auditoria (F1); aceito pelo [ADR 0030](./0030-decisoes-do-mantenedor-depois-das-fases.md))
- **Origem:** [04-modelos-e-exemplos.md](../../auditoria/04-modelos-e-exemplos.md), MOD-11 e AUR-09; [08-pesquisa-boas-praticas.md](../../auditoria/08-pesquisa-boas-praticas.md), seção sobre exemplos trabalhados (par "Decisão própria"); linha 57 de [referencias/index.mdx](../../src/content/docs/referencias/index.mdx)

## Contexto

Cada tipo de modelo publica dois exemplos: um com lacunas e um completo e aprovado. A página de referências registra esse par como "decisão própria". Os exemplos com lacunas usam o estado `pending_approval` com quem aprova vazio, o que contradiz a regra de campos obrigatórios e a definição de pendente de aprovação (MOD-11). O par precisa de uma decisão que diga qual é o estado do exemplo com lacunas e o que o completo ensina.

## Decisão

Cada tipo mantém o par de exemplos, com o mesmo `id`, que são o mesmo documento em momentos diferentes:

- **Exemplo com lacunas** (`exemplo-<tipo>-lacunas.yaml`): status `draft`, com as lacunas marcadas como `null` e as perguntas em aberto escritas explicitamente.
- **Exemplo completo** (`exemplo-<tipo>-completo.yaml`): status `approved`, sem perguntas em aberto, com histórico de pelo menos duas versões e o aviso de que a organização é inventada na primeira linha do arquivo, como o contrato editorial já prevê.

A página mostra o exemplo com lacunas antes do completo.

## Alternativas consideradas

- **Alternativa A:** publicar só o exemplo com lacunas. Não foi escolhida: o leitor não vê o destino do documento.
- **Alternativa B:** publicar só o exemplo completo. Não foi escolhida: ensina um documento pronto e aprovado e aumenta o risco de cópia sem revisão.
- **Alternativa C:** manter o exemplo com lacunas em `pending_approval`. Não foi escolhida: contradiz a definição do estado, que vale para documento estruturado que só espera confirmação (MOD-11).

## Consequências

- **Positivas:** o leitor vê o ponto de partida e o destino, e a regra de estado fica coerente com os exemplos.
- **Negativas:** há duas versões de cada tipo para manter. O exemplo completo continua sendo algo que alguém pode copiar; o aviso da Aurora reduz o risco, sem eliminá-lo.
- **Fases afetadas:** F1 muda o estado dos exemplos com lacunas. F5 reorganiza a sequência didática das páginas de tipo.
- **Breaking:** em escala pequena. O campo `status` do exemplo com lacunas muda de `pending_approval` para `draft`. Quem copiou o arquivo deve trocar o campo. O modelo em branco não muda.
