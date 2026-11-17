# Contrato editorial: Contexto

**Versão:** 0.7 · **Data desta versão:** 2026-11-17 · **Estado:** proposto (F2), aguarda aprovação do mantenedor · **Mantenedor:** Edoardo Lobl

| Versão | Data | O que mudou | Aprovado por |
|---|---|---|---|
| 0.7 | 2026-11-17 | Comece aqui descrito como o menu publicado: tutorial de negócio e visão do método; o tutorial de dados fica em aberto no ROADMAP | Proposto (F2), aguarda aprovação do mantenedor |
| 0.6 | 2026-11-17 | Promessa única da seção 1.2 da direção (EDI-01); público em três perfis leitores; portal em percurso, com grupos do menu, bloco Próximo passo, prev/next pela ordem do menu, YAML fora do percurso e sem página órfã, conferido por `scripts/check_navegacao.py`; tipo Perguntas de negócio no vocabulário (ADR 0007); oito dimensões como checklist e convenção (ADR 0014) | Proposto (F2), aguarda aprovação do mantenedor |
| 0.5 | 2026-11-17 | Termo "modelo" no lugar de "template" em rótulos e textos; cinco tipos de fonte e ADR para toda convenção do Contexto; exemplo com lacunas em `draft`; aprovações em dia útil e artefatos com data conferida; cópia histórica intacta, com notas em `archival_note` | Proposto (F1), aguarda aprovação do mantenedor |
| 0.4 | 2026-11-17 | Vocabulário com fonte única em `src/data/vocabulario.yaml` | Proposto (F0), aguarda aprovação do mantenedor |
| 0.3 | 2026-11-17 | Um termo por ideia; aviso de que a Aurora é inventada só em três lugares; uma página por tipo de documento, com estrutura fixa; menu igual ao título; regras para exemplos concretos; regra de versão | Mantenedor |
| 0.2 | 2026-11-16 | Regra dos exemplos completos e aprovados; versionamento com data obrigatório; estados de perguntas em aberto; templates Markdown sem bloco YAML | Mantenedor |
| 0.1 | 2026-11-16 | Primeira versão do contrato | Mantenedor |

## Promessa única

Transforme perguntas de negócio em documentos aprovados e versionados que uma IA consegue consultar sem inventar definições, seja a ferramenta que você usa direto, seja o sistema que a engenharia monta.

Este projeto **não promete** que os modelos resolvem por si só problemas de SQL, RAG, avaliação automática ou agentes. Documentos são insumos; sistemas precisam ser projetados e testados.

## Público e linguagem

Três perfis leitores:

- **Especialista de negócio**, que conhece a regra e precisa registrá-la.
- **Analista de dados ou martech**, que transforma a regra em indicador e dashboard.
- **Quem monta agentes ou RAG**, que recebe os documentos como insumo.

Os dois primeiros perfis e quem usa a IA direto, numa ferramenta de chat ou de código, são os leitores primários. Quem monta agentes ou RAG é o público secundário, interessado em entradas documentais bem definidas.
- Em todo termo técnico: explicar antes de utilizar, fornecer exemplo quando útil.
- Não infantilizar o leitor nem remover o conteúdo rigoroso por ser técnico.
- Sem o caractere travessão em nenhum texto.

## Regras editoriais

1. **Ensinar como fazer:** toda regra editorial acompanha pergunta operacional e evidência esperada.
2. **Explicar a origem:** diferenciar os cinco tipos de fonte: norma, pesquisa revisada por pares, prática de mercado, relato de fornecedor e convenção do Contexto. Toda convenção do Contexto aponta para um ADR em `docs/adr/`.
3. **Exibir os dois lados:** cada modelo publicado tem um exemplo com lacunas e um exemplo completo. Ver "Exemplos".
4. **Separar conhecimento e execução:** documentação não é enforcement de regras em runtime.
5. **Marcar incertezas:** em documento real, nunca inventar responsável, aprovação, fórmula, vigência, fonte, regra ou valor para deixar um modelo “completo”.
6. **Datar e versionar:** todo documento diz qual é a versão, de que data, e guarda o histórico do que mudou.
7. **Um termo por ideia:** ver "Vocabulário".

