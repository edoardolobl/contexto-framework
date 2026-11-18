# 0015. Chaves em inglês, rótulos em português

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 14; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-11

## Contexto

Os campos dos modelos têm nomes em inglês, sem um dicionário publicado em português (MOD-10), e textos visíveis do portal misturam termos em inglês (EDI-32). O ODCS 3.2.0 (Open Data Contract Standard, um padrão aberto para contratos de dados) já tem um bloco `context` para instruções a agentes de IA, com nomes de campos estáveis (I-11). Esta é uma decisão nova, vinda das pesquisas externas.

## Decisão

- **Chaves** (nomes dos campos no frontmatter e no YAML) ficam em inglês.
- Onde houver campo equivalente no ODCS 3.2.0, a chave é igual à do ODCS, por exemplo o bloco `context` com `instructions`, `verifiedStatements` e `constraints`, e `synonyms`.
- **Rótulos e explicações** ficam em português, no Markdown e no portal, seguindo o vocabulário do contrato editorial.
- A lista completa de equivalências com o ODCS fica em aberto até a F3.

## Alternativas consideradas

- **Chaves em português** (levantada na redação do ADR): mais fáceis para o público não técnico, mas afastam o Contexto dos padrões e ferramentas de dados, e mudariam todos os campos atuais.
- **Chaves em inglês com nomes próprios, sem seguir o ODCS** (levantada na redação do ADR): mantém os nomes atuais, mas perde o alinhamento com um padrão que agentes e catálogos já leem.

## Consequências

- **Positivas:** os documentos ficam legíveis por ferramentas que seguem o ODCS; o leitor vê só rótulos em português.
- **Negativas:** o ODCS usa `camelCase` (`verifiedStatements`) e os campos atuais usam `snake_case` (`valid_from`). A convenção de escrita para campos sem equivalente fica em aberto. Um dicionário de campos passa a ser obrigatório.
- **Fases afetadas:** F3 (chaves no schema 1.0, I-11, I-12, I-13); F6 (crosswalk documental com ODCS 3.2.0).
- **Breaking:** chaves renomeadas para seguir o ODCS quebram quem já usa os modelos. Entram com o schema 1.0 e a tabela de migração de campos.
