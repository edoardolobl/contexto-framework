# 0006. Markdown com frontmatter como fonte única

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 5 e seção "Markdown com frontmatter como fonte única"

## Contexto

Cada modelo existe hoje em dois arquivos escritos à mão, um .md para pessoas e um .yaml para máquinas, e os dois já divergem (MOD-04, TEC-18). O juiz da auditoria recomendava manter o par por enquanto, com um teste automático de paridade (que confere se os dois dizem o mesmo). O mantenedor divergiu e escolheu uma fonte só. Frontmatter é o bloco de campos no topo de um arquivo Markdown, entre duas linhas `---`.

## Decisão

- O formato canônico de modelos e exemplos é **Markdown com frontmatter**. É a única fonte escrita à mão.
- O .yaml de download passa a ser gerado a partir dela.
- O frontmatter é validado com JSON Schema por tipo (um arquivo que descreve os campos permitidos e obrigatórios).
- O núcleo obrigatório do frontmatter é curto, de cerca de 8 campos. Blocos técnicos (`ai_instructions`, `expected_behavior`, consulta verificada) são opcionais e marcados "para quem é técnico".
- A lista exata dos campos do núcleo fica em aberto até a F3.

## Alternativas consideradas

- **Manter o par .md e .yaml com teste de paridade** (recomendação do juiz e da proposta Governança): custo de migração menor agora, mas mantém duas cópias e o risco de divergência que já aconteceu.
- **Migrar já na primeira fase com "zero cópias à mão"** (proposta Consumo por IA): reescreveria tudo antes de o público ver algum ganho. A decisão adota o formato, mas na F3.

## Consequências

- **Positivas:** uma fonte por documento; o teste de paridade deixa de ser necessário.
- **Negativas:** a F3 fica maior: reescreve 10 modelos, 20 exemplos e 2 arquivos de histórico. Exige um gerador de .yaml, ferramenta a mais para um mantenedor sozinho. Frontmatter longo pode afastar o público não técnico.
- **Fases afetadas:** F3 (migração, schema por tipo, critério de saída do núcleo curto); F4 e F5 depois da F3, para que Evento de coleta e moldes nasçam no formato final. `ExampleDoc.astro`, `RevisionComparison.astro` e os validadores de `scripts/` passam a ler o frontmatter ou o .yaml gerado. Ligações: I-13, I-31.
- **Breaking:** sim. É o schema 1.0 ([0009](./0009-versao-do-produto-separada-do-schema.md)). Modelos 0.x ficam preservados e há tabela de migração de campos.
