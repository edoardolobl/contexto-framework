# Contrato editorial — Contexto

**Versão:** 0.1 · **Status:** proposta implementada nesta baseline · **Mantenedor:** responsável pelo repositório

## Promessa única

Orientar especialistas de diferentes áreas a produzir documentação que explicite conhecimento, contexto, critérios e exceções para que engenheiros de IA não precisem inventar regras ausentes ou inferir significados a partir de documentos ambíguos.

Este projeto **não promete** que os templates resolvem por si só problemas de SQL, RAG, avaliação automática ou agentes. Documentos são insumos; sistemas precisam ser projetados e testados.

## Público e linguagem

- Especialistas de negócio, gestores, analistas de dados e pessoas não técnicas são leitores primários.
- Engenharia de IA é um público secundário interessado em entradas documentais bem definidas.
- Em todo termo técnico: explicar antes de utilizar, fornecer exemplo quando útil.
- Não infantilizar o leitor nem remover o conteúdo rigoroso por ser técnico.

## Cinco regras editoriais

1. **Ensinar como fazer:** toda regra editorial acompanha pergunta operacional e evidência esperada.
2. **Explicar a origem:** diferenciar normas, estudos, práticas industriais e decisões autorais.
3. **Exibir exemplos:** cada template publicado deve possuir um exemplo preenchido e casos de incompletude.
4. **Separar conhecimento e execução:** documentação não é enforcement de regras em runtime.
5. **Marcar incertezas:** nunca inventar owner, aprovação, fórmula, vigência, fonte, regra ou valor para deixar um template “completo”.

## Estrutura de uma página prática

- **Compreender:** qual problema resolve, quando aplicar, por que importa.
- **Observar:** texto ambíguo, perguntas de elicitação, versão melhorada e interpretação das mudanças.
- **Aplicar:** template, instrução, perguntas e verificação.
- **Aprofundar:** referências primárias com implicações e limitações.

## Estrutura de duas camadas de metadados

### A. Frontmatter das páginas do portal

Controla título, descrição, navegação e renderização Astro/Starlight. Exemplo:

```yaml
---
title: Descobrir o que falta
description: Perguntas para encontrar ambiguidades
---
```

### B. Metadados dos documentos que o portal ensina a escrever

Expressam responsabilidade, vigência, status e fontes sobre um objeto de negócio. Exemplo:

```yaml
---
id: METRIC-001
title: Receita reconhecida — exemplo
status: pending_approval
owner: null
source_of_truth: null
valid_from: null
---
```

**Nunca misturar estas duas camadas** nem presumir que o YAML de negócio é uma especificação executável em qualquer plataforma.

## Estados editoriais propostos

- `draft`: rascunho em construção;
- `pending_approval`: completo ou parcialmente estruturado, mas ainda não validado;
- `approved`: aprovado pela autoridade identificada para a finalidade documental;
- `deprecated`: obsoleto, manter relação com a substituição quando houver.

## Trato das fontes

- Priorizar fonte oficial/primária e DOI para pesquisa acadêmica.
- Identificar publicações de fornecedores e suas limitações metodológicas.
- Não apresentar exemplos fictícios como decisões reais de uma organização.
- Não reproduzir material sob licença restritiva; usar síntese e referência.
- Não declarar que uma prática nossa é exigência normativa sem o suporte apropriado.

## Acessibilidade e interface

- Foco de teclado e rótulos visíveis; controles de checklist precisam funcionar sem conta.
- Não depender exclusivamente de cor para sinalizar um problema.
- Respeitar preferência de movimento reduzido.
- UI responsiva, legível em celular, e busca local quando o site for compilado.
- Interações pedagógicas não enviam nem armazenam respostas.

## Critério de aceitação por template

> Um especialista que domina o assunto, mas não a engenharia de IA, consegue usar o template para explicar seu conceito/processo, identificar lacunas e determinar a quem cabe resolvê-las, sem ter de inventar definições?

Checklist de aprovação editorial do template: necessidade e aplicabilidade; perguntas de elicitação; exemplo insuficiente; exemplo revisado; pendências explícitas; responsáveis; fontes; vocabulário; links; revisão.

## Gestão de alterações

- Cada alteração significativa de método deve registrar versão e motivo.
- Um template novo só entra na navegação após possuir exemplo e instruções de uso.
- Referências substituídas devem ser revistas para evitar justificativas obsoletas.
