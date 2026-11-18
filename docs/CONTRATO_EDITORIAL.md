# Contrato editorial: Contexto

**Versão:** 0.13 · **Data desta versão:** 2026-11-17 · **Estado:** aprovado pelo mantenedor (ADR 0030) · **Mantenedor:** Edoardo Lobl

| Versão | Data | O que mudou | Aprovado por |
|---|---|---|---|
| 0.13 | 2026-11-17 | Decisões do mantenedor depois das fases (ADR 0030): versões 0.4 a 0.12 aprovadas; vigência retroativa só na primeira versão de um assunto e sempre declarada em `retroactive_validity`, com motivo e quem confirmou, conferida por `scripts/check_revisions.py`; schema 1.1.0 com as chaves do ODCS `physicalName`, `businessName` e `physicalType` no lugar de `physical_name`, `business_name` e `technical_type`, e com `also_accepted` opcional nas perguntas de negócio; rótulos de campos do tipo em `src/data/campos.yaml`, conferidos contra o schema; regra do termo ambíguo (nome ou sinônimo registrado) no AGENTS.md do kit e na Skill `contexto-consultar`; nomes de produção nos laboratórios da Aurora; versão do documento em MAJOR.MINOR e tipos do ADR 0013 separados | Mantenedor |
| 0.12 | 2026-11-17 | Quatro Skills no kit (`auditar-coleta`, `contexto-elicitar`, `contexto-consultar` e `importar-plano-de-mensuracao`), com texto à mão, ressalva e `Versão alvo:` conferidas pelo gerador (ADR 0029); quinta página de Usar com IA, sobre o plano de mensuração em planilha; aviso de que o modelo CSV não tem linha de comentário; ciclo de manutenção a partir do uso, com a regra de que o relatório de erros não altera documento aprovado; piloto de validação como portão da v1.0 (MET-16, ADR 0010) | Mantenedor |
| 0.11 | 2026-11-17 | Schema 1.1.0, com `license` e `source_url` opcionais (ADR 0028); as quatro páginas de Usar com IA; saídas para máquinas (documentos por id e versão, schemas, kit para agentes e llms.txt) geradas por `scripts/gerar_saidas.py`, sem edição à mão e conferidas no CI; aviso de ficção no frontmatter do .md de cada documento publicado e dos contratos do kit, mas não no AGENTS.md nem no glossário do kit; protocolo de onboarding como critério de saída da F6 (I-26) | Mantenedor |
| 0.10 | 2026-11-17 | Sequência didática da página de tipo (I-24) em cinco passos recolhíveis, com o modelo em branco por último; limite de até 4 telas a 1440 x 900 px, sem limite próprio no celular (ADR 0017); nomes Diagnóstico e Complete (I-25); duas páginas por tipo, a que ensina e a referência de campos gerada; linha "Exemplo Aurora:" nos modelos .md; sistema visual com IBM Plex, tokens de cor e checklist visual por PR (ADR 0016); "Teste você" com resposta antes do gabarito | Mantenedor |
| 0.9 | 2026-11-17 | Tipo Evento de coleta no núcleo de entrada (ADR 0013 e 0027); grupo Laboratórios com dois laboratórios; seção opcional de triagem na página do tipo, quando o tipo pede; aviso de ficção também na primeira linha de cada .sql baixável (ADR 0012); regras para exemplos de Data Analytics sobre limite fixo do Lab 2, falta de linha x zero, dia incompleto em D+2, cenário só com fonte primária e limiar numérico como escolha do time; termos "linha de base" e "plano de mensuração" na tabela Vocabulário | Mantenedor |
| 0.8 | 2026-11-17 | Fonte única em Markdown com frontmatter; downloads gerados e conferidos no CI; schema 1.0.0 com JSON Schema por tipo; cabeçalho comum e intent; estado superseded e campo status nas perguntas em aberto (ADR 0005, 0006, 0009 e 0015); exemplo YAML do cabeçalho na ordem que o validador exige | Mantenedor |
| 0.7 | 2026-11-17 | Comece aqui descrito como o menu publicado: tutorial de negócio e visão do método; o tutorial de dados fica em aberto no ROADMAP | Mantenedor |
| 0.6 | 2026-11-17 | Promessa única da seção 1.2 da direção (EDI-01); público em três perfis leitores; portal em percurso, com grupos do menu, bloco Próximo passo, prev/next pela ordem do menu, YAML fora do percurso e sem página órfã, conferido por `scripts/check_navegacao.py`; tipo Perguntas de negócio no vocabulário (ADR 0007); oito dimensões como checklist e convenção (ADR 0014) | Mantenedor |
| 0.5 | 2026-11-17 | Termo "modelo" no lugar de "template" em rótulos e textos; cinco tipos de fonte e ADR para toda convenção do Contexto; exemplo com lacunas em `draft`; aprovações em dia útil e artefatos com data conferida; cópia histórica intacta, com notas em `archival_note` | Mantenedor |
| 0.4 | 2026-11-17 | Vocabulário com fonte única em `src/data/vocabulario.yaml` | Mantenedor |
| 0.3 | 2026-11-17 | Um termo por ideia; aviso de que a Aurora é inventada só em três lugares; uma página por tipo de documento, com estrutura fixa; menu igual ao título; regras para exemplos concretos; regra de versão | Mantenedor |
| 0.2 | 2026-11-16 | Regra dos exemplos completos e aprovados; versionamento com data obrigatório; estados de perguntas em aberto; modelos Markdown sem bloco YAML | Mantenedor |
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
| Ponto de comparação de uma série no tempo | linha de base | baseline |
| Documento que diz o que cada evento deve fazer e quando | plano de mensuração | tag plan (só na página do tipo Evento de coleta) |

