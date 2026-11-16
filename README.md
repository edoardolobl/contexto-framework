# Contexto — Framework de Conhecimento para IA

> **Uma IA não deveria adivinhar como sua organização funciona.**

O Contexto é um framework pedagógico, independente de fornecedores e clientes, para orientar especialistas de qualquer domínio a **explicitar conceitos, processos, regras, exceções e fontes**, de forma que engenheiros de IA não precisem inventar semântica de negócio a partir de acervos vagos e dispersos.

**Promessa única:** ensinar **como documentar o conhecimento organizacional**. Preencher os templates **não garante** o acerto de SQL, RAG, agentes ou avaliações automatizadas.

## Portal

https://edoardolobl.github.io/contexto-framework/

## O que existe na v0.3

### Núcleo transversal
- Princípios e método das oito dimensões;
- Roteiro de elicitação e passagem do conhecimento;
- Templates de conceitos, processos, regras, políticas e KPIs;
- Exemplos comentados em RH, Marketing, Financeiro e Analytics.

### Trilha de Dados e Analytics
- Definições semânticas de **datasets**, campos, granularidade e códigos;
- **Relacionamentos** entre tabelas, cardinalidade e riscos de junção;
- **Dashboards**, filtros, métricas, vigência e limites;
- **Rubricas AI-ready** com evidências, níveis e revisão humana;
- **Perguntas e respostas de referência**, incluindo ambiguidade e abstenção;
- **Laboratório Aurora** com dados sintéticos SQLite, SQL verificável e cálculo de taxa de sessões convertidas.

Cada tipo de documento oferece Markdown, YAML e exemplo fictício para download. Os formatos são **convenções pedagógicas**, não schemas de fornecedores.

## Reproduza o laboratório SQL

```bash
python3 -m pip install PyYAML
python3 scripts/check_analytics_fixture.py
```

A consulta em `public/downloads/aurora-reference-query.sql` deve retornar **25%** na amostra fictícia `aurora-fixture.sql`. Ela calcula **sessões únicas convertidas**, não quantidade de pedidos. Isso é um exemplo de como a documentação ajuda a explicitar a unidade da métrica, não uma prova de acurácia de modelos de IA.

## Desenvolvimento

Requer Node.js 22.12 ou superior, npm, Python 3 e PyYAML.

```bash
npm install
npm run validate:content
python3 scripts/check_decision_examples.py
python3 scripts/check_analytics_fixture.py
npm run build
npm run dev
```

O GitHub Actions executa validação de conteúdo, checagens de exemplos e build em PRs. Merges na `main` acionam a publicação do Astro Starlight no GitHub Pages.

## Estrutura

```text
src/
  components/          Elementos visuais e downloads
  content/docs/        Metodologia, templates e exemplos
  styles/              Identidade visual
public/downloads/     Templates Markdown/YAML e laboratório SQL
scripts/              Validações independentes de LLM
docs/                 Contrato editorial e roadmap
.github/workflows/    Testes e publicação
```

## Como editar com qualidade

Leia `docs/CONTRATO_EDITORIAL.md`. Cada nova página deve ensinar o leitor a compreender, observar e aplicar o conceito. Todo template publicado deve incluir instrução de uso, exemplo, perguntas de elicitação, registro de lacunas, responsáveis e fontes.

Os documentos são destinados a pessoas de negócio e tecnologia. **Não presumir que todo colaborador sabe Markdown, YAML, SQL ou arquitetura de IA**.

## Bibliografia

[Nonaka (1994)](https://doi.org/10.1287/orsc.5.1.14) · [IIBA](https://www.iiba.org/knowledgehub/the-business-analysis-standard/) · [KCS v6](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide) · [OMG DMN](https://www.omg.org/spec/DMN/1.6) · [Snowflake Semantic Views](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec) · [Rumiantsau & Fokeev (2026)](https://arxiv.org/abs/2604.25149) · [Microsoft — RAG Preparation](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-preparation-phase) · [NIST AI RMF](https://airc.nist.gov/airmf-resources/playbook/measure/)

## Licença

A definir pelo mantenedor. Até a escolha explícita, não presumir autorização geral de redistribuição de código ou conteúdo.
