# Contrato editorial: Contexto

**Versão:** 0.2 · **Data desta versão:** 2026-11-16 · **Estado:** aprovado pelo mantenedor · **Mantenedor:** Edoardo Lobl

| Versão | Data | O que mudou | Aprovado por |
|---|---|---|---|
| 0.2 | 2026-11-16 | Regra dos exemplos completos com aprovação fictícia; versionamento com data obrigatório; estados de pendência; templates Markdown sem bloco YAML | Mantenedor |
| 0.1 | 2026-11-16 | Primeira versão do contrato | Mantenedor |

## Promessa única

Orientar especialistas de diferentes áreas a produzir documentação que explicite conhecimento, contexto, critérios e exceções para que engenheiros de IA não precisem inventar regras ausentes ou inferir significados a partir de documentos ambíguos.

Este projeto **não promete** que os modelos resolvem por si só problemas de SQL, RAG, avaliação automática ou agentes. Documentos são insumos; sistemas precisam ser projetados e testados.

## Público e linguagem

- Especialistas de negócio, gestores, analistas de dados e pessoas não técnicas são leitores primários.
- Engenharia de IA é um público secundário interessado em entradas documentais bem definidas.
- Em todo termo técnico: explicar antes de utilizar, fornecer exemplo quando útil.
- Não infantilizar o leitor nem remover o conteúdo rigoroso por ser técnico.

## Cinco regras editoriais

1. **Ensinar como fazer:** toda regra editorial acompanha pergunta operacional e evidência esperada.
2. **Explicar a origem:** diferenciar normas, estudos, práticas industriais e decisões autorais.
3. **Exibir os dois lados:** cada modelo publicado tem um exemplo com lacunas e um exemplo completo. Ver "Exemplos completos e aprovação fictícia".
4. **Separar conhecimento e execução:** documentação não é enforcement de regras em runtime.
5. **Marcar incertezas:** em documento real, nunca inventar responsável, aprovação, fórmula, vigência, fonte, regra ou valor para deixar um modelo “completo”.
6. **Datar e versionar:** todo documento diz qual é a versão, de que data, e guarda o histórico do que mudou.

## Exemplos completos e aprovação fictícia

O leitor precisa ver o destino, não só o ponto de partida. Por isso:

1. Em **documento real**, a regra 5 vale sem exceção.
2. Em **exemplo didático**, é permitido mostrar um documento completo e aprovado quando três condições valem juntas:
   - a organização é a Aurora, fictícia;
   - responsável e aprovador são um cargo ou área, nunca o nome de uma pessoa;
   - o arquivo abre com aviso de exemplo fictício e traz o campo `example_notice` dizendo que a aprovação vale só dentro do exemplo.
3. Todo tipo de modelo tem **os dois exemplos**: `exemplo-<tipo>-ficticio.yaml` (com lacunas, nunca `approved`) e `exemplo-<tipo>-completo.yaml` (`approved`, sem perguntas em aberto).
4. O exemplo completo traz um **histórico com pelo menos duas versões**, para ensinar o que muda quando a regra muda.
5. Os dois exemplos compartilham o mesmo `id`: são o mesmo documento em momentos diferentes.

Risco aceito: alguém pode copiar um exemplo completo achando que é regra real. O aviso no topo, o campo `example_notice` e o nome Aurora reduzem o risco, sem eliminá-lo.

O validador (`scripts/validate_content.py`) confere as condições 2 a 5.

## Versionamento com data

Campos obrigatórios em todo modelo e exemplo:

```yaml
version: "1.1"              # versão deste documento
version_date: "2026-09-01"  # data desta versão
valid_from: "2026-09-01"    # desde quando a regra vale
version_history:            # a mais recente primeiro
  - version: "1.1"
    date: "2026-09-01"
    change: "O que mudou na regra e por quê"
    approved_by: "Cargo ou área"
```