A tríade para o que se sabe é **Confirmado / Relatado / Em aberto**. “Lacuna” é só o que o checklist encontra num documento.

O validador (`scripts/validate_content.py`) recusa as formas da coluna “Não usar” fora da bibliografia. As regras que ele aplica ficam em `src/data/vocabulario.yaml`; para mudar o vocabulário, altere a tabela acima e o arquivo juntos (`scripts/check_higiene.py` confere que todo termo do arquivo está na tabela).

## Exemplos

### O aviso de que a Aurora é inventada

Todos os exemplos usam a Aurora, uma organização inventada. Isso é dito **só nos lugares abaixo**:

1. uma frase na página inicial;
2. a seção “Os exemplos são fictícios”, em Autoria e licença;
3. a primeira linha de comentário do frontmatter de cada exemplo, que vira a primeira linha do YAML gerado, e a primeira linha de comentário de cada `.sql` baixável, porque o arquivo baixado circula sem o site (ADR 0012);
4. o frontmatter do `.md` de cada documento publicado em `public/documentos/` e dos contratos do kit (`contratos/` e `contratos/historico/`), com a mesma linha de aviso dos exemplos. O AGENTS.md do kit e o glossário do kit não repetem o aviso.

Fora deles, nenhum “fictício”, “hipotético”, “ilustrativo”, “didático”, “demonstrativo” ou “A Aurora não existe”. Repetir o aviso trata o leitor como incapaz de lembrar o que leu. “Amostra sintética” aparece uma vez, no laboratório, porque explica o tamanho da amostra. A restrição “a rubrica avalia o trabalho, nunca a pessoa” não é aviso de ficção e fica, uma vez.

O modelo CSV do plano de mensuração não tem linha de comentário, porque o formato CSV não tem comentário. Por isso a linha de exemplo leva Aurora na marca e no responsável, e o aviso de ficção não aparece no arquivo.

### Exemplos completos e aprovados

O leitor precisa ver o destino, não só o ponto de partida. Por isso:

1. Em **documento real**, a regra 5 vale sem exceção.
2. Num **exemplo**, é permitido mostrar um documento completo e aprovado quando três condições valem juntas:
   - a organização é a Aurora;
   - responsável e quem aprova são um cargo ou área, nunca o nome de uma pessoa;
   - a primeira linha do arquivo diz que a Aurora é inventada e que nomes, datas e aprovações fazem parte do caso.
