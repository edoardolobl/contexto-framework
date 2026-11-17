# Decisões do mantenedor

Data: 2026-11-17 · Commit: d08c810 · Escopo: respostas às 11 decisões da seção 3 de [10-direcao-proposta.md](./10-direcao-proposta.md) e o que elas mudam no roteiro

> Registro de decisões. Nenhum arquivo do portal foi alterado. Cada decisão deve virar um ADR datado na fase F0.

## Resumo

- Nove decisões seguem a recomendação do juiz. Duas divergem: o nome "Framework" fica, e o formato canônico passa a ser Markdown com frontmatter.
- Três decisões novas (12 a 14) vieram das pesquisas externas registradas em [12-incorporacoes.md](./12-incorporacoes.md).
- O produto prioriza dados e mensuração. Rubrica sai do núcleo.
- A migração para Markdown com frontmatter vira o schema 1.0, marcado como Breaking, com versão de produto e versão de schema separadas.
- Há acesso a 15 pessoas ou mais, então F2 (card sorting e tree test) e o portão da v1.0 têm critério de saída viável.

## Decisões

| # | Tema | Decisão | Segue o juiz? |
|---|---|---|---|
| 1 | Foco | Dados e mensuração são o trilho principal. Conceito, Política, Processo e Decisão ficam como apoio aos casos de analytics (MOD-22). | Sim |
| 2 | Rubrica | Sai do núcleo e vira trilha complementar, por exemplo para avaliar respostas da IA (NAV-16, EDI-20). | Sim |
| 3 | Papéis | Mantém `owner` e `approver`, com tabela de equivalência para DAMA e catálogos (steward). | Sim |
| 4 | Estado | Um eixo só: `draft`, `pending_approval`, `approved`, `superseded`, `deprecated`. | Sim |
| 5 | Formato canônico | **Markdown com frontmatter** como fonte única; o YAML passa a ser gerado. | **Não** (o juiz recomendava manter o par .md + .yaml por enquanto) |
| 6 | Tipo de perguntas | Fusão com o gabarito sob o nome **Perguntas de negócio**, slug `templates/perguntas-de-negocio`, com redirecionamento de `templates/casos-teste`. | Sim |
| 7 | Identidade | **Mantém "Framework"** no nome. | **Não** (o juiz recomendava "guia e método") |
| 8 | Versão | Versão do produto (package.json, CHANGELOG) separada de `schema_version` dos modelos. A migração para frontmatter é o schema 1.0. | Sim |
| 9 | Validação com pessoas | Acesso a 15 pessoas ou mais para card sorting e tree test, e a 2 ou 3 para o piloto. | n/a |
| 10 | Domínio próprio | Adiado. Fica no GitHub Pages; protocolos com `/.well-known` (UCP, Poppy) seguem em "monitorar". | Sim |
| 11 | Exemplos | Nomes plausíveis de produção (projeto BigQuery, catálogo Databricks, propriedade GA4, contêiner GTM, operações BR e MX, eventos GA4 reais), com aviso de ficção em todos os formatos, inclusive .sql (AUR-21). | Sim |
| 12 | Núcleo de entrada | Cinco tipos na porta de entrada: Indicador, Dataset com relacionamentos, Evento de coleta, Regra e decisão (inclui detecção de anomalia) e Perguntas de negócio. Conceito, Política, Processo e Dashboard no segundo nível; Rubrica na trilha complementar. | Nova (das pesquisas externas, ver [12-incorporacoes.md](./12-incorporacoes.md)) |
| 13 | Oito dimensões | Viram checklist de revisão, marcado como convenção do Contexto. Escopo, vigência, evidência e responsável viram metadados comuns no cabeçalho de todo documento. | Nova |
| 14 | Língua dos campos | Chaves em inglês, iguais às do ODCS 3.2.0 onde houver equivalente; rótulos e explicações em português no Markdown e no portal. | Nova |

## O que muda no roteiro por causa das divergências

### Markdown com frontmatter como fonte única (decisão 5)

O juiz tirou pontos da proposta "Consumo por IA" justamente por esse custo de migração. Com a decisão tomada, o roteiro se ajusta assim:

- **F3 (Schema 1.0) fica maior e mais importante.** Ela reescreve os 10 modelos, os 20 exemplos e os 2 arquivos de histórico para Markdown com frontmatter, valida o frontmatter com JSON Schema por tipo e gera o .yaml de download. O teste de paridade .md x .yaml deixa de ser necessário, porque há uma única fonte.
- **Componentes e validadores mudam junto.** Hoje [ExampleDoc.astro:16](../src/components/ExampleDoc.astro#L16) e [RevisionComparison.astro:12](../src/components/RevisionComparison.astro#L12) leem os .yaml de `public/downloads` no build, e os cinco scripts de `scripts/` validam os .yaml. Todos passam a ler o frontmatter, ou o .yaml gerado.
- **Risco para o público não técnico.** O frontmatter precisa de um núcleo curto, de cerca de 8 campos obrigatórios. Os blocos técnicos (`ai_instructions`, `expected_behavior`, consulta verificada) ficam opcionais e marcados "para quem é técnico". Isso vira critério de saída de F3.
- **Sugestão de ordem.** Fazer F3 antes de F4 (Evento de coleta) e de F5 (moldes), para que o tipo novo e os exemplos realistas já nasçam no formato final e não sejam escritos duas vezes.

### "Framework" no nome (decisão 7)

- O achado EDI-09 (identidade que oscila) continua valendo, mas a correção muda: usar **o mesmo nome em todo lugar** (README, home, contrato, `<title>`), com uma linha de apoio em linguagem simples logo abaixo, por exemplo "um guia para preparar o conhecimento do seu time para a IA".
- A promessa da seção 1.2 de [10-direcao-proposta.md](./10-direcao-proposta.md) continua valendo sem mudança.

## Próximo passo

F0: transformar estas 11 decisões em ADRs, criar `vocabulario.yaml` e `modelos.yaml`, unificar a versão do produto e condicionar o deploy aos validadores. Nada disso foi iniciado.
