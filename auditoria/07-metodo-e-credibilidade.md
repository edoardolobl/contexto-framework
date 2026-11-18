# Método e credibilidade

Data: 2026-11-17 · Commit: d08c810 · Escopo: o método do Contexto (porta de entrada, perguntas ao especialista, oito dimensões, regras de versão, papéis) e a base que sustenta sua credibilidade (bibliografia, estudo empírico citado, plano de validação).

## Resumo

- A base é honesta e vale preservar: a tríade **Confirmado / Relatado / Em aberto** tem o mesmo sentido em todo o portal, a bibliografia declara que o método é autoral e o preprint citado aparece com as ressalvas certas. A conferência final confirmou as 76 citações deste relatório nas linhas indicadas.
- O problema central é de desenho: o portal começa por um termo isolado e só chega às perguntas de negócio no fim da trilha de dados, como verificação. Nada ensina a formular uma boa pergunta nem a decompor perguntas que cruzam várias tabelas ou dashboards (MET-01).
- Há listas paralelas de perguntas que não se cruzam, e a dimensão Exceções tem definições diferentes na página do método e no checklist. É a origem concreta da sensação de colcha de retalhos (MET-02, MET-03, MET-11).
- Nenhuma dimensão cobre o comportamento esperado de um evento (frequência, recorte por operação, diferença entre zero e ausência de dado), que é exatamente o caso real do evento raro marcado como quebrado (MET-07).
- As regras de versão têm tensões internas e campos sem explicação, não dizem onde guardar as versões e não são aplicadas aos próprios documentos do projeto (MET-08, MET-09, MET-13).
- A bibliografia precisa de atualização e reforço: o KCS v6 foi substituído por um guia que trata de conhecimento para IA, e a evidência empírica depende de um único preprint de fornecedor (MET-05, MET-06).

## Pontos fortes (manter)

### Tríade Confirmado / Relatado / Em aberto com o mesmo sentido em todo o portal

