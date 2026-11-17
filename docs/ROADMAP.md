# Roadmap do Contexto

## v0.1: baseline técnica e editorial
- [x] Propósito, promessa e limites
- [x] Método das oito dimensões, elicitação e revisão
- [x] Template de KPI e exemplo
- [x] Checklist interativo e bibliografia
- [x] Publicação automatizada e validação em PR

## v0.2: documentação transversal
- [x] Seletor pedagógico de modelos
- [x] Conceitos/glossário + exemplo RH
- [x] Processos + exemplo Marketing
- [x] Regras e decisões + tabela de precedência
- [x] Políticas e referências + conflito de fontes
- [x] Passagem de conhecimento com pendências
- [x] Modelos Markdown/YAML e testes de qualidade estrutural

## v0.3: Dados e Analytics
- [x] Dataset e dicionário semântico + exemplo SQLite
- [x] Relacionamentos, cardinalidade e joins + exemplo 1:N
- [x] Dashboard e interpretação com filtros e escopo
- [x] Rubricas para entregáveis analíticos, com âncoras e revisão humana
- [x] Perguntas de referência respondíveis, ambíguas e não respondíveis
- [x] Estudo de caso integrado de KPI, dataset, dashboard e rubrica
- [x] SQL sintético reproduzível + teste automatizado independente de LLM
- [x] Validação de todas as famílias de templates e arquivos
- [x] Fundamentação bibliográfica e ressalvas ampliadas
- [ ] Revisão visual manual e testes de acessibilidade com pessoas

## v0.4: correções da auditoria independente (16/11/2026)
- [x] Links da biblioteca, título único por página, estados alinhados
- [x] Licenças MIT (código) e CC BY 4.0 (conteúdo), autoria e página de créditos
- [x] Versão, data da versão e histórico de versões em todos os modelos e exemplos
- [x] Par de exemplos por tipo: com lacunas e completo com aprovação fictícia
- [x] Modelos Markdown sem bloco YAML; páginas leem os exemplos dos arquivos de download
- [x] Páginas "Comece em 5 minutos", "Como ler os campos" e "Quando o método não basta"
- [x] Ressalvas do preprint e das fontes; lockfile; validação de links no HTML gerado

## Consolidação da experiência (v0.5 em construção)
- [x] Checkpoint A: entradas por tarefa, seleção de modelos e primeira documentação sem YAML
- [x] Checkpoint B: identificação, intervalos de vigência e versões históricas
- [x] Checkpoint C: exemplos de negócio visíveis, comparação alinhada e painel técnico único
- [x] Checkpoint visual: aumentar destaque e contraste do disclosure técnico
- [x] Checkpoint D: separar cobertura, consistência/evidências e confirmação pelo responsável; ficha prática para download
- [x] Checkpoint E: ajustes pontuais de tipografia, respiração e leitura mobile implementados; aguardando conferência visual do mantenedor
- [ ] Conferir visualmente o checkpoint E (tema claro/escuro, leitura mobile e seta única)
- [ ] Teste de compreensão com participantes externos (issue #4; após estabilizar os materiais)

## Antes de declarar a edição 1.0
- [ ] Pesquisar a aplicabilidade do método com leitores técnicos e não técnicos (issue #4)
- [ ] Teste com leitor de tela e em celular físico
- [ ] Revisão humana dos 11 exemplos completos, cujo conteúdo fictício foi escrito na v0.4
- [x] Nome mantido: Contexto. Sem domínio próprio por enquanto; o portal segue no GitHub Pages
- [ ] Planejar contribuições e governança de versões
- [ ] Verificação periódica de links externos

## Plano da auditoria de 17/11/2026

O plano completo está em [auditoria/10-direcao-proposta.md](../auditoria/10-direcao-proposta.md), seção 2, com as fases F0 a F7 e o critério de saída de cada uma. As decisões do mantenedor estão em [auditoria/11-decisoes.md](../auditoria/11-decisoes.md) e viram registros em [docs/adr/](adr/).

- [ ] **F0. Decisões e trilhos: concluída no branch, aguardando merge.** Entregue no branch `f0-decisoes-e-trilhos`: ADRs 0001 a 0017 aceitos pelo mantenedor em 17/11/2026 (0016: família IBM Plex; 0017: até 4 telas no desktop, passos recolhíveis e referência de campos à parte); `src/data/vocabulario.yaml` e `src/data/modelos.yaml`; CHANGELOG; versão do produto igual em package.json, README, página inicial e CHANGELOG; `npm run check` como comando único; deploy que só começa depois dos validadores; ações fixadas por SHA e Dependabot. Pelo ADR 0009, o contrato editorial tem versão própria de documento e fica fora da versão única do produto.
- [ ] **F1. Correções baratas e credibilidade.** Remoções, correções de citação, contraste e linha do tempo da Aurora.
- [ ] **F2. Porta de entrada.** Tipo Perguntas de negócio, menu em percurso, núcleo de entrada (ADR 0013) e checklist das oito dimensões (ADR 0014).
- [ ] **F3. Schema 1.0.** Migração para Markdown com frontmatter (ADR 0006), versão de schema (ADR 0009) e marcação Breaking.
- [ ] **F4. Mensuração.** Tipo Evento de coleta e laboratório Aurora com limite fixo.
- [ ] **F5. Moldes e visual.** Sistema visual (ADR 0016), tamanho de página de modelo (ADR 0017) e moldes com nomes de produção (ADR 0012).
- [ ] **F6. Saídas para máquinas.** Kit para agentes e crosswalk documental, sem domínio próprio (ADR 0011).
- [ ] **F7. Agentes e prova.** Piloto com pessoas, que é o portão da v1.0 (ADR 0010).

O framework documenta *como tornar o conhecimento explícito*. Não certifica agentes, RAG ou SQL gerado.
