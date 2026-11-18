# Instruções para quem contribui com o Contexto

Este arquivo orienta agentes de IA e pessoas que editam este repositório. O AGENTS.md que vai para os times, no kit para agentes, fica em `src/kit/AGENTS.md`. Os dois não se misturam.

## O que é o repositório

O Contexto é um guia e método para transformar perguntas de negócio em documentos aprovados e versionados. O repositório tem o portal (Astro e Starlight), os modelos, os exemplos, os laboratórios em SQLite e os validadores em Python. A versão do produto fica em `package.json`. O contrato editorial está em `docs/CONTRATO_EDITORIAL.md`, e as decisões, em `docs/adr/`.

## Onde fica cada coisa

Fontes editáveis, à mão:

- `src/modelos/`: um Markdown por tipo de documento, fonte dos modelos.
- `src/exemplos/`: exemplos com lacunas e exemplos completos, em Markdown com frontmatter.
- `src/data/`: listas e regras que os scripts e o portal leem, como `vocabulario.yaml`, `campos.yaml` e `modelos.yaml`.
- `src/kit/`: fonte do kit para agentes (`kit.yaml`, o AGENTS.md do kit e `skills/`).
- `src/content/docs/`: páginas do portal.
- `schemas/`: JSON Schema por tipo, na versão 1.1.0. `schemas/historico/1.0.0/` guarda a versão anterior.
- `docs/`: contrato, ADRs, roadmap, notas de design e protocolos de experimento. `docs/piloto/` tem o kit do piloto com pessoas, que é o portão da v1.0: roteiro, tarefas, ficha do especialista, termo, folha de registro, pontuação e resultados. Essa pasta não guarda dado pessoal.
- `scripts/`: validadores e geradores em Python. Os testes ficam em `scripts/tests/`. Duas ferramentas de uso manual não rodam no `npm run check`: `scripts/planilha_para_evento.py`, que converte o plano de mensuração de uma planilha, e `scripts/erros_para_perguntas.py`, que gera o relatório de erros do teste com as perguntas e não altera documento.
- `auditoria/`: registro histórico da auditoria. Não altere.

Gerados, que não se editam à mão (o CI falha se saírem de sincronia com as fontes):

- `public/downloads/`: `template-*.md`, `template-*.yaml`, `exemplo-*.yaml` e `historico/`, pelo `npm run gerar:downloads`. Os `.sql` e o `roteiro-revisao-documental.md` são à mão.
- `public/documentos/`, `public/schemas/`, `public/downloads/kit/` e `public/llms.txt`, pelo `npm run gerar:saidas`.
- `src/content/docs/referencias/campos/`, pelo `npm run gerar:referencias`.

## Comandos

- `npm run test:scripts`: testes dos validadores, em pytest e em node --test.
- `npm run check:content`: confere o conteúdo e os arquivos gerados, sem build.
- `npm run check`: tudo, com build, links e checklist visual. Demora; o CI roda.
- `npm run gerar:downloads`, `npm run gerar:referencias` e `npm run gerar:saidas`: regeneram os arquivos gerados depois de uma mudança na fonte.
- `npm run dev`: portal em modo de desenvolvimento.

## Regras

1. Lógica nova em `scripts/` entra por teste antes: escreva o teste em `scripts/tests/`, veja falhar e só então implemente.
2. Mudança de regra editorial muda `docs/CONTRATO_EDITORIAL.md` junto, com nova linha na tabela de versões.
3. Use o vocabulário. Cada ideia tem um termo só, na tabela "Vocabulário" do contrato e em `src/data/vocabulario.yaml`. O validador recusa as formas proibidas, inclusive em páginas e downloads.
4. Nada de travessão (U+2014) nem de meia-risca (U+2013) em texto publicado. Use dois-pontos, vírgula ou parênteses.
5. Português do Brasil e linguagem simples para público misto. Explique termo técnico antes de usá-lo.
6. Convenção nova do Contexto pede um ADR em `docs/adr/`, a partir de `0000-modelo.md`, com uma linha no índice do `README.md` da pasta.
7. O aviso de que a Aurora é inventada aparece só nos lugares que o contrato lista, na seção "O aviso de que a Aurora é inventada".
8. Em exemplo, responsável e quem aprova são cargo ou área, nunca nome de pessoa.
9. Nenhum campo de protocolo entra no núcleo dos documentos (ADR 0025). Protocolo é adaptador descartável, como em `docs/design/mcp.md`.
10. Não altere `auditoria/`. Ela é registro histórico.
11. Não faça commit nem push sem pedido de quem mantém o repositório.
12. No shell zsh, o modo noclobber impede sobrescrever arquivo com `>`. Use `>|` ou um script Python.
13. Link para arquivo do repositório usa caminho relativo. Link `blob/main` só pode apontar para arquivo que existe.
