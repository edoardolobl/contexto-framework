# Plano de validação com leitores: proposta para após v0.3

**Estado:** o teste com pessoas descrito aqui ainda é planejamento e não foi realizado. Os dois experimentos com agentes abaixo já rodaram.

**Caso 1 (F4):** [protocolo e resultados](experimentos/caso-1.md). Executado no Claude Code em 2026-11-17, com o critério de saída da F4 atendido nessa ferramenta; faltam o Codex e o Antigravity.

**Onboarding (F6):** [protocolo e resultados](experimentos/onboarding.md). Executado no Claude Code em 2026-11-17, com o critério de saída não atingido; faltam o Codex e o Antigravity. Os erros viraram perguntas em aberto propostas no [relatório do onboarding](experimentos/onboarding-perguntas-em-aberto.md).

**Piloto com pessoas (F7):** aguarda execução; ver a seção F7 no fim deste arquivo.

## Pergunta principal

O framework realmente permite que uma pessoa **experiente no assunto, mas sem familiaridade com engenharia de IA**, produza documentação mais explícita e saiba reconhecer o que ainda precisa ser decidido?

A avaliação tem que observar isso, não a capacidade de um LLM de executar SQL.

## Participantes recomendados

- Uma ou duas pessoas sem experiência em programação, mas que conheçam um processo;
- Uma ou duas pessoas analistas de Dados/BI;
- Uma pessoa de engenharia responsável por consumir documentação.

Essas quantidades são um **ponto de partida exploratório**, não uma recomendação estatística para estimar resultado populacional.

## Roteiro

### Cenário A: Regras e processos

1. Fornecer um processo fictício com termos ambíguos.
2. Pedir à pessoa participante que encontre o template apropriado sem orientação.
3. Solicitar que identifique gatilho, atores, decisões, exceções e fontes.
4. Pedir que registre pelo menos duas lacunas sem inventar respostas.
5. Verificar se ela distingue “pendente de aprovação” de “aprovado”.

### Cenário B: Analítica de dados

1. Apresentar os dados fictícios da Aurora.
2. Solicitar a definição de “sessões convertidas”.
3. Mostrar o cálculo 50% (pedidos confirmados por sessão) e perguntar se satisfaz a métrica.
4. Observar se a pessoa identifica cardinalidade e diferença de unidade.
5. Pedir que complete o template de KPI com fontes e pendências.

### Cenário C: Rubrica

1. Apresentar a frase “avaliar a qualidade da análise”.
2. Pedir critérios observáveis e exemplos de nível 2 versus nível 4.
3. Perguntar o que fazer quando não há evidência suficiente.
4. Verificar se ela evita concluir automaticamente o resultado da avaliação.

### Cenário D: Download e reuso

1. Pedir que a pessoa baixe o modelo Markdown do tipo que escolheu e o abra no editor que costuma usar.
2. Observar se ela entende a tabela "Identificação" e o "Histórico de versões" sem ajuda.
3. Pedir que registre a versão e a data do rascunho.
4. Mostrar o exemplo completo e perguntar se a aprovação é real ou fictícia.

## O que coletar

- Se a pessoa encontrou o template sem assistência;
- Quais lacunas identificou e quais passaram despercebidas;
- Se anotou informações desconhecidas sem presumir respostas;
- Se distinguiu o exemplo fictício de uma regra oficial;
- Quais instruções eram incompreensíveis ou desnecessariamente técnicas;
- Onde o documento final precisaria de revisão por especialista;
- Comentários livres dos participantes.

## Critério de êxito

Proposta de limiar mínimo, a confirmar pelo mantenedor antes das sessões: pelo menos 2 de cada 3 participantes encontram o modelo sem ajuda, e nenhum preenche uma lacuna por dedução sem marcá-la. Abaixo disso, a edição 1.0 não deve se declarar validada com leitores. Registre erros, dúvidas e melhorias por tarefa. A revisão editorial deve responder **qual lacuna pedagógica precisa ser corrigida**, e não apenas reunir elogios.

## Limites

Este plano não testa eficiência de RAG, confiabilidade de agentes, aderência normativa nem resultados de avaliações de emprego. Se algum material de usuário real for utilizado num teste, deve ser tratado segundo as permissões e políticas aplicáveis.

## F2: card sorting e tree test

**Origem:** [ADR 0010](adr/0010-validacao-com-pessoas.md) e incorporação I-10 em [12-incorporacoes.md](../auditoria/12-incorporacoes.md).

**Estado:** aguarda execução. Nenhuma sessão foi realizada.

### Card sorting

- **Participantes:** 15 pessoas ou mais, do público misto: especialistas de negócio, analistas de dados ou martech, quem usa a IA direto e quem monta agentes ou RAG.
- **Material:** cartões com os rótulos dos grupos do menu (Comece aqui, Percurso, Modelos, Laboratórios, Entender, Consultar, Usar com IA) e cartões com os rótulos das páginas.
- **Tarefa:** a pessoa agrupa as páginas e dá um nome a cada grupo com as próprias palavras. Registrar onde cada página foi colocada e quais não couberam em nenhum grupo.
- **Limiar:** a definir pelo mantenedor antes da primeira sessão.

### Tree test

- **Tarefas:** de 5 a 8, saindo das cinco entradas por sintoma da home e dos sete passos do percurso.
- **Registro:** cada tarefa tem a página esperada escrita antes da sessão.
- **Critério de sucesso:** pelo menos 80% de acerto nas tarefas do percurso.

Cada tarefa registra a origem (sintoma ou passo), a página esperada e se o participante acertou.

### Medir aprendizagem, não satisfação (I-10)

- **Rodadas:** de 5 a 8 participantes por rodada.
- **Sequência:** pré-teste, tarefa observada no portal, pós-teste em caso não visto e retenção numa segunda data.
- **Indicador principal:** a definição escrita pelo participante fez a IA acertar o gabarito?
- **Não medir:** nota de satisfação ou de facilidade como resultado principal.


## F7: piloto, portão da v1.0

**Origem:** [ADR 0010](adr/0010-validacao-com-pessoas.md), [ADR 0029](adr/0029-agentes-e-prova.md), I-10 e MET-16.

**Estado:** aguarda execução. O protocolo completo, com materiais, ordem e pontuação, está em [docs/piloto/README.md](piloto/README.md).

- **Participantes:** 2 ou 3 pessoas do público misto, reproduzindo os casos 1 e 2 antes e depois de usar o Contexto, com uma tarefa de transferência em caso não visto.
- **Indicador principal:** 'a definição escrita pela pessoa fez a IA acertar o gabarito?'
- **Critério do portão (proposto, a confirmar pelo mantenedor antes da primeira sessão):** em cada caso, em pelo menos 2 de 3 pessoas (ou 2 de 2), o texto escrito depois faz a IA acertar a pergunta principal e o texto escrito antes não fazia; a linha de base, só com os dados e sem texto, não acerta a pergunta principal; e nenhuma definição escrita depois preenche responsável, aprovação, fórmula ou vigência sem fonte e sem marcar como em aberto. A pergunta principal proposta é a Q02 do QA-AURORA-002@1.0 no caso 1 e a Q01 do QA-AURORA-001@1.1 no caso 2.