## Vocabulário

Cada ideia tem um nome só, em páginas, componentes, modelos e textos dos YAML. Nomes de campos YAML e código SQL não mudam.

| Ideia | Termo | Não usar |
|---|---|---|
| Caso no limite da regra | caso-limite | caso de fronteira, edge case, casos limites |
| Período em que vale | vigência | validade |
| Estado numerado do documento | versão; “ID da versão” | revisão, quando quer dizer versão (“revisão” é só o ato de revisar) |
| Quem mantém | responsável | dono, proprietário |
| Quem tem a palavra final | quem aprova | aprovador |
| O que ninguém decidiu | pergunta em aberto; “em aberto” | pendência, pendente (o estado do documento continua “pendente de aprovação”) |
| Painel de visualização | dashboard | painel |
| Respostas certas de um conjunto de perguntas | gabarito; “resposta esperada” para uma pergunta | resposta de referência |
| Documento com as perguntas que a IA vai receber e as respostas esperadas | Perguntas de negócio | Perguntas de referência, casos de teste |
| Ligação entre tabelas | junção | join, fora do SQL |
| Descobrir conhecimento com as pessoas | descobrir, perguntar | elicitar, fora da bibliografia |
| Pedido de campanha | brief | briefing |
| Medida acompanhada | indicador; KPI só no nome do modelo e nos identificadores | métrica, fora da bibliografia |
| Conjunto de dados | dataset | conjunto de dados |
| Pedido ao banco | consulta | query |
| Arquivo para preencher | modelo | template, fora de nome de arquivo, endereço e código |

A tríade para o que se sabe é **Confirmado / Relatado / Em aberto**. “Lacuna” é só o que o checklist encontra num documento.

O validador (`scripts/validate_content.py`) recusa as formas da coluna “Não usar” fora da bibliografia. As regras que ele aplica ficam em `src/data/vocabulario.yaml`; para mudar o vocabulário, altere a tabela acima e o arquivo juntos (`scripts/check_higiene.py` confere que todo termo do arquivo está na tabela).

## Exemplos

### O aviso de que a Aurora é inventada

Todos os exemplos usam a Aurora, uma organização inventada. Isso é dito **em três lugares e só neles**:

1. uma frase na página inicial;
2. a seção “Os exemplos são fictícios”, em Autoria e licença;
3. a primeira linha de comentário de cada YAML de exemplo, porque o arquivo baixado circula sem o site.

Fora deles, nenhum “fictício”, “hipotético”, “ilustrativo”, “didático”, “demonstrativo” ou “A Aurora não existe”. Repetir o aviso trata o leitor como incapaz de lembrar o que leu. “Amostra sintética” aparece uma vez, no laboratório, porque explica o tamanho da amostra. A restrição “a rubrica avalia o trabalho, nunca a pessoa” não é aviso de ficção e fica, uma vez.

### Exemplos completos e aprovados

O leitor precisa ver o destino, não só o ponto de partida. Por isso:

1. Em **documento real**, a regra 5 vale sem exceção.
2. Num **exemplo**, é permitido mostrar um documento completo e aprovado quando três condições valem juntas:
   - a organização é a Aurora;
   - responsável e quem aprova são um cargo ou área, nunca o nome de uma pessoa;
   - a primeira linha do arquivo diz que a Aurora é inventada e que nomes, datas e aprovações fazem parte do caso.
3. Todo tipo de modelo tem **os dois exemplos**: `exemplo-<tipo>-lacunas.yaml` (estado `draft`, nunca `approved`; MOD-11) e `exemplo-<tipo>-completo.yaml` (`approved`, sem perguntas em aberto).
4. O exemplo completo traz um **histórico com pelo menos duas versões**, para ensinar o que muda quando a regra muda.
5. Os dois exemplos compartilham o mesmo `id`: são o mesmo documento em momentos diferentes.

Risco aceito: alguém pode copiar um exemplo completo achando que é regra real. A linha no topo do arquivo e o nome Aurora reduzem o risco, sem eliminá-lo.

### Exemplos concretos

