# Contexto — Framework de Conhecimento para IA

> **Uma IA não deveria adivinhar como sua organização funciona.**

Contexto é um framework pedagógico, genérico e independente de fornecedores para ajudar especialistas de domínio a **explicitar conhecimento tácito, conceitos, regras, exceções, fontes e autoridade**, de modo que engenheiros de IA não precisem inventar definições ausentes em acervos ambíguos e dispersos.

## Promessa única

**Ensinar como documentar o conhecimento organizacional**, com método, perguntas de elicitação, templates e exemplos comentados. Preencher templates **não garante** SQL, RAG ou agentes corretos. A implementação, o controle de acesso e a avaliação técnica permanecem sob responsabilidade das equipes de engenharia.

## Versão v0.2

Além do módulo de KPI da v0.1, agora há uma trilha transversal para:

- **Conceitos e glossários:** termos preferidos, sinônimos, contraexemplos e diferenças entre domínios.
- **Processos:** gatilhos, entradas, atividades, responsáveis, decisões, desvios e evidências.
- **Regras e decisões:** condições, prioridades, resultados e tratamento do desconhecido.
- **Políticas e referências:** autoridade, vigência, fontes, conflito documental e exceções.
- **Revisão e entrega:** lista de pendências e verificação da qualidade documental.

Cada novo template oferece **Markdown + YAML + exemplo preenchido fictício**. Um seletor pedagógico ajuda a escolher o modelo por tarefa. A trilha de Dados & Analytics será ampliada na v0.3.

## Portal publicado

https://edoardolobl.github.io/contexto-framework/

## Desenvolvimento

Requer Node.js 22.12+ e Python 3. Para verificar YAML, instale PyYAML com `python3 -m pip install PyYAML`.

```bash
npm install
npm run validate:content
npm run build
npm run dev
```

O projeto usa Astro Starlight e publica automaticamente via GitHub Pages após merge na branch `main`. Pull requests executam validação de conteúdo e build.

## Organização

```text
src/
  components/          Componentes pedagógicos e downloads
  content/docs/        Páginas de metodologia, templates e exemplos
  styles/              Identidade visual
public/downloads/     Modelos e exemplos Markdown/YAML
docs/                 Contrato editorial e roadmap
scripts/              Validação editorial
.github/workflows/    Verificação e publicação
```

## Como contribuir editorialmente ao projeto

1. Comece pelo [contrato editorial](docs/CONTRATO_EDITORIAL.md).
2. Escreva uma página que ajude o leitor a compreender, observar e aplicar a técnica.
3. Crie template, exemplo fictício, questões de elicitação e referências primárias.
4. Não preencha lacunas com suposições. Escreva **quem deve decidir**.
5. Execute o validador e o build antes do pull request.

O repositório é mantido por uma pessoa. A proposta editorial independe de qualquer empresa ou cliente.

## Referências

[IIBA](https://www.iiba.org/knowledgehub/the-business-analysis-standard/) · [KCS](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide) · [Diátaxis](https://diataxis.fr/) · [OMG BPMN](https://www.omg.org/spec/BPMN/2.0.2) · [OMG DMN](https://www.omg.org/spec/DMN/1.6) · [W3C SKOS](https://www.w3.org/TR/skos-reference/)

## Licença

A definir pelo mantenedor. Até a escolha explícita de licença, não presumir autorização geral de redistribuição de código ou conteúdo.