- `version_date` e `valid_from` são coisas diferentes: uma regra pode ser aprovada hoje para valer no mês que vem.
- `change` descreve a mudança na regra, não a edição do texto.
- Um rascunho também tem versão e data; `approved_by` fica `null`.
- Nos modelos Markdown, os mesmos dados aparecem nas seções "Identificação" e "Histórico de versões", em português.

## Estrutura de uma página prática

- **Compreender:** qual problema resolve, quando aplicar, por que importa.
- **Observar:** texto ambíguo, perguntas de elicitação, versão melhorada e interpretação das mudanças.
- **Aplicar:** modelo, instrução, perguntas e verificação.
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
title: Receita reconhecida: exemplo
status: pending_approval
owner: null
source_of_truth: null
valid_from: null
---
```

**Nunca misturar estas duas camadas** nem presumir que o YAML de negócio é uma especificação executável em qualquer plataforma.

## Estados

**Estado do documento** (campo `status`). Só estes quatro:

| Código | Em português | Significa |
|---|---|---|
| `draft` | Rascunho | Em construção |
| `pending_approval` | Pendente de aprovação | Estruturado, ainda não validado por quem aprova |
| `approved` | Aprovado | Confirmado pela autoridade identificada |
| `deprecated` | Obsoleto | Não vale mais; aponta para o substituto quando houver |

**Estado de uma pendência ou de um conflito** (campo `state`, dentro de perguntas em aberto e de fontes em conflito). Só estes dois:

| Código | Em português |
|---|---|
| `unresolved` | Não resolvido |
| `resolved` | Resolvido, com a resolução, quem resolveu e a data |

Não usar outras grafias (`needs_approval`, `pending_confirmation`, `pendente_de_aprovacao` e semelhantes).

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

## Critério de aceitação por modelo

> Um especialista que domina o assunto, mas não a engenharia de IA, consegue usar o modelo para explicar seu conceito/processo, identificar lacunas e determinar a quem cabe resolvê-las, sem ter de inventar definições?

Checklist de aprovação editorial do modelo: necessidade e aplicabilidade; perguntas de elicitação; exemplo com lacunas; exemplo completo com aprovação fictícia; histórico de versões; pendências explícitas; responsáveis; fontes; vocabulário; links; revisão.

## Uma só fonte para os exemplos

As páginas não copiam trechos YAML dos exemplos. Usam o componente `ExampleDoc`, que lê o arquivo em `public/downloads/` na hora do build. O que a página mostra é o que o leitor baixa.

Os modelos Markdown não começam com bloco YAML: abrem com a tabela "Identificação", em português, para quem não conhece YAML.

## Gestão de alterações

- Cada alteração significativa de método deve registrar versão e motivo.
- Um modelo novo só entra na navegação após possuir exemplo e instruções de uso.
- Referências substituídas devem ser revistas para evitar justificativas obsoletas.

## Regras adicionais para exemplos de Data Analytics

1. **Unidade antes da fórmula:** diferenciar pedidos, sessões, clientes, itens e eventos antes de mostrar a conta.
2. **Granularidade e joins:** declarar o que cada linha representa, cardinalidade e riscos de multiplicação.
3. **Exemplo numérico verificável:** quando houver valor esperado, fornecer amostra sintética e consulta ou procedimento reproduzível.
4. **Abstenção fundamentada:** incluir pelo menos um exemplo sem cobertura temporal, sem definição ou fora do escopo.
5. **Rubricas e decisões humanas:** diferenciar `not_evaluable` de nota zero; não fazer inferências pessoais nem autorizar contratação automática.
6. **Documentação não é enforcement:** diferenciar gabarito documental, SQL verificado, camada semântica executável e sistema de agentes.

A execução de testes automatizados pode encontrar contradições nos exemplos, mas não prova que um documento de produção é correto. A aprovação do especialista continua indispensável.

## Como validar o próprio framework

O [plano de validação exploratória](PLANO_VALIDACAO.md) propõe exercícios com pessoas técnicas e não técnicas. Não marcar como “validado por usuários” um material que apenas passou pelo build do Astro.
