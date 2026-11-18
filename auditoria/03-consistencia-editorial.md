# Consistência editorial

Data: 2026-11-17 · Commit: d08c810 · Escopo: vocabulário, nomes de modelos e verificações, estrutura das páginas de tipo, rótulos de campos de versão e coerência entre portal (`src/content/docs`, `src/components`, `public/downloads`), README, ROADMAP e `docs/CONTRATO_EDITORIAL.md`.

## Resumo

- A espinha das páginas de tipo é uniforme: as 10 páginas seguem as cinco seções H2 do contrato na mesma ordem, com dois cartões de exemplo e um bloco de downloads cada. A sensação de colcha de retalhos vem de outro lugar.
- A colcha aparece nos nomes: a mesma ideia recebe vários rótulos (terceira verificação, página de revisão, modelos, campos de versão, aprovar x validar x homologar), e algumas palavras centrais do vocabulário (responsável, roteiro, ficha, pedido, cartão) ganham mais de um sentido.
- Há desvios pontuais da estrutura fixa: a tabela O que perguntar muda de formato em 3 páginas, O problema não traz números em 2, e seções extras aparecem em posições variáveis. O contrato também não descreve blocos que todas as páginas têm.
- README e ROADMAP ficam fora do validador e contradizem o vocabulário, a versão publicada e a organização do menu. São a primeira coisa que um visitante do GitHub lê.
- A promessa do método pressupõe um engenheiro de IA entre especialista e sistema. O portal não menciona o uso direto por Claude Code, Codex ou Antigravity, nem traz exemplos de GA4, GTM, tag plan ou BigQuery, que são os casos que motivaram o projeto.
- Verificação independente: as 178 citações conferem com as linhas indicadas (reconferidas na conferência final). Cinco achados foram ajustados e sete tiveram a severidade rebaixada (ver "Descartados na verificação").

## Pontos fortes (manter)

**Sequência macro das páginas de tipo é uniforme.** As 10 páginas de tipo têm as cinco seções H2 do contrato na mesma ordem (algumas com H2 extras entre elas), dois ExampleDoc cada e um TemplateDownloads. Essa é a espinha que deve ser preservada.