3. Todo tipo de modelo tem **os dois exemplos**: `exemplo-<tipo>-lacunas.yaml` (estado `draft`, nunca `approved`; MOD-11) e `exemplo-<tipo>-completo.yaml` (`approved`, sem perguntas em aberto). Os nomes de arquivo continuam, mas a fonte fica em `src/exemplos/`.
4. O exemplo completo traz um **histórico com pelo menos duas versões**, para ensinar o que muda quando a regra muda.
5. Os dois exemplos compartilham o mesmo `id`: são o mesmo documento em momentos diferentes.

Risco aceito: alguém pode copiar um exemplo completo achando que é regra real. A linha no topo do arquivo e o nome Aurora reduzem o risco, sem eliminá-lo.

### Exemplos concretos

1. **Começa por um conflito com números:** duas fontes, duas pessoas ou duas datas que dão respostas diferentes.
2. **O documento completo fala do caso:** critérios, âncoras, passos e limites citam valores, datas e nomes da Aurora, não frases que serviriam para qualquer empresa.
3. **O texto da página não repete o cartão:** comenta o que o cartão não diz.
4. **Termina com “Teste você”:** o leitor responde antes de ver o gabarito, e a página explica o erro de cada alternativa. Pelo menos um caso atravessa uma mudança de versão. Nada é enviado nem guardado.
5. **Números da amostra são calculados, não digitados:** o validador refaz a conta no SQLite e confere o texto.
6. **Datas conferidas:** dia da semana, prazos em dias úteis (fim de semana não conta; o prazo vence no fim do último dia útil), aprovações em dia útil (o validador avisa) e coerência com o histórico de versões. Nenhum documento cita artefato, registro ou versão com data posterior à sua. As datas dos artefatos ficam em `src/data/artefatos.yaml`, e o validador acusa a referência com data posterior.

Diagnóstico e Complete usam os dois exemplos existentes, o com lacunas e o completo. Não criam exemplo nem fato novo.

O validador confere as condições de “Exemplos completos e aprovados”, as notas da rubrica, os encaminhamentos da tabela de decisão e os números da amostra.

## Versionamento com data

Todo modelo e todo exemplo declara o schema 1.1.0 no campo `schema_version` (ADR 0028). O schema diz o formato do arquivo e muda em ritmo próprio, separado da versão do produto e da versão do documento (ADR 0009). A 1.1.0 troca três chaves do dataset pelos nomes do ODCS (`physicalName`, `businessName` e `physicalType`, ADR 0030); um dataset escrito na 1.0.0 precisa trocar essas três chaves. Nenhuma versão 1.x tinha sido publicada, por isso a troca não tem período de transição. A 1.1.0 também acrescenta campos opcionais:

- `license`: a licença do documento, como identificador SPDX. Nos modelos em branco fica `null`, porque cada time escolhe a sua licença. Nos exemplos, `CC-BY-4.0`.
- `source_url`: o endereço publicado do documento. Nos modelos em branco fica `null`. Nos exemplos, é o endereço publicado do próprio exemplo.
- `retroactive_validity`: só na primeira versão de um assunto cujo `valid_from` é anterior a `version_date`. Traz `reason` (por que a regra vale desde antes desta versão) e `confirmed_by` (cargo ou área que confirmou).
- `also_accepted`: só nas perguntas de negócio. Outro comportamento que também vale para a pergunta, com a condição que a resposta precisa cumprir.

Para sair do rascunho, o documento precisa de um núcleo de oito campos: `id`, `title`, `version`, `status`, `owner`, `approver`, `version_date` e `intent.question`. Os campos de data e de histórico também são obrigatórios:

```yaml
id: "METRIC-001"            # o mesmo id em todas as versões do documento
schema_version: "1.1.0"     # versão do formato, não do documento
type: kpi                   # igual ao nome do modelo
title: "Receita reconhecida"
version: "1.1"              # versão deste documento
status: approved
owner: "Cargo ou área"      # responsável por manter o documento
approver: "Cargo ou área"   # quem aprova
valid_from: "2026-09-01"    # desde quando a regra vale
version_date: "2026-09-01"  # data desta versão
review_interval: "P6M"      # revisão a cada seis meses, em ISO 8601
intent:
  question: "Qual é a receita reconhecida no mês?"
version_history:            # a mais recente primeiro
  - version: "1.1"
    date: "2026-09-01"
    change: "O que mudou na regra e por quê"
    approved_by: "Cargo ou área"
```

