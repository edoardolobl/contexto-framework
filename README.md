# Contexto — Framework de Conhecimento para IA

**Uma IA não deveria adivinhar como sua organização funciona.**

Contexto é um framework aberto, independente de fornecedores e organizações, para orientar especialistas de diferentes áreas a explicitar conhecimento tácito, significados, regras, exceções e evidências em documentos verificáveis. O framework ensina **como documentar**, para reduzir a necessidade de a engenharia de IA inferir ou inventar regras de negócio.

## Promessa — e limites

A documentação é um insumo para aplicações RAG, agentes e analytics. **Preencher templates não garante respostas corretas, SQL correto ou sistemas confiáveis.** Cabe aos responsáveis por cada domínio validar as definições, e à engenharia testar a implementação.

## Conteúdo da versão inicial

- Fundamentos da promessa metodológica
- Método das oito dimensões
- Template e exemplo fictício de KPI
- Documentação semântica para Dados e Analytics
- Referências bibliográficas

## Desenvolvimento

Requer Node.js 22 ou superior.

```bash
npm install
npm run dev
npm run build
```

## Publicação

O workflow `.github/workflows/deploy.yml` constrói o site e envia o resultado ao GitHub Pages. Nas configurações do repositório, em **Settings → Pages**, selecione **GitHub Actions** como fonte de publicação.

O destino esperado, depois de habilitar Pages e completar um build bem-sucedido, é:
https://edoardolobl.github.io/contexto-framework/

## Estado do projeto

**v0.1 — fundação técnica e editorial em construção.** Esta é uma primeira sincronização no GitHub. A versão visual local anterior possuía componentes e páginas adicionais que ainda precisam ser integrados e testados no repositório.

## Licença

A definir. Até a escolha explícita de licença, não pressupor autorização geral de reutilização de código ou conteúdo.