- [src/content/docs/templates/kpi.mdx:15](../src/content/docs/templates/kpi.mdx#L15) `## O problema`
- [src/content/docs/templates/dataset.mdx:39](../src/content/docs/templates/dataset.mdx#L39) `## Antes e depois da decisão`
- [src/content/docs/templates/rubrica.mdx:81](../src/content/docs/templates/rubrica.mdx#L81) `## Teste você`

**Vocabulário e aviso de ficção garantidos por validador nas páginas.** O validador percorre páginas, componentes e downloads e recusa as formas proibidas e o aviso de ficção fora dos lugares combinados. Amostra sintética fica restrita ao laboratório.

- [scripts/validate_content.py:305](../scripts/validate_content.py#L305) `TERM_FILES = [`
- [scripts/validate_content.py:323](../scripts/validate_content.py#L323) `FICTION = re.compile(`
- [src/content/docs/exemplos/analytics-integrado.mdx:14](../src/content/docs/exemplos/analytics-integrado.mdx#L14) `O laboratório usa uma amostra sintética pequena`

**Universo Aurora coerente entre páginas e cartões.** Datas, prazos em dias úteis e versões batem entre texto e YAML. Isso dá credibilidade e serve de molde concreto.

- [src/content/docs/templates/politica.mdx:65](../src/content/docs/templates/politica.mdx#L65) `O conflito foi resolvido em 14/08, depois da despesa`
- [public/downloads/exemplo-politica-completo.yaml:76](../public/downloads/exemplo-politica-completo.yaml#L76) `resolved_at: "2026-08-14"`
- [src/content/docs/templates/processo.mdx:106](../src/content/docs/templates/processo.mdx#L106) `Ao fim de terça, 22/09: são 2 dias úteis, e o fim de semana não conta.`

**Problemas abertos com conflito numérico concreto.** Os melhores exemplos mostram o custo da ambiguidade com números. É exatamente o tipo de molde que o projeto quer oferecer.

- [src/content/docs/templates/conceito.mdx:20](../src/content/docs/templates/conceito.mdx#L20) `Em 30/09, o RH informou **214** participantes ativos; a coordenação do programa informou **131**.`
- [src/content/docs/templates/rubrica.mdx:10](../src/content/docs/templates/rubrica.mdx#L10) `Dois revisores, o mesmo e-mail, notas 8 e 4`

**Tabelas O que perguntar ensinam perguntas de negócio.** Ajudam a produzir documentação a partir de perguntas de negócio, um objetivo declarado do projeto.

- [src/content/docs/templates/conceito.mdx:37](../src/content/docs/templates/conceito.mdx#L37) `| Que regra coloca alguém dentro do termo? | Uma inscrição ainda não iniciada conta como participação ativa? | Critérios de inclusão e exclusão |`
- [src/content/docs/templates/kpi.mdx:27](../src/content/docs/templates/kpi.mdx#L27) `“Conversão” é pedido criado, pago, confirmado ou entregue?`

**Tríade Confirmado / Relatado / Em aberto usada de forma estável.** Termo central explicado com exemplo e usado com o mesmo sentido em Comece, Como ler os campos, a página de descoberta e os modelos.

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:101](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L101) `Esses três nomes aparecem em todo o portal com o mesmo sentido`
- [src/content/docs/metodo/elicitar.mdx:40](../src/content/docs/metodo/elicitar.mdx#L40) `O encontro termina com três listas curtas`

**Teste você atravessa mudanças de versão.** Ensina vigência na prática, com respostas escondidas. É o diferencial pedagógico do portal.

- [src/content/docs/templates/conceito.mdx:75](../src/content/docs/templates/conceito.mdx#L75) `Em 31/08 ainda valia a versão 1.0, com janela de 60 dias`
- [src/content/docs/templates/decisao.mdx:68](../src/content/docs/templates/decisao.mdx#L68) `Em 20/08 valia a versão 1.0, que mandava evidência desconhecida para revisão.`

**Ressalvas honestas sobre fontes e limites.** O preprint aparece com seus limites e há uma página dedicada aos limites do método. Isso sustenta a credibilidade.

- [src/content/docs/dados/visao-geral.mdx:41](../src/content/docs/dados/visao-geral.mdx#L41) `É **um indício de utilidade**, não prova de suficiência nem garantia de produção.`
- [src/content/docs/metodo/limites.mdx:43](../src/content/docs/metodo/limites.mdx#L43) `Entregar um documento incompleto e transparente é um resultado legítimo.`

**Regra de numeração de versão alinhada entre contrato e portal.** Contrato e Como ler os campos usam a mesma pergunta de decisão e a mesma tabela.

- [docs/CONTRATO_EDITORIAL.md:124](../docs/CONTRATO_EDITORIAL.md#L124) `| Muda algum resultado | Maior (1.0 → 2.0) |`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:86](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L86) `A pergunta que decide o número é`

**Menu igual ao título.** Elimina uma fonte comum de divergência de nomes na navegação.

- [astro.config.mjs:43](../astro.config.mjs#L43) `Sem rótulos próprios: o menu mostra o título da página`

## Índice de achados

| ID | Severidade | Título |
|---|---|---|
| EDI-01 | Média | Promessa pressupõe um engenheiro de IA entre especialista e sistema |
| EDI-31 | Média | Exemplos não cobrem os cenários reais que motivaram o projeto |
| EDI-02 | Média | Terceira verificação tem quatro nomes, e um deles contraria o vocabulário |
| EDI-15 | Média | Aprovar, validar, confirmar, homologar e revisar usados para o mesmo ato |
| EDI-13 | Média | RACI usa R = executa e não tem a coluna Responsável |
| EDI-16 | Média | Página de Perguntas de referência contradiz o próprio YAML sobre quem conferiu |
| EDI-03 | Média | A página de revisão e seus arquivos têm vários nomes; roteiro e ficha servem para várias coisas |
| EDI-08 | Média | Modelos com vários nomes: decisão, perguntas de referência, dashboard, conceito |
| EDI-14 | Média | Campos de versão com rótulos diferentes entre páginas, componentes e modelos |
| EDI-04 | Média | Tabela O que perguntar foge do formato do contrato em 3 das 10 páginas |
| EDI-05 | Média | O problema sem conflito numérico em Processo e Perguntas de referência |
| EDI-06 | Média | Seções extras e faltantes em posições variáveis nas páginas de tipo |
| EDI-26 | Média | Vários modelos de processo do método convivem sem relação explícita |
| EDI-10 | Média | Seletor e tabela da página de modelos descrevem os mesmos 10 modelos com frases diferentes |
| EDI-21 | Média | Jargão técnico sem explicação para leitor não técnico |
| EDI-18 | Média | README e ROADMAP violam vocabulário e aviso de ficção; o validador não os cobre |
| EDI-19 | Média | Versões divergentes entre portal, README, ROADMAP e contrato |
| EDI-07 | Baixa | Contrato não descreve blocos que todas as páginas têm; botão de download duplicado |
| EDI-09 | Baixa | Identidade do projeto oscila entre framework, método, metodologia e guia |
| EDI-11 | Baixa | Quatro camadas, quatro modelos lista cinco modelos |
| EDI-12 | Baixa | Definição de Exceções contraditória entre checklist e oito dimensões |
| EDI-17 | Baixa | Categorias de perguntas diferem entre modelo, laboratório, YAML e ROADMAP |
| EDI-20 | Baixa | Rubrica fica em trilhas diferentes no README/ROADMAP e no portal |
| EDI-22 | Baixa | Ressalvas de limite repetidas em várias páginas |
| EDI-23 | Baixa | A conta 25% x 50% é repetida em muitas páginas |
| EDI-24 | Baixa | O exemplo de metadados do contrato não segue as regras do próprio contrato |
| EDI-25 | Baixa | Explicações duplicadas e divergentes sobre Obsoleto e vigência |
| EDI-27 | Baixa | Palavras com dois sentidos: pedido e cartão |
| EDI-28 | Baixa | Bibliografia cita diagramas ASCII que não existem nas páginas |
| EDI-29 | Baixa | Modelo KPI em Markdown com seção de perguntas em aberto duplicada e numeração própria |
| EDI-30 | Baixa | Exemplo da página inicial desconectado dos exemplos da Aurora |
| EDI-32 | Baixa | Termos em inglês em textos de governança e componentes |

Dentro de cada severidade, os achados vêm primeiro pelo efeito no público-alvo e no método, depois pela facilidade de correção.

## Achados

### EDI-01 · Promessa pressupõe um engenheiro de IA entre especialista e sistema

**Severidade:** Média (rebaixada de alta na verificação)
**Confiança:** Média

**O que acontece:** Contrato, README, checklist, Responsabilidades e a visão geral do método descrevem uma passagem do especialista para a engenharia de IA. O caso que motivou o projeto é outro: o analista conecta Claude Code, Codex ou Antigravity direto a Databricks, GA4 ou planilhas, sem engenheiro no meio. Uma busca em páginas e componentes não encontra menção a Claude, Codex, Antigravity, NotebookLM ou ao agente que a própria pessoa usa.

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:13](../docs/CONTRATO_EDITORIAL.md#L13) `para que engenheiros de IA não precisem inventar regras ausentes ou inferir significados`
- [README.md:5](../README.md#L5) `de forma que engenheiros de IA não precisem inventar semântica de negócio`
- [src/content/docs/validacao/checklist.mdx:70](../src/content/docs/validacao/checklist.mdx#L70) `Não cabe ao engenheiro de IA descobrir sozinho regras, significados ou exceções`
- [src/content/docs/governanca/papeis.mdx:17](../src/content/docs/governanca/papeis.mdx#L17) `| Engenharia de IA | Especifica requisitos de consumo, integra e testa os sistemas |`
- [src/content/docs/metodo/visao-geral.mdx:6](../src/content/docs/metodo/visao-geral.mdx#L6) `para que quem constrói sistemas de IA não precise adivinhar regras`

**Impacto:** O público principal real (o analista que usa o agente direto) não se reconhece na promessa. Isso também enfraquece a ponte futura para skills, WebMCP e documentação para agentes.

**Recomendação:** Reescrever a Promessa única para incluir o uso direto pelo agente (o documento como contexto para o agente que a pessoa já usa). Manter a engenharia de IA como um dos consumidores, não o único.

**Observação no portal:** Nenhuma página publicada cita os harnesses que o público já usa; a engenharia de IA aparece como o único consumidor explícito.

### EDI-31 · Exemplos não cobrem os cenários reais que motivaram o projeto

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** A trilha de dados se apoia numa única amostra de duas tabelas e seis sessões, num único dia. Não há exemplo de eventos de tracking (GA4/GTM, tag plan), de mídia, de várias operações ou de evento raro que exige histórico. Uma busca nas páginas não encontra GA4, GTM, tag plan nem BigQuery. Databricks aparece só num link da fundamentação do dataset.

**Evidências:**

- [src/content/docs/exemplos/analytics-integrado.mdx:18](../src/content/docs/exemplos/analytics-integrado.mdx#L18) `` `demo_sessions`: uma linha por sessão. ``
- [src/content/docs/dados/visao-geral.mdx:45](../src/content/docs/dados/visao-geral.mdx#L45) `duas tabelas pequenas, uma definição, uma consulta de referência e um dashboard, todos ligados`
- [src/content/docs/exemplos/analytics-integrado.mdx:40](../src/content/docs/exemplos/analytics-integrado.mdx#L40) `O período do exemplo é **1º de outubro de 2026**.`

**Impacto:** Um analista com o problema do evento zerado não encontra um molde, e as consultas complexas (várias tabelas e dashboards) ficam sem exemplo.

**Recomendação:** Acrescentar um segundo caso integrado de tracking (tag plan mais tabela de eventos por operação, com regra de granularidade e janela histórica para decidir se um evento está quebrado) e uma pergunta de referência sobre isso.

**Observação no portal:** O laboratório publicado é o único caso integrado de dados, com recorte de um dia.

### EDI-02 · Terceira verificação tem quatro nomes, e um deles contraria o vocabulário

**Severidade:** Média (rebaixada de alta na verificação)
**Confiança:** Alta

**O que acontece:** O contrato separa responsável (quem mantém) de quem aprova (palavra final). O cartão da terceira verificação diz Confirmação por responsável, o ROADMAP diz confirmação pelo responsável, a página diz quem pode aprovar e o README diz quem tem autoridade. O mesmo bloco ainda pede Quem revisou, e o componente chama as verificações de etapas.

**Evidências:**

- [src/components/ReviewStages.astro:23](../src/components/ReviewStages.astro#L23) `title: 'Confirmação por responsável',`
- [docs/CONTRATO_EDITORIAL.md:45](../docs/CONTRATO_EDITORIAL.md#L45) `| Quem tem a palavra final | quem aprova | aprovador |`
- [src/content/docs/validacao/checklist.mdx:45](../src/content/docs/validacao/checklist.mdx#L45) `## 3. Confirmação: quem pode aprovar esta versão?`
- [src/content/docs/validacao/checklist.mdx:51](../src/content/docs/validacao/checklist.mdx#L51) `- **Quem revisou:** pessoa, área ou função com autoridade identificada.`
- [README.md:16](../README.md#L16) `confirmação por quem tem autoridade`
- [docs/ROADMAP.md:45](../docs/ROADMAP.md#L45) `confirmação pelo responsável`
- [src/components/ReviewStages.astro:30](../src/components/ReviewStages.astro#L30) `aria-label="Três etapas independentes de revisão documental"`

**Impacto:** No passo que decide se algo vira regra, o rótulo do cartão usa o termo que o vocabulário reserva para quem mantém, o que embaralha a distinção central do método.

**Recomendação:** Padronizar como Confirmação por quem aprova em todos os lugares, trocar Quem revisou por Quem aprovou nesse bloco e usar só verificações (não etapas).

### EDI-15 · Aprovar, validar, confirmar, homologar e revisar usados para o mesmo ato

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O contrato só fixa revisão como ato de revisar e quem aprova como autoridade. O portal usa homologa, validação, Validar e Peça revisão para o momento da aprovação.

**Evidências:**

- [src/content/docs/templates/conceito.mdx:60](../src/content/docs/templates/conceito.mdx#L60) `| Quem homologa a definição? | A Gerência de Pessoas, com registro em ata |`
- [src/content/docs/templates/index.mdx:36](../src/content/docs/templates/index.mdx#L36) `Só declare a informação aprovada depois da validação de quem responde pelo assunto.`
- [src/content/docs/validacao/checklist.mdx:47](../src/content/docs/validacao/checklist.mdx#L47) `A validação documental depende de alguém com autoridade sobre o assunto.`
- [src/content/docs/metodo/visao-geral.mdx:19](../src/content/docs/metodo/visao-geral.mdx#L19) `| **4. Validar** | Confirmar com a fonte autorizada`
- [docs/CONTRATO_EDITORIAL.md:43](../docs/CONTRATO_EDITORIAL.md#L43) `é só o ato de revisar`

**Impacto:** O validador não pega sinônimos de verbo. O leitor não sabe se revisar já é aprovar, e essa é a distinção que o método mais quer proteger.

**Recomendação:** Ampliar o vocabulário: aprovar (ato de quem aprova), revisar (ler e apontar), conferir (comparar com fonte). Proibir homologar, e validar no sentido de aprovar.

### EDI-13 · RACI usa R = executa e não tem a coluna Responsável

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** A página Responsabilidades define Responsável como quem mantém o documento. A matriz RACI logo abaixo não tem essa coluna e usa R com o sentido de executa, o que colide com o termo do vocabulário. A página também fala em Responsável pelo dado, um terceiro sentido.

**Evidências:**

- [src/content/docs/governanca/papeis.mdx:14](../src/content/docs/governanca/papeis.mdx#L14) `| Responsável | Mantém o documento: registra mudanças, versões e perguntas em aberto |`
- [src/content/docs/governanca/papeis.mdx:37](../src/content/docs/governanca/papeis.mdx#L37) `| Atividade | Especialista | Quem aprova | Governança | Engenharia IA |`
- [src/content/docs/governanca/papeis.mdx:45](../src/content/docs/governanca/papeis.mdx#L45) `R = executa; A = responde pela aprovação final`
- [src/content/docs/governanca/papeis.mdx:28](../src/content/docs/governanca/papeis.mdx#L28) `| Responsável pelo dado, com validação do negócio |`

**Impacto:** O leitor não técnico não consegue mapear os papéis do método para a matriz, e o termo central responsável passa a ter dois sentidos.

**Recomendação:** Incluir a coluna Responsável na matriz, ou explicar que o R do RACI não é o responsável do vocabulário. Avaliar trocar a RACI por uma tabela simples de quem faz o quê.

### EDI-16 · Página de Perguntas de referência contradiz o próprio YAML sobre quem conferiu

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O texto diz que a Gerência de E-commerce conferiria as respostas. O exemplo completo registra que a Analytics de E-commerce conferiu e a Gerência aprovou, e a tabela da própria página diz que quem revisou foi a Analytics.

**Evidências:**

- [src/content/docs/templates/casos-teste.mdx:55](../src/content/docs/templates/casos-teste.mdx#L55) `Enquanto ninguém da Gerência de E-commerce conferiu as respostas, Q01 carrega essa ressalva:`
- [public/downloads/exemplo-casos-teste-completo.yaml:22](../public/downloads/exemplo-casos-teste-completo.yaml#L22) `Primeira versão aprovada, depois que a Analytics de E-commerce conferiu as respostas de Q01 a Q06`
- [public/downloads/exemplo-casos-teste-completo.yaml:23](../public/downloads/exemplo-casos-teste-completo.yaml#L23) `approved_by: "Gerência de E-commerce (Aurora)"`
- [src/content/docs/templates/casos-teste.mdx:35](../src/content/docs/templates/casos-teste.mdx#L35) `| Quem revisou, e quando | Analytics de E-commerce, 02/10/2026 |`

**Impacto:** A página contradiz o cartão que mostra e confunde quem revisa com quem aprova.

**Recomendação:** Trocar a frase por "Enquanto a Analytics de E-commerce não conferiu as respostas e a Gerência não aprovou".

### EDI-03 · A página de revisão e seus arquivos têm vários nomes; roteiro e ficha servem para várias coisas

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** A página Revisar e entregar é chamada de checklist de revisão, roteiro de revisão e Revisar o que já está escrito, e o slug é `validacao/checklist`. O download é chamado de ficha de revisão, mas o arquivo se intitula Roteiro de revisão documental. Ficha também nomeia o pacote de perguntas em aberto. Roteiro também nomeia a página de descoberta, as oito dimensões e os passos de versão.

**Evidências:**

- [src/content/docs/validacao/checklist.mdx:2](../src/content/docs/validacao/checklist.mdx#L2) `title: Revisar e entregar`
- [src/content/docs/fundamentos/comece-em-5-minutos.mdx:64](../src/content/docs/fundamentos/comece-em-5-minutos.mdx#L64) `[Use o checklist de revisão]`
- [src/components/PrincipleTiles.astro:12](../src/components/PrincipleTiles.astro#L12) `title: 'Revisar o que já está escrito',`
- [src/components/PrincipleTiles.astro:14](../src/components/PrincipleTiles.astro#L14) `action: 'Abrir o roteiro de revisão',`
- [src/content/docs/validacao/checklist.mdx:15](../src/content/docs/validacao/checklist.mdx#L15) `[**Baixar ficha de revisão em texto**](../../downloads/roteiro-revisao-documental.md)`
- [public/downloads/roteiro-revisao-documental.md:1](../public/downloads/roteiro-revisao-documental.md#L1) `# Roteiro de revisão documental: Contexto`
- [src/content/docs/validacao/checklist.mdx:81](../src/content/docs/validacao/checklist.mdx#L81) `Quando sobram perguntas, entregue-as numa ficha.`
- [src/content/docs/fundamentos/conhecimento-tacito.mdx:35](../src/content/docs/fundamentos/conhecimento-tacito.mdx#L35) `use o [roteiro de perguntas](../../metodo/elicitar/)`
- [src/content/docs/metodo/oito-dimensoes.mdx:34](../src/content/docs/metodo/oito-dimensoes.mdx#L34) `As oito dimensões são um roteiro autoral.`
- [src/content/docs/metodo/identificacao-versoes.mdx:76](../src/content/docs/metodo/identificacao-versoes.mdx#L76) `Esse roteiro é um **critério para documentar e revisar**`

**Impacto:** O leitor não sabe se checklist, roteiro e ficha são a mesma coisa. Isso confunde a navegação e o que deve ser baixado.

**Recomendação:** Acrescentar ao vocabulário do contrato: roteiro (de perguntas), ficha de revisão, ficha de perguntas em aberto e checklist. Alinhar o título do arquivo baixável e os textos de chamada.

### EDI-08 · Modelos com vários nomes: decisão, perguntas de referência, dashboard, conceito

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O modelo de decisão se chama Regras e decisões, Modelo de decisão e regra de triagem. O de perguntas de referência se chama `casos-teste` (slug), Modelo de gabarito, Perguntas de referência e gabarito e, no README, um quarto nome com a forma proibida pelo vocabulário. O documento de dashboard é chamado de guia de leitura, e o conceito, de glossário.

**Evidências:**

- [src/content/docs/templates/decisao.mdx:2](../src/content/docs/templates/decisao.mdx#L2) `title: Regras e decisões`
- [src/components/TemplateDownloads.astro:20](../src/components/TemplateDownloads.astro#L20) `{ name: 'Modelo de decisão'`
- [src/content/docs/templates/processo.mdx:76](../src/content/docs/templates/processo.mdx#L76) `conforme a [regra de triagem](../decisao/)`
- [src/components/TemplateDownloads.astro:56](../src/components/TemplateDownloads.astro#L56) `{ name: 'Modelo de gabarito', href: 'template-casos-teste.md'`
- [public/downloads/template-casos-teste.md:1](../public/downloads/template-casos-teste.md#L1) `# [Perguntas de referência e gabarito]`
- [README.md:27](../README.md#L27) `**Perguntas e respostas de referência**`
- [src/components/TemplateStart.astro:51](../src/components/TemplateStart.astro#L51) `result: 'Um guia de leitura com indicadores, escopo, filtros, atualização e fontes.',`
- [docs/ROADMAP.md:12](../docs/ROADMAP.md#L12) `Conceitos/glossário + exemplo RH`

**Impacto:** Viola o princípio Um termo por ideia nos próprios produtos do método. O leitor não sabe se triagem é outro documento.

**Recomendação:** Fixar no vocabulário um nome por modelo e um nome para o artefato que ele produz. Ajustar componentes, Markdown e textos de ligação. Avaliar renomear o slug `casos-teste` com redirecionamento.

### EDI-14 · Campos de versão com rótulos diferentes entre páginas, componentes e modelos

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** `version_date` aparece como Data desta versão e como Data do registro. `valid_from` aparece como Vale a partir de e como Regra válida desde. `revision_id` aparece como Identificador da versão, ID da versão e Identificador desta versão.

**Evidências:**

- [src/content/docs/fundamentos/como-ler-os-campos.mdx:35](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L35) `` | Data desta versão | `version_date` | ``
- [src/content/docs/metodo/identificacao-versoes.mdx:18](../src/content/docs/metodo/identificacao-versoes.mdx#L18) `` | **Data do registro** | `version_date` | ``
- [src/components/RevisionComparison.astro:38](../src/components/RevisionComparison.astro#L38) `<div><dt>Regra válida desde</dt>`
- [public/downloads/template-kpi.md:21](../public/downloads/template-kpi.md#L21) `| Vale a partir de | |`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:29](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L29) `` | Identificador da versão | `revision_id` | ``
- [src/content/docs/metodo/identificacao-versoes.mdx:17](../src/content/docs/metodo/identificacao-versoes.mdx#L17) `` | **ID da versão** | `revision_id` | ``
- [public/downloads/template-kpi.md:19](../public/downloads/template-kpi.md#L19) `| Identificador desta versão | |`

**Impacto:** O versionamento é o diferencial do método. Rótulos variáveis fazem o leitor duvidar se são campos diferentes.

**Recomendação:** Acrescentar ao contrato uma tabela de rótulos de campo (YAML x português) e usá-la em páginas, componentes e modelos Markdown.

### EDI-04 · Tabela O que perguntar foge do formato do contrato em 3 das 10 páginas

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O contrato manda uma tabela com pergunta, como aparece na Aurora e o que registrar. A do KPI troca a última coluna por nomes de campos YAML. A do processo inverte a ordem e começa por Elemento. A de Perguntas de referência tem duas colunas e lista o que registrar em cada pergunta, não perguntas a fazer ao especialista.

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:138](../docs/CONTRATO_EDITORIAL.md#L138) `2. **O que perguntar**, numa tabela só: pergunta, como ela aparece na Aurora, o que registrar.`
- [src/content/docs/templates/conceito.mdx:35](../src/content/docs/templates/conceito.mdx#L35) `| Pergunta | Na Aurora | O que registrar |`
- [src/content/docs/templates/kpi.mdx:25](../src/content/docs/templates/kpi.mdx#L25) `| Pergunta | O que ela descobre | Campo do modelo |`
- [src/content/docs/templates/processo.mdx:26](../src/content/docs/templates/processo.mdx#L26) `| Elemento | Na frase da Aurora | Pergunta a fazer |`
- [src/content/docs/templates/casos-teste.mdx:28](../src/content/docs/templates/casos-teste.mdx#L28) `| O que registrar em cada pergunta | Na Aurora, para Q01 |`

**Impacto:** A seção que mais ensina a fazer perguntas de negócio muda de forma entre páginas. No KPI, o leitor não técnico recebe nomes de campos YAML no lugar do que registrar.

**Recomendação:** Normalizar as três tabelas no formato Pergunta | Na Aurora | O que registrar. Para Perguntas de referência, listar perguntas que o especialista deve fazer ao montar o gabarito.

### EDI-05 · O problema sem conflito numérico em Processo e Perguntas de referência

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O contrato exige que o exemplo comece por um conflito com números e que O problema traga números. Processo abre com uma frase vaga sem números, e Perguntas de referência abre com uma explicação conceitual.

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:89](../docs/CONTRATO_EDITORIAL.md#L89) `1. **Começa por um conflito com números:**`
- [docs/CONTRATO_EDITORIAL.md:137](../docs/CONTRATO_EDITORIAL.md#L137) `1. **O problema**, com números:`
- [src/content/docs/templates/processo.mdx:20](../src/content/docs/templates/processo.mdx#L20) `Parece um fluxo, mas omite entradas, aprovações, condições, exceções e evidências.`
- [src/content/docs/templates/casos-teste.mdx:16](../src/content/docs/templates/casos-teste.mdx#L16) `Antes de uma equipe técnica avaliar um RAG ou agente, quem responde pelo conhecimento precisa dizer`

**Impacto:** As duas páginas perdem a abertura que torna o problema palpável, justo no modelo mais ligado a testar agentes.

**Recomendação:** Abrir Processo com um custo mensurável (ex.: publicações sem comprovante encontradas pela auditoria). Abrir Perguntas de referência com um agente que respondeu 50% quando o certo era pedir esclarecimento.

### EDI-06 · Seções extras e faltantes em posições variáveis nas páginas de tipo

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O subtítulo O que o histórico de versões ensina falta em Política, que usa outro título, e em Perguntas de referência. Conceito, Processo, Política e Rubrica têm H2 extras entre Teste você e Baixe o modelo, cada um com nome diferente. O KPI abre com um antes e depois (BeforeAfter) além do par de cartões.

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:139](../docs/CONTRATO_EDITORIAL.md#L139) `3. **Antes e depois da decisão**: o cartão com lacunas e o cartão completo, cada um uma vez, e o que o histórico de versões ensina.`
- [src/content/docs/templates/politica.mdx:67](../src/content/docs/templates/politica.mdx#L67) `### Duas versões diferentes no mesmo documento`
- [src/content/docs/templates/conceito.mdx:77](../src/content/docs/templates/conceito.mdx#L77) `## Termo preferido, sinônimo e termo relacionado`
- [src/content/docs/templates/processo.mdx:110](../src/content/docs/templates/processo.mdx#L110) `## Verifique o seu documento`
- [src/content/docs/templates/politica.mdx:82](../src/content/docs/templates/politica.mdx#L82) `## Verifique o seu documento`
- [src/content/docs/templates/rubrica.mdx:92](../src/content/docs/templates/rubrica.mdx#L92) `## O que uma IA revisora pode e não pode fazer`
- [src/content/docs/templates/kpi.mdx:19](../src/content/docs/templates/kpi.mdx#L19) `<BeforeAfter />`

**Impacto:** O leitor que passa de uma página para outra não encontra os mesmos blocos no mesmo lugar, e o conteúdo extra parece remendo.

**Recomendação:** Definir no contrato uma seção opcional padrão (ex.: Aprofundamento) numa posição fixa e padronizar o subtítulo do histórico.

### EDI-26 · Vários modelos de processo do método convivem sem relação explícita

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** A visão geral tem cinco movimentos (com o cabeçalho Etapa), as oito dimensões têm uma seção Como aplicar com passos próprios, e o checklist anuncia três verificações mas numera até 4 (Entregar). Não há uma página que mostre como esses roteiros se encaixam.

**Evidências:**

- [src/content/docs/metodo/visao-geral.mdx:12](../src/content/docs/metodo/visao-geral.mdx#L12) `## Os cinco movimentos`
- [src/content/docs/metodo/visao-geral.mdx:14](../src/content/docs/metodo/visao-geral.mdx#L14) `| Etapa | O que fazer | Saída esperada |`
- [src/content/docs/metodo/oito-dimensoes.mdx:36](../src/content/docs/metodo/oito-dimensoes.mdx#L36) `## Como aplicar`
- [src/content/docs/validacao/checklist.mdx:13](../src/content/docs/validacao/checklist.mdx#L13) `siga as três verificações abaixo`
- [src/content/docs/validacao/checklist.mdx:68](../src/content/docs/validacao/checklist.mdx#L68) `## 4. Entregar: o pacote e as perguntas em aberto`

**Impacto:** O leitor iniciante não sabe qual sequência seguir. É um sintoma de camadas acrescentadas em rodadas diferentes.

**Recomendação:** Ancorar tudo nos cinco movimentos e mostrar em cada página em qual movimento ela entra. Renumerar o checklist (três verificações mais uma entrega sem número).

### EDI-10 · Seletor e tabela da página de modelos descrevem os mesmos 10 modelos com frases diferentes

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** Encontrar um modelo mostra o TemplateFinder e, logo abaixo, uma tabela com as mesmas opções escritas de outro jeito. O grupo se chama Conhecimento do negócio no seletor e Documentos do negócio no menu.

**Evidências:**

- [src/components/TemplateFinder.astro:4](../src/components/TemplateFinder.astro#L4) `label: 'Descrever como um trabalho é executado'`
- [src/content/docs/templates/index.mdx:17](../src/content/docs/templates/index.mdx#L17) `| Descrever as etapas de um trabalho | [Processo](processo/)`
- [src/components/TemplateFinder.astro:6](../src/components/TemplateFinder.astro#L6) `label: 'Registrar uma política ou obrigação'`
- [src/content/docs/templates/index.mdx:19](../src/content/docs/templates/index.mdx#L19) `| Identificar qual política vale | [Política](politica/)`
- [src/components/TemplateFinder.astro:15](../src/components/TemplateFinder.astro#L15) `{ id: 'negocio', label: 'Conhecimento do negócio' },`
- [astro.config.mjs:48](../astro.config.mjs#L48) `{ label: 'Documentos do negócio', collapsed: true, items: [`

**Impacto:** A mesma lista, na mesma tela, com redação diferente sugere duas classificações e aumenta a carga de leitura.

**Recomendação:** Usar uma única fonte de dados para o seletor e a tabela, ou remover um dos dois. Alinhar o nome do grupo com o menu.

### EDI-21 · Jargão técnico sem explicação para leitor não técnico

**Severidade:** Média (rebaixada de alta na verificação)
**Confiança:** Alta

**O que acontece:** O contrato manda explicar todo termo técnico antes de usar. RAG aparece em 9 arquivos de página sem definição. DDL não tem a sigla expandida, schema só ganha uma glosa curta na descrição da visão de dados, e embeddings aparece sem explicação. O KPI expõe nomes de campos YAML na tabela de perguntas.

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:21](../docs/CONTRATO_EDITORIAL.md#L21) `Em todo termo técnico: explicar antes de utilizar, fornecer exemplo quando útil.`
- [src/content/docs/fundamentos/conhecimento-tacito.mdx:9](../src/content/docs/fundamentos/conhecimento-tacito.mdx#L9) `Não é uma técnica de RAG; é um problema anterior ao RAG.`
- [src/content/docs/templates/kpi.mdx:17](../src/content/docs/templates/kpi.mdx#L17) `O acervo tem dashboards, um schema SQL e a frase`
- [src/content/docs/dados/visao-geral.mdx:12](../src/content/docs/dados/visao-geral.mdx#L12) `Um DDL descreve tabelas e colunas.`
- [src/content/docs/dados/visao-geral.mdx:37](../src/content/docs/dados/visao-geral.mdx#L37) `Não escolhe banco, não gera embeddings`
- [src/content/docs/templates/kpi.mdx:27](../src/content/docs/templates/kpi.mdx#L27) `` | Evento que conta no numerador | `calculation` | ``

**Impacto:** O público primário declarado (não técnico) esbarra em termos que o próprio contrato manda explicar, justo nas páginas de dados que mais interessam ao caso de uso.

**Recomendação:** Criar um glossário curto (RAG, schema, DDL, granularidade, cardinalidade, junção, YAML, vigência, acervo), com explicação na primeira ocorrência de cada página ou um link para o glossário. Tirar os nomes de campos YAML da tabela do KPI.

### EDI-18 · README e ROADMAP violam vocabulário e aviso de ficção; o validador não os cobre

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O README usa as formas `elicitação`, `métricas` e o nome de gabarito que o vocabulário proíbe, além de `fictícia` (duas vezes). O ROADMAP usa `pendências`, `joins`, `painel` e `fictício`. O contrato limita a regra de vocabulário a páginas, componentes, modelos e YAML, e a lista de arquivos do validador (páginas em `src/content/docs`, componentes e downloads) não inclui o README nem `docs/`.

**Evidências:**

- [README.md:18](../README.md#L18) `Roteiro de elicitação e passagem do conhecimento;`
- [README.md:25](../README.md#L25) `**Dashboards**, filtros, métricas, vigência e limites;`
- [README.md:39](../README.md#L39) `` na amostra fictícia `aurora-fixture.sql` ``
- [docs/ROADMAP.md:16](../docs/ROADMAP.md#L16) `Passagem de conhecimento com pendências`
- [docs/ROADMAP.md:21](../docs/ROADMAP.md#L21) `Relacionamentos, cardinalidade e joins + exemplo 1:N`
- [docs/ROADMAP.md:43](../docs/ROADMAP.md#L43) `painel técnico único`
- [docs/CONTRATO_EDITORIAL.md:37](../docs/CONTRATO_EDITORIAL.md#L37) `Cada ideia tem um nome só, em páginas, componentes, modelos e textos dos YAML.`
- [scripts/validate_content.py:305](../scripts/validate_content.py#L305) `TERM_FILES = [`

**Impacto:** A primeira coisa que um visitante do GitHub lê contradiz o contrato, o que aumenta a sensação de colcha de retalhos e de pouco rigor.

**Recomendação:** Estender o escopo do contrato e do validador ao README e aos `docs/*.md` (com exceções explícitas para notas internas, se desejado).

### EDI-19 · Versões divergentes entre portal, README, ROADMAP e contrato

**Severidade:** Média
**Confiança:** Alta

**O que acontece:** O portal e o README dizem v0.4, mas o README lista como existentes na v0.4 as três verificações, que o ROADMAP coloca no Checkpoint D da v0.5 em construção. O contrato tem versão própria (0.3), e o ROADMAP fala em edição 1.0 como marco seguinte, sem explicar a relação entre esses esquemas.

**Evidências:**

- [src/content/docs/index.mdx:28](../src/content/docs/index.mdx#L28) `<small>Versão 0.4 · os exemplos usam a Aurora`
- [README.md:13](../README.md#L13) `## O que existe na v0.4`
- [README.md:16](../README.md#L16) `Revisão de documentos em **três verificações independentes**`
- [docs/ROADMAP.md:40](../docs/ROADMAP.md#L40) `## Consolidação da experiência (v0.5 em construção)`
- [docs/ROADMAP.md:45](../docs/ROADMAP.md#L45) `Checkpoint D: separar cobertura, consistência/evidências e confirmação pelo responsável`
- [docs/CONTRATO_EDITORIAL.md:3](../docs/CONTRATO_EDITORIAL.md#L3) `**Versão:** 0.3`
- [docs/ROADMAP.md:50](../docs/ROADMAP.md#L50) `## Antes de declarar a edição 1.0`

**Impacto:** Um projeto que ensina versionamento não mostra uma versão clara de si mesmo, e o leitor não sabe o que está publicado.

**Recomendação:** Adotar um único esquema (versão do produto com CHANGELOG), explicar que o contrato tem versão própria e atualizar o README a cada lançamento.

### EDI-07 · Contrato não descreve blocos que todas as páginas têm; botão de download duplicado

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** Toda página de tipo abre com uma frase de destaque e o bloco TemplateStart (Antes de preencher), com botão de download. A seção Baixe o modelo repete esse download no fim. A estrutura fixa do contrato não menciona nenhum dos dois blocos.

**Evidências:**

- [src/content/docs/templates/kpi.mdx:11](../src/content/docs/templates/kpi.mdx#L11) `<p class="editorial-lead">A fórmula pode estar certa e a pergunta de negócio, errada</p>`
- [src/components/TemplateStart.astro:66](../src/components/TemplateStart.astro#L66) `<p class="template-start__eyebrow">ANTES DE PREENCHER</p>`
- [src/components/TemplateStart.astro:87](../src/components/TemplateStart.astro#L87) `Baixar modelo em texto`
- [docs/CONTRATO_EDITORIAL.md:137](../docs/CONTRATO_EDITORIAL.md#L137) `1. **O problema**, com números:`

**Impacto:** O contrato deixa de ser a fonte da verdade da estrutura, e novas páginas podem divergir sem que ninguém perceba.

**Recomendação:** Registrar no contrato a frase de abertura e o TemplateStart como itens 0 da estrutura. Decidir se o download aparece uma ou duas vezes.

### EDI-09 · Identidade do projeto oscila entre framework, método, metodologia e guia

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** Título e README dizem framework; a descrição do site diz Método; a bibliografia diz metodologia autoral; a página inicial diz guia prático; o selo do topo diz documentação do conhecimento.

**Evidências:**

- [README.md:5](../README.md#L5) `O Contexto é um framework pedagógico`
- [astro.config.mjs:27](../astro.config.mjs#L27) `description: 'Método para documentar conhecimento organizacional`
- [src/content/docs/referencias/index.mdx:7](../src/content/docs/referencias/index.mdx#L7) `É uma **metodologia autoral**`
- [src/components/LandingHero.astro:15](../src/components/LandingHero.astro#L15) `Um guia prático, aberto e independente de plataformas.`
- [src/components/LandingHero.astro:7](../src/components/LandingHero.astro#L7) `CONTEXTO · DOCUMENTAÇÃO DO CONHECIMENTO`

**Impacto:** Isso enfraquece o posicionamento e a credibilidade, porque cada porta de entrada apresenta o projeto de um jeito.

**Recomendação:** Escolher uma categoria (ex.: guia ou método) e uma frase-definição única, usada no README, na descrição do site, na página inicial e na bibliografia.

### EDI-11 · Quatro camadas, quatro modelos lista cinco modelos

**Severidade:** Baixa (rebaixada de média na verificação)
**Confiança:** Alta

**O que acontece:** O título da seção promete quatro modelos, mas a tabela liga cinco: KPI, Dataset, Relacionamento, Dashboard e Perguntas de referência.

**Evidências:**

- [src/content/docs/dados/visao-geral.mdx:22](../src/content/docs/dados/visao-geral.mdx#L22) `## Quatro camadas, quatro modelos`
- [src/content/docs/dados/visao-geral.mdx:27](../src/content/docs/dados/visao-geral.mdx#L27) `[Dataset](../../templates/dataset/) e [Relacionamento entre tabelas](../../templates/relacionamento/)`

**Impacto:** É uma contradição numérica visível na porta de entrada da trilha de dados, fácil de corrigir.

**Recomendação:** Trocar para Quatro camadas, cinco modelos ou separar Semântica dos dados em duas linhas.

### EDI-12 · Definição de Exceções contraditória entre checklist e oito dimensões

**Severidade:** Baixa (rebaixada de média na verificação)
**Confiança:** Média

**O que acontece:** As oito dimensões definem exceções como desvios previstos da regra. O checklist interativo pergunta sobre casos não previstos. A própria página das oito dimensões também inclui o que fazer quando falta informação, o que deixa a fronteira ambígua.

**Evidências:**

- [src/components/ReadinessChecklist.astro:9](../src/components/ReadinessChecklist.astro#L9) `['Exceções', 'Casos não previstos e o que fazer com eles estão identificados?'],`
- [src/content/docs/metodo/oito-dimensoes.mdx:34](../src/content/docs/metodo/oito-dimensoes.mdx#L34) `**Exceções** são desvios previstos da regra, não casos em que ela não se aplica.`
- [src/content/docs/metodo/oito-dimensoes.mdx:29](../src/content/docs/metodo/oito-dimensoes.mdx#L29) `| Exceções | Exceções, casos-limite, o que fazer quando falta informação |`

**Impacto:** O mesmo critério de cobertura é descrito com sentidos diferentes, o que pode gerar marcações inconsistentes.

**Recomendação:** Alinhar o texto do checklist e a tabela da linha 29 à definição da linha 34 (ex.: Desvios previstos da regra e quem os autoriza estão descritos?).

### EDI-17 · Categorias de perguntas diferem entre modelo, laboratório, YAML e ROADMAP

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** O modelo define três categorias: Respondível, Ambígua e Fora da cobertura. O laboratório conta uma respondível, duas de explicação, uma ambígua e três sem número. O YAML completo fala em fora do escopo, e o ROADMAP, em não respondíveis.

**Evidências:**

- [src/content/docs/templates/casos-teste.mdx:24](../src/content/docs/templates/casos-teste.mdx#L24) `| Fora da cobertura | As fontes não cobrem a pergunta`
- [src/content/docs/exemplos/analytics-integrado.mdx:93](../src/content/docs/exemplos/analytics-integrado.mdx#L93) `uma respondível (25%), duas de explicação`
- [public/downloads/exemplo-casos-teste-completo.yaml:30](../public/downloads/exemplo-casos-teste-completo.yaml#L30) `purpose: "Distinguir perguntas respondíveis, ambíguas e fora do escopo"`
- [docs/ROADMAP.md:24](../docs/ROADMAP.md#L24) `Perguntas de referência respondíveis, ambíguas e não respondíveis`

**Impacto:** A taxonomia que deveria orientar a avaliação de agentes muda de nome conforme a página.

**Recomendação:** Usar as três categorias do modelo em todo lugar. Tratar responder explicando como subtipo de Respondível.

### EDI-20 · Rubrica fica em trilhas diferentes no README/ROADMAP e no portal

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** README e ROADMAP colocam a rubrica na trilha de Dados e Analytics, para entregáveis analíticos. O portal a coloca em Documentos do negócio, com um exemplo de e-mail de marketing.

**Evidências:**

- [README.md:26](../README.md#L26) `- **Rubricas** com critérios explícitos, evidências, níveis e revisão humana;`
- [docs/ROADMAP.md:23](../docs/ROADMAP.md#L23) `Rubricas para entregáveis analíticos`
- [astro.config.mjs:49](../astro.config.mjs#L49) `'templates/conceito', 'templates/processo', 'templates/decisao', 'templates/politica', 'templates/rubrica'`
- [src/content/docs/templates/rubrica.mdx:20](../src/content/docs/templates/rubrica.mdx#L20) `Em 15/09, a Revisão de Conteúdo recebeu o e-mail da campanha Semana do Refil:`

**Impacto:** A lista do que existe diverge entre o README e o portal.

**Recomendação:** Atualizar README e ROADMAP para refletir a organização atual do menu.

### EDI-22 · Ressalvas de limite repetidas em várias páginas

**Severidade:** Baixa (rebaixada de média na verificação)
**Confiança:** Média

**O que acontece:** O contrato tira o aviso de ficção das páginas porque repeti-lo trata o leitor como incapaz. Mesmo assim, a ressalva de que documentar não garante SQL, RAG ou agente aparece em pelo menos seis páginas (limites, perguntas de referência, versões, checklist, processo, visão de dados). O conselho de não escolher a fonte mais recente aparece em quatro.

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:70](../docs/CONTRATO_EDITORIAL.md#L70) `Repetir o aviso trata o leitor como incapaz de lembrar o que leu.`
- [src/content/docs/metodo/limites.mdx:47](../src/content/docs/metodo/limites.mdx#L47) `Preencher os modelos não garante acerto de SQL, RAG ou agentes.`
- [src/content/docs/templates/casos-teste.mdx:78](../src/content/docs/templates/casos-teste.mdx#L78) `O Contexto **não certifica** nenhuma arquitetura RAG ou agente.`
- [src/content/docs/metodo/identificacao-versoes.mdx:76](../src/content/docs/metodo/identificacao-versoes.mdx#L76) `não implementa nem garante a recuperação correta de um RAG ou agente.`
- [src/content/docs/validacao/checklist.mdx:111](../src/content/docs/validacao/checklist.mdx#L111) `## O que este roteiro não certifica`
- [src/content/docs/governanca/papeis.mdx:49](../src/content/docs/governanca/papeis.mdx#L49) `Não escolha a fonte mais recente automaticamente`
- [src/content/docs/metodo/limites.mdx:28](../src/content/docs/metodo/limites.mdx#L28) `não escolha a mais recente nem a mais repetida`

**Impacto:** O tom fica defensivo e o texto, repetitivo, o que contribui para a sensação de remendo.

**Recomendação:** Concentrar as ressalvas em Quando o método não basta e deixar só um link curto nas outras páginas, com a mesma lógica do aviso de ficção.

### EDI-23 · A conta 25% x 50% é repetida em muitas páginas

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** O fio condutor é bom, mas o par 25% e 50% aparece em 10 arquivos de página, com explicação na página inicial, na visão de dados, no KPI, em versões e na bibliografia, entre outros.

**Evidências:**

- [src/content/docs/index.mdx:22](../src/content/docs/index.mdx#L22) `uma taxa de **25% de sessões convertidas** não significa o mesmo que **50% de pedidos por sessão elegível**`
- [src/content/docs/dados/visao-geral.mdx:8](../src/content/docs/dados/visao-geral.mdx#L8) `a mesma pergunta sobre conversão dá 25% ou 50% nas mesmas seis sessões`
- [src/content/docs/metodo/identificacao-versoes.mdx:40](../src/content/docs/metodo/identificacao-versoes.mdx#L40) `**A fórmula antiga produziria 50%; a nova produz 25%.**`
- [src/content/docs/referencias/index.mdx:67](../src/content/docs/referencias/index.mdx#L67) `retorna **50%** para uma medida diferente`

**Impacto:** A redundância é moderada e deixa as páginas de dados parecidas entre si.

**Recomendação:** Explicar a conta só no laboratório e, nas outras páginas, citar o resultado com link.

### EDI-24 · O exemplo de metadados do contrato não segue as regras do próprio contrato

**Severidade:** Baixa (rebaixada de média na verificação)
**Confiança:** Alta

**O que acontece:** O contrato declara `version`, `version_date`, `valid_from` e `version_history` obrigatórios em todo modelo e exemplo, mas o próprio exemplo de metadados não traz os campos de versão e usa `owner`. O contrato também não documenta `approver`, `revision_id`, `valid_to` e `supersedes_revision`, que o portal usa em toda parte (busca sem resultados no contrato).

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:100](../docs/CONTRATO_EDITORIAL.md#L100) `Campos obrigatórios em todo modelo e exemplo:`
- [docs/CONTRATO_EDITORIAL.md:162](../docs/CONTRATO_EDITORIAL.md#L162) `id: METRIC-001`
- [docs/CONTRATO_EDITORIAL.md:165](../docs/CONTRATO_EDITORIAL.md#L165) `owner: null`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:33](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L33) `` | Quem aprova | `approver` | ``

**Impacto:** O documento normativo perde autoridade quando contradiz a si mesmo, e quem contribui não encontra no contrato a lista real de campos.

**Recomendação:** Trocar o exemplo por um trecho real (KPI-AURORA-001) e acrescentar a tabela completa de campos de identificação.

### EDI-25 · Explicações duplicadas e divergentes sobre Obsoleto e vigência

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** O contrato diz que Obsoleto não vale mais; Como ler os campos diz que não é mais recomendado como referência atual. A convenção de `valid_to` exclusivo é explicada duas vezes, em Como ler os campos e em Versões e vigência.

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:182](../docs/CONTRATO_EDITORIAL.md#L182) `` | `deprecated` | Obsoleto | Não vale mais; aponta para o substituto quando houver | ``
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:59](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L59) `Não é mais recomendado como referência atual; isso não apaga sua utilidade para análise histórica`
- [src/content/docs/fundamentos/como-ler-os-campos.mdx:37](../src/content/docs/fundamentos/como-ler-os-campos.mdx#L37) `` No YAML, `valid_to` guarda **o dia seguinte**, o primeiro em que ela já não vale ``
- [src/content/docs/metodo/identificacao-versoes.mdx:50](../src/content/docs/metodo/identificacao-versoes.mdx#L50) `` Neste framework, `valid_from` inclui o dia inicial e `valid_to` **exclui** o dia informado ``

**Impacto:** Duas fontes para a mesma regra tendem a divergir com o tempo, e isso já começou no caso de Obsoleto.

**Recomendação:** Definir uma página dona de cada regra (estados em Como ler os campos, vigência em Versões e vigência) e usar links nas outras.

### EDI-27 · Palavras com dois sentidos: pedido e cartão

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** Pedido nomeia a ordem de e-commerce e também o pedido de campanha, que o contrato manda chamar de brief e as páginas também chamam de solicitação. Cartão nomeia o cartão de exemplo e o cartão de dashboard.

**Evidências:**

- [docs/CONTRATO_EDITORIAL.md:51](../docs/CONTRATO_EDITORIAL.md#L51) `| Pedido de campanha | brief | briefing |`
- [src/content/docs/templates/processo.mdx:80](../src/content/docs/templates/processo.mdx#L80) `O pedido CAMP-0914, o e-mail da campanha Semana do Refil`
- [src/content/docs/templates/decisao.mdx:16](../src/content/docs/templates/decisao.mdx#L16) `Ao completar a [solicitação de campanha](../processo/)`
- [src/content/docs/templates/dashboard.mdx:3](../src/content/docs/templates/dashboard.mdx#L3) `Documente qual definição cada cartão segue`

**Impacto:** Os dois sentidos convivem no mesmo portal e confundem quem cruza as trilhas de negócio e de dados.

**Recomendação:** Registrar no vocabulário: solicitação de campanha (com brief como conteúdo), pedido só para e-commerce, e um termo distinto para o cartão de exemplo (ex.: ficha de exemplo).

### EDI-28 · Bibliografia cita diagramas ASCII que não existem nas páginas

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** A bibliografia diz que os diagramas ASCII do Contexto não são BPMN formal, mas as páginas não têm diagramas ASCII. Os únicos blocos de código nas páginas são `sql` e `yaml`.

**Evidências:**

- [src/content/docs/referencias/index.mdx:27](../src/content/docs/referencias/index.mdx#L27) `Diagramas ASCII e YAML do Contexto não são BPMN formal`

**Impacto:** Restos de versões anteriores minam a confiança na bibliografia.

**Recomendação:** Revisar a bibliografia contra o conteúdo atual.

### EDI-29 · Modelo KPI em Markdown com seção de perguntas em aberto duplicada e numeração própria

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** `template-kpi.md` é o único modelo com seções numeradas (os outros nove não têm nenhuma) e tem duas seções seguidas para perguntas em aberto.

**Evidências:**

- [public/downloads/template-kpi.md:63](../public/downloads/template-kpi.md#L63) `## 8. Perguntas ainda em aberto`
- [public/downloads/template-kpi.md:66](../public/downloads/template-kpi.md#L66) `## Perguntas em aberto`
- [public/downloads/template-conceito.md:26](../public/downloads/template-conceito.md#L26) `## Para que serve este conceito?`

**Impacto:** O usuário preenche a mesma informação em dois lugares, e o modelo mais usado (KPI) destoa dos outros.

**Recomendação:** Remover a seção 8 e retirar a numeração, ou numerar todos os modelos.

### EDI-30 · Exemplo da página inicial desconectado dos exemplos da Aurora

**Severidade:** Baixa
**Confiança:** Média

**O que acontece:** O hero e a visão geral usam cliente ativo e conversão. Os exemplos trabalhados usam participante ativo e taxa de sessões convertidas.

**Evidências:**

- [src/components/LandingHero.astro:21](../src/components/LandingHero.astro#L21) `Considere clientes ativos e calcule a conversão.`
- [src/content/docs/metodo/visao-geral.mdx:10](../src/content/docs/metodo/visao-geral.mdx#L10) `pode significar uma coisa no e-commerce, outra no CRM e outra no Financeiro`
- [src/content/docs/templates/conceito.mdx:16](../src/content/docs/templates/conceito.mdx#L16) `` Um relatório traz a coluna `participante_ativo` ``

**Impacto:** É uma oportunidade perdida de ligar a primeira impressão ao fio condutor do portal.

**Recomendação:** Usar no hero um caso que exista nos exemplos (participante ativo ou conversão web de 01/10).

### EDI-32 · Termos em inglês em textos de governança e componentes

**Severidade:** Baixa
**Confiança:** Alta

**O que acontece:** O ROADMAP usa baseline, Checkpoint e disclosure. O rótulo acessível dos downloads usa template, enquanto as páginas dizem modelo.

**Evidências:**

- [docs/ROADMAP.md:3](../docs/ROADMAP.md#L3) `## v0.1: baseline técnica e editorial`
- [docs/ROADMAP.md:44](../docs/ROADMAP.md#L44) `Checkpoint visual: aumentar destaque e contraste do disclosure técnico`
- [src/components/TemplateDownloads.astro:71](../src/components/TemplateDownloads.astro#L71) `aria-label="Arquivos de exemplo e template para reutilizar"`

**Impacto:** Leitores de tela ouvem template onde a página diz modelo, e o ROADMAP fica menos legível para colaboradores não técnicos.

**Recomendação:** Trocar template por modelo nos rótulos visíveis e acessíveis. Traduzir os termos do ROADMAP ou explicá-los.

## Descartados na verificação

- **EDI-X1:** Suspeita de que o cartão completo aparecesse duas vezes por causa do RevisionComparison em Versões e vigência. O componente mostra só um resumo (fórmula ou definição e datas), não o cartão inteiro.
- **EDI-X2:** Suspeita de datas incoerentes na política. O YAML e a página são coerentes: resolução em 14/08, registro aprovado em 18/08, gatilho de revisão em 01/10.
- **EDI-X3:** A contagem de 11 exemplos completos do ROADMAP está certa: 10 tipos mais o dataset de pedidos.
- **EDI-19 (Princípios):** A afirmação de que o README cita Princípios, cuja página teria sido redirecionada, não se sustenta. `astro.config.mjs` não tem redirecionamento de nenhuma página Princípios, e não existe página com esse nome em `src/content/docs`. O README cita algo que não existe como página, mas não há prova de redirecionamento.
- **EDI-19 (checkpoint E):** Não há contradição no checkpoint E. A linha 46 do ROADMAP marca os ajustes como implementados e aguardando conferência visual, e a linha 47 é a conferência ainda por fazer. São itens distintos e coerentes.
- **EDI-24 (METRIC-001):** `METRIC-001` é um identificador em inglês, e o contrato libera identificadores e nomes de campo (linha 37: nomes de campos YAML e código SQL não mudam). Isso não viola o vocabulário.
- **EDI-28 (precedência):** Não há contradição entre o seletor (prioridade entre regras) e a página de decisões. A página explica que a precedência é dispensável quando a política de acerto é única e apresenta a alternativa primeira, em que a ordem conta. O modelo Markdown tem o campo Precedência se duas condições forem verdadeiras (`public/downloads/template-decisao.md`, linha 47).
- **EDI-06 (notas de limite):** A afirmação de que as notas finais sobre limites existem em 6 páginas e faltam em 4 não trazia evidência e não foi confirmada. Foi retirada do achado.
- **EDI-21 (cardinalidade):** A notação 1:1, 1:N e N:N em `relacionamento.mdx`, linha 29, é explicada pelo exemplo da coluna ao lado (uma sessão, zero ou mais pedidos). Não cabe como jargão sem explicação.

## Não coberto nesta rodada

- Renderização visual do portal publicado (tema claro e escuro, celular): só a fonte foi lida.
- Conteúdo integral dos YAML de exemplo, exceto os metadados do exemplo completo de Perguntas de referência.
- Modelos Markdown: além do KPI, só a ausência de numeração nos outros nove foi conferida.
- `docs/PLANO_VALIDACAO.md` não foi lido.
- Textos visíveis dos componentes ExampleDoc, ExampleMeaning, JoinDiagram, AnalyticsLabDownloads e SiteFooter.
- Validade dos links externos e aderência da bibliografia à literatura atual (sem pesquisa web nesta dimensão).
- Se o validador checa a estrutura de seções das páginas de tipo.
- A contagem exata de páginas com a explicação completa da conta 25% x 50% (EDI-23): só os 10 arquivos que citam 25% foram conferidos.