- `version_date` e `valid_from` são coisas diferentes: uma regra pode ser aprovada hoje para valer no mês que vem.
- **Vigência retroativa:** `valid_from` anterior a `version_date` só vale na primeira versão de um assunto, quando o documento registra uma regra que já estava em uso, e sempre declarada em `retroactive_validity`, com motivo e quem confirmou. Uma versão que substitui outra nunca reescreve a vigência da anterior. O validador confere as duas condições (ADR 0030).
- `change` descreve a mudança na regra, não a edição do texto.
- `review_interval` usa duração ISO 8601 (`P6M` são seis meses). É obrigatório quando o documento tem `context.instructions`, para que a instrução ao agente não envelheça sem revisão.
- A cópia histórica de uma versão guarda o texto como foi aprovado. Quando outra versão toma o lugar dela, a cópia passa a `status: superseded`, e `superseded_by_revision` aponta a versão que a substituiu. O campo `recorded_at`, data em que o registro foi feito, aparece só nessa cópia substituída (I-15).
- Notas escritas depois, por exemplo que a versão foi substituída, vão para `archival_note`, com a data em que a nota foi escrita (MOD-12, AUR-04).
- Todo Indicador com versão maior declara `history_recalculation`: `recalculate`, quando a série antiga é recalculada, ou `method_break`, quando ela fica marcada como quebra de método (I-14).
- Um rascunho também tem versão e data; `approved_by` fica `null`.
- A versão do documento segue MAJOR.MINOR (ADR 0030). O formato aceita PATCH, mas nenhum exemplo o usa.
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

- **Grupos do menu:** Comece aqui (tutorial de negócio e visão do método; o tutorial de dados ainda não existe e está em aberto no [ROADMAP](ROADMAP.md)), Percurso, Modelos, Laboratórios (dois: o de Data Analytics e o de eventos de coleta), Entender, Consultar e Usar com IA.
- **Percurso em sete passos**, com fonte em `src/data/percurso.yaml`: 1 Escreva a pergunta de negócio; 2 Delimite o acervo; 3 Descubra o que falta; 4 Escreva com o modelo (a página de modelos); 5 Revise e aprove; 6 Teste com as perguntas; 7 Leve à sua ferramenta de IA.
- **Próximo passo:** toda página do percurso termina com o bloco Próximo passo. O prev/next segue a ordem do menu, e não a ordem das pastas.
- **Modelos:** o grupo segue o nível de `src/data/modelos.yaml`: o núcleo de entrada (ADR 0013), o segundo nível e a trilha complementar da rubrica (ADR 0003). O tipo Evento de coleta está no núcleo de entrada (ADR 0013 e 0027).
- **Usar com IA:** cinco páginas. `usar-com-ia/kit-para-agentes` apresenta o kit mínimo para baixar; `usar-com-ia/preparar-para-notebooklm-ou-rag` mostra como preparar um documento para um agente ou um RAG; `usar-com-ia/enderecos-e-schemas` diz onde ficam os documentos, os endereços e os schemas publicados; `usar-com-ia/agents-md` traz o modelo de AGENTS.md para os times; `usar-com-ia/plano-de-mensuracao-em-planilha` leva o plano de mensuração de uma planilha para o formato do Contexto (ADR 0029).
- **Nenhuma página órfã:** toda página tem entrada no menu ou em outra página, e nenhuma página fica sem saída. `scripts/check_navegacao.py` confere.
- **YAML só em páginas de modelo e de referência,** nunca no percurso (NAV-08).
- **Duas páginas por tipo de documento:** a que ensina, em `/templates/<slug>/`, com a sequência descrita abaixo; e a referência de campos, em `/referencias/campos/<slug>/`, gerada por `scripts/gerar_referencias.py` a partir de `src/data/campos.yaml` e dos schemas. A referência não se edita à mão e o CI a confere. O índice "Referência de campos" fica no grupo Consultar.
- **Cada cartão de exemplo aparece em uma página só.** Onde outra página precisa dele, entra um link.
- **O menu mostra o título da página.** O sidebar lista só os slugs, sem rótulo próprio, e nenhuma página muda o rótulo pelo frontmatter. O validador confere.
- **Página movida ou renomeada ganha redirecionamento** em `astro.config.mjs`, e o validador recusa link para o endereço antigo.