1. **Começa por um conflito com números:** duas fontes, duas pessoas ou duas datas que dão respostas diferentes.
2. **O documento completo fala do caso:** critérios, âncoras, passos e limites citam valores, datas e nomes da Aurora, não frases que serviriam para qualquer empresa.
3. **O texto da página não repete o cartão:** comenta o que o cartão não diz.
4. **Termina com “Teste você”:** casos com a resposta escondida, pelo menos um atravessando uma mudança de versão.
5. **Números da amostra são calculados, não digitados:** o validador refaz a conta no SQLite e confere o texto.
6. **Datas conferidas:** dia da semana, prazos em dias úteis (fim de semana não conta; o prazo vence no fim do último dia útil), aprovações em dia útil (o validador avisa) e coerência com o histórico de versões. Nenhum documento cita artefato, registro ou versão com data posterior à sua. As datas dos artefatos ficam em `src/data/artefatos.yaml`, e o validador acusa a referência com data posterior.

O validador confere as condições de “Exemplos completos e aprovados”, as notas da rubrica, os encaminhamentos da tabela de decisão e os números da amostra.

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
- A cópia histórica de uma versão fica como foi aprovada. Notas escritas depois, por exemplo que a versão foi substituída, vão para `archival_note`, com a data em que a nota foi escrita (MOD-12, AUR-04).
- Um rascunho também tem versão e data; `approved_by` fica `null`.
- Nos modelos Markdown, os mesmos dados aparecem nas seções "Identificação" e "Histórico de versões", em português.

Qual número mudar:

| Mudança | Versão |
|---|---|
| Correção só de texto | A mesma |
| Esclarece sem mudar nenhum resultado | Menor (1.0 → 1.1) |
| Muda algum resultado | Maior (1.0 → 2.0) |
| Passa a medir outra coisa | Novo `id` |

## Organização do portal

O portal segue o percurso do leitor, não a ordem das pastas. A decisão está no [ADR 0023](adr/0023-percurso-em-sete-passos.md).

- **Grupos do menu:** Comece aqui (tutorial de negócio e visão do método; o tutorial de dados ainda não existe e está em aberto no [ROADMAP](ROADMAP.md)), Percurso, Modelos, Laboratórios, Entender, Consultar e Usar com IA.
- **Percurso em sete passos**, com fonte em `src/data/percurso.yaml`: 1 Escreva a pergunta de negócio; 2 Delimite o acervo; 3 Descubra o que falta; 4 Escreva com o modelo (a página de modelos); 5 Revise e aprove; 6 Teste com as perguntas; 7 Leve à sua ferramenta de IA.
- **Próximo passo:** toda página do percurso termina com o bloco Próximo passo. O prev/next segue a ordem do menu, e não a ordem das pastas.
- **Modelos:** o grupo segue o nível de `src/data/modelos.yaml`: o núcleo de entrada (ADR 0013), o segundo nível e a trilha complementar da rubrica (ADR 0003).
- **Nenhuma página órfã:** toda página tem entrada no menu ou em outra página, e nenhuma página fica sem saída. `scripts/check_navegacao.py` confere.
- **YAML só em páginas de modelo e de referência,** nunca no percurso (NAV-08).
- **Uma página por tipo de documento**, com o modelo e o exemplo juntos. O endereço continua em `/templates/...`.
- **Cada cartão de exemplo aparece em uma página só.** Onde outra página precisa dele, entra um link.
- **O menu mostra o título da página.** O sidebar lista só os slugs, sem rótulo próprio, e nenhuma página muda o rótulo pelo frontmatter. O validador confere.
- **Página movida ou renomeada ganha redirecionamento** em `astro.config.mjs`, e o validador recusa link para o endereço antigo.

### Estrutura de uma página de tipo

1. **O problema**, com números: uma situação da Aurora em que a falta do documento custa algo visível.
2. **O que perguntar**, numa tabela só: pergunta, como ela aparece na Aurora, o que registrar.
3. **Antes e depois da decisão**: o cartão com lacunas e o cartão completo, cada um uma vez, e o que o histórico de versões ensina.
4. **Teste você**, com as respostas escondidas.
5. **Baixe o modelo**, e a fundamentação.

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

