# Contexto — Framework de Conhecimento para IA

> Um método para que especialistas documentem o significado de processos, métricas, regras e exceções sem delegar ao engenheiro de IA a tarefa de inferir conhecimento que ninguém formalizou.

**Status:** v0.1 — primeira fatia vertical: método, exemplo pedagógico de KPI, checklist e bibliografia. Os demais módulos seguem em expansão.

## O que está incluído

- Portal **Astro + Starlight**, em português brasileiro, com navegação e busca estática.
- Contrato editorial em [`docs/CONTRATO_EDITORIAL.md`](docs/CONTRATO_EDITORIAL.md).
- Método das oito dimensões, elicitação, promessa e limites.
- Template de KPI portável em `public/downloads/` e exemplo fictício.
- Comparação antes/depois e checklist interativo sem backend.
- Bibliografia e matriz inicial de rastreabilidade.
- Workflow GitHub Pages e workflow de validação editorial em pull requests.

## Pré-requisitos

- Node.js 22.12 ou superior e npm.
- Python 3 e PyYAML para validação completa dos exemplos YAML.

## Desenvolvimento local

```bash
npm install
npm run validate:content
npm run dev
```

Abra a URL informada pelo Astro. O projeto utiliza um subcaminho `/contexto-framework/` na publicação padrão do GitHub Pages. Para validar a versão estática:

```bash
npm run build
npm run preview
```

## Publicação

O site é publicado por `.github/workflows/deploy.yml` após push em `main`. O GitHub Pages deve usar a opção **GitHub Actions** em Settings → Pages.

**Portal:** https://edoardolobl.github.io/contexto-framework/

## Organização do código

```text
src/
  components/           Componentes visuais e checklist
  content/docs/         Páginas Markdown e MDX
  styles/               Design system
  content.config.ts     Coleção Starlight
public/downloads/      Templates portáteis
.github/workflows/      Validação e publicação
scripts/                Validação documental
docs/                   Contrato editorial e roadmap
```

## Como editar o conteúdo

A manutenção é individual: edite páginas em `src/content/docs/`. O YAML no início das páginas do portal controla navegação e apresentação. Os templates baixados possuem outros metadados, referentes ao objeto documentado.

Ao publicar um template novo, inclua explicação de uso, perguntas de elicitação, exemplo incompleto, exemplo revisado, fontes, lacunas e validação.

## Princípios

1. Uma prática relatada não é necessariamente uma regra oficialmente aprovada.
2. Metadados não devem ser preenchidos por suposição.
3. Documento bem estruturado não garante desempenho de RAG, SQL ou agentes.
4. Exemplos são fictícios e não contêm dados confidenciais.
5. O framework pertence à camada documental, não à camada de execução.

## Fontes metodológicas

[Diátaxis](https://diataxis.fr/) · [KCS v6](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide) · [IIBA](https://www.iiba.org/knowledgehub/the-business-analysis-standard/) · [Rumiantsau & Fokeev (2026)](https://arxiv.org/abs/2604.25149)

## Licença

Ainda não definida. Não pressupor licença open source ou permissão geral de redistribuição.
