# 0011. Adiar domínio próprio

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 10

## Contexto

O portal é publicado no GitHub Pages, num endereço do GitHub. Alguns protocolos novos para agentes de IA (UCP e Poppy) exigem arquivos em `/.well-known`, uma pasta na raiz de um domínio próprio. A pesquisa recomendou decidir sobre o domínio antes de qualquer recurso desse tipo (AG-11). Esses protocolos têm dias ou semanas de vida.

## Decisão

- O domínio próprio fica adiado. O portal continua no GitHub Pages.
- UCP e Poppy, e qualquer protocolo que dependa de `/.well-known`, seguem na lista "monitorar".
- Quando o tema volta à pauta fica em aberto.

## Alternativas consideradas

- **Registrar um domínio agora:** custo e manutenção para servir protocolos que ainda podem mudar ou sumir.
- **Pôr o domínio no roadmap com data:** criaria um compromisso sem um uso real que o justifique.

## Consequências

- **Positivas:** nenhum custo novo; o núcleo continua sem campos de protocolo, como pede a regra de desacoplamento.
- **Negativas:** URLs ficam presas ao endereço do GitHub; uma mudança futura de domínio vai pedir redirecionamentos.
- **Fases afetadas:** F6 (saídas para máquinas sem `/.well-known`; datas dos protocolos reconferidas no início da fase); F7 (MCP só como nota de design, I-28).
- **Breaking:** nenhum.
