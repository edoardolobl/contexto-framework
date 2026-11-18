# 0029. Agentes e prova

- **Estado:** Proposto
- **Data:** 2026-11-17
- **Proposto por:** F7 (fase Agentes e prova; quando aceito, vira "**Decidido por:** mantenedor")
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F7, seção 4 (riscos: instruções para IA que envelhecem ou são lidas como garantia) e regra de desacoplamento; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-29 a I-31 e I-10; [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 9 (ADR 0010); [ADR 0021](./0021-responder-esclarecer-ou-abster-se.md), [ADR 0025](./0025-instrucao-minima-ao-agente.md) e [ADR 0028](./0028-saidas-para-maquinas.md)

## Contexto

A F6 entregou o kit mínimo para agentes, com o AGENTS.md, o glossário, os contratos e uma Skill. A F7 completa o que falta para o uso real: Skills para descobrir e consultar conhecimento, um caminho de entrada para quem trabalha em planilha, um ciclo para manter os documentos depois de publicados e a prova com pessoas que dá o portão da v1.0 (MET-16). Instruções para IA envelhecem e podem ser lidas como garantia; por isso cada adaptador precisa dizer para que versão foi escrito e de que não garante o comportamento do agente.

## Decisão

1. **Skills como adaptadores descartáveis.** As Skills seguem o formato Agent Skills (uma pasta com `SKILL.md`). O texto é escrito à mão em `src/kit/skills/<nome>/`, com arquivos estáticos opcionais na mesma pasta. Cada `SKILL.md` traz a ressalva de que a Skill orienta, mas não garante o comportamento do agente, e a linha `Versão alvo:`. O `scripts/kit.py` confere as duas coisas e falha se faltarem.
2. **`contexto-elicitar` devolve só rascunho.** A Skill descobre conhecimento com a pessoa e devolve um rascunho com as lacunas em `open_questions`. Ela nunca inventa responsável, aprovação, fórmula ou vigência, e não marca nada como aprovado.
3. **`contexto-consultar` segue o ADR 0021.** A Skill responde, esclarece ou abstém-se, como define o ADR 0021. Ela não antecipa as correções que o protocolo de onboarding ainda pede ao kit; essas correções passam pelo ciclo da decisão 5.
4. **Plano de mensuração em planilha.** O plano entra como CSV com separador `;` e BOM, com uma linha por evento e operação. A conversão gera um rascunho no formato do Contexto. Célula vazia vira pergunta em aberto, nunca um valor presumido.
5. **Manutenção a partir do uso.** Quando a IA erra uma pergunta do gabarito, o erro vira uma pergunta em aberto proposta num relatório, ligada ao documento correspondente (I-29). O script que gera o relatório não altera documento. A correção só entra numa versão nova, que passa pela aprovação de quem tem a palavra final. O ciclo é usar, detectar, corrigir, validar e republicar. Ele completa a revisão por calendário (`review_interval`) e não a substitui.
6. **Deriva só como nota.** A comparação dos documentos com o warehouse e o contêiner GTM (I-30) fica em `docs/design/deriva.md` como nota de design, depois da v1.0. Nada é implementado nesta fase.
7. **MCP continua nota.** `docs/design/mcp.md` segue sem código. Implementar o servidor fica para depois da v1.0. A reconferência da versão do protocolo fica como pergunta em aberto do mantenedor.
8. **Portão da v1.0.** A v1.0 só sai depois de um piloto com 2 ou 3 pessoas reproduzindo os casos 1 e 2, antes e depois de usar o Contexto. O piloto fica registrado em `docs/piloto/` e é citável. O protocolo está em `docs/piloto/README.md`.

## Alternativas consideradas

- **Skill gerada a partir dos documentos:** não foi escolhida. O texto da Skill precisa de julgamento sobre o que o agente deve fazer, e um gerador o transformaria em lista de campos. Fica para depois, se o formato se mostrar estável.
- **Skill que aprova ou calcula sem perguntar:** não foi escolhida. Contraria a regra 5 do contrato editorial e o ADR 0021.
- **Correção automática do documento pelo script de erros:** não foi escolhida. Um erro do gabarito pode ser um erro da IA ou do gabarito, e só quem aprova decide qual.
- **Implementar o servidor MCP agora:** não foi escolhida. O protocolo muda em semanas, e a v1.0 não depende dele.
- **Piloto só com revisão de especialistas:** não foi escolhida. Não mede se a pessoa aprende nem se o documento muda a resposta da IA (ADR 0010).

## Consequências

- **Positivas:** cada adaptador declara a versão para a qual foi escrito e pode ser trocado sem mudar o núcleo. A manutenção tem um caminho registrado. O portão da v1.0 tem protocolo e pode ser citado.
- **Negativas:** o ciclo de manutenção depende de alguém usar a IA e registrar os erros. O piloto custa tempo do mantenedor e exige cuidado com dados pessoais. As Skills orientam, mas não garantem o comportamento do agente.
- **Fases afetadas:** F7 (as Skills, o CSV de planilha, o ciclo de manutenção, a nota de deriva, a nota de MCP e o piloto). O portão da v1.0 depende do piloto registrado.
- **Breaking:** nenhum. Os documentos, o schema e os identificadores não mudam. O núcleo continua sem campo de protocolo (ADR 0025).
