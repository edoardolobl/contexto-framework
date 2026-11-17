# Registros de decisão (ADR)

Um ADR (Architecture Decision Record, ou registro de decisão de arquitetura) é um texto curto e numerado que registra uma única decisão do projeto: o problema, o que foi decidido, o que ficou de fora e o que muda por causa disso. Ele existe para que qualquer pessoa entenda, meses depois, por que o Contexto é como é, sem depender da memória de quem decidiu.

## Formato

Cada ADR é um arquivo Markdown nesta pasta, com o nome `NNNN-titulo-curto.md`: quatro dígitos e um título em português, minúsculo, sem acentos e com hífens.

O arquivo segue o [modelo](./0000-modelo.md):

- **Cabeçalho:** estado, data, quem decidiu (ou quem propôs) e a origem na auditoria.
- **Contexto:** o problema, em 2 a 5 frases, com os IDs dos achados que o motivaram.
- **Decisão:** o que foi decidido, de forma concreta.
- **Alternativas consideradas:** as outras opções e por que não foram escolhidas.
- **Consequências:** o que melhora, o que piora, quais fases (F0 a F7) mudam e se há mudança Breaking (que quebra quem já usa os modelos).

Estados possíveis:

- **Proposto:** escrito, ainda sem a palavra do mantenedor.
- **Aceito:** o mantenedor aprovou. A partir daí o texto não muda.
- **Substituído por NNNN:** uma decisão nova tomou o lugar desta. O ADR antigo fica na pasta, com o link para o novo.

## Como propor um ADR

1. Copie [0000-modelo.md](./0000-modelo.md) para um arquivo novo com o próximo número livre da tabela abaixo.
2. Preencha as seções. Use o vocabulário de [CONTRATO_EDITORIAL.md](../CONTRATO_EDITORIAL.md) (seção "Vocabulário").
3. Marque **Estado: Proposto** e escreva **Proposto por:** no lugar de "Decidido por".
4. Acrescente uma linha na tabela abaixo e abra um PR.
5. O mantenedor decide. Se aceitar, ele muda o estado para **Aceito**, troca "Proposto por" por "Decidido por" e atualiza a data.

Para mudar uma decisão aceita, escreva um ADR novo. Não edite o antigo: só marque nele "Substituído por NNNN".

## Índice

| Número | Título | Estado | Data |
|---|---|---|---|
| [0000](./0000-modelo.md) | Modelo de ADR | n/a | n/a |
| [0001](./0001-registrar-decisoes-em-adr.md) | Registrar decisões em ADR | Aceito | 2026-11-17 |
| [0002](./0002-dados-e-mensuracao-como-trilho-principal.md) | Dados e mensuração como trilho principal | Aceito | 2026-11-17 |
| [0003](./0003-rubrica-em-trilha-complementar.md) | Rubrica em trilha complementar | Aceito | 2026-11-17 |
| [0004](./0004-manter-owner-e-approver.md) | Manter `owner` e `approver` | Aceito | 2026-11-17 |
| [0005](./0005-um-eixo-de-estado.md) | Um eixo só de estado do documento | Aceito | 2026-11-17 |
| [0006](./0006-markdown-com-frontmatter-como-fonte-unica.md) | Markdown com frontmatter como fonte única | Aceito | 2026-11-17 |
| [0007](./0007-tipo-perguntas-de-negocio.md) | Tipo Perguntas de negócio | Aceito | 2026-11-17 |
| [0008](./0008-manter-framework-no-nome.md) | Manter "Framework" no nome | Aceito | 2026-11-17 |
| [0009](./0009-versao-do-produto-separada-do-schema.md) | Versão do produto separada da versão do schema | Aceito | 2026-11-17 |
| [0010](./0010-validacao-com-pessoas.md) | Validação com pessoas | Aceito | 2026-11-17 |
| [0011](./0011-adiar-dominio-proprio.md) | Adiar domínio próprio | Aceito | 2026-11-17 |
| [0012](./0012-exemplos-com-nomes-de-producao.md) | Exemplos com nomes plausíveis de produção | Aceito | 2026-11-17 |
| [0013](./0013-nucleo-de-entrada-com-cinco-tipos.md) | Núcleo de entrada com cinco tipos | Aceito | 2026-11-17 |
| [0014](./0014-oito-dimensoes-como-checklist.md) | Oito dimensões como checklist de revisão | Aceito | 2026-11-17 |
| [0015](./0015-chaves-em-ingles-rotulos-em-portugues.md) | Chaves em inglês, rótulos em português | Aceito | 2026-11-17 |
| [0016](./0016-sistema-visual.md) | Sistema visual | Aceito | 2026-11-17 |
| [0017](./0017-tamanho-de-pagina-de-modelo.md) | Tamanho de página de modelo | Aceito | 2026-11-17 |
| [0018](./0018-nao-resolver-politicas-conflitantes-por-data.md) | Não resolver políticas conflitantes pela data | Proposto | 2026-11-17 |
| [0019](./0019-par-de-exemplos-com-lacunas-e-completo.md) | Par de exemplos com lacunas e completo | Proposto | 2026-11-17 |
| [0020](./0020-dashboard-como-guia-de-leitura.md) | Dashboard como guia de leitura ligado ao indicador | Proposto | 2026-11-17 |
| [0021](./0021-responder-esclarecer-ou-abster-se.md) | Responder, esclarecer ou abster-se | Proposto | 2026-11-17 |
| [0022](./0022-laboratorio-pequeno-verificado-em-sqlite.md) | Laboratório pequeno verificado em SQLite, sem LLM | Proposto | 2026-11-17 |
| [0023](./0023-percurso-em-sete-passos.md) | Percurso em sete passos | Proposto | 2026-11-17 |
| [0024](./0024-descoberta-por-incidente.md) | Descoberta por incidente | Proposto | 2026-11-17 |
| [0025](./0025-instrucao-minima-ao-agente.md) | Instrução mínima ao agente | Proposto | 2026-11-17 |
| [0026](./0026-schema-1-0-e-fonte-unica.md) | Schema 1.0 e fonte única | Proposto | 2026-11-17 |
| [0027](./0027-evento-de-coleta-e-laboratorio-de-mensuracao.md) | Evento de coleta e laboratório de mensuração | Proposto | 2026-11-17 |
