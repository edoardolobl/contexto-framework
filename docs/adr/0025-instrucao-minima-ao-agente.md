# 0025. Instrução mínima ao agente

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decidido por:** mantenedor (texto proposto pela auditoria (F2); aceito pelo [ADR 0030](./0030-decisoes-do-mantenedor-depois-das-fases.md))
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), seção 1.5, item 5, e regra de desacoplamento; [08-pesquisa-boas-praticas.md](../../auditoria/08-pesquisa-boas-praticas.md), AG-05; relação com o [ADR 0021](./0021-responder-esclarecer-ou-abster-se.md)

## Contexto

O público usa a IA direto, em ferramentas como Claude Code, Codex ou NotebookLM, mas nenhuma página ensina onde colocar os arquivos nem como citá-los numa conversa (05-navegacao-e-ux.md). As regras que um agente precisa seguir estão só no contrato editorial, escrito para pessoas (AG-05). Um trecho de AGENTS.md dá ao agente a instrução mínima, sem colocar campo de protocolo no núcleo dos documentos.

## Decisão

- **Trecho para os times:** um trecho de AGENTS.md, com onde fica cada coisa (os documentos aprovados, as perguntas de negócio e o gabarito) e como o agente deve citar cada documento.
- **Duas regras:**
  1. Sem indicador aprovado, não calcula; pergunta.
  2. Usa só documento aprovado e cita id e versão.
- **Adaptador descartável:** o trecho declara a versão da ferramenta para a qual foi escrito e pode ser trocado sem mudar o núcleo. O núcleo (documentos, schema e IDs) não carrega nenhum campo de protocolo, conforme a regra de desacoplamento.
- **Fora desta fase:** os blocos `ai_instructions` nos modelos ficam para a F4.
- **Ressalva:** o trecho orienta o agente; não garante que ele siga as regras.

## Alternativas consideradas

- **Bloco `ai_instructions` já no núcleo:** colocaria instrução de agente dentro do documento, acoplado a um protocolo. Não foi escolhido nesta fase; fica para a F4, depois que a regra de desacoplamento estiver testada.
- **Só o contrato, sem trecho:** o agente lê regras escritas para pessoas e não tem como saber o que fazer quando falta um indicador aprovado (AG-05). Não foi escolhido.
- **Skill ou MCP agora:** os protocolos ainda estão em monitoramento (seção 2 da direção). Acoplaria o núcleo a um formato que pode mudar. Não foi escolhido.

## Consequências

- **Positivas:** o time tem uma regra pronta para colar no projeto, e o agente pergunta em vez de inventar um cálculo.
- **Negativas:** o trecho só funciona se a ferramenta lê o AGENTS.md; orienta, mas não garante o comportamento; precisa ser revisado quando o contrato mudar.
- **Fases afetadas:** F2 (guia "Leve à sua ferramenta de IA" com o trecho); F4 (blocos `ai_instructions` no núcleo).
- **Breaking:** nenhum. O trecho não muda o formato de nenhum modelo.