**Estado de uma pergunta em aberto ou de um conflito** (campo `state`, dentro de perguntas em aberto e de fontes em conflito). Só estes dois:

| Código | Em português |
|---|---|
| `unresolved` | Não resolvido |
| `resolved` | Resolvido, com a resolução, quem resolveu e a data |

Não usar outras grafias (`needs_approval`, `pending_confirmation`, `pendente_de_aprovacao` e semelhantes).

## Trato das fontes

- Priorizar fonte oficial/primária e DOI para pesquisa acadêmica.
- Identificar publicações de fornecedores e suas limitações metodológicas.
- Não apresentar exemplos como decisões reais de uma organização.
- Não reproduzir material sob licença restritiva; usar síntese e referência.
- Não declarar que uma prática nossa é exigência normativa sem o suporte apropriado.

## Acessibilidade e interface

- Foco de teclado e rótulos visíveis; controles de checklist precisam funcionar sem conta.
- Não depender exclusivamente de cor para sinalizar um problema.
- Respeitar preferência de movimento reduzido.
- UI responsiva, legível em celular, e busca local quando o site for compilado.
- Interações pedagógicas não enviam nem armazenam respostas.
- Códigos do YAML (`not_evaluable`, `evidence_sufficient`) não aparecem crus no texto legível do cartão.

## Critério de aceitação por modelo

> Um especialista que domina o assunto, mas não a engenharia de IA, consegue usar o modelo para explicar seu conceito/processo, identificar lacunas e determinar a quem cabe resolvê-las, sem ter de inventar definições?

Checklist de aprovação editorial do modelo: necessidade e aplicabilidade; perguntas para descobrir o que falta; exemplo com lacunas; exemplo completo e aprovado; histórico de versões; perguntas em aberto explícitas; responsáveis; fontes; vocabulário; links; “Teste você”; revisão.

## Uma só fonte para os exemplos

As páginas não copiam trechos YAML dos exemplos. Usam o componente `ExampleDoc`, que lê o arquivo em `public/downloads/` na hora do build. O que a página mostra é o que o leitor baixa.

Os modelos Markdown não começam com bloco YAML: abrem com a tabela "Identificação", em português, para quem não conhece YAML.

Os modelos vêm de `src/data/modelos.yaml`, que alimenta `TemplateFinder`, `TemplateDownloads` e `TemplateStart`. As oito dimensões vêm de `src/data/dimensoes.yaml`, que alimenta o checklist.

## Gestão de alterações

- Cada alteração significativa de método deve registrar versão e motivo.
- Um modelo novo só entra na navegação após possuir exemplo e instruções de uso.
- Referências substituídas devem ser revistas para evitar justificativas obsoletas.
- Mudança grande passa por revisão independente, feita por quem não escreveu o texto, antes do merge.

## Regras adicionais para exemplos de Data Analytics

1. **Unidade antes da fórmula:** diferenciar pedidos, sessões, clientes, itens e eventos antes de mostrar a conta.
2. **Granularidade e junções:** declarar o que cada linha representa, cardinalidade e riscos de multiplicação.
3. **Exemplo numérico verificável:** quando houver valor esperado, fornecer amostra sintética e consulta ou procedimento reproduzível.
4. **Abstenção fundamentada:** incluir pelo menos um exemplo sem cobertura temporal, sem definição ou fora do escopo.
5. **Documentação não é enforcement:** diferenciar gabarito documental, SQL verificado, camada semântica executável e sistema de agentes.

A execução de testes automatizados pode encontrar contradições nos exemplos, mas não prova que um documento de produção é correto. A aprovação do especialista continua indispensável.

## Rubricas

Diferenciar “não avaliável” de nota zero; avaliar o trabalho, nunca a pessoa; a rubrica não aprova nem decide sozinha. Quando a nota alimenta outro documento, a ligação fica escrita nos dois.

## Como validar o próprio framework

O [plano de validação exploratória](PLANO_VALIDACAO.md) propõe exercícios com pessoas técnicas e não técnicas. Não marcar como “validado por usuários” um material que apenas passou pelo build do Astro.