É a ideia mais forte do método para o público não técnico e ataca o caso do indicador genérico, porque impede que prática relatada ou definição presumida vire regra. Deve ser o eixo de qualquer reestruturação.

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:101](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L101) `Dentro de um mesmo documento convivem três tipos de afirmação. Mantenha-os separados. Esses três nomes aparecem em todo o portal com o mesmo sentido:`
- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:34](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L34) `**Confirmado** tem fonte e alguém com autoridade. **Relatado** é como as pessoas dizem que fazem, e não vira regra só porque é comum.`
- [src/content/docs/metodo/elicitar.mdx:40](../src/content/docs/metodo/elicitar.mdx#L40) `O encontro termina com três listas curtas: o que ficou **confirmado**, o que foi **relatado** e precisa de fonte, e o que está **em aberto**`

### Honestidade sobre autoria, limites e fontes

O portal declara que as oito dimensões são autorais, que nenhuma fonte prescreve o método e que a eficácia com pessoas reais ainda não foi testada. Isso dá credibilidade e deve ser mantido.

- [src/content/docs/referencias/index.mdx:7](../src/content/docs/referencias/index.mdx#L7) `É uma **metodologia autoral**: não existe uma norma que determine as “oito dimensões” exatamente como apresentadas aqui.`
- [src/content/docs/referencias/index.mdx:46](../src/content/docs/referencias/index.mdx#L46) `A coluna do meio indica **de onde veio a ideia**, não uma exigência da fonte. Nenhuma das fontes prescreve o que o Contexto faz.`
- [src/content/docs/metodo/limites.mdx:52](../src/content/docs/metodo/limites.mdx#L52) `A eficácia do método com pessoas reais também ainda não foi testada`

### Ressalvas do preprint 2604.25149 conferem com o artigo

O portal marca o estudo como preprint sem revisão por pares, de autores ligados à Cube, com um dataset e uma tentativa por pergunta, e o apresenta como indício, não prova. A conferência com o PDF foi feita pelo analista original; nesta rodada foram confirmadas as citações no repositório.

- [src/content/docs/referencias/index.mdx:36](../src/content/docs/referencias/index.mdx#L36) `**Preprint, sem revisão por pares.** Autores vinculados à Cube, fornecedora de camada semântica. Um dataset e um banco. Uma tentativa por pergunta.`
- [src/content/docs/dados/visao-geral.mdx:41](../src/content/docs/dados/visao-geral.mdx#L41) `É **um indício de utilidade**, não prova de suficiência nem garantia de produção.`

### Exemplos das oito dimensões são concretos e batem com os arquivos de exemplo

A coluna "Resposta útil" cita valores que existem nos YAML completos, como POL-FIN-014 versão 3. É o molde que o mantenedor quer para todos os modelos.

- [src/content/docs/metodo/oito-dimensoes.mdx:16](../src/content/docs/metodo/oito-dimensoes.mdx#L16) `| Evidência | Qual é a fonte oficial e como se verifica? | “Está no sistema” | “Política POL-FIN-014, versão 3, na intranet” |`
- [public/downloads/exemplo-politica-completo.yaml:15](../public/downloads/exemplo-politica-completo.yaml#L15) `source_of_truth: "POL-FIN-014, versão 3, publicada na intranet em Políticas > Finanças"`

### Perguntas de referência com três desfechos: responder, pedir esclarecimento, abster-se

É a semente do que o mantenedor quer: perguntas de negócio reais, cada uma com resposta esperada, evidência e versão da definição. A Q07, que compara versões, é o tipo de pergunta que teria evitado o erro do indicador genérico. Hoje ela aparece só no fim da trilha de dados.

- [src/content/docs/templates/casos-teste.mdx:22](../src/content/docs/templates/casos-teste.mdx#L22) `| Respondível | As fontes cobrem significado, escopo e período | Responder com definição e evidência |`
- [src/content/docs/templates/casos-teste.mdx:51](../src/content/docs/templates/casos-teste.mdx#L51) `| Q07 | A taxa de sessões web convertidas de 01/10/2026 pode ser comparada com a de 10/09/2026, do relatório de setembro?`

### Vigência como intervalo e recusa de escolher a versão mais recente

Separar o ID do assunto, o ID da versão, a data do registro e a vigência, e não reconstruir versões antigas a partir do resumo de mudanças, é prática madura e coerente com DCMI e PROV-O.

- [src/content/docs/metodo/identificacao-versoes.mdx:10](../src/content/docs/metodo/identificacao-versoes.mdx#L10) `A solução documental não é escolher automaticamente o arquivo com a data mais recente.`
- [src/content/docs/metodo/identificacao-versoes.mdx:84](../src/content/docs/metodo/identificacao-versoes.mdx#L84) `**Não reconstruir a versão antiga a partir do resumo das mudanças**`
- [src/content/docs/governanca/papeis.mdx:49](../src/content/docs/governanca/papeis.mdx#L49) `Não escolha a fonte mais recente automaticamente: data de publicação não garante autoridade.`

### O checklist gera lista de lacunas, não nota

Evita a falsa sensação de qualidade das listas com pontuação. Está no texto e no componente interativo.

- [src/content/docs/validacao/checklist.mdx:25](../src/content/docs/validacao/checklist.mdx#L25) `**O resultado desta etapa é uma lista de lacunas**, e não uma nota de qualidade.`
- [src/components/ReadinessChecklist.astro:17](../src/components/ReadinessChecklist.astro#L17) `<strong>Não é uma nota:</strong>`

## Índice de achados

| ID | Severidade | Título |
|---|---|---|
| MET-01 | Alta | O método não parte de perguntas de negócio nem ensina a formulá-las |
| MET-02 | Média | Conjuntos paralelos de perguntas sem ligação entre si |
| MET-03 | Média | Definição de Exceções diverge entre a página do método e o checklist |
| MET-05 | Média | KCS v6 está desatualizado: foi substituído pelo guia Knowledge-Centered Success, que trata de IA |
| MET-06 | Média | A evidência empírica depende de um único preprint de fornecedor |
| MET-07 | Média | Nenhuma dimensão cobre o comportamento esperado do evento |
| MET-08 | Média | Regras de versão têm tensões internas e campos sem explicação |
| MET-09 | Média | O portal não explica onde nem como guardar as versões |
| MET-10 | Média | A matriz RACI omite o papel Responsável e a letra R colide com o vocabulário |
| MET-04 | Baixa | A página das dimensões promete uma origem por dimensão que a bibliografia não mostra |
| MET-11 | Baixa | A forma de registrar o Relatado muda de página para página |
| MET-12 | Baixa | A ressalva sobre o documento "não escrito às cegas" exagera um pouco |
| MET-13 | Baixa | O próprio projeto não segue as regras de versão que ensina |
| MET-14 | Baixa | A distinção entre tácito e explícito é atribuída só a Nonaka, sem Polanyi |
| MET-15 | Baixa | A separação entre responder, esclarecer e abster-se é atribuída a uma fonte que não a sustenta como escrito |
| MET-16 | Baixa | A eficácia do método não foi testada e o plano de validação está parado |

## Achados

### MET-01 · O método não parte de perguntas de negócio nem ensina a formulá-las

**Severidade:** Alta
**Confiança:** Alta

**O que acontece:** O objetivo central do mantenedor é produzir documentação a partir de perguntas de negócio e ensinar as pessoas a fazê-las. O portal faz o contrário: a porta de entrada é uma frase que a equipe usa. O passo "Delimitar" não tem página própria; a pasta `metodo` só tem as páginas elicitar, identificacao-versoes, limites, oito-dimensoes e visao-geral. As perguntas de negócio só aparecem no fim, como "Verificação" na trilha de dados. A expressão "pergunta(s) de negócio" aparece em 4 lugares entre src, public/downloads, docs e README: três são campos a preencher (oito-dimensoes, template-relacionamento, template-dataset) e um é a frase de abertura do modelo de KPI. Nenhum trata a pergunta como ponto de partida ou como habilidade a aprender. Não há orientação sobre o que faz uma boa pergunta (unidade, período, recorte, comparação, decisão apoiada) nem sobre como decompor perguntas que cruzam várias tabelas ou dashboards.

**Evidências:**

- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:10](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L10) `## 1. Escolha uma frase que sua equipe usa`
- [src/content/docs/metodo/visao-geral.mdx:16](../src/content/docs/metodo/visao-geral.mdx#L16) `| **1. Delimitar** | Identificar o assunto, quem o usa e quando vale | Objetivo e escopo |`
- [src/content/docs/dados/visao-geral.mdx:29](../src/content/docs/dados/visao-geral.mdx#L29) `| Verificação | “Quais perguntas o acervo deve conseguir responder?” | [Perguntas de referência](../../templates/casos-teste/) |`
- [src/content/docs/metodo/oito-dimensoes.mdx:27](../src/content/docs/metodo/oito-dimensoes.mdx#L27) `| Objetivo | Finalidade, pergunta de negócio, decisão apoiada |`
- [public/downloads/template-conceito.md:27](../public/downloads/template-conceito.md#L27) `- Qual pergunta ajuda a responder?`
- [public/downloads/template-dataset.md:27](../public/downloads/template-dataset.md#L27) `- Que perguntas de negócio ajuda a responder?`

**Impacto:** Um analista que chega com "quero que a IA me diga quais eventos do tag plan pararam" não encontra um caminho que comece por essa pergunta e desça até as definições, dados e regras de que ela depende. O portal ensina a documentar termos isolados, não a deixar uma pergunta respondível. Os dois casos reais do mantenedor nascem justamente de perguntas sem as regras de negócio por trás.

**Recomendação:** Inverter a entrada do método:

1. Começar por uma ficha de pergunta de negócio: a pergunta como a pessoa faria, a decisão que ela apoia, unidade, recorte, período, comparação esperada e fontes candidatas.
2. Para cada pergunta, listar as definições, regras e dados de que ela depende. Isso leva naturalmente aos modelos que já existem.
3. Fechar com o gabarito de Perguntas de referência, que já existe.

Criar uma página curta "Como escrever uma boa pergunta de negócio", usando as três categorias de `casos-teste.mdx` (responder, pedir esclarecimento, abster-se) como exercício. Esse desenho segue a prática dos fornecedores: a Microsoft começa a preparação de um RAG pela coleta de perguntas de exemplo, o Databricks Genie usa a formulação típica da pergunta como título de cada consulta de exemplo e o Snowflake guarda em `verified_queries` a pergunta junto com o SQL que a responde.

**Observação no portal:** Fontes consultadas em 17/11/2026.

- Microsoft, fase de preparação de RAG: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-preparation-phase. A página descreve definir o domínio, reunir o conteúdo e "gather sample questions that are pertinent to the domain".
- Databricks, exemplos de consulta para o Genie: https://learn.microsoft.com/en-us/azure/databricks/genie/add-instructions. A orientação é usar "the most typical phrasing of the user's question as the title".
- Snowflake, especificação YAML de semantic views: https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec, seção `verified_queries` (pergunta em linguagem natural mais o SQL que a responde).

### MET-02 · Conjuntos paralelos de perguntas sem ligação entre si

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O portal tem várias listas de perguntas para o especialista que não se referenciam: as 8 perguntas das dimensões, o roteiro de descoberta (onde novatos erram e outros temas), as 3 perguntas do início rápido, as perguntas do exercício de conhecimento tácito e as tabelas "O que perguntar" dos modelos. A página de descoberta (`elicitar.mdx`) não menciona as dimensões: uma busca por "dimens" nela não retorna nada. A visão geral põe "Descobrir" antes de "Estruturar com as oito dimensões", mas a página das dimensões manda fazer essas perguntas ao especialista, ou seja, elas também são perguntas de descoberta.

**Evidências:**

- [src/content/docs/metodo/elicitar.mdx:14](../src/content/docs/metodo/elicitar.mdx#L14) `1. **Onde alguém novo costuma errar?** Registre o pressuposto que experientes aplicam automaticamente.`
- [src/content/docs/metodo/oito-dimensoes.mdx:6](../src/content/docs/metodo/oito-dimensoes.mdx#L6) `Estas perguntas funcionam como um roteiro, não como burocracia. Faça-as ao especialista do assunto e documente respostas verificáveis.`
- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:18](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L18) `## 2. Faça três perguntas`
- [src/content/docs/fundamentos/conhecimento-tacito.mdx:27](../src/content/docs/fundamentos/conhecimento-tacito.mdx#L27) `Escolha uma regra que sua área aplica todos os dias. Faça a si mesmo estas perguntas:`
- [src/content/docs/metodo/visao-geral.mdx:18](../src/content/docs/metodo/visao-geral.mdx#L18) `| **3. Estruturar** | Aplicar as oito dimensões e o modelo adequado | Documento contextualizado |`

**Impacto:** É a colcha de retalhos que o mantenedor percebe. O leitor não sabe qual lista usar nem se responder a uma cobre a outra. Quando uma dimensão muda, fica difícil manter todas as listas coerentes.

**Recomendação:** Eleger um único esqueleto de perguntas, por exemplo as oito dimensões, e marcar cada pergunta de descoberta, do início rápido e das tabelas "O que perguntar" com a dimensão que ela alimenta. O roteiro de descoberta passa a ser "perguntas difíceis para cada dimensão".

### MET-03 · Definição de Exceções diverge entre a página do método e o checklist

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** A página das oito dimensões define Exceções como "desvios previstos da regra". O checklist interativo pergunta por "Casos não previstos". A tabela das dimensões fala em "fora do fluxo esperado". Há também uma divergência menor em Vigência: a dimensão inclui "quem revisa", mas o item do checklist não pergunta isso.

**Evidências:**

- [src/content/docs/metodo/oito-dimensoes.mdx:34](../src/content/docs/metodo/oito-dimensoes.mdx#L34) `**Exceções** são desvios previstos da regra, não casos em que ela não se aplica.`
- [src/content/docs/metodo/oito-dimensoes.mdx:14](../src/content/docs/metodo/oito-dimensoes.mdx#L14) `| Exceções | O que acontece fora do fluxo esperado? |`
- [src/components/ReadinessChecklist.astro:9](../src/components/ReadinessChecklist.astro#L9) `['Exceções', 'Casos não previstos e o que fazer com eles estão identificados?'],`
- [src/content/docs/metodo/oito-dimensoes.mdx:17](../src/content/docs/metodo/oito-dimensoes.mdx#L17) `| Vigência | Desde quando vale, qual versão é esta e quem revisa? |`
- [src/components/ReadinessChecklist.astro:12](../src/components/ReadinessChecklist.astro#L12) `['Vigência', 'Estado, versão e vigência são conhecidos ou marcados como em aberto?'],`

**Impacto:** Uma das oito dimensões tem formulações conflitantes no núcleo do método. Revisores diferentes vão apontar lacunas diferentes no mesmo documento, o que mina a credibilidade do checklist.

**Recomendação:** Decidir uma definição (sugestão: exceções previstas, mais um campo separado "o que fazer quando surge um caso não previsto") e gerar o texto do checklist a partir de uma única fonte de dados das dimensões, compartilhada pela página e pelo componente.

### MET-05 · KCS v6 está desatualizado: foi substituído pelo guia Knowledge-Centered Success, que trata de IA

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O portal cita o KCS v6 Practices Guide em pelo menos sete lugares (referências, papéis, conhecimento tácito, visão geral do método, roteiro de revisão documental, README) e diz que as fontes foram revistas em novembro de 2026. O Consortium for Service Innovation publicou o "Knowledge-Centered Success: Practices Guide", baseado no v6, que renomeia a metodologia e traz orientação para conhecimento usado por IA e automação. Os papéis passaram para a prática Process Integration.

**Evidências:**

- [src/content/docs/referencias/index.mdx:16](../src/content/docs/referencias/index.mdx#L16) `| [KCS v6, *Practices Guide*](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide) | Captura, estrutura e evolução de conhecimento |`
- [src/content/docs/governanca/papeis.mdx:57](../src/content/docs/governanca/papeis.mdx#L57) `[KCS: Roles and Competencies](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide)`
- [src/content/docs/referencias/index.mdx:77](../src/content/docs/referencias/index.mdx#L77) `**Revisão desta edição:** novembro de 2026.`

**Impacto:** A fonte mais citada do método aparece numa versão antiga, justamente quando a nova trata do mesmo problema do Contexto: conhecimento estruturado para IA. Isso enfraquece a credibilidade e desperdiça um argumento forte.

**Recomendação:** Atualizar para https://library.serviceinnovation.org/KCS/Knowledge-Centered_Success_Practices_Guide e citar a seção de papéis em Process Integration. Manter a nota de licença CC BY-NC 4.0 e de marca KCS®. Ajustar README, roteiro de revisão documental e as páginas que citam o v6.

**Observação no portal:** Confirmado por busca nesta verificação. A página do guia novo diz que o nome mudou de Knowledge-Centered Service para Knowledge-Centered Success e que "structured, up-to-date knowledge is the path to success". A página "What's New" diz que Process Integration agora inclui "KCS Roles and the Proficiency Model".

### MET-06 · A evidência empírica depende de um único preprint de fornecedor

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** A seção de semântica tem um único estudo empírico, um preprint de autores da Cube. As outras entradas (dbt, Snowflake, Databricks, Microsoft, NIST) são documentação de produto ou de referência, não estudos. Ficam de fora estudos revisados por pares que sustentam a mesma tese e o padrão aberto e neutro para camadas semânticas, o Apache Ossie.

**Evidências:**

- [src/content/docs/referencias/index.mdx:36](../src/content/docs/referencias/index.mdx#L36) `[Rumiantsau & Fokeev (2026), *Semantic Layers for Reliable LLM-Powered Data Analytics:`
- [README.md:79](../README.md#L79) `[Rumiantsau & Fokeev (2026, preprint)](https://arxiv.org/abs/2604.25149)`

**Impacto:** Para um público misto, um preprint de fornecedor é alicerce fraco. Falta a referência que mostra que um documento de contexto de negócio escrito com especialistas melhora as respostas, que é a promessa do Contexto.

**Recomendação:** Acrescentar:

1. Painter et al., JAMIA Open, https://doi.org/10.1093/jamiaopen/ooaf003, revisado por pares, com documento de contexto construído com especialistas.
2. BIRD, Li et al., NeurIPS 2023, https://arxiv.org/abs/2305.03111, sobre o efeito da evidência de conhecimento externo em text-to-SQL.
3. Apache Ossie (em incubação), antigo Open Semantic Interchange, https://ossie.apache.org/, como alvo executável neutro para o qual os YAML do portal podem apontar.
4. Opcional: o benchmark da dbt Labs de 2026, marcado como fonte de fornecedor.

Destacar também o resultado do preprint de que um agente com busca não superou a linha de base, porque afeta diretamente quem usa Claude Code, Codex ou Antigravity.

**Observação no portal:** Confirmado nesta verificação: https://ossie.apache.org/ diz "Ossie was previously known as Open Semantic Interchange (OSI)". Da leitura do analista original, não reconferida nesta rodada: o PDF de https://arxiv.org/abs/2604.25149 atribui os números 8,3% e 78,3% a "Zargari Marandi et al., 2024", mas o artigo do JAMIA Open com esses números é de Jeffery L. Painter et al.

### MET-07 · Nenhuma dimensão cobre o comportamento esperado do evento

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O caso 1 do mantenedor (evento raro marcado como quebrado por não ter disparado num dia, ou por disparar numa operação e não em outra) exige registrar frequência esperada, sazonalidade, recorte por operação e a diferença entre zero e ausência de dado. As oito dimensões e a lista do que o schema não diz cobrem granularidade, tempo e limites, mas não volume ou frequência esperados nem como interpretar a ausência. O que existe de mais próximo é parcial: o modelo de dashboard tem `comparison_baseline` (base de comparação para leitura) e o de dataset pergunta a frequência de atualização da carga. Buscas por "raro", "sazonal", "linha de base", "tag plan", "GA4" e "GTM" nas páginas e modelos não retornam nada fora da bibliografia.

**Evidências:**

- [src/content/docs/dados/visao-geral.mdx:17](../src/content/docs/dados/visao-geral.mdx#L17) `- **Tempo:** qual data define o período, e em que fuso?`
- [src/content/docs/dados/visao-geral.mdx:20](../src/content/docs/dados/visao-geral.mdx#L20) `- **Limites:** quais perguntas o dado não cobre, por canal, período ou unidade?`
- [src/content/docs/metodo/oito-dimensoes.mdx:11](../src/content/docs/metodo/oito-dimensoes.mdx#L11) `| Contexto | Quando se aplica e quando não se aplica? |`
- [public/downloads/template-dashboard.yaml:32](../public/downloads/template-dashboard.yaml#L32) `comparison_baseline: null`
- [src/content/docs/templates/dataset.mdx:33](../src/content/docs/templates/dataset.mdx#L33) `| Com que frequência atualiza, e com que atraso? | Carga diária ou estática? | Atualização |`

**Impacto:** Mesmo com o portal aplicado à risca, a IA do caso 1 continuaria sem a regra que teria evitado o falso positivo. A promessa do método fica descolada dos problemas de analytics operacional (GTM, GA4, plataformas de mídia) que motivaram o projeto.

**Recomendação:** Acrescentar à trilha de dados uma pergunta obrigatória de comportamento esperado: com que frequência isto acontece, por operação, canal ou unidade; qual janela histórica usar para dizer que algo parou; zero significa ausência de evento ou falha de coleta. Avaliar um modelo leve de plano de medição ou tag plan, com o exemplo de um evento raro e de um evento que só existe em uma operação. Aproveitar o `comparison_baseline` do dashboard como ponto de partida.

### MET-08 · Regras de versão têm tensões internas e campos sem explicação

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** Uma correção só de texto mantém a mesma versão. Isso permite dois textos aprovados diferentes sob o mesmo ID, enquanto o portal diz que duas versões nunca compartilham o mesmo ID e pede para preservar a cópia integral de cada versão aprovada. Não é contradição lógica estrita, mas deixa sem resposta o que fazer com a cópia arquivada depois da correção. Outros pontos:

- A tabela dos "cinco campos" lista cinco informações que somam sete nomes de campo e não inclui `version`.
- O campo `last_reviewed` aparece nos modelos YAML de conceito, KPI e política e em vários exemplos, mas não é explicado em nenhuma página de src.
- O contrato editorial lista como obrigatórios só `version`, `version_date`, `valid_from` e `version_history`, sem `revision_id`, `valid_to` e `supersedes_revision`.
- O `valid_to` exclui o dia no YAML e inclui o dia no Markdown, o que obriga a somar um dia na conversão.

**Evidências:**

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:29](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L29) `duas versões nunca compartilham o mesmo ID`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:90](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L90) `| Só o texto, nada muda no resultado (erro de digitação, link) | Mesma versão | Corrigir uma palavra |`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:82](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L82) `**Preserve a cópia integral das versões aprovadas.**`
- [src/content/docs/metodo/identificacao-versoes.mdx:12](../src/content/docs/metodo/identificacao-versoes.mdx#L12) `## Os cinco campos que resolvem grande parte do problema`
- [public/downloads/template-kpi.yaml:19](../public/downloads/template-kpi.yaml#L19) `last_reviewed: null`
- [docs/CONTRATO_EDITORIAL.md:100](../docs/CONTRATO_EDITORIAL.md#L100) `Campos obrigatórios em todo modelo e exemplo:`
- [src/content/docs/metodo/identificacao-versoes.mdx:50](../src/content/docs/metodo/identificacao-versoes.mdx#L50) ``Neste framework, `valid_from` inclui o dia inicial e `valid_to` **exclui** o dia informado``
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:37](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L37) ``No Markdown, escreva o último dia em que esta versão vale. No YAML, `valid_to` guarda **o dia seguinte**``

**Impacto:** A versão é um dos pilares que o mantenedor quer. Regras com lacunas e campos sem explicação levam cada equipe a criar sua própria interpretação, que é justamente o problema que o método promete resolver.

**Recomendação:** Escolher entre (a) três níveis no estilo Semantic Versioning (https://semver.org/), com o nível mais baixo para correções de texto e cada mudança com ID próprio, ou (b) manter dois níveis e dizer explicitamente que correções de texto substituem a cópia arquivada sem gerar versão. Documentar `last_reviewed` ou removê-lo. Considerar `valid_to` com o último dia incluído nos dois formatos. Alinhar o contrato editorial à lista real de campos.

### MET-09 · O portal não explica onde nem como guardar as versões

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O portal exige cópia integral de cada versão aprovada, mas não diz onde nem como guardá-la (Git, histórico do Google Docs ou do SharePoint, pasta de arquivo) e deixa isso para a governança da organização. O próprio portal só guarda cópias de dois tipos de documento. O roadmap ainda tem "governança de versões" como item não feito.

**Evidências:**

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:82](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L82) `**Preserve a cópia integral das versões aprovadas.**`
- [src/content/docs/validacao/checklist.mdx:65](../src/content/docs/validacao/checklist.mdx#L65) `Registrar a aprovação e o arquivo da versão, segundo a governança da organização`
- [src/content/docs/metodo/identificacao-versoes.mdx:87](../src/content/docs/metodo/identificacao-versoes.mdx#L87) `No portal, só conceito e KPI guardam **cópias integrais** das versões antigas.`
- [docs/ROADMAP.md:55](../docs/ROADMAP.md#L55) `- [ ] Planejar contribuições e governança de versões`

**Impacto:** Para o público não técnico, a regra fica abstrata sem um caminho prático, e as versões tendem a se perder. Para agentes, a falta de convenção de arquivo e pasta dificulta recuperar a versão que valia numa data.

**Recomendação:** Acrescentar um guia curto "Onde guardar as versões", com duas trilhas: sem Git (Google Docs ou SharePoint com histórico ligado e uma pasta "arquivo" com nomes no formato `id@versão`) e com Git (um arquivo por documento, uma tag ou commit por versão aprovada e uma pasta `historico/`, como já faz `public/downloads/historico`).

### MET-10 · A matriz RACI omite o papel Responsável e a letra R colide com o vocabulário

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** A tabela de papéis define "Responsável" como quem mantém o documento, mas a RACI logo abaixo não tem coluna para esse papel. Na mesma página, R significa "executa", enquanto o portal usa "responsável" para quem mantém. Um leitor não técnico vai ler R como "Responsável".

**Evidências:**

- [src/content/docs/governanca/papeis.mdx:14](../src/content/docs/governanca/papeis.mdx#L14) `| Responsável | Mantém o documento: registra mudanças, versões e perguntas em aberto |`
- [src/content/docs/governanca/papeis.mdx:37](../src/content/docs/governanca/papeis.mdx#L37) `| Atividade | Especialista | Quem aprova | Governança | Engenharia IA |`
- [src/content/docs/governanca/papeis.mdx:45](../src/content/docs/governanca/papeis.mdx#L45) `R = executa; A = responde pela aprovação final; C = consultado; I = informado.`

**Impacto:** O papel que mantém versões e perguntas em aberto, central no método, some da matriz. A ambiguidade da palavra "responsável" confunde o público misto.

**Recomendação:** Incluir a coluna "Responsável (mantém)" na RACI, com atividades como registrar versão e manter as perguntas em aberto, e trocar a legenda de siglas por palavras por extenso.

### MET-04 · A página das dimensões promete uma origem por dimensão que a bibliografia não mostra

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** A página das oito dimensões diz que a bibliografia mostra de onde vem a inspiração de cada uma. Na tabela de rastreabilidade, o método aparece numa linha com "afinidade temática" genérica com IIBA, KCS e DCMI. Outras linhas ligam decisões próximas de algumas dimensões a fontes (SKOS para sinônimos, KCS para versões, DMN para precedência), mas não há um mapeamento explícito de cada dimensão a uma fonte nem justificativa para o número oito.

**Evidências:**

- [src/content/docs/metodo/oito-dimensoes.mdx:34](../src/content/docs/metodo/oito-dimensoes.mdx#L34) `a [bibliografia](../../referencias/) mostra de onde vem a inspiração de cada uma`
- [src/content/docs/referencias/index.mdx:50](../src/content/docs/referencias/index.mdx#L50) `| Método das oito dimensões | Afinidade temática com IIBA, KCS e DCMI; formulação própria | Perguntas de elicitação que qualquer especialista pode usar |`

**Impacto:** A promessa não se cumpre de forma direta justamente na página que sustenta a credibilidade do método. Um leitor crítico percebe.

**Recomendação:** Trocar o texto por "a bibliografia mostra as fontes que inspiraram o método como um todo", ou acrescentar uma tabela de dimensão por fonte (Significado e SKOS; Vigência e DCMI `dcterms:valid` e PROV-O; Responsabilidade e KCS; Regras e Exceções e DMN). Explicar em uma frase por que são oito.

### MET-11 · A forma de registrar o Relatado muda de página para página

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** O roteiro de descoberta usa `reported_practice`, campo que não existe em nenhum modelo. A página de campos manda registrar o relatado nas perguntas em aberto. O modelo de KPI em Markdown tem duas seções de perguntas em aberto seguidas. O roteiro de revisão documental e o checklist usam rótulos diferentes para o resultado da aprovação.

**Evidências:**

- [src/content/docs/metodo/elicitar.mdx:29](../src/content/docs/metodo/elicitar.mdx#L29) `reported_practice: "A equipe geralmente exclui cancelamentos."`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:106](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L106) `| **Relatado** | “A gente costuma fazer assim”, sem fonte ou confirmação | Em perguntas em aberto, como prática a confirmar |`
- [public/downloads/template-kpi.md:63](../public/downloads/template-kpi.md#L63) `## 8. Perguntas ainda em aberto`
- [public/downloads/template-kpi.md:66](../public/downloads/template-kpi.md#L66) `## Perguntas em aberto`
- [public/downloads/roteiro-revisao-documental.md:63](../public/downloads/roteiro-revisao-documental.md#L63) `- Resultado: **aprovado / em aberto, à espera de esclarecimento / devolvido para correção**`
- [src/content/docs/validacao/checklist.mdx:54](../src/content/docs/validacao/checklist.mdx#L54) `aprovado para o uso definido, devolvido para correção ou ainda pendente de aprovação`

**Impacto:** São inconsistências pequenas que, somadas, reforçam a sensação de colcha de retalhos e confundem quem copia a estrutura.

**Recomendação:** Adotar `reported_practice` como campo oficial das perguntas em aberto em todos os modelos, ou removê-lo do roteiro. Fundir as duas seções do `template-kpi.md`. Unificar os rótulos de resultado entre o checklist e o roteiro de revisão documental.

### MET-12 · A ressalva sobre o documento "não escrito às cegas" exagera um pouco

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** Segundo a leitura do artigo feita pelo analista original, o documento semântico do estudo foi escrito por um analista que conhecia o dataset, mas não tinha visto as perguntas do benchmark na forma final. O portal diz que o documento "não foi escrito às cegas em relação às perguntas", o que sugere que o autor viu as perguntas.

**Evidências:**

- [src/content/docs/referencias/index.mdx:36](../src/content/docs/referencias/index.mdx#L36) `O documento semântico não foi escrito às cegas em relação às perguntas.`

**Impacto:** Imprecisão pequena, mas numa seção cuja força é a exatidão das ressalvas.

**Recomendação:** Reescrever como: "O documento foi escrito por um analista que conhecia o dataset, mas não as perguntas na forma final; os autores reconhecem que um documento escrito antes de qualquer contato com o benchmark poderia render menos."

**Observação no portal:** PDF de https://arxiv.org/pdf/2604.25149, seção 6.5: o documento foi escrito por um analista que "had seen the dataset but had not seen the benchmark questions in their final form". Leitura do analista original, não reconferida nesta verificação.

### MET-13 · O próprio projeto não segue as regras de versão que ensina

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** O método pede versão, data e histórico em todo documento, mas os documentos do projeto usam marcações diferentes: v0.4 no README, "v0.5 em construção" no roadmap, 0.3 no contrato editorial e "após v0.3" no plano de validação. Não há CHANGELOG na raiz, e as páginas do método não exibem versão nem data. A busca em src não encontrou marcação de versão na página inicial.

**Evidências:**

- [README.md:13](../README.md#L13) `## O que existe na v0.4`
- [docs/ROADMAP.md:40](../docs/ROADMAP.md#L40) `## Consolidação da experiência (v0.5 em construção)`
- [docs/CONTRATO_EDITORIAL.md:3](../docs/CONTRATO_EDITORIAL.md#L3) `**Versão:** 0.3 · **Data desta versão:** 2026-11-17`
- [docs/PLANO_VALIDACAO.md:1](../docs/PLANO_VALIDACAO.md#L1) `# Plano de validação com leitores: proposta para após v0.3`

**Impacto:** Regras de versão que não são aplicadas ao próprio método perdem força como exemplo, sobretudo se a documentação vai ser lida por agentes.

**Recomendação:** Criar um `CHANGELOG.md` no formato do histórico de versões do portal, mostrar versão e data do método nas páginas do método e alinhar os números de versão do README, do roadmap, do contrato editorial e do plano de validação.

### MET-14 · A distinção entre tácito e explícito é atribuída só a Nonaka, sem Polanyi

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** A página de conhecimento tácito apresenta a distinção como central "especialmente em Nonaka (1994)". A distinção vem de Michael Polanyi, de quem Nonaka parte. A bibliografia também cita só Nonaka para esse tema.

**Evidências:**

- [src/content/docs/fundamentos/conhecimento-tacito.mdx:9](../src/content/docs/fundamentos/conhecimento-tacito.mdx#L9) `A distinção entre conhecimento tácito e explícito é central na literatura de criação do conhecimento organizacional, especialmente em Nonaka (1994).`

**Impacto:** Atribuição incompleta numa página conceitual. Impacto baixo, mas pesa para leitores acadêmicos.

**Recomendação:** Citar Polanyi, M. (1966), *The Tacit Dimension*, como origem da distinção, e manter Nonaka (1994) como aplicação organizacional.

### MET-15 · A separação entre responder, esclarecer e abster-se é atribuída a uma fonte que não a sustenta como escrito

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** A bibliografia atribui a decisão a "Microsoft RAG, princípios de evidência". A página da Microsoft sobre recuperação fala de exemplos positivos e negativos na avaliação, não de pedir esclarecimento nem de abstenção. "Princípios de evidência" não tem referência.

**Evidências:**

- [src/content/docs/referencias/index.mdx:62](../src/content/docs/referencias/index.mdx#L62) `| Separar responder, esclarecer e abster-se | Microsoft RAG, princípios de evidência | Perguntas de referência e limites conhecidos |`

**Impacto:** É uma das decisões mais úteis do portal, e a fonte atribuída não a sustenta como está escrito.

**Recomendação:** Descrever a origem com precisão: a Microsoft sustenta testar casos positivos e negativos e prever perguntas que o acervo não responde; a distinção entre pedir esclarecimento e abster-se é decisão própria do Contexto. Se quiser fonte para essa distinção, conferir e citar trabalhos sobre abstenção em text-to-SQL.

**Observação no portal:** A página https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval diz "You should test positive and negative examples", e o analista original não encontrou nela menção a esclarecimento nem a abstenção. Nesta rodada, a página da fase de preparação (https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-preparation-phase) tem a seção "Unaddressed queries", que orienta a solução a dizer que não sabe a resposta. Ela sustenta a abstenção, mas não a etapa de pedir esclarecimento, e não é a página que a bibliografia sugere.

### MET-16 · A eficácia do método não foi testada e o plano de validação está parado

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** O portal admite que o método não foi testado com pessoas. O plano de validação ainda se apresenta como "proposta para após v0.3", e o teste com participantes segue em aberto no roadmap. Não há critério de êxito ligado ao objetivo de formular perguntas de negócio.

**Evidências:**

- [src/content/docs/metodo/limites.mdx:52](../src/content/docs/metodo/limites.mdx#L52) `o [plano de validação](https://github.com/edoardolobl/contexto-framework/blob/main/docs/PLANO_VALIDACAO.md) está publicado e aguarda execução.`
- [docs/PLANO_VALIDACAO.md:1](../docs/PLANO_VALIDACAO.md#L1) `# Plano de validação com leitores: proposta para após v0.3`
- [docs/ROADMAP.md:48](../docs/ROADMAP.md#L48) `- [ ] Teste de compreensão com participantes externos (issue #4; após estabilizar os materiais)`

**Impacto:** A credibilidade de longo prazo depende de mostrar que o método funciona com o público-alvo. Hoje a única evidência é a lógica interna e um preprint sobre LLMs, não sobre o método.

**Recomendação:** Atualizar o plano para a versão atual e incluir um cenário que reproduza os dois casos do mantenedor: a pessoa formula a pergunta de negócio, documenta a regra que falta e um agente responde antes e depois. Um piloto com 2 ou 3 pessoas já gera uma evidência citável.

## Descartados na verificação

- **MET-R1:** Havia a suspeita de que o portal errava ao dizer "99 perguntas" quando o resumo do arXiv diz 100. O PDF confirma que a q33 foi excluída e que todas as análises usam n=99; o portal está correto.
- **MET-R2:** Havia a suspeita de que "nas mesmas seis sessões" contradizia "quatro elegíveis". O `aurora-fixture.sql` tem 6 sessões, das quais S3 (interna) e S4 (app) ficam fora pelos filtros, o que deixa 4 elegíveis. Não há contradição.
- **MET-R3:** As afirmações sobre a ISO 30401 (emendas de 2022 e 2024, em revisão) conferem com a página da ISO.
- **MET-R4:** Os campos atribuídos ao Snowflake Semantic Views existem na especificação YAML (`synonyms`, `sample_values`, `relationships`, `verified_queries`). A licença CC BY-NC 4.0 do guia KCS e o DMN 1.6 na OMG também conferem.

## Não coberto nesta rodada

- Conteúdo das páginas do IIBA Business Analysis Standard e do BABOK v3, capítulo 4: o acesso exige login.
- Texto da ISO 30401 (norma paga): não foi verificado se a cláusula de papéis sustenta a citação em `governanca/papeis.mdx`.
- Texto integral de Nonaka (1994) e a relação com Polanyi: vêm de conhecimento prévio, não de leitura nesta rodada.
- O PDF do arXiv 2604.25149 não foi reaberto nesta verificação. As afirmações de MET-12 e a observação de MET-06 sobre Zargari Marandi e Painter dependem da leitura do analista original.
- Os modelos e páginas de processo, decisão, política, rubrica, dataset, relacionamento e dashboard não foram lidos por completo.
- Validadores e build não foram executados, e o portal publicado não foi conferido no navegador; a execução estava bloqueada.
- WebMCP, Personal Agent Protocol e UCP estão fora do foco desta dimensão.
- Não foi feita a comparação das oito dimensões com ISO/IEC 11179 e Datasheets for Datasets.
