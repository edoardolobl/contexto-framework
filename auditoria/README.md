# Auditoria do Contexto (pente fino)

Data: 2026-11-17 · Commit: d08c810 · Escopo: repositório inteiro (portal Starlight em `src/`, modelos e exemplos em `public/downloads/`, contrato e planos em `docs/`, validadores em `scripts/`, workflows em `.github/workflows/`) e portal publicado em https://edoardolobl.github.io/contexto-framework/, mais seis frentes de pesquisa externa.

> **Operação só de leitura.** Nenhum arquivo do repositório foi alterado. A única escrita foi esta pasta `auditoria/`.

## Propósito

O Contexto nasceu para ajudar times a criar uma camada semântica entre modelos de IA e bases de dados ou operação (GTM, GA4, dashboards, plataformas de mídia, BigQuery, Databricks), com um guia simples para público misto, documentação versionada produzida a partir de perguntas de negócio e modelos com exemplos concretos.
O pedido do responsável: um pente fino de tudo (texto, literatura, modelos, experiência, navegação e visual) para trocar a sensação de colcha de retalhos por consistência e credibilidade, antes de evoluir para agentes, skills, WebMCP, Poppy e UCP.

## Resumo

- A auditoria registra **159 achados** em oito dimensões: 9 de severidade alta, 72 média, 77 baixa e 1 informativo. Outros 35 foram descartados pelo verificador.
- O maior problema é de produto, não de código: o percurso não começa pela pergunta de negócio e não cobre o caso de mensuração (evento raro tratado como quebrado).
- A base de governança é boa e deve ser mantida (id estável, versão, vigência, responsável e quem aprova por cargo, `synonyms` separado de `not_synonyms`, `answer | clarify | abstain`).
- A direção recomendada é "Da pergunta ao documento aprovado": esqueleto pedagógico com trilhos de governança e saídas para IA, sem acoplar o núcleo a protocolos imaturos.
- A tese central do projeto tem apoio forte na literatura, mas ainda não foi testada com agentes nem com pessoas do público-alvo dentro do próprio projeto.

## Resumo executivo

