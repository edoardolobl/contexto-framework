# Modelos, exemplos e o universo Aurora

Data: 2026-11-17 · Commit: d08c810 · Escopo: os 10 tipos de modelo para download (`public/downloads/template-*.md` e `template-*.yaml`), os exemplos com lacunas e completos, a cópia histórica do indicador 1.0, o Laboratório Aurora (`aurora-fixture.sql`, `aurora-reference-query.sql`, `scripts/check_analytics_fixture.py`) e as páginas e componentes que mostram esses arquivos no portal.

## Resumo

- O núcleo é bom e deve ser mantido: a disciplina de `null` com pergunta em aberto, os pares com lacunas e completo, o histórico de versões que explica a mudança na regra e o Laboratório Aurora, cujas contas (25%, 40% e 50%) conferem na amostra e são refeitas por um verificador.
- O caso real 1 do mantenedor (evento do tag plan marcado como quebrado no Databricks porque é raro ou dispara só numa operação) não tem lugar nos modelos nem nos exemplos. Nenhum modelo registra volume esperado, sazonalidade, quando zero é normal ou segmentação obrigatória por operação, e não existe tipo para plano de mensuração, GA4/GTM ou fonte de dados (MOD-01, MOD-02, MOD-08, AUR-01).
- O caso real 2 (indicador genérico do treinamento) está bem coberto: o conflito de 50% contra 25% entre dashboards, os significados em outras áreas e o gabarito com responder, esclarecer e abster são moldes fortes.
- A sensação de colcha de retalhos tem causas concretas: o .md e o .yaml do mesmo tipo pedem campos diferentes, o cabeçalho comum varia entre os 10 tipos, a pergunta em aberto aparece em quatro formatos, e o mesmo tipo tem até seis nomes (MOD-04, MOD-05, MOD-07, MOD-15).
- O eixo de versionamento, que é a promessa central, perde credibilidade em exemplos que contradizem a própria regra: a cópia histórica da versão 1.0 cita a 2.0, rascunhos de julho citam registros de outubro e rascunhos afirmam e perguntam a mesma coisa (MOD-12, AUR-03, AUR-04, AUR-08).
- O analista não técnico baixa um formulário .md vazio: nenhum dos 20 arquivos de modelo traz um exemplo Aurora no lugar onde se escreve, e os exemplos para download existem só em YAML (MOD-03, AUR-13).

## Pontos fortes (manter)

### Cabeçalho de identificação uniforme nos 10 modelos .md

A mesma tabela de identificação, com os mesmos rótulos em português e os mesmos estados, se repete em todos os tipos. Isso dá previsibilidade ao público misto e serve de base para padronizar o resto.