### Estrutura de uma página de tipo

A ordem é a mesma em todo tipo, para que o leitor saiba onde está. Cada página tem **no máximo 4 telas a 1440 x 900 px**, com os passos fechados. Não há limite próprio no celular: ele é conferido pelo checklist visual (ADR 0017). `scripts/check_visual.mjs` confere as 4 telas, e `scripts/check_paginas_modelo.py` confere a ordem abaixo.

1. **Antes de preencher:** para que serve o tipo, quando usá-lo e o que ter em mãos.
2. **O problema**, com par contrastante: a mesma pergunta, duas definições e dois resultados, de preferência com números tirados dos exemplos ou dos laboratórios, como o 25% x 50% da Aurora.
3. **Aprenda com a Aurora**, em cinco passos recolhíveis (componente Steps do Starlight, com um details por passo):
   1. **Exemplo comentado:** o exemplo completo, com 2 a 4 perguntas de autoexplicação e o que o histórico de versões ensina.
   2. **Diagnóstico:** o exemplo com lacunas, para encontrar o que falta ou o erro sutil antes do gabarito (I-25).
   3. **Complete:** um trecho do exemplo completo com um campo em branco, para escrever e comparar (I-25).
   4. **Caso novo:** uma situação nova para o modelo em branco, com a tabela "O que perguntar" (pergunta, como ela aparece na Aurora, o que registrar).
   5. **Teste você:** perguntas que pedem uma resposta antes do gabarito, e explicam o erro de cada alternativa.
4. **Triagem**, seção opcional e recolhida, que só entra quando o tipo pede. O tipo Evento de coleta a usa para separar o que é quebra do que é esperado (ADR 0027).
5. **Baixe o modelo**, por último: o modelo em branco, com o link para a referência de campos e a fundamentação.

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

## Nomes das chaves e camadas (ADR 0015)

- **Chaves** (nomes dos campos no frontmatter e no YAML) ficam em inglês e em `snake_case`. Onde há equivalente direto no ODCS 3.2.0, a grafia é a do ODCS: o bloco `context` com `instructions`, `verifiedStatements` e `constraints`, `synonyms`, `authoritativeDefinitions` e, no dataset, `physicalName`, `businessName` e `physicalType` (ADR 0030). A página de correspondência com o ODCS diz quais chaves são equivalentes diretos.
- **Rótulos** que o leitor vê ficam em português e vêm de `src/data/campos.yaml`: a lista `cabecalho` para o cabeçalho comum e a lista `campos_do_tipo` para campos do tipo que precisam de rótulo fixo. Cada rótulo repete o `title` do campo no schema.
- **O Conceito** usa SKOS no bloco `vocabulary`: `prefLabel`, `altLabel`, `broader`, `related` e `not_synonyms`.
- **Três camadas por documento** (I-13): o significado em linguagem humana; o lugar onde mora a regra executável (SQL, metric view ou filtro), que o documento aponta sem repetir; e a instrução curta ao agente. Instrução em texto só quando não há alternativa estruturada.

## Estados

**Estado do documento** (campo `status`). Só estes cinco:

| Código | Em português | Significa |
|---|---|---|
| `draft` | Rascunho | Em construção |
| `pending_approval` | Pendente de aprovação | Estruturado, ainda não validado por quem aprova |
| `approved` | Aprovado | Confirmado pela autoridade identificada |
| `superseded` | Substituído | Outra versão do mesmo `id` tomou o lugar; `superseded_by_revision` aponta qual |
| `deprecated` | Obsoleto | O assunto deixou de valer; pode apontar outro documento, quando houver |

A fronteira entre os dois estados de saída:

- **Substituído** (`superseded`): o assunto continua valendo, e outra versão do mesmo `id` tomou o lugar. A cópia histórica aprovada e trocada usa este estado.
- **Obsoleto** (`deprecated`): o assunto deixou de valer, e nenhuma versão nova do mesmo `id` o substitui.