1. **O percurso não parte da pergunta de negócio.** O menu abre com tarefas e modelos, e o grupo que explica o método fica recolhido. Perguntas de negócio aparecem no fim desse grupo, com três nomes diferentes (NAV-03, NAV-04, MET-01, MET-02).
   - [astro.config.mjs:46](../astro.config.mjs#L46) `{ label: 'Comece por uma tarefa', items: ['fundamentos/comece-em-5-minutos', 'validacao/checklist', 'templates'] },`
   - [astro.config.mjs:55](../astro.config.mjs#L55) `{ label: 'Entenda o método', collapsed: true, items: [`
2. **O caso real de mensuração não tem lugar no projeto.** Uma busca textual por `GA4|GTM|tag plan` em `src/` e `public/downloads/` não retorna nada. Não existe tipo de documento para evento de coleta, nem campos de comportamento esperado (frequência, granularidade por operação, histórico). É exatamente o que faltou ao agente que marcou um evento raro como quebrado (MOD-01, MOD-02, NAV-01, AUR-01, MET-07, EDI-31).
3. **A promessa fala com um intermediário, e a jornada termina antes da IA.** O contrato escreve para "engenheiros de IA", mas o público que usa Claude Code, Codex ou Antigravity direto não encontra o passo de levar a documentação à ferramenta (EDI-01, NAV-02).
   - [docs/CONTRATO_EDITORIAL.md:13](../docs/CONTRATO_EDITORIAL.md#L13) `para que engenheiros de IA não precisem inventar regras ausentes ou inferir significados a partir de documentos ambíguos.`
   - [src/content/docs/metodo/visao-geral.mdx:10](../src/content/docs/metodo/visao-geral.mdx#L10) `O engenheiro de IA não deveria inventar essa definição.`
4. **Os modelos não têm esquema declarado e o cabeçalho comum varia.** O validador deduz os campos válidos a partir do próprio modelo, e campos de revisão aparecem em só 3 dos 10 modelos YAML (TEC-12, TEC-18, MOD-04, MOD-05).
   - [scripts/validate_content.py:147](../scripts/validate_content.py#L147) `template_keys[data.get("type")] = set(data)`
   - [public/downloads/template-kpi.yaml:19](../public/downloads/template-kpi.yaml#L19) `last_reviewed: null` (o mesmo campo só existe também em `template-conceito.yaml:15` e `template-politica.yaml:15`)
5. **O deploy publica sem passar pelos validadores.** O workflow de publicação só instala e gera o site; os validadores rodam em outro workflow, sem bloquear o deploy (TEC-10).
   - [.github/workflows/deploy.yml:26](../.github/workflows/deploy.yml#L26) `- run: npm run build`
   - [.github/workflows/content-check.yml:20](../.github/workflows/content-check.yml#L20) `run: python scripts/validate_content.py`
6. **A credibilidade depende de um teste que ainda não aconteceu.** O plano de validação com leitores continua como proposta para uma versão já ultrapassada pelo pacote (MET-16). Algumas citações precisam de correção e de uma tabela de evidências por tipo de fonte (MET-05, MET-06, MET-12, MET-14, MET-15).
   - [docs/PLANO_VALIDACAO.md:1](../docs/PLANO_VALIDACAO.md#L1) `# Plano de validação com leitores: proposta para após v0.3`
   - [package.json:4](../package.json#L4) `"version": "0.4.0",`
7. **As plataformas de camada semântica convergem em pontos que o Contexto ainda não tem.** Snowflake, Databricks Genie, Looker e BigQuery aceitam pares de pergunta e consulta verificada; quase todas pedem expressão de cálculo estruturada; Snowflake e Looker separam regras de geração de SQL das regras de tratar a pergunta. Faltam no Contexto: formato único de consulta verificada, expressão de indicador estruturada, filtros nomeados e um bloco de instruções para IA. Detalhes e fontes em [08-pesquisa-boas-praticas.md](./08-pesquisa-boas-praticas.md).
8. **Nada legível por máquina além do sitemap.** No portal publicado, `llms.txt`, `robots.txt` e `AGENTS.md` respondem 404, e `public/` só tem ícones e `downloads/`. Dá para resolver sem esperar protocolo nenhum: `llms.txt` via plugin [starlight-llms-txt](https://github.com/delucis/starlight-llms-txt), um JSON Schema por tipo, URI por id e versão, licença em formato de máquina e um mapeamento para o [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/).

## Arquivos desta pasta

| Arquivo | Assunto | Alta | Média | Baixa | Info | Total | Descartados |
|---|---|---|---|---|---|---|---|
| [01-tecnico-validadores-e-ci.md](./01-tecnico-validadores-e-ci.md) | Validadores em Python, build, CI e componentes que leem arquivos (TEC) | 0 | 6 | 12 | 0 | 18 | 5 |
| [02-acessibilidade.md](./02-acessibilidade.md) | WCAG 2.2 AA pela leitura do código: contraste, anúncios, foco (A11Y) | 0 | 5 | 10 | 0 | 15 | 1 |
| [03-consistencia-editorial.md](./03-consistencia-editorial.md) | Promessa, vocabulário, tom e aderência ao contrato editorial (EDI) | 0 | 17 | 15 | 0 | 32 | 9 |
| [04-modelos-e-exemplos.md](./04-modelos-e-exemplos.md) | Modelos YAML e Markdown, exemplos com lacunas e completos (MOD) e coerência do universo Aurora (AUR) | 3 | 17 | 21 | 1 | 42 | 13 |
| [05-navegacao-e-ux.md](./05-navegacao-e-ux.md) | Menu, página inicial, paginação, seletor de modelos e percurso (NAV) | 3 | 8 | 5 | 0 | 16 | 0 |
| [06-identidade-visual.md](./06-identidade-visual.md) | Tokens, CSS próprio, componentes e temas claro e escuro (VIS) | 2 | 11 | 7 | 0 | 20 | 3 |
| [07-metodo-e-credibilidade.md](./07-metodo-e-credibilidade.md) | Fundamentação, citações, método e validação com leitores (MET) | 1 | 8 | 7 | 0 | 16 | 4 |
| [08-pesquisa-boas-praticas.md](./08-pesquisa-boas-praticas.md) | Seis frentes de pesquisa externa, com fontes conferidas | n/a | n/a | n/a | n/a | n/a | n/a |
| [09-casos-de-uso.md](./09-casos-de-uso.md) | Os dois casos reais do responsável e um caso de cruzamento entre fontes, testados contra os modelos atuais | n/a | n/a | n/a | n/a | n/a | n/a |
| [10-direcao-proposta.md](./10-direcao-proposta.md) | Julgamento das três direções, direção recomendada, roteiro e decisões | n/a | n/a | n/a | n/a | n/a | n/a |
| [11-decisoes.md](./11-decisoes.md) | Respostas do mantenedor às 14 decisões e ajustes no roteiro | n/a | n/a | n/a | n/a | n/a | n/a |
| [12-incorporacoes.md](./12-incorporacoes.md) | O que três pesquisas externas acrescentam a cada fase do roteiro | n/a | n/a | n/a | n/a | n/a | n/a |
| [13-ui-ux-tasteskill.md](./13-ui-ux-tasteskill.md) | UI e UX medidos no navegador com a tasteskill 2.5.1, com capturas em `evidencias-ui/` (UX) | 2 | 6 | 2 | 0 | 10 | n/a |
| **Total** | | **9** | **72** | **77** | **1** | **159** | **35** |

Ordem de leitura sugerida: este índice, depois [10-direcao-proposta.md](./10-direcao-proposta.md), depois [05-navegacao-e-ux.md](./05-navegacao-e-ux.md) e [04-modelos-e-exemplos.md](./04-modelos-e-exemplos.md), e por fim as demais dimensões conforme a decisão a tomar.

## Como foi feito

1. **Oito dimensões auditadas** (técnico, acessibilidade, editorial, modelos, navegação, visual, método e laboratório Aurora), cada uma por um agente ECC ou de uso geral. Cada achado de cada dimensão passou por um **verificador cético** que tentou refutá-lo; 35 caíram e estão listados em "Descartados na verificação" de cada arquivo.
2. **Seis frentes de pesquisa** com Exa e busca na web: camada semântica nas plataformas; evidência empírica e martech; agentes e protocolos; perguntas de negócio e versionamento; experiência para público misto; governança e catálogos. Cada frente teve uma **checagem de fontes** que abriu os links, corrigiu atribuições e rebaixou afirmações sem suporte.
3. **Síntese**: os achados foram confrontados com os dois casos reais do responsável (evento raro tratado como quebrado; indicador calculado com a definição genérica). Três propostas de direção (Pedagogia, Consumo por IA, Governança) foram escritas e avaliadas por um **juiz** com cinco critérios de 1 a 5. Resultado: Pedagogia 21, Consumo por IA 19, Governança 19.
4. **Conferência final das âncoras**: cada citação `arquivo:linha` foi conferida linha a linha contra o commit d08c810.

## Convenção de evidência e severidade

**Evidência.** Toda afirmação sobre o repositório traz caminho relativo à raiz, linha (contada a partir de 1) e citação exata, uma substring literal daquela linha com até 200 caracteres, no formato [caminho:linha](../caminho#Llinha) seguido do trecho em código. Ausências (por exemplo, nenhum resultado para `GA4`) são registradas com o comando de busca usado. Sem evidência, não é achado. Fontes web aparecem sempre com link completo.

**Severidade.**

| Nível | Significado |
|---|---|
| Alta | Impede o objetivo central do projeto (público misto chegar a um documento que a IA usa sem inventar definições) ou contradiz um dos casos reais. |
| Média | Gera erro, confusão ou perda de credibilidade em um percurso comum, com solução conhecida. |
| Baixa | Inconsistência pontual, manutenção ou polimento. |
| Info | Observação sem defeito, útil para decisão. |

**Confiança** (em cada achado): Alta quando a evidência basta sozinha; Média quando depende de interpretação ou de comportamento não executado; Baixa quando é inferência que precisa de teste.

Cada dimensão calibrou a severidade por conta própria. Há achados repetidos entre dimensões, por exemplo a falta de tag plan (MOD-01, MOD-02, NAV-01, AUR-01, MET-07, EDI-31), a definição de Exceções (EDI-12, MET-03), a matriz RACI (EDI-13, MET-10), o dourado de baixo contraste (A11Y-08, VIS-12) e a seção duplicada do modelo de KPI em Markdown (EDI-29, MOD-21, MET-11). Por isso o total soma ocorrências, não problemas distintos.

## Limitações

- **Validadores e build não foram executados**, porque a execução de scripts foi bloqueada nesta sessão. As falhas por traceback e erros de validador (TEC-03, TEC-04, TEC-07 com KeyError, TEC-08, TEC-12 com ValueError) foram deduzidas da leitura, e a severidade pode mudar ao rodar os cinco scripts de `scripts/`, o `astro build` e o `check_built_links` sobre o resultado.
- **O estado real do CI não foi consultado.** Que os pull requests rodam os validadores vem só da leitura do YAML, não do histórico de execuções do GitHub Actions.
- **Contraste e tamanho de fonte** (A11Y-04, A11Y-05, A11Y-08, A11Y-13, VIS-12) foram calculados a partir do CSS, sem renderizar. As sobrescritas do Starlight podem mudar o resultado.
- **Leitor de tela** (A11Y-01, A11Y-07, A11Y-10) é inferência, sem teste com VoiceOver ou NVDA.
- **Visual** (VIS-02 no tema escuro, VIS-06 sobre a fonte Inter, VIS-18 sobre espaçamento) pede confirmação na aba de rede e em capturas.
- **Paginação e becos sem saída** (NAV-05, NAV-06) foram deduzidos da ordem do menu e de buscas, sem percorrer o HTML gerado.
- **Paridade entre o portal no ar e o commit d08c810** não foi confirmada.
- **A tese do projeto não foi testada na prática.** Ninguém colocou um agente diante do laboratório Aurora, sem e com os documentos, nem reproduziu os dois casos do responsável.
- **Viés de mesma família de modelo.** Quem audita e quem verifica são da mesma família, e o `git log` mostra 22 commits com "Co-Authored-By: Claude", 12 deles do mesmo modelo desta auditoria. Os pontos cegos tendem a coincidir.
- **A verificação conferiu a existência das citações, não a interpretação.** Uma citação correta não garante que a conclusão esteja certa.
- **Ancoragem no enquadramento.** Todos os auditores receberam os dois casos do responsável, o que puxa os achados para tag plan e indicador.
- **Fontes de fornecedor.** Boa parte da pesquisa vem de documentação de Snowflake, Databricks, dbt e Cube, o que puxa as recomendações para esquemas técnicos.
- **Fontes ainda em aberto.** O status de incubação do Apache Ossie diverge entre frentes; Poppy e UCP foram marcados como verificados por uma frente e não verificados por outra; renomeações (Gemini Notebook, Knowledge Catalog, revisão 2026-07-28 do MCP, Keep a Changelog 2.0.0, llms.txt v2) e as datas de 13/11/2026 pedem segunda fonte primária antes de ir para o portal. Obras como DMBOK, Klein 1989, ISO 22400-2, ISO 24495-1 e os artigos da Lei 15.263 foram citadas provavelmente por fonte secundária.

## Próximos passos sugeridos

1. **Decisões de rumo do responsável**, antes de qualquer mudança: núcleo de campos obrigatórios por modelo; foco do produto (só dados ou dois trilhos, como no MOD-22); domínio próprio; esquema de versões. Ver a seção de decisões em [10-direcao-proposta.md](./10-direcao-proposta.md).
2. **Registro único de achados**: deduplicar os 159 achados com uma rubrica de severidade comum e montar uma matriz de decisões para recomendações que se contradizem (por exemplo `replaced_by` e `superseded_by_revision`; `phrasings` e `paraphrases`; SemVer de três ou dois níveis), registrando cada escolha como ADR.
3. **Orçamento de complexidade**: separar os campos propostos em núcleo obrigatório, opcional e só para exportação, com teto por modelo e uma razão escrita para cada campo.
4. **Rodar o que não rodou**: os validadores com fixtures boas e ruins numa cópia isolada, o build, `gh run list` no CI e axe ou Lighthouse no portal publicado (tema claro, tema escuro e 390 px).
5. **Teste pareado com agente**: as perguntas do gabarito mais uma pergunta de evento zerado, sem e com os documentos, com dois modelos de famílias diferentes, registrando data e versão dos documentos.
6. **Piloto com 2 ou 3 pessoas não técnicas**, seguindo o próprio plano de validação, e uma revisão independente por outra família de modelo e por alguém que nunca viu o projeto.
7. **Correções baratas primeiro** (fase F1 da direção proposta): correções de citação, contraste AA, deploy condicionado aos validadores e linha do tempo Aurora coerente.
8. **Segunda fonte** para cada produto renomeado e para cada protocolo novo antes de citá-los no portal.

## Não coberto nesta rodada

- **Contribuição e adoção por outros times.** Não há CONTRIBUTING nem modelos de issue; `.github/` só tem `workflows/`. Ninguém examinou como um time externo propõe um modelo ou relata um erro.
- **Medição do portal.** O `head` só carrega ícones, sem ferramenta de medição; toda a análise de navegação é inferida, não observada.
  - [astro.config.mjs:31](../astro.config.mjs#L31) `head: [`
- **Busca interna, SEO e cartão de compartilhamento.** A busca nativa do Starlight não foi testada com termos do público ("evento zerado", "KPI", "tag plan"), e os metadados de compartilhamento não foram auditados no HTML gerado.
- **Formato de entrega para quem não é técnico.** Tag plans vivem em Google Sheets, e ninguém testou abrir os `.md` e `.yaml` no Google Docs, no Word ou no Sheets, nem avaliou um modelo de plano de mensuração em planilha.
- **Idioma e público multinacional.** O portal só tem pt-BR, e não foi avaliado se isso é decisão ou limitação.
  - [astro.config.mjs:36](../astro.config.mjs#L36) `locales: { root: { label: 'Português', lang: 'pt-BR' } },`
- **Licença de conteúdo de terceiros.** Não foi conferida a compatibilidade entre a CC BY 4.0 do conteúdo e trechos ou adaptações de fontes CC BY-NC (KCS) ou pagas (ISO, DMBOK).
- **Histórico do repositório.** O `git log` tem 66 commits entre 2026-11-16 e 2026-11-17, em rodadas "fix/r3-*"; não foi usado para explicar a origem das inconsistências.
- **Frentes de pesquisa que faltaram:** como Antigravity, Codex e Claude Code carregam contexto (regras, AGENTS.md, CLAUDE.md, skills, MCP); projetos parecidos de "dados prontos para IA" para público não técnico; ensino para adultos não técnicos e gestão da mudança; tag plans em planilha usados por profissionais de GTM e GA4; vieses de LLM como juiz; segurança de ligar agentes direto a bases de produção.