- [public/downloads/template-kpi.md:11](../public/downloads/template-kpi.md#L11) `| Identificador do assunto (estável) **(obrigatório)** | |`
- [public/downloads/template-conceito.md:11](../public/downloads/template-conceito.md#L11) `| Identificador do assunto (estável) **(obrigatório)** | |`
- [public/downloads/template-kpi.md:24](../public/downloads/template-kpi.md#L24) `Estados possíveis: **Rascunho**, **Pendente de aprovação**, **Aprovado**, **Obsoleto**.`

### Disciplina de null e pergunta em aberto com impacto e responsável

A regra é não trocar o desconhecido por um palpite e registrar a pergunta, o impacto e quem resolve. Isso ataca o erro do caso 2 do mantenedor, em que a IA preenche a lacuna com a definição genérica do treinamento. O exemplo com lacunas mostra o impacto em números.

- [public/downloads/template-kpi.yaml:2](../public/downloads/template-kpi.yaml#L2) `Não troque null por um palpite: registre a dúvida em open_questions.`
- [public/downloads/template-kpi.yaml:69](../public/downloads/template-kpi.yaml#L69) `impact: null            # o que dá errado enquanto ela não tem resposta`
- [public/downloads/exemplo-kpi-lacunas.yaml:66](../public/downloads/exemplo-kpi-lacunas.yaml#L66) `impact: "Na mesma amostra, uma leitura pode dar o dobro da outra"`

### Pares com lacunas e completo, com histórico que explica a mudança na regra

Cada tipo mostra o mesmo documento antes e depois da decisão, e o histórico registra o que mudou na regra e por quê. É o tipo de molde que o mantenedor pede.

- [public/downloads/exemplo-kpi-completo.yaml:20](../public/downloads/exemplo-kpi-completo.yaml#L20) `change: "O numerador passa a contar sessões únicas com pedido confirmado. Antes contava pedidos, o que inflava a taxa`
- [public/downloads/exemplo-dataset-completo.yaml:22](../public/downloads/exemplo-dataset-completo.yaml#L22) `change: "Documentado que session_date é data local sem hora, depois de dúvida sobre fuso no fechamento diário`

### Laboratório Aurora com números calculados, reproduzíveis e coerentes entre arquivos

A amostra SQL, a consulta de referência, o dicionário, o relacionamento, o indicador, o dashboard e o gabarito chegam aos mesmos números. Na amostra, S1, S2, S5 e S6 são elegíveis e só S1 converte (25%). Sem o filtro de sessão interna, S3 entra e converte (2 em 5, 40%). Pela fórmula 1.0, O1 e O2 dão 2 pedidos em 4 sessões (50%). É o único exemplo de consulta com várias tabelas e deve ser o núcleo do trilho de dados.

- [public/downloads/aurora-reference-query.sql:5](../public/downloads/aurora-reference-query.sql#L5) `-- Resultado esperado: 25.0.`
- [public/downloads/exemplo-dataset-completo.yaml:97](../public/downloads/exemplo-dataset-completo.yaml#L97) `Sem esse filtro, a taxa de 01/10 passa de 25% para 40%`
- [public/downloads/exemplo-casos-teste-completo.yaml:57](../public/downloads/exemplo-casos-teste-completo.yaml#L57) `reference_answer: "50% é pedidos confirmados por sessão elegível (2 em 4). O indicador conta sessões: S1 conta uma vez, o que dá 25%"`
- [src/components/AnalyticsLabDownloads.astro:5](../src/components/AnalyticsLabDownloads.astro#L5) `note:'SQLite · DDL e 12 registros'`

### Verificador automático liga YAML, página e SQLite

O script confere os comportamentos esperados de Q01 a Q07, as fórmulas das duas versões do indicador, o numerador nulo do rascunho e as colunas do dicionário contra o schema real. Sustenta a regra editorial de números calculados, não digitados.

- [scripts/check_analytics_fixture.py:63](../scripts/check_analytics_fixture.py#L63) `base = {"Q01": "answer", "Q02": "answer", "Q03": "clarify", "Q04": "abstain", "Q05": "abstain", "Q06": "abstain"}`
- [scripts/check_analytics_fixture.py:86](../scripts/check_analytics_fixture.py#L86) `if rate_with_internal != "40%":`
- [scripts/check_analytics_fixture.py:141](../scripts/check_analytics_fixture.py#L141) `if set(documented) != real_columns:`
- [docs/CONTRATO_EDITORIAL.md:94](../docs/CONTRATO_EDITORIAL.md#L94) `6. **Datas conferidas:** dia da semana, prazos em dias úteis`

### Versionamento propagado entre documentos ligados

A mudança de 15/09 chega ao indicador, ao relacionamento e ao dashboard na mesma data, com `valid_to` exclusivo da 1.0 em 2026-09-15 e o texto "vigente de 15/08 a 14/09" na página.

- [public/downloads/historico/exemplo-kpi-v1.0.yaml:12](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L12) `valid_to: "2026-09-15"  # fim exclusivo da vigência; null = sem fim documentado`
- [public/downloads/exemplo-relacionamento-completo.yaml:18](../public/downloads/exemplo-relacionamento-completo.yaml#L18) `change: "Incluída a regra de contar sessão distinta, acompanhando a versão 2.0 do KPI-AURORA-001"`
- [public/downloads/exemplo-dashboard-completo.yaml:22](../public/downloads/exemplo-dashboard-completo.yaml#L22) `change: "Cartão passa a seguir a versão 2.0 do KPI-AURORA-001. Incluído aviso de que valores anteriores não são comparáveis"`
- [src/content/docs/templates/kpi.mdx:48](../src/content/docs/templates/kpi.mdx#L48) `A versão 1.0, vigente de 15/08 a 14/09, contava **pedidos** confirmados por sessão`

### Conflito entre dashboards, riscos de junção e significados em outras áreas

O Resumo da Diretoria mostra 50% e o dashboard oficial 25% para o mesmo dia, com causa registrada. É o caso 2 do mantenedor (número concreto, mas falso para o contexto) transformado em molde. Os campos de risco de duplicação na junção e de outros significados do termo cobrem o cenário de várias tabelas.

- [public/downloads/exemplo-dashboard-completo.yaml:58](../public/downloads/exemplo-dashboard-completo.yaml#L58) `shows: "Conversão web em 01/10/2026: 50%"`
- [public/downloads/exemplo-dashboard-completo.yaml:59](../public/downloads/exemplo-dashboard-completo.yaml#L59) `cause: "Continua com a fórmula da versão 1.0 do KPI-AURORA-001: conta pedidos confirmados por sessão, não sessões convertidas"`
- [public/downloads/exemplo-relacionamento-completo.yaml:52](../public/downloads/exemplo-relacionamento-completo.yaml#L52) `- "S1 possui O1 e O2: a linha de S1 aparece duas vezes na junção"`
- [public/downloads/exemplo-kpi-completo.yaml:36](../public/downloads/exemplo-kpi-completo.yaml#L36) `- "Conversão de lead: outro indicador, não usar como sinônimo"`

### Caso-limite S3 mostra o valor de documentar um 0/1

A sessão interna com compra real de funcionário mostra, com número, que o nome da coluna não basta (25% contra 40%). É o tipo de regra de negócio que faltou no caso real do Antigravity.

- [src/content/docs/templates/dataset.mdx:22](../src/content/docs/templates/dataset.mdx#L22) `Quem calcula a conversão web de 01/10 sem saber o que essa coluna significa conta **5 sessões, 2 com pedido confirmado: 40%**.`
- [public/downloads/exemplo-dataset-completo.yaml:66](../public/downloads/exemplo-dataset-completo.yaml#L66) `1 = sessão aberta na rede do escritório da Aurora: testes da equipe, demonstrações e compras de funcionários.`

### Gabarito com responder, esclarecer e abster, inclusive entre versões

O modelo de perguntas de referência separa perguntas respondíveis, ambíguas e fora de cobertura. O exemplo inclui uma pergunta de comparabilidade entre datas, e a contagem da página do laboratório bate com o YAML.

- [public/downloads/template-casos-teste.yaml:31](../public/downloads/template-casos-teste.yaml#L31) `expected_behavior: null  # answer | clarify | abstain`
- [public/downloads/exemplo-casos-teste-completo.yaml:117](../public/downloads/exemplo-casos-teste-completo.yaml#L117) `Os dois números medem coisas diferentes, e a diferença entre eles não é variação de conversão`
- [public/downloads/exemplo-casos-teste-completo.yaml:85](../public/downloads/exemplo-casos-teste-completo.yaml#L85) `reason_if_abstain: "Fora do escopo declarado: o indicador não foi definido para app. Encaminhar a quem responde pelo KPI"`
- [src/content/docs/exemplos/analytics-integrado.mdx:93](../src/content/docs/exemplos/analytics-integrado.mdx#L93) `uma respondível (25%), duas de explicação (por que não 50%, e por que 01/10 não se compara com 10/09), uma ambígua e três sem número`

### Rubrica com âncoras observáveis e calibração com conta correta

As âncoras descrevem comportamentos verificáveis. As notas de calibração conferem com a fórmula e os pesos 40, 25, 20 e 15: os níveis 1, 1, 1 e 3 dão 32,5, e os níveis 4, 3, 4 e 3 dão 90.

- [public/downloads/exemplo-rubrica-completo.yaml:86](../public/downloads/exemplo-rubrica-completo.yaml#L86) `formula: "Soma de (nível ÷ 4 × peso) dos critérios avaliados, de 0 a 100"`
- [public/downloads/exemplo-rubrica-completo.yaml:102](../public/downloads/exemplo-rubrica-completo.yaml#L102) `score: 32.5`

### Casos de marketing realistas e com contas que fecham

Prazos em dias úteis, nota da rubrica e contagens do conceito fecham. Detalhes como 41 reclamações no SAC sobre frete na região Norte soam como operação real.

- [src/content/docs/templates/processo.mdx:89](../src/content/docs/templates/processo.mdx#L89) `Prazo: 3 dias úteis, até 21/09; depois disso, escala à Diretoria de Marketing`
- [public/downloads/exemplo-rubrica-completo.yaml:18](../public/downloads/exemplo-rubrica-completo.yaml#L18) `Motivo: 41 reclamações no SAC em agosto sobre frete grátis negado na região Norte`
- [src/content/docs/templates/conceito.mdx:29](../src/content/docs/templates/conceito.mdx#L29) `| **Total** | **214** | **214** | **131** |`

### Avisos honestos sobre o que o modelo não é

Cada YAML declara que é convenção documental e não especificação executável, o que dá credibilidade e evita promessas falsas.

- [public/downloads/template-dataset.yaml:1](../public/downloads/template-dataset.yaml#L1) `# Convenção documental, não é schema executável de fornecedor.`
- [public/downloads/template-decisao.yaml:1](../public/downloads/template-decisao.yaml#L1) `# Contrato documental; não é executável DMN.`

### Roteiro de revisão alinhado às oito dimensões e com evidência por afirmação

O roteiro pede a fonte exata de cada afirmação, não uma fonte genérica, e separa cobertura, consistência e confirmação.

- [public/downloads/roteiro-revisao-documental.md:37](../public/downloads/roteiro-revisao-documental.md#L37) `Registre separadamente as **afirmações relevantes** do documento, não apenas uma fonte genérica para todo o arquivo.`
- [public/downloads/roteiro-revisao-documental.md:66](../public/downloads/roteiro-revisao-documental.md#L66) `**Não marque “aprovado” somente porque todas as dimensões foram preenchidas.**`

## Índice de achados

Os prefixos indicam a frente de análise: MOD para a estrutura dos modelos e AUR para o conteúdo do universo Aurora. Alguns pares tratam do mesmo problema por ângulos diferentes; cada achado aponta o par em **Relacionado**.

| ID | Severidade | Título |
|---|---|---|
| MOD-01 | Alta | Nenhum modelo registra volume esperado, sazonalidade ou quando zero é normal |
| MOD-02 | Alta | Faltam tipos centrais: plano de mensuração, fonte de dados, glossário e banco de perguntas |
| AUR-01 | Alta | Universo sem tag plan, GA4/GTM, mídia, várias operações ou histórico |
| MOD-03 | Média | Os modelos .md, indicados ao público não técnico, não trazem exemplo preenchido |
| AUR-13 | Média | Os 20 arquivos de modelo não trazem nenhum exemplo Aurora embutido |
| MOD-04 | Média | A paridade entre .md e .yaml está quebrada, embora o portal diga que o conteúdo é o mesmo |
| MOD-05 | Média | O cabeçalho YAML comum não é igual nos 10 tipos |
| MOD-06 | Média | Listas vazias não mostram o formato esperado, e os exemplos criam estruturas próprias |
| MOD-07 | Média | O formato de open_questions muda conforme a página, e o modelo não registra a resolução |
| MOD-08 | Média | Não há campo para segmentação obrigatória por operação, país, marca ou plataforma |
| MOD-18 | Média | Não há onde registrar incidentes de coleta e problemas de qualidade com período |
| MOD-10 | Média | Chaves e valores enumerados em inglês, sem dicionário de campos publicado |
| AUR-02 | Média | Exemplos aprovados preenchem os campos operacionais com "laboratório" |
| AUR-06 | Média | O exemplo de session_date em setembro contradiz Q05, e o dicionário não declara cobertura temporal |
| AUR-05 | Média | Pedido TEST numa sessão não interna, sem regra documentada |
| MOD-11 | Média | Exemplos com lacunas contradizem a regra de campos obrigatórios e o estado pendente de aprovação |
| MOD-12 | Média | A versão histórica 1.0 do indicador cita a versão 2.0, que ainda não existia |
| AUR-04 | Média | A cópia histórica do indicador 1.0 foi escrita com conhecimento da versão 2.0 |
| AUR-03 | Média | Documentos de julho e agosto citam registros de 01/10 e a consulta da versão 2.0 |
| AUR-08 | Média | Rascunhos 0.1 afirmam e perguntam a mesma coisa |
| MOD-09 | Baixa | Os exemplos do laboratório deixam como não aplicáveis os campos que mais importam em produção |
| MOD-17 | Baixa | A consulta verificada não é um bloco estruturado próprio |
| MOD-19 | Baixa | Moeda e unidades monetárias não têm campo nem exemplo |
| MOD-20 | Baixa | O histórico de versões não aponta para a cópia integral arquivada |
| MOD-16 | Baixa | A vigência final tem significados diferentes no .md e no YAML |
| MOD-13 | Baixa | O exemplo de decisão com lacunas se contradiz sobre os campos do brief |
| MOD-14 | Baixa | Convenção de identificadores e de referências cruzadas inconsistente |
| MOD-15 | Baixa | O tipo perguntas de referência tem vários nomes diferentes |
| MOD-21 | Baixa | Inconsistências visuais entre os arquivos de modelo |
| AUR-12 | Baixa | Amostra mínima limita a demonstração de consultas complexas |
| AUR-09 | Baixa | Estado dos rascunhos e das cópias históricas diverge do vocabulário publicado |
| AUR-10 | Baixa | O gabarito fixa só a versão do indicador, embora dependa de outros documentos |
| AUR-15 | Baixa | O indicador 1.0 entrou em vigor antes dos documentos de dados que cita como autoridade |
| AUR-07 | Baixa | BeforeAfter mostra a fórmula final num estado pendente, contra a linha do tempo do indicador |
| AUR-11 | Baixa | Página e YAML divergem sobre quem conferiu o gabarito |
| AUR-14 | Baixa | Três aprovações datadas em sábado |
| AUR-16 | Baixa | O rascunho da rubrica cita a etapa 3 de um processo que só tem duas etapas |
| AUR-17 | Baixa | Dados da amostra duplicados à mão em componentes e páginas, com verificação parcial |
| AUR-19 | Baixa | Nomes divergentes para a fonte oficial da política e exceção diferente da aprovada |
| AUR-20 | Baixa | A ficha HANDOFF-001 foge do padrão dos documentos Aurora |
| AUR-21 | Baixa | Aviso de que a Aurora é inventada ausente nos SQL e presente fora dos lugares previstos |
| MOD-22 | Info | Cinco dos dez tipos usam exemplos fora de dados e analytics |

## Achados

### MOD-01 · Nenhum modelo registra volume esperado, sazonalidade ou quando zero é normal

**Severidade:** Alta

**Confiança:** Alta

**O que acontece:** Os modelos de KPI, dataset e dashboard não têm campo para a frequência esperada de um evento ou indicador, a raridade, a sazonalidade, o limiar de alerta ou a condição em que zero é esperado. O único tratamento de zero é a divisão por zero. O dashboard tem `comparison_baseline`, mas é o período de comparação do cartão, não um volume esperado. O .md do dashboard pede limiares aprovados, e o YAML não tem esse campo. Não há nenhuma ocorrência de "sazonal" ou "seasonal" em `public` nem em `src`.

**Evidências:**

- [public/downloads/template-kpi.yaml:47](../public/downloads/template-kpi.yaml#L47) `zero_denominator_policy: null`
- [public/downloads/template-kpi.yaml:46](../public/downloads/template-kpi.yaml#L46) `null_handling: null`
- [public/downloads/template-dashboard.md:41](../public/downloads/template-dashboard.md#L41) `- Agregações e limiares aprovados:`
- [public/downloads/template-dashboard.yaml:32](../public/downloads/template-dashboard.yaml#L32) `comparison_baseline: null`

**Impacto:** É o caso 1 do mantenedor. Um agente que cruza o tag plan com o Databricks não tem onde ler que um evento é raro, que costuma ficar dias sem disparar ou que só dispara numa operação. Por isso marca como quebrado algo que está normal. O modelo também não ensina a fazer a pergunta que evitaria o falso alarme.

**Recomendação:** Criar um bloco comum de comportamento esperado (por exemplo, `expected_behavior` ou `expectativa`) com volume típico por período e segmento, janela mínima de observação antes de concluir que o evento parou, sazonalidade conhecida, quando zero é esperado, limiar de alerta e janela de comparação. Esse bloco entra no novo tipo de plano de mensuração (MOD-02) e no KPI. Os exemplos devem incluir um evento raro, com a instrução de olhar um histórico (por exemplo, 28 dias) antes de declarar quebra.

**Relacionado:** MOD-02, MOD-08, AUR-01.

### MOD-02 · Faltam tipos centrais: plano de mensuração, fonte de dados, glossário e banco de perguntas

**Severidade:** Alta

**Confiança:** Alta

**O que acontece:** Os 10 tipos são conceito, processo, decisão, política, rubrica, KPI, dataset, relacionamento, dashboard e perguntas de referência. Não há modelo de plano de mensuração ou tag plan, com evento, gatilho, parâmetros, onde dispara e estado. Também não há modelo de fonte de dados ou conexão, com sistema, conector, acesso, atraso e responsável. O glossário existe só como um conceito por arquivo, e as perguntas de negócio existem só como gabarito de verificação. Não há nenhuma ocorrência de GA4, GTM, tag plan ou tag manager em `public` nem em `src`.

**Evidências:**

- [src/content/docs/templates/index.mdx:21](../src/content/docs/templates/index.mdx#L21) `| Explicar como um indicador é calculado | [Indicador (KPI)](kpi/) | [Baixar](../downloads/template-kpi.md) |`
- [src/content/docs/templates/index.mdx:25](../src/content/docs/templates/index.mdx#L25) `| Definir perguntas que o acervo deve responder | [Perguntas de referência](casos-teste/) | [Baixar](../downloads/template-casos-teste.md) |`
- [src/content/docs/dados/visao-geral.mdx:24](../src/content/docs/dados/visao-geral.mdx#L24) `| Camada | Qual pergunta responde? | Modelo |`
- [public/downloads/template-casos-teste.yaml:1](../public/downloads/template-casos-teste.yaml#L1) `# Gabarito documental, não resultado de teste de um modelo de IA.`
- [public/downloads/template-conceito.md:12](../public/downloads/template-conceito.md#L12) `| Tipo de documento | Conceito ou termo de glossário |`

**Impacto:** O público-alvo trabalha com GTM, GA4, plataformas de mídia, BigQuery e Databricks, mas não encontra ponto de partida para o artefato que mais usa, o tag plan. Também não há onde registrar de qual conector vem cada dado. O mantenedor quer ensinar a pessoa a formular perguntas de negócio, mas o único lugar para elas é um gabarito de verificação feito depois da documentação.

**Recomendação:** Priorizar um tipo de plano de mensuração: evento, definição de negócio, gatilho, parâmetros e tipos, onde dispara por operação, marca ou país, comportamento esperado (MOD-01), tabela de destino no warehouse, estado e responsável. Depois, um tipo de fonte de dados ou conexão e um banco de perguntas de negócio usado como ponto de entrada, que aponta para os documentos que cada pergunta exige. Avaliar o glossário como índice de conceitos, não como um arquivo por termo. Antes de fixar os campos, comparar com planos de rastreamento de mercado e com contratos de dados; essas referências devem ser confirmadas na frente de literatura.

**Relacionado:** MOD-01, AUR-01.

### AUR-01 · Universo sem tag plan, GA4/GTM, mídia, várias operações ou histórico

**Severidade:** Alta

**Confiança:** Alta

**O que acontece:** O trilho de Analytics da Aurora gira em torno de uma taxa de conversão de e-commerce num único dia. Não há exemplo de plano de tagueamento, evento de GA4/GTM, plataforma de mídia, operação ou unidade de negócio, nem regra do tipo "evento raro: olhar o histórico" ou "separar por operação". Uma busca por GA4, GTM, tag plan, tagueamento, BigQuery, Databricks e UTM em `src` e `public/downloads` só encontra links de fundamentação. Os outros exemplos completos ficam em RH e Financeiro.

**Evidências:**

- [public/downloads/aurora-fixture.sql:3](../public/downloads/aurora-fixture.sql#L3) `-- O indicador usa só 01/10, canal web, sem sessões internas; S3 (interna) e S4 (app) estão na amostra para mostrar os filtros.`
- [README.md:20](../README.md#L20) `- Exemplos comentados em RH, Marketing, Financeiro e Analytics.`
- [public/downloads/exemplo-conceito-completo.yaml:31](../public/downloads/exemplo-conceito-completo.yaml#L31) `domain: "Programa voluntário de integração: Aurora"`
- [public/downloads/exemplo-politica-completo.yaml:4](../public/downloads/exemplo-politica-completo.yaml#L4) `title: "Despesas em eventos: Aurora"`
- [src/content/docs/referencias/index.mdx:39](../src/content/docs/referencias/index.mdx#L39) `| [Databricks: Tune Genie Agent quality](https://docs.databricks.com/gcp/en/genie/add-instructions) |`

**Impacto:** O analista com o problema "quais eventos do tag plan estão zerados no Databricks" não encontra molde para documentar a frequência normal do evento, a operação em que ele dispara e a janela mínima de histórico. A IA continuaria marcando como quebrado um evento raro ou exclusivo de uma operação.

**Recomendação:** Ampliar o universo Aurora com um segundo laboratório de tagueamento: tag plan (evento, gatilho, operação, frequência esperada, criticidade), tabela de eventos diários com duas operações e um evento raro, e gabarito com a pergunta "quais eventos pararam?", cuja resposta esperada exige comparar por operação e com o histórico. Reaproveitar os tipos existentes (dataset, relacionamento, KPI, perguntas de referência) e o novo tipo de plano de mensuração.

**Observação da verificação:** a busca sem distinção de maiúsculas por `ga4|gtm|tag plan|bigquery|utm|mídia` em `src` e `public/downloads` retornou só links de fundamentação (Snowflake e Databricks), nenhum exemplo.

**Relacionado:** MOD-01, MOD-02, MOD-08, AUR-12.

### MOD-03 · Os modelos .md, indicados ao público não técnico, não trazem exemplo preenchido

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O portal recomenda o Markdown a quem não é da área técnica. Os 10 modelos .md para download, porém, são listas de rótulos sem conteúdo de exemplo. As ocorrências de "exemplo" neles são nomes de campo, exceto uma dica de fórmula na rubrica. Todos os exemplos para download são YAML, e não existe versão .md preenchida. Atenuante: cada página de modelo mostra os exemplos YAML já em português (aba "O que diz", componente `ExampleDoc`). A pessoa vê um exemplo no site, mas não leva um .md preenchido para usar de molde.

**Evidências:**

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:6](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L6) `O **Markdown** é texto comum, com perguntas para responder: use este se você não é da área técnica.`
- [public/downloads/template-kpi.md:37](../public/downloads/template-kpi.md#L37) `- Numerador (definição e critérios):`
- [src/components/TemplateDownloads.astro:64](../src/components/TemplateDownloads.astro#L64) `{ name: 'Exemplo com lacunas', href: 'exemplo-kpi-lacunas.yaml', format: 'YAML · nada aprovado' },`
- [src/components/TemplateDownloads.astro:65](../src/components/TemplateDownloads.astro#L65) `{ name: 'Exemplo completo', href: 'exemplo-kpi-completo.yaml', format: 'YAML · aprovado' },`
- [src/content/docs/templates/kpi.mdx:44](../src/content/docs/templates/kpi.mdx#L44) `<ExampleDoc file="exemplo-kpi-completo.yaml" />`

**Impacto:** Vai contra o pedido do mantenedor de modelos com exemplos realistas que sirvam de molde no próprio arquivo. O analista não técnico baixa um formulário vazio. Para comparar enquanto preenche, precisa voltar ao site ou abrir um YAML com chaves em inglês.

**Recomendação:** Publicar, para cada tipo, o exemplo completo também em .md, gerado do mesmo YAML para não divergir. No .md vazio, colocar uma linha curta de exemplo em cada campo crítico (por exemplo, "Numerador: sessões elegíveis com pelo menos um pedido CONFIRMED; uma sessão com dois pedidos conta uma vez").

**Relacionado:** AUR-13.

### AUR-13 · Os 20 arquivos de modelo não trazem nenhum exemplo Aurora embutido

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Os 20 arquivos `template-*.md` e `template-*.yaml` têm zero menções à Aurora. Os campos do modelo são perguntas e rótulos genéricos, e o exemplo concreto só existe em arquivos separados. O mantenedor pediu que os próprios modelos sirvam de molde.

**Evidências:**

- [public/downloads/template-kpi.md:37](../public/downloads/template-kpi.md#L37) `- Numerador (definição e critérios):`
- [public/downloads/template-kpi.md:3](../public/downloads/template-kpi.md#L3) `Um campo em branco é melhor do que um palpite.`

**Impacto:** O público não técnico abre o modelo e não vê, no lugar onde vai escrever, como fica uma boa resposta.

**Recomendação:** Acrescentar a cada campo do modelo .md uma linha curta "Exemplo Aurora:", gerada a partir do exemplo completo para não divergir.

**Observação da verificação:** a contagem sem distinção de maiúsculas de "aurora" em `public/downloads/template-*` retornou 0 nos 20 arquivos.

**Relacionado:** MOD-03.

### MOD-04 · A paridade entre .md e .yaml está quebrada, embora o portal diga que o conteúdo é o mesmo

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Vários campos existem num formato e não no outro. Dashboard: limiares, o que fazer com categoria inexistente, reprocessamentos e mudanças na coleta só existem no .md. Processo: sistemas oficiais, condição para executar a etapa e quem recebe a informação só existem no .md. KPI e decisão: quando revisar só existe no .md, e os testes do KPI só no YAML. O .md de KPI não pede domínio, que o YAML tem. O .md de conceito não pede quando não se aplica, que o YAML tem como `context.does_not_apply_when`.

**Evidências:**

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:6](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L6) `O conteúdo é o mesmo.`
- [public/downloads/template-dashboard.md:48](../public/downloads/template-dashboard.md#L48) `- Reprocessamentos históricos:`
- [public/downloads/template-dashboard.md:52](../public/downloads/template-dashboard.md#L52) `- Mudanças na coleta de dados ou na definição:`
- [public/downloads/template-processo.md:38](../public/downloads/template-processo.md#L38) `- Sistemas e evidências oficiais:`
- [public/downloads/template-kpi.md:61](../public/downloads/template-kpi.md#L61) `- Quando este indicador deve ser revisto:`
- [public/downloads/template-kpi.yaml:65](../public/downloads/template-kpi.yaml#L65) `tests: []`
- [public/downloads/template-conceito.yaml:27](../public/downloads/template-conceito.yaml#L27) `does_not_apply_when: null`

**Impacto:** Quem preenche o .md e depois converte para YAML, ou o contrário, perde informação sem perceber. Um agente que lê o YAML não encontra o que o time escreveu no .md, por exemplo uma mudança na coleta de dados, que é central no caso do tag plan.

**Recomendação:** Definir um esquema único por tipo (por exemplo, JSON Schema) e gerar o .md e o .yaml a partir dele, com uma tabela de correspondência entre rótulo e chave. Incluir uma verificação automática de paridade no build.

**Relacionado:** MOD-05, MOD-06, MOD-10, MOD-21.

### MOD-05 · O cabeçalho YAML comum não é igual nos 10 tipos

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** `last_reviewed` existe só em conceito, KPI e política. `domain` fica no topo em KPI e perguntas de referência, dentro de `context` em conceito e não existe nos outros 7. `related_documents` falta no modelo de perguntas de referência. A ordem dos campos do KPI difere da dos demais (`domain`, `status`, `owner` e `approver` vêm antes de `version`). Nenhum .md pede a data da última revisão. Só os .md de conceito e de perguntas de referência pedem domínio, e mesmo assim no corpo, não na tabela de identificação.

**Evidências:**

- [public/downloads/template-kpi.yaml:10](../public/downloads/template-kpi.yaml#L10) `domain: null`
- [public/downloads/template-kpi.yaml:19](../public/downloads/template-kpi.yaml#L19) `last_reviewed: null`
- [public/downloads/template-dataset.yaml:15](../public/downloads/template-dataset.yaml#L15) `source_of_truth: null`
- [public/downloads/template-conceito.yaml:24](../public/downloads/template-conceito.yaml#L24) `  domain: null`
- [public/downloads/template-casos-teste.yaml:22](../public/downloads/template-casos-teste.yaml#L22) `domain: null`
- [public/downloads/template-conceito.md:28](../public/downloads/template-conceito.md#L28) `- Em que domínio é usado?`

**Impacto:** Um agente ou script que indexa o acervo não consegue filtrar por domínio nem achar documentos sem revisão recente de forma uniforme. O conjunto parece colcha de retalhos, como diz o mantenedor.

**Recomendação:** Fixar um cabeçalho único e obrigatório, na mesma ordem nos 10 tipos: `id`, `revision_id`, `title`, `type`, `domain`, `status`, `owner`, `approver`, `version`, `version_date`, `valid_from`, `valid_to`, `supersedes_revision`, `last_reviewed`, `source_of_truth`, `version_history`, `open_questions` e `related_documents`. Levar domínio e última revisão para a tabela de identificação do .md.

**Relacionado:** MOD-04, MOD-14.

### MOD-06 · Listas vazias não mostram o formato esperado, e os exemplos criam estruturas próprias

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Vários campos estruturados aparecem no modelo só como lista vazia: tabela de decisão, chaves de junção, fontes em conflito, exemplos de calibração e perguntas e respostas do KPI. Os exemplos completos usam objetos com subcampos que o modelo não anuncia: `name` e `allowed_values` nas entradas, `when` e `then` na tabela de decisão, `left` e `right` nas chaves de junção, e `positions`, `resolution` e `resolved_at` nas fontes em conflito.

**Evidências:**

- [public/downloads/template-decisao.yaml:29](../public/downloads/template-decisao.yaml#L29) `decision_table: []`
- [public/downloads/template-relacionamento.yaml:29](../public/downloads/template-relacionamento.yaml#L29) `join_keys: []`
- [public/downloads/template-politica.yaml:46](../public/downloads/template-politica.yaml#L46) `conflicting_sources: []`
- [public/downloads/template-rubrica.yaml:51](../public/downloads/template-rubrica.yaml#L51) `calibration_examples: []`
- [public/downloads/exemplo-decisao-completo.yaml:47](../public/downloads/exemplo-decisao-completo.yaml#L47) `  - when: {brief_complete: false, evidence_sufficient: any}`
- [public/downloads/exemplo-politica-completo.yaml:62](../public/downloads/exemplo-politica-completo.yaml#L62) `  - id: CONFLICT-001`

**Impacto:** Cada time inventa uma forma diferente de preencher a mesma lista. Isso quebra a consistência entre documentos e impede que um agente leia de forma confiável, por exemplo, as chaves de junção.

**Recomendação:** Mostrar no modelo um item de exemplo com todos os subcampos em `null`, como já é feito em `open_questions`, nos passos do processo e nos testes da decisão. Documentar cada subcampo no esquema único do MOD-04.

### MOD-07 · O formato de open_questions muda conforme a página, e o modelo não registra a resolução

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Os modelos usam `question`, `impact`, `resolution_owner` e `state`. A página "Descobrir o que falta" (`metodo/elicitar.mdx`) acrescenta `reported_practice` e `authoritative_rule`. A ficha de entrega da página "Revisar e entregar" acrescenta `id` e `priority`, usa `domain_owner` e cria o tipo `documentation_handoff`, que não tem modelo para download. A página "Como ler os campos" diz que a pergunta resolvida leva a resolução, quem resolveu e a data, mas o modelo não tem esses campos. Só o exemplo de política os usa, e dentro de `conflicting_sources`.

**Evidências:**

- [public/downloads/template-kpi.yaml:70](../public/downloads/template-kpi.yaml#L70) `resolution_owner: null  # quem pode resolver`
- [src/content/docs/metodo/elicitar.mdx:29](../src/content/docs/metodo/elicitar.mdx#L29) `reported_practice: "A equipe geralmente exclui cancelamentos."`
- [src/content/docs/validacao/checklist.mdx:86](../src/content/docs/validacao/checklist.mdx#L86) `type: documentation_handoff`
- [src/content/docs/validacao/checklist.mdx:96](../src/content/docs/validacao/checklist.mdx#L96) `priority: null`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:66](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L66) `` | Resolvido | `resolved`, com a resolução, quem resolveu e a data | ``
- [public/downloads/exemplo-politica-completo.yaml:76](../public/downloads/exemplo-politica-completo.yaml#L76) `resolved_at: "2026-08-14"`

**Impacto:** A pergunta em aberto é o centro do método e aparece em quatro formatos. Isso confunde quem aprende e impede que o acervo guarde a trilha de decisão, que é o que torna confiável a documentação versionada.

**Recomendação:** Adotar um só formato de pergunta em aberto em todos os modelos e páginas: `id`, `question`, `reported_practice`, `impact`, `resolution_owner`, `priority`, `state`, `resolution`, `resolved_by` e `resolved_at`. Decidir se a ficha de entrega vira um 11º modelo para download ou sai da página.

**Relacionado:** AUR-20.

### MOD-08 · Não há campo para segmentação obrigatória por operação, país, marca ou plataforma

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O escopo do KPI tem só canais incluídos e excluídos e uma população em texto livre. A granularidade também é texto livre. Não há campo para dizer que o indicador ou evento deve ser analisado separadamente por operação, país ou marca, nem para dizer quais segmentos não podem ser somados ou comparados.

**Evidências:**

- [public/downloads/template-kpi.yaml:34](../public/downloads/template-kpi.yaml#L34) `included_channels: []`
- [public/downloads/template-kpi.yaml:44](../public/downloads/template-kpi.yaml#L44) `granularity: null`
- [public/downloads/exemplo-kpi-completo.yaml:50](../public/downloads/exemplo-kpi-completo.yaml#L50) `granularity: "dia + canal web"`

**Impacto:** No caso 1, o evento disparou numa operação e não na outra. Sem uma regra explícita de separar por operação, o agente soma tudo ou avalia só uma e chega a uma conclusão errada.

**Recomendação:** Acrescentar ao KPI e ao novo plano de mensuração um bloco de segmentação: dimensões obrigatórias de análise (operação, país, marca, plataforma), segmentos em que o item não se aplica e regras de soma entre segmentos. No exemplo, usar duas operações com comportamentos diferentes.

**Relacionado:** MOD-01, AUR-01.

### MOD-18 · Não há onde registrar incidentes de coleta e problemas de qualidade com período

**Severidade:** Média

**Confiança:** Média

**O que acontece:** Problemas conhecidos só aparecem como listas de texto livre (`known_caveats`, `known_limitations`). A pergunta sobre mudanças na coleta existe só no .md do dashboard. Não há estrutura com início, fim, segmento afetado, efeito e correção.

**Evidências:**

- [public/downloads/template-dataset.yaml:54](../public/downloads/template-dataset.yaml#L54) `known_caveats: []`
- [public/downloads/template-dashboard.yaml:38](../public/downloads/template-dashboard.yaml#L38) `known_limitations: []`
- [public/downloads/template-dashboard.md:52](../public/downloads/template-dashboard.md#L52) `- Mudanças na coleta de dados ou na definição:`

**Impacto:** Num tag plan, saber que um evento ficou fora do ar entre duas datas numa operação é o que separa um alerta real de um problema já conhecido. Sem estrutura, o agente não consegue filtrar incidentes por período.

**Recomendação:** Acrescentar um bloco `data_incidents` (início, fim, segmento afetado, sintoma, causa, correção, estado) no dataset, no dashboard e no plano de mensuração.

### MOD-10 · Chaves e valores enumerados em inglês, sem dicionário de campos publicado

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** As chaves YAML e os valores enumerados (por exemplo `one_to_many`, `answer`, `clarify`, `abstain`, `complement_information`, `not_evaluable`) estão em inglês, e os textos em português. A página "Como ler os campos" traduz só o cabeçalho e os estados. Fora dela, a tradução existe apenas em parte, no componente que monta a visualização dos exemplos no site, e inclui rótulos fixos para as entradas do exemplo da Aurora. Chaves como `sentinel_values` e `snapshot_or_events` não aparecem explicadas em nenhuma página de `src/content`.

**Evidências:**

- [public/downloads/template-dataset.yaml:48](../public/downloads/template-dataset.yaml#L48) `snapshot_or_events: null`
- [public/downloads/template-dataset.yaml:38](../public/downloads/template-dataset.yaml#L38) `sentinel_values: []`
- [src/components/ExampleMeaning.astro:47](../src/components/ExampleMeaning.astro#L47) `complement_information: 'Devolver para complementação',`
- [src/components/ExampleMeaning.astro:39](../src/components/ExampleMeaning.astro#L39) `brief_complete: 'Brief completo?',`

**Impacto:** Chaves em inglês ajudam na interoperabilidade com ferramentas e agentes, mas o público não técnico não sabe o que é `sentinel_values` ou `snapshot_or_events` ao abrir o YAML.

**Recomendação:** Manter as chaves em inglês e publicar um dicionário de campos para download, com chave, rótulo em português, explicação e exemplo, gerado do esquema único (MOD-04). Os comentários do YAML vazio devem trazer o rótulo em português de cada chave.

### AUR-02 · Exemplos aprovados preenchem os campos operacionais com "laboratório"

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Os campos que mais importam para uma IA interpretar dado vivo (plataforma, frequência de atualização, latência, frescor) estão preenchidos com valores de laboratório nos exemplos aprovados. Ao mesmo tempo, os documentos apontam como fonte o "Catálogo de dados da Aurora" e o "portal de BI da Aurora", misturando a narrativa de empresa com o artefato de ensino.

**Evidências:**

- [public/downloads/exemplo-dataset-completo.yaml:35](../public/downloads/exemplo-dataset-completo.yaml#L35) `platform: SQLite (laboratório)`
- [public/downloads/exemplo-dataset-completo.yaml:87](../public/downloads/exemplo-dataset-completo.yaml#L87) `update_frequency: "Carga estática do laboratório"`
- [public/downloads/exemplo-dataset-completo.yaml:88](../public/downloads/exemplo-dataset-completo.yaml#L88) `known_latency: "Não aplicável ao laboratório"`
- [public/downloads/exemplo-kpi-completo.yaml:59](../public/downloads/exemplo-kpi-completo.yaml#L59) `data_freshness: "Carga estática no laboratório"`
- [public/downloads/exemplo-dashboard-completo.yaml:49](../public/downloads/exemplo-dashboard-completo.yaml#L49) `latency: "Não aplicável"`
- [public/downloads/exemplo-dashboard-completo.yaml:14](../public/downloads/exemplo-dashboard-completo.yaml#L14) `source_of_truth: "Dashboard Conversão Web no portal de BI da Aurora"`

**Impacto:** Quem copia o exemplo aprende a preencher frescor e latência com "não aplicável", justamente a informação que evitaria falsos "eventos zerados".

**Recomendação:** Separar o laboratório executável (SQLite, tabelas `demo_*`) do documento que serve de molde. Nos YAML aprovados, usar valores de operação plausíveis (por exemplo, exportação diária às 06h, atraso típico de até 24 h) e manter só uma nota dizendo que o laboratório reproduz um recorte disso em SQLite.

**Relacionado:** MOD-09.

### AUR-06 · O exemplo de session_date em setembro contradiz Q05, e o dicionário não declara cobertura temporal

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Q05 cita DATASET-AURORA-SESSIONS como fonte para abster-se por falta de registros de setembro. O mesmo dicionário dá "2026-09-01" como exemplo de valor da coluna e não tem campo que declare o período coberto, só a ressalva genérica de não extrapolar.

**Evidências:**

- [public/downloads/exemplo-dataset-completo.yaml:81](../public/downloads/exemplo-dataset-completo.yaml#L81) `examples: ["2026-09-01"]`
- [public/downloads/exemplo-casos-teste-completo.yaml:94](../public/downloads/exemplo-casos-teste-completo.yaml#L94) `required_sources: ["DATASET-AURORA-SESSIONS"]`
- [public/downloads/exemplo-casos-teste-completo.yaml:95](../public/downloads/exemplo-casos-teste-completo.yaml#L95) `evidence_description: "Não há registros de setembro de 2026"`
- [public/downloads/exemplo-dataset-completo.yaml:96](../public/downloads/exemplo-dataset-completo.yaml#L96) `- "Não extrapolar a amostra para outros períodos ou canais"`

**Impacto:** Um RAG que recupere o dicionário encontra um valor de setembro. A abstenção esperada não tem evidência citável no documento que o gabarito aponta.

**Recomendação:** Trocar o exemplo para "2026-10-01" e acrescentar ao modelo de dataset um campo de cobertura (por exemplo `coverage: {from, to, gaps}`), central também para o caso do evento zerado.

**Relacionado:** MOD-01.

### AUR-05 · Pedido TEST numa sessão não interna, sem regra documentada

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O dicionário de sessões diz que `is_internal = 1` cobre "testes da equipe", e o de pedidos chama TEST de "pedido de teste interno". Na amostra, o pedido O6 TEST está em S5, sessão com `is_internal = 0`. Nenhum YAML explica esse caso. S5 só aparece nas tabelas da página, no diagrama e na lista de sessões elegíveis, e os testes do relacionamento cobrem só S1 e S2.

**Evidências:**

- [public/downloads/aurora-fixture.sql:24](../public/downloads/aurora-fixture.sql#L24) `('S5', 'web', 0, '2026-10-01'),`
- [public/downloads/aurora-fixture.sql:33](../public/downloads/aurora-fixture.sql#L33) `('O6', 'S5', 'TEST');`
- [public/downloads/exemplo-dataset-pedidos-completo.yaml:58](../public/downloads/exemplo-dataset-pedidos-completo.yaml#L58) `TEST: pedido de teste interno, não conta`
- [public/downloads/exemplo-dataset-completo.yaml:66](../public/downloads/exemplo-dataset-completo.yaml#L66) `testes da equipe, demonstrações e compras de funcionários`
- [public/downloads/exemplo-relacionamento-completo.yaml:58](../public/downloads/exemplo-relacionamento-completo.yaml#L58) `- "S2 tem pedido cancelado e não conta como sessão convertida"`
- [src/content/docs/exemplos/analytics-integrado.mdx:48](../src/content/docs/exemplos/analytics-integrado.mdx#L48) `S1, S2, S5 e S6 (**4 sessões**)`

**Impacto:** Uma IA pode concluir que S5 deveria ser interna ou que o filtro está quebrado. Se S5 saísse do denominador, a taxa seria 33%, não 25%; a regra que decide isso não está escrita.

**Recomendação:** Documentar como caso-limite explícito (por exemplo, teste de QA fora da rede do escritório: a sessão conta no denominador, o pedido não conta no numerador), incluir em `validation.test_cases` do relacionamento e, se fizer sentido, criar uma pergunta no gabarito.

**Observação da verificação:** a frente original rodou a amostra no sqlite3 e confirmou que S5 entra nas 4 sessões elegíveis e não no numerador; o resultado de 25% depende dessa regra não escrita. Nesta rodada a conta foi conferida só contra o SQL e os YAML.

### MOD-11 · Exemplos com lacunas contradizem a regra de campos obrigatórios e o estado pendente de aprovação

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O .md marca responsável e quem aprova como obrigatórios para começar. A página "Como ler os campos" define pendente de aprovação como documento estruturado que só espera a confirmação. Mesmo assim, os 10 exemplos com lacunas usam `pending_approval` com `approver` nulo, 9 deles também com `owner` nulo (a rubrica é a exceção), e trazem perguntas estruturais em aberto.

**Evidências:**

- [public/downloads/template-kpi.md:7](../public/downloads/template-kpi.md#L7) `Os campos marcados com **(obrigatório)** são o mínimo para começar.`
- [public/downloads/template-kpi.md:15](../public/downloads/template-kpi.md#L15) `| Quem aprova (cargo ou área) **(obrigatório)** | |`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:57](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L57) `` | Pendente de aprovação | `pending_approval` | Está estruturado, falta quem aprova confirmar | ``
- [public/downloads/exemplo-kpi-lacunas.yaml:7](../public/downloads/exemplo-kpi-lacunas.yaml#L7) `status: pending_approval`
- [public/downloads/exemplo-kpi-lacunas.yaml:9](../public/downloads/exemplo-kpi-lacunas.yaml#L9) `approver: null`

**Impacto:** O exemplo ensina o contrário da regra. O leitor não sabe se pode começar sem responsável, nem quando usar rascunho e quando usar pendente de aprovação.

**Recomendação:** Mudar os exemplos com lacunas para `draft`, ou preencher responsável e quem aprova e deixar as lacunas só no conteúdo. Outra saída é rever a regra de obrigatório para aceitar responsável desconhecido, desde que registrado em `open_questions`.

**Relacionado:** AUR-09.

### MOD-12 · A versão histórica 1.0 do indicador cita a versão 2.0, que ainda não existia

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O arquivo histórico se apresenta como a versão 1.0 aprovada em 2026-08-15. Mesmo assim, o título, os significados em outras áreas e a precedência de fontes mencionam a definição 2.0, de 2026-09-15. O conteúdo aprovado foi alterado depois, em vez de ficar só uma nota de arquivamento separada.

**Evidências:**

- [public/downloads/historico/exemplo-kpi-v1.0.yaml:4](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L4) `title: "Pedidos confirmados por sessão elegível (definição antiga rotulada conversão web)"`
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:33](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L33) `- "Sessões convertidas: definição revisada na versão 2.0"`
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:62](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L62) `A consulta aurora-reference-query.sql implementa a versão 2.0, NÃO a 1.0.`
- [public/downloads/template-kpi.md:75](../public/downloads/template-kpi.md#L75) `**Guarde o documento completo de cada versão aprovada:**`

**Impacto:** O exemplo que deveria ensinar a preservar versões íntegras mostra uma versão alterada depois de aprovada. Isso fragiliza a credibilidade do método de versionamento e confunde agentes que consultam a regra vigente em cada data.

**Recomendação:** Manter o arquivo histórico idêntico ao aprovado em 2026-08-15. Colocar as notas posteriores (substituída pela 2.0, não usar a consulta de referência) num aviso de arquivamento separado, como o comentário da linha 1 ou um campo `archival_note` fora do conteúdo aprovado.

**Relacionado:** AUR-04.

### AUR-04 · A cópia histórica do indicador 1.0 foi escrita com conhecimento da versão 2.0

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O arquivo histórico deveria preservar o que foi aprovado em 15/08, mas título, sinônimos, significados em outros domínios e precedência de fontes mencionam a versão 2.0 e a consulta que a implementa. O próprio portal manda preservar a cópia integral das versões aprovadas. Este achado acrescenta ao MOD-12 a evidência dos sinônimos e da regra do portal.

**Evidências:**

- [public/downloads/historico/exemplo-kpi-v1.0.yaml:4](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L4) `title: "Pedidos confirmados por sessão elegível (definição antiga rotulada conversão web)"`
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:30](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L30) `synonyms: ["conversão web (rótulo histórico impreciso)"]`
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:33](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L33) `- "Sessões convertidas: definição revisada na versão 2.0"`
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:62](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L62) `- "A consulta aurora-reference-query.sql implementa a versão 2.0, NÃO a 1.0. Não a utilizar para reconstruir esta fórmula histórica."`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:82](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L82) `3. **Preserve a cópia integral das versões aprovadas.**`

**Impacto:** O exemplo ensina, sem querer, que a versão arquivada pode ser reescrita depois. Um agente que use a 1.0 para responder sobre agosto recebe termos que não existiam na época.

**Recomendação:** Manter o conteúdo da 1.0 como aprovado em 15/08 e colocar as notas posteriores num campo separado de arquivamento (por exemplo `archival_note`, `superseded_by`), datado no arquivamento.

**Relacionado:** MOD-12, MOD-20.

### AUR-03 · Documentos de julho e agosto citam registros de 01/10 e a consulta da versão 2.0

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** Os registros S1 e O1/O2 têm `session_date` 2026-10-01, e o gabarito 0.1 de 01/10 diz ter sido escrito após a disponibilização da amostra. Mesmo assim, o rascunho do relacionamento (20/07), o rascunho do dicionário de sessões (20/07) e o dicionário de pedidos (1.0, 20/08) já citam S1, O1, O2 e `aurora-reference-query.sql`, que implementa a versão 2.0 do indicador, de 15/09. O dicionário de sessões 1.2 (02/10) registra o efeito na amostra de 01/10, mas `validation.checked_at` continua em 12/09.

**Evidências:**

- [public/downloads/exemplo-casos-teste-completo.yaml:26](../public/downloads/exemplo-casos-teste-completo.yaml#L26) `change: "Rascunho do gabarito após disponibilização da amostra"`
- [public/downloads/aurora-fixture.sql:20](../public/downloads/aurora-fixture.sql#L20) `('S1', 'web', 0, '2026-10-01'),`
- [public/downloads/exemplo-relacionamento-lacunas.yaml:8](../public/downloads/exemplo-relacionamento-lacunas.yaml#L8) `version_date: "2026-07-20"`
- [public/downloads/exemplo-relacionamento-lacunas.yaml:44](../public/downloads/exemplo-relacionamento-lacunas.yaml#L44) `- "S1 possui O1 e O2: a linha de S1 aparece duas vezes na junção"`
- [public/downloads/exemplo-dataset-pedidos-completo.yaml:77](../public/downloads/exemplo-dataset-pedidos-completo.yaml#L77) `known_caveats: ["Uma sessão pode ter mais de um pedido confirmado (S1 tem O1 e O2)"]`
- [public/downloads/exemplo-dataset-lacunas.yaml:84](../public/downloads/exemplo-dataset-lacunas.yaml#L84) `sample_queries: ["aurora-reference-query.sql"]`
- [public/downloads/aurora-reference-query.sql:2](../public/downloads/aurora-reference-query.sql#L2) `-- Definição da Aurora (KPI-AURORA-001, versão 2.0); não equivale ao indicador de outra empresa.`
- [public/downloads/exemplo-dataset-completo.yaml:102](../public/downloads/exemplo-dataset-completo.yaml#L102) `checked_at: "2026-09-12"`

**Impacto:** O projeto ensina vigência e "o que se sabia em cada data". Evidência citada antes de existir corrói a credibilidade justamente do eixo de versionamento.

**Recomendação:** Escolher uma narrativa única: o laboratório é um recorte estático usado desde julho (e os textos sobre disponibilização da amostra mudam), ou os documentos anteriores a 01/10 citam outros registros ou nenhum. Atualizar `validation.checked_at` na versão 1.2 do dicionário de sessões. Avaliar no `check_revisions.py` uma regra que impeça citar artefato ou registro datado depois da `version_date`.

**Relacionado:** AUR-08, AUR-15.

### AUR-08 · Rascunhos 0.1 afirmam e perguntam a mesma coisa

**Severidade:** Média

**Confiança:** Alta

**O que acontece:** O rascunho do relacionamento (20/07) já traz a estratégia "contar session_id distinto", o teste "S1 conta como uma sessão convertida" e `verified_query` apontando para a consulta da versão 2.0, mas mantém em aberto a pergunta se conta pedido ou sessão distinta. No rascunho da decisão, o teste fala em "brief com os cinco campos" enquanto a pergunta em aberto é quais campos tornam um brief completo.

**Evidências:**

- [public/downloads/exemplo-relacionamento-lacunas.yaml:42](../public/downloads/exemplo-relacionamento-lacunas.yaml#L42) `- "Para sessões convertidas, contar session_id distinto dos pedidos confirmados elegíveis"`
- [public/downloads/exemplo-relacionamento-lacunas.yaml:51](../public/downloads/exemplo-relacionamento-lacunas.yaml#L51) `verified_query: "aurora-reference-query.sql"`
- [public/downloads/exemplo-relacionamento-lacunas.yaml:54](../public/downloads/exemplo-relacionamento-lacunas.yaml#L54) `- question: "Para contar sessões convertidas, conta-se cada pedido confirmado ou cada sessão distinta?"`
- [public/downloads/exemplo-decisao-lacunas.yaml:56](../public/downloads/exemplo-decisao-lacunas.yaml#L56) `brief com os cinco campos, nenhum ensaio anexado`
- [public/downloads/exemplo-decisao-lacunas.yaml:78](../public/downloads/exemplo-decisao-lacunas.yaml#L78) `- question: "Quais campos tornam um brief completo?"`

**Impacto:** O exemplo com lacunas é o molde que ensina o público não técnico a registrar o que não se sabe. Se ele afirma e pergunta a mesma coisa, o molde perde clareza.

**Recomendação:** Revisar cada `*-lacunas.yaml` com a regra: nada que o histórico do completo atribua a uma versão posterior aparece no 0.1, e nada respondido no corpo aparece como pergunta em aberto. Estender o verificador, como já feito para o numerador do indicador.

**Relacionado:** MOD-13, AUR-03.

### MOD-09 · Os exemplos do laboratório deixam como não aplicáveis os campos que mais importam em produção

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** Nos exemplos, atualização, atraso e frescor aparecem como carga estática ou não aplicável. O fuso é descrito em prosa, sem identificador de fuso. No KPI completo, as perguntas e respostas esperadas e os testes estão vazios. Os comentários justificam que esses itens vieram depois desta versão, e a escolha é coerente com o laboratório, mas o exemplo aprovado não mostra como preencher esses campos.

**Evidências:**

- [public/downloads/exemplo-dataset-completo.yaml:88](../public/downloads/exemplo-dataset-completo.yaml#L88) `known_latency: "Não aplicável ao laboratório"`
- [public/downloads/exemplo-kpi-completo.yaml:59](../public/downloads/exemplo-kpi-completo.yaml#L59) `data_freshness: "Carga estática no laboratório"`
- [public/downloads/exemplo-kpi-completo.yaml:57](../public/downloads/exemplo-kpi-completo.yaml#L57) `timezone: "Data local da loja, já gravada em session_date"`
- [public/downloads/exemplo-kpi-completo.yaml:71](../public/downloads/exemplo-kpi-completo.yaml#L71) `expected_questions_and_answers: []  # gabarito de outubro foi criado depois desta versão`

**Impacto:** O analista não vê um molde de atraso de atualização (por exemplo, a exportação diária do GA4 para o BigQuery) nem de fuso da propriedade contra fuso do warehouse. São erros comuns ao cruzar GA4 com dados internos.

**Recomendação:** Manter o laboratório para as contas e acrescentar um exemplo de cenário de produção, ainda com a Aurora, com atraso típico e máximo, horário de corte, fuso IANA (`America/Sao_Paulo`), diferença entre fuso da propriedade e do warehouse e reprocessamento.

**Relacionado:** AUR-02.

### MOD-17 · A consulta verificada não é um bloco estruturado próprio

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** O gabarito já tem `reference_answer`, `reviewed_by` e `reviewed_at` por pergunta, e `depends_on_versions` para os documentos. Mas não há campo próprio para o texto SQL, o dialeto e a data dos dados consultados. `required_sources` mistura IDs de documentos e nomes de arquivo SQL. No relacionamento, `verified_query` é um texto único, e no dataset `sample_queries` é uma lista solta.

**Evidências:**

- [public/downloads/exemplo-casos-teste-completo.yaml:46](../public/downloads/exemplo-casos-teste-completo.yaml#L46) `required_sources: ["KPI-AURORA-001", "aurora-reference-query.sql"]`
- [public/downloads/template-relacionamento.yaml:43](../public/downloads/template-relacionamento.yaml#L43) `verified_query: null`
- [public/downloads/template-dataset.yaml:55](../public/downloads/template-dataset.yaml#L55) `sample_queries: []`
- [public/downloads/template-casos-teste.yaml:37](../public/downloads/template-casos-teste.yaml#L37) `reviewed_by: null`

**Impacto:** Perguntas de exemplo com consulta verificada são um insumo útil para agentes que geram SQL a partir de texto. Sem estrutura, o agente não sabe qual consulta responde qual pergunta, em que dialeto nem com dados de qual data. A afirmação de que ferramentas de mercado tratam isso como estrutura própria não foi verificada aqui.

**Recomendação:** Criar um bloco `verified_queries` (pergunta, SQL ou arquivo, dialeto, resultado esperado, data dos dados, verificado por e em) e usá-lo no gabarito, no KPI e no novo banco de perguntas. Antes, confirmar a prática de mercado na frente de literatura.

### MOD-19 · Moeda e unidades monetárias não têm campo nem exemplo

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** O KPI e o dataset têm `unit` em texto livre, e os exemplos de dados usam só percentual e dia (as demais colunas ficam com `unit` nulo). Não há campo de moeda, câmbio ou impostos. A única pergunta sobre receita no gabarito é de abstenção, porque não há definição.

**Evidências:**

- [public/downloads/template-kpi.yaml:43](../public/downloads/template-kpi.yaml#L43) `unit: null`
- [public/downloads/exemplo-casos-teste-completo.yaml:109](../public/downloads/exemplo-casos-teste-completo.yaml#L109) `reason_if_abstain: "Indicador não definido na documentação"`

**Impacto:** Indicadores de mídia e e-commerce (custo, receita, ROAS) misturam moedas, impostos e câmbio. Sem molde, a IA usa a convenção genérica, como no caso 2 do mantenedor.

**Recomendação:** Incluir moeda, regra de câmbio e tratamento de impostos e frete nos campos de unidade, e um exemplo monetário no laboratório (por exemplo, receita líquida em BRL).

### MOD-20 · O histórico de versões não aponta para a cópia integral arquivada

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** Os modelos pedem que se guarde o documento completo de cada versão aprovada, mas as entradas de `version_history` só têm `version`, `date`, `change` e `approved_by`, sem campo que indique onde está a cópia. O roteiro de revisão tem essa coluna.

**Evidências:**

- [public/downloads/template-kpi.yaml:25](../public/downloads/template-kpi.yaml#L25) `approved_by: null        # cargo ou área que aprovou; null enquanto não aprovado`
- [public/downloads/roteiro-revisao-documental.md:81](../public/downloads/roteiro-revisao-documental.md#L81) `| Versão | Data | O que mudou e por quê | Quem confirmou | Arquivo integral da versão anterior |`

**Impacto:** Um agente que precisa da regra de uma data passada não tem como localizar a versão integral a partir do documento vigente.

**Recomendação:** Acrescentar `archived_copy` (caminho ou link) a cada entrada de `version_history` e uma coluna equivalente na tabela do .md.

### MOD-16 · A vigência final tem significados diferentes no .md e no YAML

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** No .md, o campo pede o último dia de vigência (inclusive). No YAML, `valid_to` guarda o dia seguinte (exclusivo). A diferença está documentada, com exemplo, na página "Como ler os campos", mas exige conversão manual sempre que o documento passa de um formato para o outro.

**Evidências:**

- [public/downloads/template-kpi.md:22](../public/downloads/template-kpi.md#L22) `| Último dia de vigência (em branco se não houver fim) | |`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:37](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L37) ``No YAML, `valid_to` guarda **o dia seguinte**, o primeiro em que ela já não vale``

**Impacto:** Um erro de um dia na vigência faz um agente aplicar a versão errada justamente no dia da troca de definição, o caso ensinado com o indicador 1.0 e 2.0.

**Recomendação:** Usar o mesmo significado nos dois formatos. Por exemplo, trocar o rótulo do .md para "Deixa de valer em (primeiro dia sem vigência)", ou deixar o YAML inclusivo e renomear o campo para `valid_until`.

### MOD-13 · O exemplo de decisão com lacunas se contradiz sobre os campos do brief

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A entrada `brief_complete` diz que ainda não se sabe quais campos são obrigatórios, e uma pergunta em aberto repete a dúvida. Mesmo assim, um teste do mesmo arquivo cita um brief com os cinco campos, e as regras de prioridade dizem que o conflito já foi resolvido.

**Evidências:**

- [public/downloads/exemplo-decisao-lacunas.yaml:29](../public/downloads/exemplo-decisao-lacunas.yaml#L29) `definition: "Ainda não definido: confirmar com a área quais campos são obrigatórios"`
- [public/downloads/exemplo-decisao-lacunas.yaml:56](../public/downloads/exemplo-decisao-lacunas.yaml#L56) `brief com os cinco campos, nenhum ensaio anexado`
- [public/downloads/exemplo-decisao-lacunas.yaml:51](../public/downloads/exemplo-decisao-lacunas.yaml#L51) `foi resolvido criando uma linha própria para esse caso.`

**Impacto:** O exemplo com lacunas fica quase igual ao completo e não mostra com clareza o que falta. Isso enfraquece a comparação entre antes e depois.

**Recomendação:** Deixar no rascunho só o que estava definido na versão 0.1: tirar dos testes a menção aos cinco campos e o texto de conflito resolvido, ou marcar esses trechos como hipótese a confirmar.

**Relacionado:** AUR-08.

### MOD-14 · Convenção de identificadores e de referências cruzadas inconsistente

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** Os prefixos misturam forma completa e abreviada: CONCEPT, DECISION e DATASET contra REL, DASH e QA. O segundo segmento às vezes é a organização (AURORA) e às vezes o domínio (ONBOARDING, CAMPAIGN). Alguns identificadores têm número e outros não. As referências misturam o ID do documento e o nome físico da tabela.

**Evidências:**

- [public/downloads/exemplo-conceito-completo.yaml:2](../public/downloads/exemplo-conceito-completo.yaml#L2) `id: CONCEPT-ONBOARDING-001`
- [public/downloads/exemplo-dataset-completo.yaml:2](../public/downloads/exemplo-dataset-completo.yaml#L2) `id: DATASET-AURORA-SESSIONS`
- [public/downloads/exemplo-relacionamento-completo.yaml:31](../public/downloads/exemplo-relacionamento-completo.yaml#L31) `dataset: demo_sessions        # DATASET-AURORA-SESSIONS`
- [public/downloads/exemplo-dataset-lacunas.yaml:82](../public/downloads/exemplo-dataset-lacunas.yaml#L82) `related_datasets: ["demo_orders"]`

**Impacto:** Um agente que segue os links entre documentos precisa adivinhar se uma referência é ID ou tabela. Sem regra de nomeação, cada time cria a sua.

**Recomendação:** Documentar uma regra de ID (prefixo do tipo, domínio, sequência) e exigir que as referências entre documentos usem sempre o ID. Quando necessário, dar o nome físico num campo separado.

### MOD-15 · O tipo perguntas de referência tem vários nomes diferentes

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** O mesmo tipo aparece como "casos-teste" no nome do arquivo, "gabarito" no botão de download e no título do exemplo, "Perguntas de referência" na página, "Perguntas de referência e gabarito" no .md, `reference_question_set` no YAML e QA no prefixo do ID.

**Evidências:**

- [src/components/TemplateDownloads.astro:56](../src/components/TemplateDownloads.astro#L56) `{ name: 'Modelo de gabarito', href: 'template-casos-teste.md', format: 'Markdown · para preencher em texto' },`
- [public/downloads/template-casos-teste.md:1](../public/downloads/template-casos-teste.md#L1) `# [Perguntas de referência e gabarito]`
- [public/downloads/template-casos-teste.yaml:6](../public/downloads/template-casos-teste.yaml#L6) `type: reference_question_set`

**Impacto:** Reforça a sensação de colcha de retalhos e dificulta a busca, tanto para pessoas quanto para agentes.

**Recomendação:** Escolher um nome canônico em português e em inglês e aplicá-lo ao arquivo, à página, ao botão, ao `type` e ao prefixo do ID.

### MOD-21 · Inconsistências visuais entre os arquivos de modelo

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** Só o KPI .md numera as seções, e ele tem duas seções de perguntas em aberto. Só o KPI .yaml abre com título em caixa alta e marcador de documento. O conceito .yaml repete a explicação de `null` em duas linhas seguidas.

**Evidências:**

- [public/downloads/template-kpi.md:63](../public/downloads/template-kpi.md#L63) `## 8. Perguntas ainda em aberto`
- [public/downloads/template-kpi.md:66](../public/downloads/template-kpi.md#L66) `## Perguntas em aberto`
- [public/downloads/template-kpi.yaml:1](../public/downloads/template-kpi.yaml#L1) `# TEMPLATE DE DOCUMENTAÇÃO SEMÂNTICA DE KPI`
- [public/downloads/template-conceito.yaml:1](../public/downloads/template-conceito.yaml#L1) `# Preencha apenas informações confirmadas. null = desconhecido.`

**Impacto:** São detalhes pequenos, mas reforçam a percepção de falta de acabamento e confundem quem compara dois modelos.

**Recomendação:** Padronizar o esqueleto dos 10 arquivos: mesmo comentário de abertura, numeração de seções em todos ou em nenhum, uma só seção de perguntas em aberto. De preferência, gerar tudo do esquema único (MOD-04).

### AUR-12 · Amostra mínima limita a demonstração de consultas complexas

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** O laboratório tem 6 sessões, 6 pedidos, 1 dia, 2 tabelas e 1 dashboard, e a própria página o resume assim. O objetivo declarado do mantenedor inclui consultas com várias tabelas, vários dashboards e cruzamentos. A taxa de 25% é útil para conta à mão; o julgamento de que está acima do realista é externo ao repositório e não foi verificado.

**Evidências:**

- [src/content/docs/exemplos/analytics-integrado.mdx:14](../src/content/docs/exemplos/analytics-integrado.mdx#L14) `O laboratório usa uma amostra sintética pequena, para que cada cálculo possa ser refeito à mão.`
- [src/content/docs/dados/visao-geral.mdx:45](../src/content/docs/dados/visao-geral.mdx#L45) `duas tabelas pequenas, uma definição, uma consulta de referência e um dashboard, todos ligados`
- [public/downloads/aurora-fixture.sql:1](../public/downloads/aurora-fixture.sql#L1) `-- Laboratório Aurora: 6 sessões e 6 pedidos, para refazer as contas à mão.`

**Impacto:** Analistas experientes podem achar o exemplo de brinquedo, e falta um caso de cruzamento (mídia, sessão e pedido, ou duas operações) que mostre a camada semântica resolvendo uma análise de verdade.

**Recomendação:** Manter a amostra mínima como nível 1 e acrescentar um nível 2 com vários dias, duas operações, uma tabela de custo de mídia e taxa plausível, verificado pelo mesmo SQLite.

**Relacionado:** AUR-01.

### AUR-09 · Estado dos rascunhos e das cópias históricas diverge do vocabulário publicado

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** Todos os exemplos com lacunas usam `pending_approval` com `approver` nulo, e o do indicador registra "Primeiro rascunho". A página "Como ler os campos" define `pending_approval` como "falta quem aprova confirmar" e `draft` como "ainda escrevendo". As cópias históricas que não estão mais em vigor mantêm `status: approved`, embora o vocabulário tenha `deprecated` para o que não é mais referência atual.

**Evidências:**

- [public/downloads/exemplo-kpi-lacunas.yaml:7](../public/downloads/exemplo-kpi-lacunas.yaml#L7) `status: pending_approval`
- [public/downloads/exemplo-kpi-lacunas.yaml:9](../public/downloads/exemplo-kpi-lacunas.yaml#L9) `approver: null`
- [public/downloads/exemplo-kpi-lacunas.yaml:20](../public/downloads/exemplo-kpi-lacunas.yaml#L20) `change: "Primeiro rascunho, com lacunas registradas"`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:57](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L57) `` | Pendente de aprovação | `pending_approval` | Está estruturado, falta quem aprova confirmar | ``
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:59](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L59) `` | Obsoleto | `deprecated` | Não é mais recomendado como referência atual ``
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:6](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L6) `status: approved`

**Impacto:** Quem aprende pelo exemplo não sabe quando usar `draft`. Um agente que filtre por estado recebe sinais misturados.

**Recomendação:** Usar `draft` nos 0.1 com `approver` nulo, ou explicar por que `pending_approval`. Definir a convenção para versões substituídas (`approved` com `valid_to`, ou `deprecated`) e aplicá-la igual no conceito e no indicador.

**Relacionado:** MOD-11.

### AUR-10 · O gabarito fixa só a versão do indicador, embora dependa de outros documentos

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** QA-AURORA-001 cobre cinco documentos e tem perguntas que dependem do relacionamento (Q02) e do dicionário (Q05), mas `depends_on_versions` registra só o indicador. O gatilho de nova validação menciona mudança de relacionamento sem versão contra a qual comparar.

**Evidências:**

- [public/downloads/exemplo-casos-teste-completo.yaml:38](../public/downloads/exemplo-casos-teste-completo.yaml#L38) `KPI-AURORA-001: "2.0"`
- [public/downloads/exemplo-casos-teste-completo.yaml:58](../public/downloads/exemplo-casos-teste-completo.yaml#L58) `required_sources: ["REL-AURORA-SESSIONS-ORDERS", "KPI-AURORA-001"]`
- [public/downloads/exemplo-casos-teste-completo.yaml:128](../public/downloads/exemplo-casos-teste-completo.yaml#L128) `- "Mudança de granularidade ou de relacionamento"`

**Impacto:** Uma mudança no dicionário (como a 1.2 de 02/10) não dispara a revisão do gabarito de forma rastreável.

**Recomendação:** Registrar em `depends_on_versions` todas as dependências citadas em `required_sources` e `covered_documents`.

### AUR-15 · O indicador 1.0 entrou em vigor antes dos documentos de dados que cita como autoridade

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** O indicador 1.0 (15/08) aponta DATASET-AURORA-SESSIONS como dataset oficial e REL-AURORA-SESSIONS-ORDERS como caminho de junção, mas os dois só foram aprovados em 20/08. A página "Versões e vigência" manda considerar só versões aprovadas e confirmar a versão das dependências.

**Evidências:**

- [public/downloads/historico/exemplo-kpi-v1.0.yaml:58](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L58) `authoritative_dataset: "DATASET-AURORA-SESSIONS"`
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:60](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L60) `valid_join_paths: ["REL-AURORA-SESSIONS-ORDERS"]`
- [public/downloads/exemplo-dataset-completo.yaml:25](../public/downloads/exemplo-dataset-completo.yaml#L25) `date: "2026-08-20"`
- [public/downloads/exemplo-relacionamento-completo.yaml:21](../public/downloads/exemplo-relacionamento-completo.yaml#L21) `date: "2026-08-20"`
- [src/content/docs/metodo/identificacao-versoes.mdx:71](../src/content/docs/metodo/identificacao-versoes.mdx#L71) `3. **Considere somente versões aprovadas** para a finalidade solicitada.`

**Impacto:** Entre 15 e 19/08 o indicador aprovado dependia de documentos não aprovados, contra a regra que o próprio portal ensina.

**Recomendação:** Aprovar os dicionários e o relacionamento antes ou no mesmo dia do indicador 1.0, ou registrar no indicador 1.0 a dependência em aberto.

### AUR-07 · BeforeAfter mostra a fórmula final num estado pendente, contra a linha do tempo do indicador

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** O quadro "Depois" da página de KPI apresenta "Sessões convertidas ÷ sessões elegíveis" com estado pendente de aprovação e escopo "Loja Aurora". Na história da Aurora, o rascunho pendente deixou o numerador em aberto (o verificador exige isso), a 1.0 aprovada contou pedidos e a escolha por sessões só veio na 2.0.

**Evidências:**

- [src/components/BeforeAfter.astro:12](../src/components/BeforeAfter.astro#L12) `<div><dt>Fórmula</dt><dd>Sessões convertidas ÷ sessões elegíveis × 100</dd></div>`
- [src/components/BeforeAfter.astro:15](../src/components/BeforeAfter.astro#L15) `<div><dt>Estado</dt><dd>Pendente de aprovação (<code>pending_approval</code>)</dd></div>`
- [public/downloads/exemplo-kpi-lacunas.yaml:38](../public/downloads/exemplo-kpi-lacunas.yaml#L38) `numerator: null`
- [public/downloads/historico/exemplo-kpi-v1.0.yaml:42](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L42) `formula_description: "(Pedidos confirmados elegíveis / Sessões elegíveis) × 100"`
- [scripts/check_analytics_fixture.py:127](../scripts/check_analytics_fixture.py#L127) `fail("exemplo-kpi-lacunas.yaml: o rascunho não pode já trazer o numerador que só foi decidido depois")`

**Impacto:** A mesma página mostra duas histórias incompatíveis para o mesmo indicador, reforçando a sensação de colcha de retalhos. O quadro é ilustrativo, o que limita a gravidade.

**Recomendação:** Fazer o BeforeAfter ler os mesmos YAML (lacunas e completo), ou alinhar o texto ao rascunho 0.1 (numerador em aberto) ou à 2.0 aprovada.

### AUR-11 · Página e YAML divergem sobre quem conferiu o gabarito

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A página diz que a ressalva existia enquanto ninguém da Gerência de E-commerce conferiu as respostas. O YAML e a tabela da própria página dizem que quem conferiu foi a Analytics de E-commerce; a Gerência aprovou.

**Evidências:**

- [src/content/docs/templates/casos-teste.mdx:55](../src/content/docs/templates/casos-teste.mdx#L55) `Enquanto ninguém da Gerência de E-commerce conferiu as respostas, Q01 carrega essa ressalva:`
- [src/content/docs/templates/casos-teste.mdx:35](../src/content/docs/templates/casos-teste.mdx#L35) `| Quem revisou, e quando | Analytics de E-commerce, 02/10/2026 |`
- [public/downloads/exemplo-casos-teste-completo.yaml:22](../public/downloads/exemplo-casos-teste-completo.yaml#L22) `depois que a Analytics de E-commerce conferiu as respostas de Q01 a Q06`

**Impacto:** Confunde o papel de quem revisa com o de quem aprova, distinção que o próprio portal ensina.

**Recomendação:** Trocar "Gerência de E-commerce" por "Analytics de E-commerce" na linha 55, ou explicitar os dois papéis.

### AUR-14 · Três aprovações datadas em sábado

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** Indicador 1.0 (15/08/2026), dashboard 1.0 (22/08/2026) e dicionário de sessões 1.1 (12/09/2026, também o `checked_at`) caem em sábado; todas as outras datas dos YAML são dias úteis. O contrato editorial pede conferir datas; a regra literal trata de dia da semana citado e prazos em dias úteis, então não é violação direta, mas tira verossimilhança. A maioria dos rascunhos de áreas diferentes nasce no mesmo dia, 20/07 (exceções: gabarito em 01/10 e política em 11/08).

**Evidências:**

- [public/downloads/historico/exemplo-kpi-v1.0.yaml:8](../public/downloads/historico/exemplo-kpi-v1.0.yaml#L8) `version_date: "2026-08-15"`
- [public/downloads/exemplo-dashboard-completo.yaml:25](../public/downloads/exemplo-dashboard-completo.yaml#L25) `date: "2026-08-22"`
- [public/downloads/exemplo-dataset-completo.yaml:21](../public/downloads/exemplo-dataset-completo.yaml#L21) `date: "2026-09-12"`
- [docs/CONTRATO_EDITORIAL.md:94](../docs/CONTRATO_EDITORIAL.md#L94) `6. **Datas conferidas:** dia da semana`

**Impacto:** Detalhes assim tiram verossimilhança de um universo que pretende parecer operação real.

**Recomendação:** Mover essas datas para dias úteis (ajustando os "Teste você" que dependem delas), variar as datas dos rascunhos e incluir no validador um aviso para aprovação em fim de semana.

**Observação da verificação:** na conferência de todas as datas dos YAML, só 2026-08-15, 2026-08-22 e 2026-09-12 caem em fim de semana (sábado).

### AUR-16 · O rascunho da rubrica cita a etapa 3 de um processo que só tem duas etapas

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A rubrica 0.1 (20/07) diz ser usada na etapa 3 do processo de campanha. O processo 0.1, da mesma data, tem só S01 e S02, e a conferência de evidências acontece em S02.

**Evidências:**

- [public/downloads/exemplo-rubrica-lacunas.yaml:23](../public/downloads/exemplo-rubrica-lacunas.yaml#L23) `allowed_use: ["Revisão de material na etapa 3 do processo de campanha", "Calibração entre revisores"]`
- [public/downloads/exemplo-processo-lacunas.yaml:43](../public/downloads/exemplo-processo-lacunas.yaml#L43) `name: "Conferir evidências e critérios"`

**Impacto:** Referência cruzada quebrada entre rascunhos, visível para quem compara os dois.

**Recomendação:** Na rubrica, referir-se à etapa por ID estável ou nome, não por número.

### AUR-17 · Dados da amostra duplicados à mão em componentes e páginas, com verificação parcial

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** O `JoinDiagram` codifica sessões e pedidos à mão e afirma que o verificador confere as contas, mas o verificador só procura as strings "50%" e "25%" na página de relacionamento e não lê o componente nem as tabelas da página do laboratório. A consulta de pedidos confirmados no verificador não filtra a data, ao contrário das outras.

**Evidências:**

- [src/components/JoinDiagram.astro:4](../src/components/JoinDiagram.astro#L4) `* Os valores vêm da amostra aurora-fixture.sql; check_analytics_fixture.py confere as contas.`
- [src/components/JoinDiagram.astro:18](../src/components/JoinDiagram.astro#L18) `{ id: 'O6', status: 'TEST', y: 194, from: 'S5', hit: false },`
- [scripts/check_analytics_fixture.py:93](../scripts/check_analytics_fixture.py#L93) `"templates/relacionamento.mdx": ["50%", "25%"],`
- [scripts/check_analytics_fixture.py:46](../scripts/check_analytics_fixture.py#L46) `WHERE s.channel='web' AND s.is_internal=0 AND o.status_code='CONFIRMED'`
- [src/content/docs/exemplos/analytics-integrado.mdx:33](../src/content/docs/exemplos/analytics-integrado.mdx#L33) `| O1 | S1 | CONFIRMED |`

**Impacto:** Se a amostra mudar, diagrama e tabelas podem divergir sem que o build acuse.

**Recomendação:** Gerar diagrama e tabelas a partir da amostra em tempo de build, ou estender o verificador para comparar as linhas da tabela MDX e do `JoinDiagram` com o SQLite, e incluir o filtro de data na consulta de pedidos.

### AUR-19 · Nomes divergentes para a fonte oficial da política e exceção diferente da aprovada

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A página chama a POL-FIN-014 de "Manual". O YAML a trata como política publicada em Políticas > Finanças. A página "Oito dimensões" resume a fonte como "na intranet". A tabela de perguntas usa como exceção "evento com cliente", e a exceção aprovada no YAML é "evento contratado em emergência".

**Evidências:**

- [src/content/docs/templates/politica.mdx:26](../src/content/docs/templates/politica.mdx#L26) `` | Manual `POL-FIN-014`, versão 3 | Vigente desde 01/07/2026 | ``
- [public/downloads/exemplo-politica-completo.yaml:78](../public/downloads/exemplo-politica-completo.yaml#L78) `source_precedence_rule: "A política publicada em Políticas > Finanças prevalece sobre e-mails, resumos e apresentações.`
- [src/content/docs/metodo/oito-dimensoes.mdx:16](../src/content/docs/metodo/oito-dimensoes.mdx#L16) `“Política POL-FIN-014, versão 3, na intranet”`
- [src/content/docs/templates/politica.mdx:41](../src/content/docs/templates/politica.mdx#L41) `| Quem autoriza exceções, e com que evidência? | Despesa acima do limite em evento com cliente | Exceção e registro |`
- [public/downloads/exemplo-politica-completo.yaml:57](../public/downloads/exemplo-politica-completo.yaml#L57) `- condition: "Evento contratado em emergência, sem tempo para aprovação prévia"`

**Impacto:** Num exemplo cujo tema é distinguir fontes por autoridade, rótulos ambíguos enfraquecem a lição para pessoas e para um RAG.

**Recomendação:** Padronizar "política POL-FIN-014, versão 3, em Políticas > Finanças" em todas as páginas e alinhar o exemplo de exceção ao YAML.

### AUR-20 · A ficha HANDOFF-001 foge do padrão dos documentos Aurora

**Severidade:** Baixa

**Confiança:** Alta

**O que acontece:** A ficha de entrega não tem `version`, `version_date` nem `version_history`, que o contrato editorial torna obrigatórios em todo modelo e exemplo. Ela diz levar perguntas do processo de campanha, mas reescreve o impacto de uma delas com outro texto.

**Evidências:**

- [src/content/docs/validacao/checklist.mdx:85](../src/content/docs/validacao/checklist.mdx#L85) `id: HANDOFF-001`
- [src/content/docs/validacao/checklist.mdx:94](../src/content/docs/validacao/checklist.mdx#L94) `impact: "O fluxo não define qual responsável deve decidir"`
- [public/downloads/exemplo-processo-lacunas.yaml:71](../public/downloads/exemplo-processo-lacunas.yaml#L71) `impact: "Uma campanha com prazo legal pode ser barrada pelo fluxo normal"`
- [docs/CONTRATO_EDITORIAL.md:100](../docs/CONTRATO_EDITORIAL.md#L100) `Campos obrigatórios em todo modelo e exemplo:`

**Impacto:** Um tipo de documento sem modelo, sem versão e com texto divergente reforça a impressão de inconsistência.

**Recomendação:** Transformar a ficha num tipo com modelo e versão, ou copiar literalmente as perguntas e impactos do processo 0.1.

**Relacionado:** MOD-07.

### AUR-21 · Aviso de que a Aurora é inventada ausente nos SQL e presente fora dos lugares previstos

**Severidade:** Baixa

**Confiança:** Média

**O que acontece:** O contrato editorial justifica o aviso na primeira linha dos YAML porque o arquivo circula sem o site, mas os SQL para download não dizem que a Aurora é inventada (a consulta só diz que a definição não equivale à de outra empresa). O README usa "aprovação fictícia" e "amostra fictícia", termos que o contrato veta fora de três lugares, se o README estiver no escopo do contrato.

**Evidências:**

- [public/downloads/aurora-fixture.sql:1](../public/downloads/aurora-fixture.sql#L1) `-- Laboratório Aurora: 6 sessões e 6 pedidos, para refazer as contas à mão.`
- [docs/CONTRATO_EDITORIAL.md:68](../docs/CONTRATO_EDITORIAL.md#L68) `3. a primeira linha de comentário de cada YAML de exemplo, porque o arquivo baixado circula sem o site.`
- [docs/CONTRATO_EDITORIAL.md:70](../docs/CONTRATO_EDITORIAL.md#L70) `Fora deles, nenhum “fictício”, “hipotético”, “ilustrativo”`
- [README.md:39](../README.md#L39) ``na amostra fictícia `aurora-fixture.sql`.``
- [README.md:30](../README.md#L30) `**exemplo completo com aprovação fictícia**`

**Impacto:** Baixo, mas é inconsistência editorial verificável e fácil de corrigir.

**Recomendação:** Estender a regra da primeira linha aos .sql e decidir explicitamente se o README está dentro ou fora do contrato.

### MOD-22 · Cinco dos dez tipos usam exemplos fora de dados e analytics

**Severidade:** Info

**Confiança:** Média

**O que acontece:** Conceito, processo, decisão, política e rubrica usam exemplos de integração de novos funcionários, campanha e despesas em eventos. Só os tipos de dados (KPI, dataset, relacionamento, dashboard e perguntas de referência) formam um caso conectado no Laboratório Aurora.

**Evidências:**

- [src/content/docs/templates/index.mdx:29](../src/content/docs/templates/index.mdx#L29) `Quem trabalha com tabelas, SQL e dashboards encontra os quatro modelos de dados ligados no [Laboratório Aurora]`
- [public/downloads/exemplo-politica-completo.yaml:4](../public/downloads/exemplo-politica-completo.yaml#L4) `title: "Despesas em eventos: Aurora"`

**Impacto:** Não é um erro: o mantenedor também cita bases de operação. Mas o público principal (marketing e analytics) tem um único caso conectado, e os tipos gerais não mostram como se ligam a um indicador ou a um evento.

**Recomendação:** Decidir se o produto foca em dados e mensuração, reescrevendo os exemplos gerais no mesmo universo de e-commerce e mídia, ou se mantém dois trilhos explícitos. De qualquer forma, ligar ao menos um conceito e uma decisão ao caso de analytics, por exemplo o conceito de sessão interna e a decisão de quando declarar um evento quebrado.

**Relacionado:** AUR-01.

## Descartados na verificação

| ID | Motivo |
|---|---|
| AUR-18 | A resposta "100%" do Teste você 3 está correta sob contagem consistente: juntando sessões elegíveis com pedidos confirmados, sessões distintas dão 1/1 e linhas dão 2/2. A própria resposta conclui que o denominador precisa vir das sessões elegíveis antes da junção (4). "O denominador vira 1" é simplificação, não contradição. |
| AUR-22 | A amostra tem de fato seis sessões, e a frase diz que a mesma pergunta dá 25% ou 50% "nas mesmas seis sessões", isto é, sobre a mesma amostra. Os filtros que levam a quatro elegíveis são explicados na página do laboratório. É leitura possível, não erro demonstrável. |
| Contas do laboratório | Refeitas na amostra de `aurora-fixture.sql`: 25% com os filtros, 40% sem o filtro de sessão interna, 50% pela fórmula 1.0. Não há erro de conta nem divergência entre YAML, SQL e MDX. |
| Contas da rubrica | As notas de calibração conferem com os pesos 40, 25, 20 e 15: 32,5 e 90. |
| Contagens do conceito | 131 + 52 + 11 + 12 + 8 = 214. |
| Vigências sobrepostas | O `valid_to` exclusivo de 2026-09-15 na versão 1.0 coincide com o `valid_from` da 2.0. |
| Dias da semana nas páginas | 01/10/2026 é quinta e 02/10/2026 é sexta, coerentes com os textos. |
| Prazo em dias úteis do CAMP-0914 | Conferido, sem erro. |
| ID citado sem documento | Todo ID citado tem documento correspondente. |
| Campos de exemplo fora do modelo | Só diferenças esperadas em chaves de mapa. A falta de formato dos subcampos está tratada no MOD-06. |

## Não coberto nesta rodada

- Não executei build, scripts do repositório nem SQL. As contas do laboratório e da rubrica foram conferidas à mão na amostra e nos pesos. As observações de verificação em AUR-05 vêm da frente original e foram conferidas só contra o código e os YAML.
- Não li por inteiro os exemplos com lacunas de rubrica, perguntas de referência, conceito, processo, política, relacionamento e dashboard. Conferi status, `owner` e `approver` de todos, e o de decisão por inteiro.
- Não verifiquei as referências externas citadas nas recomendações (planos de rastreamento de mercado, Open Data Contract Standard, Snowflake Cortex Analyst, Databricks Genie). Elas precisam ser confirmadas na frente de literatura.
- Não fiz pesquisa externa sobre taxas de conversão típicas; o julgamento de realismo da taxa de 25% em AUR-12 não tem evidência no repositório.
- Não avaliei a renderização do portal publicado (https://edoardolobl.github.io/contexto-framework/) nem a experiência de download. Pelo código, confirmei só que as páginas de modelo mostram os exemplos YAML pelo componente `ExampleDoc`; os componentes `TemplateStart`, `TemplateFinder` e `ReadinessChecklist` não foram revisados e podem já exibir exemplos ao lado dos modelos (relevante para MOD-03 e AUR-13).
- Não auditei por inteiro `docs/ROADMAP.md`, `docs/PLANO_VALIDACAO.md`, `src/content/docs/referencias/index.mdx` e a página de limites.