**Estado de uma pergunta em aberto** (campo `status`, junto de `question`, `impact`, `owner_to_resolve` e `resolution`; MOD-07). Só estes dois:

| Código | Em português |
|---|---|
| `unresolved` | Não resolvido |
| `resolved` | Resolvido, com a resolução, quem resolveu e a data |

**Estado de uma fonte em conflito** (campo `state`, dentro da política conflitante). Só estes dois:

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
- **Fonte:** família IBM Plex (Sans no texto, Serif nos títulos de destaque, Mono no YAML e nos nomes de campo), servida pelo próprio site, sem serviço externo (ADR 0016).
- **Títulos:** um tamanho por nível, de `h1` a `h5`.
- **Fundos:** três, e só três: base, superfície e inverso.
- **Componentes:** quatro primitivas (cartão, rótulo, botão e aviso); componentes nativos do Starlight onde houver equivalente.
- **Botões:** um par só, principal e secundário, em todo o portal.
- **Cores:** só como tokens em `:root`, sem `!important`. O Stylelint confere.
- **Checklist visual:** em cada PR, a 1440 e a 390 px, nos temas claro e escuro.
- **Exercícios:** `fieldset` com `legend`, e resposta anunciada.
- Detalhes de uso ficam em [GUIA_VISUAL.md](GUIA_VISUAL.md).

## Critério de aceitação por modelo

> Um especialista que domina o assunto, mas não a engenharia de IA, consegue usar o modelo para explicar seu conceito/processo, identificar lacunas e determinar a quem cabe resolvê-las, sem ter de inventar definições?

Checklist de aprovação editorial do modelo: necessidade e aplicabilidade; perguntas para descobrir o que falta; exemplo com lacunas; exemplo completo e aprovado; histórico de versões; perguntas em aberto explícitas; responsáveis; fontes; vocabulário; links; “Teste você”; par contrastante; exemplo comentado; Diagnóstico; Complete; caso novo; referência de campos; linhas “Exemplo Aurora:” no modelo `.md`; revisão.

## Uma só fonte para os exemplos

As páginas não copiam trechos YAML dos exemplos. Usam o componente `ExampleDoc`, que lê o arquivo em `public/downloads/` na hora do build. O que a página mostra é o que o leitor baixa.

A fonte de cada modelo é `src/modelos/<slug>.md`, e a de cada exemplo é `src/exemplos/<nome>.md`. Ambas são Markdown com frontmatter, e só essas fontes se editam à mão.

- Os `.yaml` e os `.md` de `public/downloads/` são gerados por `scripts/gerar_downloads.py` e não se editam à mão. Para regenerar, rode `npm run gerar:downloads`.
- O CI falha se os arquivos gerados estiverem fora de sincronia com as fontes.
- O modelo `.md` baixado abre com os campos no topo, para quem não conhece YAML. As seções "Identificação" (rótulos em português de `src/data/campos.yaml`) e "Histórico de versões" são geradas.
- O `ExampleDoc` lê o `.yaml` gerado.
- Em cada campo crítico do modelo `.md` baixado há uma linha `Exemplo Aurora:`, gerada do exemplo completo pelo `scripts/gerar_downloads.py`, a partir do marcador `<!-- contexto:exemplo chave -->` na fonte. Sempre há uma linha para `intent.question`, e cada modelo tem pelo menos quatro linhas `Exemplo Aurora:` (seção 1.5 item 9, AUR-13, MOD-03).

Os modelos vêm de `src/data/modelos.yaml`, que alimenta `TemplateFinder`, `TemplateDownloads` e `TemplateStart`. As oito dimensões vêm de `src/data/dimensoes.yaml`, que alimenta o checklist.

As saídas para máquinas seguem a mesma regra. `scripts/gerar_saidas.py` gera `public/documentos/` (cada documento por id e versão, em Markdown), `public/schemas/`, o kit para agentes em `public/downloads/kit/` e `public/llms.txt`. Nenhum deles se edita à mão, e o CI confere que estão em dia. A fonte do kit fica em `src/kit/` (`kit.yaml`, o AGENTS.md do kit e `skills/`); as quatro Skills são textos escritos à mão, com arquivos estáticos em `src/kit/skills/<nome>/`; a ressalva exata e a linha `Versão alvo:` são conferidas pelo gerador (ADR 0029). Para regenerar, rode `npm run gerar:saidas`.

