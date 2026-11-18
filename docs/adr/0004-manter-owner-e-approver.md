# 0004. Manter `owner` e `approver`

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 3

## Contexto

Os modelos usam `owner` (o responsável, cargo ou área que mantém o documento) e `approver` (quem aprova). A matriz de papéis do portal omite o responsável e usa a letra R com outro sentido (EDI-13, MET-10). As propostas avaliadas sugeriam renomear `owner` para `steward`, como no DAMA e nos catálogos de dados, ou para `maintainer`. Qualquer renomeação quebra quem já usa os modelos.

## Decisão

- Os campos continuam `owner` e `approver`.
- O portal ganha uma tabela de equivalência com o DAMA e os catálogos de dados, em que `owner` corresponde ao papel de steward.
- Os rótulos em português seguem o contrato: "responsável" e "quem aprova".
- O conteúdo completo da tabela de equivalência e a página onde ela fica estão em aberto.

## Alternativas consideradas

- **Renomear para `steward` e `approver`** (proposta Consumo por IA): alinha com o DAMA, mas é Breaking e usa um termo pouco conhecido do público não técnico.
- **Renomear para `maintainer` e `approver`** (proposta Governança): também é Breaking, sem ganho de alinhamento com padrão externo.

## Consequências

- **Positivas:** ninguém precisa migrar campos de papel. Quem vem do DAMA ou de um catálogo encontra a correspondência na tabela.
- **Negativas:** o nome do campo não é o do padrão de mercado; a tabela de equivalência precisa ser mantida.
- **Fases afetadas:** F1 (tabela de papéis corrigida, EDI-13 e MET-10); F3 (`owner` e `approver` no cabeçalho comum do schema 1.0); F6 (crosswalk com ODCS e catálogos).
- **Breaking:** nenhum.
