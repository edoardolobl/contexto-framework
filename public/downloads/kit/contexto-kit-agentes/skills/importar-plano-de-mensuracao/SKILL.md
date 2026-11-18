---
name: importar-plano-de-mensuracao
description: "Use esta Skill quando a pessoa entregar um plano de mensuração em planilha (CSV do Excel ou do Google Planilhas) e quiser transformá-lo em documentos de Evento de coleta. Ela confere as colunas, converte cada evento em um rascunho que valida no schema evento-coleta 1.1.0, devolve os erros por linha sem corrigir a planilha e entrega os rascunhos com a lista de perguntas em aberto para quem responde pelo evento. Célula vazia vira pergunta em aberto, nunca palpite, e nada sai aprovado: o estado é sempre draft. Não use para aprovar documento nem para responder perguntas sobre dados."
license: CC-BY-4.0
---

# Importar plano de mensuração: da planilha ao rascunho

Versão alvo: especificação Agent Skills, conferida em 17/11/2026. Licença: CC BY 4.0.

Esta Skill orienta o agente. Ela não garante o comportamento dele.

## Arquivos

- `references/colunas.md`: as 20 colunas da planilha, o campo de cada uma, o nível (evento ou operação), como preencher e o que acontece com a célula vazia.
- `references/EVENT-AURORA-GENERATE-LEAD@1.1.md`: um Evento de coleta completo e aprovado, como exemplo do documento que o rascunho deve virar depois da revisão.

O gerador copia o exemplo do kit para a pasta `references/`.

O modelo da planilha não vai no kit. Baixe pelo endereço publicado: https://edoardolobl.github.io/contexto-framework/downloads/plano-de-mensuracao-modelo.csv

## Passos

1. **Confira as colunas.** Compare o cabeçalho da planilha com `references/colunas.md`. Coluna que falta é erro; coluna desconhecida é ignorada com aviso. Se a planilha não segue o modelo, devolva a diferença à pessoa.
2. **Converta com o script, se houver.** Se o agente está numa cópia do repositório do Contexto, rode `python3 scripts/planilha_para_evento.py PLANILHA.csv --saida PASTA`. Use `--data AAAA-MM-DD` para fixar a data e `--substituir` só se a pessoa pediu para trocar arquivos existentes.
3. **Leia os erros por linha e devolva-os à pessoa.** Cada erro cita o arquivo e a linha do CSV. Não corrija a planilha por conta própria, nem adivinhe o valor certo. Peça a correção e rode de novo.
4. **Sem o script, converta à mão.** Siga `references/colunas.md`, monte um rascunho por evento e valide o frontmatter no schema publicado do evento-coleta 1.1.0: https://edoardolobl.github.io/contexto-framework/schemas/1.1.0/evento-coleta.schema.json. Use o exemplo em `references/EVENT-AURORA-GENERATE-LEAD@1.1.md` para ver a forma de um documento completo.
5. **Entregue os rascunhos e as perguntas em aberto.** Passe cada rascunho e a lista de perguntas em aberto a quem responde pelo evento. Diga que o próximo passo é revisar com essa pessoa. A aprovação é decisão dela.

## Regras que não mudam

- Nunca preencha uma célula vazia: ela vira uma pergunta em aberto, com estado unresolved.
- Nunca preencha quem aprova, a vigência nem a aprovação (approver, valid_from, valid_to, approved_by).
- O estado do rascunho é sempre draft. Rascunho não vale como regra.
- Todo rascunho leva a pergunta "Quem aprova o documento do evento X?".
- Não invente identificador, gatilho, fuso nem tolerância ao silêncio.