## Gestão de alterações

- Cada alteração significativa de método deve registrar versão e motivo.
- Um modelo novo só entra na navegação após possuir exemplo e instruções de uso.
- Referências substituídas devem ser revistas para evitar justificativas obsoletas.
- Mudança grande passa por revisão independente, feita por quem não escreveu o texto, antes do merge.
- **Manutenção a partir do uso:** quando a IA erra uma pergunta do gabarito, o erro vira uma pergunta em aberto proposta num relatório, ligada ao documento correspondente. O relatório de `scripts/erros_para_perguntas.py` não altera documento aprovado. A correção entra numa versão nova, em rascunho, e passa pela aprovação de quem tem a palavra final. O ciclo é usar, detectar, corrigir, validar e republicar. Ele completa a revisão por calendário (`review_interval`) e não a substitui (I-29, ADR 0029).

## Regras adicionais para exemplos de Data Analytics

1. **Unidade antes da fórmula:** diferenciar pedidos, sessões, clientes, itens e eventos antes de mostrar a conta.
2. **Granularidade e junções:** declarar o que cada linha representa, cardinalidade e riscos de multiplicação.
3. **Exemplo numérico verificável:** quando houver valor esperado, fornecer amostra sintética e consulta ou procedimento reproduzível.
4. **Abstenção fundamentada:** incluir pelo menos um exemplo sem cobertura temporal, sem definição ou fora do escopo.
5. **Documentação não é enforcement:** diferenciar gabarito documental, SQL verificado, camada semântica executável e sistema de agentes.
6. **Limite fixo do laboratório:** cada laboratório declara o seu limite de escopo (operações, eventos, dias e incidentes) e não cresce além dele. O Lab 2 segue o limite fixo do ADR 0027, que fecha o ponto em aberto do ADR 0022.
7. **Falta de linha não é zero:** numa tabela agregada, um dia sem linha pode significar zero ou falha de coleta. O exemplo diz qual dos dois, com a política de dia sem linha do Evento de coleta.
8. **Dia incompleto:** um dia recente não entra na conclusão enquanto não estiver completo. No Lab 2, o dia D só fica completo em D+2 às 06h no fuso da operação; antes disso, fica fora da conta. Esse prazo vale para a tabela diária da Aurora e é escolha do time; outra fonte, como o export do GA4 para o BigQuery, pode ter janela própria de chegada tardia, que o exemplo cita quando usa essa fonte.
9. **Cenário só com fonte primária:** cada cenário do banco de cenários cita documentação oficial lida (Google Analytics Help ou Google for Developers). Cenário sem confirmação nessas fontes fica de fora (ADR 0027).
10. **Limiar numérico é escolha do time:** nenhum limiar de alerta é regra universal. Quando um exemplo traz número, diz que é escolha do time que o adota.
11. **Nomes de produção:** os laboratórios usam no SQLite o último trecho do nome de produção (`sessoes_web`, `pedidos`) e documentam o nome completo (`aurora-analytics.web.sessoes_web`, `aurora-analytics.vendas.pedidos`) na amostra, na consulta e no dicionário (ADR 0012 e ADR 0030).

A execução de testes automatizados pode encontrar contradições nos exemplos, mas não prova que um documento de produção é correto. A aprovação do especialista continua indispensável.

## Rubricas

Diferenciar “não avaliável” de nota zero; avaliar o trabalho, nunca a pessoa; a rubrica não aprova nem decide sozinha. Quando a nota alimenta outro documento, a ligação fica escrita nos dois.

## Como validar o próprio framework

O [plano de validação exploratória](PLANO_VALIDACAO.md) propõe exercícios com pessoas técnicas e não técnicas. Não marcar como “validado por usuários” um material que apenas passou pelo build do Astro. O protocolo do piloto, que é o portão da v1.0, está em [docs/piloto/README.md](piloto/README.md).
