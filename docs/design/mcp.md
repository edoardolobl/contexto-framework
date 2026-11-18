# Nota de design: o Contexto como servidor MCP

- **Estado:** nota de design, sem código. Implementar fica para depois da v1.0, decidido no [ADR 0029](../adr/0029-agentes-e-prova.md).
- **Data:** 2026-11-17
- **Fase:** F6 escreveu esta nota; F7 a manteve sem código ([ADR 0028](../adr/0028-saidas-para-maquinas.md) e [ADR 0029](../adr/0029-agentes-e-prova.md)). A reconferência da versão do protocolo é pergunta em aberto do mantenedor.
- **Versão alvo:** Model Context Protocol (MCP) 2026-07-28. Reconferir antes de qualquer implementação, porque as datas de protocolos mudam em semanas.
- **Origem:** [08-pesquisa-boas-praticas.md](../../auditoria/08-pesquisa-boas-praticas.md), AG-07; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-28; [ADR 0011](../adr/0011-adiar-dominio-proprio.md)

## Por que uma nota

Um servidor MCP poderia entregar os documentos aprovados a um agente sem que eles sejam copiados para o projeto dele. Esta nota registra o desenho para que a F7 comece de um ponto escrito. Nenhum servidor existe, e o portal não expõe nenhum endpoint.

## Resources: documentos somente leitura

- Cada documento aprovado é um resource somente leitura, identificado por uma URI no modelo contexto://, seguido do id, de arroba e da versão.
- O campo lastModified vem de version_date, a data da versão do documento, e não da data do arquivo.
- Documento que não está aprovado (rascunho, pendente de aprovação, substituído ou obsoleto) fica fora da listagem ou com prioridade baixa. A escolha entre as duas opções fica para a F7.
- Os campos audience e priority do resource indicam para quem o conteúdo serve e quanta prioridade ele tem. Eles seguem a especificação da revisão 2026-07-28.

## Tools: consultas e validações, só de leitura

- resolver_versao: recebe o id e uma data de referência e devolve a versão cuja vigência cobre a data. A vigência vai de valid_from até valid_to, sem incluir o dia de valid_to.
- validar_documento: confere um documento contra o schema publicado da versão de schema que ele declara. Não altera nada.
- Nenhuma tool escreve, aprova nem muda o estado de um documento.

## Prompts opcionais

Prompts são escolhidos pela pessoa, não pelo modelo. Podem reunir as perguntas de descoberta do método ou as perguntas marcadas como onboarding. Nenhum prompt está implementado.

## Regras de desacoplamento

- O núcleo (documentos, schema e identificadores) não tem nenhum campo de MCP. Essa regra vale em todas as fases ([10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), seção 2).
- O servidor seria um adaptador descartável. Se o protocolo mudar, troca-se a camada, e os documentos continuam iguais.
- Não há /.well-known nem domínio próprio. O endereço segue o do GitHub Pages até haver decisão nova ([ADR 0011](../adr/0011-adiar-dominio-proprio.md)).

## Fora desta nota

- Nenhum servidor, tool ou prompt implementado.
- Autenticação, cache e limites de uso ficam para depois da v1.0, se a nota virar projeto ([ADR 0029](../adr/0029-agentes-e-prova.md)).

## Fontes, com data

- Model Context Protocol, anúncio da revisão 2026-07-28, publicado em 28/07/2026: https://blog.modelcontextprotocol.io/posts/2026-07-28/
- Changelog da revisão 2026-07-28: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx
- Especificação de resources, revisão 2026-07-28: https://modelcontextprotocol.io/specification/2026-07-28/server/resources
- Especificação de prompts, revisão 2025-11-25: https://modelcontextprotocol.io/specification/2025-11-25/server/prompts
- Fontes registradas na pesquisa de 13/11/2026 ([08-pesquisa-boas-praticas.md](../../auditoria/08-pesquisa-boas-praticas.md), AG-07). Esta nota não reconferiu os endereços; a F7 faz essa conferência junto com a versão.
