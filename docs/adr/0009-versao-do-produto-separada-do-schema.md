# 0009. Versão do produto separada da versão do schema

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 8

## Contexto

O projeto não segue a regra de versão que ensina: package.json diz 0.4.0, o README fala em v0.4 e o contrato editorial em 0.3 (EDI-19, MET-13). As regras de versão dos documentos também têm tensões internas (MET-08). Uma mesma numeração para o site e para o formato dos modelos mistura duas coisas que mudam em ritmos diferentes. Schema é a descrição formal dos campos de um tipo de modelo.

## Decisão

- **Versão do produto:** a do site e do repositório. Fica em `package.json`, README, página inicial e CHANGELOG (registro de mudanças no formato Keep a Changelog), que devem dizer a mesma versão. `scripts/check_higiene.py` confere essa igualdade.
- **Versão de documento:** cada documento governado, inclusive o contrato editorial, tem versão própria, registrada no próprio texto. Essa versão não entra na conferência do produto.
- **Versão do schema:** a do formato dos modelos, no campo `schema_version` de cada modelo.
- As três numerações são independentes.
- A migração para Markdown com frontmatter ([0006](./0006-markdown-com-frontmatter-como-fonte-unica.md)) é o **schema 1.0**, marcado como Breaking no CHANGELOG.
- O número da próxima versão do produto e a regra exata de MAJOR, MINOR e PATCH para o schema ficam em aberto.

## Alternativas consideradas

- **Uma numeração só para produto e modelos:** uma correção de texto no site mudaria a versão dos modelos, e vice-versa.
- **Manter `template_version` como nome do campo** (termo usado em [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), seção 3, pergunta 8): a decisão usa `schema_version`, que diz o que o número versiona.

## Consequências

- **Positivas:** quem baixou um modelo sabe em que formato ele está; o site pode evoluir sem mexer nos modelos.
- **Negativas:** duas numerações para manter e explicar.
- **Fases afetadas:** F0 (versão do produto igual em package.json, README, página inicial e CHANGELOG; o contrato passa a ter versão própria de documento); F3 (`schema_version` e schema 1.0).
- **Breaking:** o schema 1.0 é Breaking. Modelos 0.x ficam em `historico/`, com tabela de migração de campos.
