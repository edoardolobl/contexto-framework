# 0001. Registrar decisões em ADR

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), nota de abertura e "Próximo passo"; [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), seção 1.2 (enxerto da Governança) e fase F0

## Contexto

O portal justifica escolhas importantes com a linha "Decisão própria", sem data, sem alternativas e sem quem decidiu (por exemplo em `src/content/docs/referencias/index.mdx`, linhas 55 e 57). A pesquisa de boas práticas recomenda registros de decisão numerados (PV-12). A auditoria deixou 14 decisões do mantenedor e duas propostas de interface que precisam de um lugar estável (I-04, [13-ui-ux-tasteskill.md](../../auditoria/13-ui-ux-tasteskill.md)). Um projeto que ensina versão e aprovação precisa praticar o mesmo com as próprias decisões.

## Decisão

- Toda decisão de produto, formato, vocabulário ou interface vira um ADR em `docs/adr/`, no formato descrito no [README](./README.md).
- Numeração sequencial de quatro dígitos. O 0000 é o modelo.
- Estados: Proposto, Aceito e Substituído por NNNN. Só o mantenedor muda um ADR para Aceito.
- ADR aceito não é editado. Uma mudança de rumo vira um ADR novo, e o antigo ganha o link para ele.
- As 14 decisões de 2026-11-17 viram os ADRs 0002 a 0015, na ordem de [11-decisoes.md](../../auditoria/11-decisoes.md).

Fica em aberto se os ADRs também aparecem no portal ou só no repositório.

## Alternativas consideradas

- **Manter as linhas "Decisão própria" no portal:** não dizem quando, por quê, nem o que foi descartado. Foi esse o problema que motivou o ADR.
- **Registrar só em [11-decisoes.md](../../auditoria/11-decisoes.md):** é uma tabela de respostas; não tem espaço para alternativas e consequências, e não aceita substituição de uma decisão isolada.
- **ADR só no repositório, sem decidir agora sobre o portal** (proposta Consumo por IA): adotado em parte; a publicação no portal fica em aberto.
- **Criar já o tipo de documento "Registro de decisão" para os times** (PV-12): é outro assunto, um modelo para o leitor; não foi decidido aqui.

## Consequências

- **Positivas:** cada escolha tem data, motivo e alternativas. Quem contribui sabe onde propor uma mudança.
- **Negativas:** mais um passo para o mantenedor, que precisa aceitar cada ADR.
- **Fases afetadas:** F0 (critério de saída "ADRs aprovados"); F1 (critério "zero linhas 'Decisão própria' sem ADR").
- **Breaking:** nenhum.
