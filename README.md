# Contexto: Framework de Conhecimento para IA

> Transforme perguntas de negócio em documentos aprovados e versionados que uma IA consegue consultar sem inventar definições, seja a ferramenta que você usa direto, seja o sistema que a engenharia monta.

Apoio: *Uma IA não deveria adivinhar como sua organização funciona.*

O Contexto **não garante** o acerto de SQL, RAG, agentes ou avaliações automatizadas. Os documentos são insumos; os sistemas precisam ser projetados e testados.

## Portal

https://edoardolobl.github.io/contexto-framework/

## O que existe na v0.4

### Núcleo transversal
- Percurso em **sete passos**, da pergunta de negócio ao teste com a ferramenta de IA ([ADR 0023](docs/adr/0023-percurso-em-sete-passos.md));
- Descoberta por **entrevista de um incidente real**, em vez de questionário ([ADR 0024](docs/adr/0024-descoberta-por-incidente.md));
- Revisão de documentos em **três verificações independentes**: cobertura, consistência/evidências e confirmação por quem tem autoridade; [ficha em texto](public/downloads/roteiro-revisao-documental.md) para preencher sem YAML;
- **Checklist de revisão** com as oito dimensões, uma convenção do Contexto ([ADR 0014](docs/adr/0014-oito-dimensoes-como-checklist.md));
- Modelos de conceitos, processos, regras, políticas e indicadores (modelo KPI);
- Exemplos comentados em RH, Marketing, Financeiro e Analytics.

### Trilha de Dados e Analytics
- Definições semânticas de **datasets**, campos, granularidade e códigos;
- **Relacionamentos** entre tabelas, cardinalidade e riscos de junção;
- **Dashboards**, filtros, **indicadores**, vigência e limites;
- **Rubrica** com critérios explícitos, evidências, níveis e revisão humana, como trilha complementar ([ADR 0003](docs/adr/0003-rubrica-em-trilha-complementar.md));
- **Perguntas de negócio**, com o gabarito (as respostas esperadas), incluindo ambiguidade e abstenção;
- **Laboratório Aurora** com dados sintéticos SQLite, SQL verificável e cálculo de taxa de sessões convertidas.

Cada tipo de documento oferece quatro arquivos: modelo em Markdown (sem YAML, para preencher em texto), modelo em YAML, **exemplo com lacunas** e **exemplo completo com aprovação fictícia**. Todos trazem versão, data da versão e histórico de versões. Os formatos são **convenções pedagógicas**, não schemas de fornecedores.

## Reproduza o laboratório SQL

```bash
python3 -m pip install PyYAML
python3 scripts/check_analytics_fixture.py
```

A consulta em `public/downloads/aurora-reference-query.sql` deve retornar **25%** na amostra fictícia `aurora-fixture.sql`. Ela calcula **sessões únicas convertidas**, não quantidade de pedidos. Isso é um exemplo de como a documentação ajuda a explicitar a unidade do indicador, não uma prova de acurácia de modelos de IA.

## Desenvolvimento

Requer Node.js 22.12 ou superior, npm e Python 3. As dependências Python de desenvolvimento (PyYAML e pytest) estão em `requirements-dev.txt`.

```bash
python3 -m pip install -r requirements-dev.txt
npm ci
npm run check
npm run dev
```

`npm run check` roda, nesta ordem, os testes dos validadores, as checagens de conteúdo (páginas, downloads, higiene, decisão, amostra SQLite e versões), o build e a conferência de links no HTML gerado. O GitHub Actions roda a mesma sequência em todo PR, e a publicação no GitHub Pages só acontece depois que ela passa num merge na `main`.

Decisões de projeto ficam registradas em [`docs/adr/`](docs/adr/) e as mudanças, em [`CHANGELOG.md`](CHANGELOG.md). O vocabulário que o validador aplica e a lista de tipos de documento ficam em [`src/data/`](src/data/).

## Estrutura

```text
src/
  components/          Elementos visuais e downloads
  content/docs/        Metodologia, modelos e exemplos
  data/                Fontes únicas: vocabulário e lista de tipos de documento
  styles/              Identidade visual
public/downloads/     Modelos Markdown/YAML e laboratório SQL
scripts/              Validações independentes de LLM
docs/                 Contrato editorial e roadmap
  adr/                Registros de decisão (ADR)
.github/workflows/    Testes e publicação
```

## Como editar com qualidade

Leia `docs/CONTRATO_EDITORIAL.md`. Cada nova página deve ensinar o leitor a compreender, observar e aplicar o conceito. Todo modelo publicado deve incluir instrução de uso, os dois exemplos (com lacunas e completo), histórico de versões, perguntas de descoberta, registro de lacunas, responsáveis e fontes.

Os documentos são destinados a pessoas de negócio e tecnologia. **Não presumir que todo colaborador sabe Markdown, YAML, SQL ou arquitetura de IA**.

## Bibliografia

[Nonaka (1994)](https://doi.org/10.1287/orsc.5.1.14) · [IIBA](https://www.iiba.org/knowledgehub/the-business-analysis-standard/) · [Knowledge-Centered Success: Practices Guide](https://library.serviceinnovation.org/KCS/Knowledge-Centered_Success_Practices_Guide) · [OMG DMN](https://www.omg.org/spec/DMN/1.6) · [Snowflake Semantic Views](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec) · [Rumiantsau & Fokeev (2026, preprint)](https://arxiv.org/abs/2604.25149) · [Microsoft: RAG Preparation](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-preparation-phase) · [NIST AI RMF](https://airc.nist.gov/airmf-resources/playbook/measure/)

## Autoria

Criado e mantido por **Edoardo Lobl** ([LinkedIn](https://www.linkedin.com/in/edoardolobl/) · [GitHub](https://github.com/edoardolobl)).

## Licença

- **Código** (componentes, estilos, scripts, configuração, arquivos SQL e blocos de código exibidos nas páginas): [MIT](LICENSE).
- **Conteúdo** (páginas do portal, método, modelos e exemplos em Markdown e YAML, documentação): [CC BY 4.0](LICENSE-CONTENT).

O nome "Contexto" e o logotipo não são licenciados para uso como marca. Normas, guias, artigos e marcas de terceiros citados na bibliografia permanecem sob os direitos de seus titulares.

Usar os modelos para escrever documentos internos da sua organização não exige atribuição. Ao republicar ou adaptar o material, cite: *Contexto: Framework de Conhecimento para IA*, de Edoardo Lobl, CC BY 4.0, com o link do portal.
