# Piloto com pessoas: portão da v1.0

- **Estado:** aguarda execução. Nenhuma sessão foi realizada.
- **Data:** 2026-11-17
- **Fase:** F7 (agentes e prova), [ADR 0010](../adr/0010-validacao-com-pessoas.md) e [ADR 0029](../adr/0029-agentes-e-prova.md)
- **Origem:** [07-metodo-e-credibilidade.md](../../auditoria/07-metodo-e-credibilidade.md), MET-16; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-10; [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F7

## Objetivo

Duas ou três pessoas do público misto reproduzem os casos 1 e 2, antes e depois de usar o Contexto. O piloto mede se a definição que a pessoa escreve muda a resposta da IA. Não mede satisfação nem facilidade.

- **Caso 1:** evento raro tratado como quebrado. A tarefa é escrever o documento do evento `generate_lead` que deixe a IA responder a pergunta "quais eventos pararam".
- **Caso 2:** indicador calculado com a definição genérica. A tarefa é escrever a definição da taxa de sessões web convertidas que deixe a IA chegar à conta do time.

## Indicador principal

'a definição escrita pela pessoa fez a IA acertar o gabarito?'

## Critério do portão (proposto)

Proposta a confirmar pelo mantenedor antes da primeira sessão. O portão compara o antes com o depois, porque acertar no depois não basta: a IA pode acertar só com os dados, sem texto nenhum.

- **Ganho do antes para o depois:** em cada caso, em pelo menos 2 de 3 pessoas (ou 2 de 2, se só duas participarem), o texto escrito depois faz a IA acertar a pergunta principal, e o texto escrito antes da mesma pessoa não fazia.
- **Linha de base sem texto:** antes da primeira sessão, a IA responde às perguntas pontuadas só com os dados do caso, sem nenhum texto, em três execuções, pela [pontuação](pontuacao.md). Se a linha de base já acerta a pergunta principal de um caso, o ganho nesse caso não prova efeito do texto, e o mantenedor decide se troca a pergunta antes das sessões.
- **Sem invenção:** nenhuma definição escrita depois preenche responsável, aprovação, fórmula ou vigência sem fonte e sem marcar como em aberto.

**Pergunta principal (proposta):**

- **Caso 1:** a Q02 do QA-AURORA-002@1.0 ("O generate_lead parou no Brasil?"). A tarefa 1 pede só o documento do `generate_lead`, e a conclusão da Q01 depende de julgar o `add_to_cart` no México, que a pessoa não documenta. A Q01 também já diz "considerando os dias completos até 15/11/2026", e no [caso 1](../experimentos/caso-1.md) a IA sem documentação chegou à conclusão dela em 4 de 6 execuções. A Q01 fica como apoio.
- **Caso 2:** a Q01 do QA-AURORA-001@1.1. A Q02 fica como apoio.

**Perguntas ao mantenedor, antes da primeira sessão:**

- O limiar de 2 de 3 pessoas (ou 2 de 2) serve?
- No caso 1, a pergunta principal passa a ser a Q02, ou a tarefa 1 é ampliada ao plano de mensuração inteiro e a Q01 continua principal?
- Se a linha de base acertar a pergunta principal de um caso, qual pergunta a substitui?

O resultado do portão fica em [resultados.md](resultados.md), que o mantenedor preenche.

## Pessoas e papéis

- **Participantes:** 2 ou 3, do público misto: especialista de negócio, analista de dados ou martech, e quem usa a IA direto ou monta agentes. Como as pessoas são recrutadas e como os dados delas são tratados fica em aberto ([ADR 0010](../adr/0010-validacao-com-pessoas.md)). Cada pessoa recebe um código, de P1 a P3.
- **Facilitador:** conduz a sessão e dá as falas do roteiro. Não ensina durante as tarefas. Responde como especialista só o que for perguntado, pela [ficha do especialista](ficha-do-especialista.md).
- **Avaliador:** registra tempos, perguntas à ficha, campos com fonte, perguntas em aberto e invenções na [folha de registro](folha-de-registro.md). Pontua depois, pela [pontuação](pontuacao.md). Se o mesmo mantenedor acumular os dois papéis, registre tudo na folha antes de pontuar.

## Materiais e ordem

Duração de cerca de 90 minutos por pessoa. A ordem segue o [roteiro da sessão](roteiro-da-sessao.md):

| Etapa | Tempo | O que acontece |
|---|---|---|
| 1. Boas-vindas e termo | 5 min | Leitura em voz alta do [termo de consentimento](termo-de-consentimento.md) |
| 2. Pré-teste | 5 min | Seis itens em [pre-e-pos-teste.md](pre-e-pos-teste.md), respondidos sem consulta |
| 3. Caso 1 antes | 10 min | Texto livre, sem o Contexto, pela [tarefa 1](tarefas.md) |
| 4. Caso 2 antes | 10 min | Texto livre, sem o Contexto, pela [tarefa 2](tarefas.md) |
| 5. Percurso do portal | 20 min | Escreva a pergunta, Descubra o que falta e o modelo .md do tipo |
| 6. Caso 1 depois | 10 min | Modelo .md do tipo Evento de coleta |
| 7. Caso 2 depois | 10 min | Modelo .md do tipo Indicador |
| 8. Transferência | 10 min | Caso não visto, pela [tarefa 3](tarefas.md) |
| 9. Pós-teste | 5 min | Os mesmos seis itens do pré-teste |
| 10. Conversa final | 5 min | Perguntas abertas sobre o que foi difícil |

Materiais que a pessoa recebe: o termo, o pré-teste e o pós-teste, o enunciado das tarefas, o acesso ao portal e a ferramenta de IA que ela já usa, o banco do caso 1 e o arquivo de dados do caso 2 (os dois do laboratório), e para a transferência as tabelas de pedidos e itens do laboratório de eventos.

Materiais só do facilitador ou do avaliador: o roteiro, a ficha do especialista, a folha de registro e a pontuação. A pontuação não é entregue à pessoa.

## Como a IA é pontuada

Cada texto escrito vai para a IA sozinho, com os dados do laboratório, em três execuções, cada uma numa sessão nova. O texto acerta a pergunta quando acerta em pelo menos 2 das 3. A regra completa, com a chave das perguntas, está em [pontuacao.md](pontuacao.md). Os gabaritos usados são QA-AURORA-002@1.0 (caso 1) e QA-AURORA-001@1.1 (caso 2), sem mudança neles. A linha de base sem texto segue a mesma regra, com os dados e sem documento.

## Limitações

- **Amostra pequena:** duas ou três pessoas. O resultado não é taxa de acerto nem prova de generalização.
- **Mesmo caso antes e depois:** a pessoa já viu o caso antes, e isso pode melhorar o depois por treino. A transferência, em caso não visto, ajuda a separar esse efeito.
- **Avaliador da mesma família de modelos:** se a IA que pontua for da mesma família da IA testada, os pontos cegos podem coincidir. Registre o modelo do avaliador.
- **Laboratório, não produção:** os dados são os do laboratório, e não os de um time real.

## Dados pessoais

O piloto não registra nome, contato, cargo nominal nem gravação de áudio ou vídeo. Os textos escritos e as respostas da IA são registrados sob o código da pessoa. O termo de consentimento não substitui a orientação jurídica do mantenedor sobre a LGPD.

## Arquivos desta pasta

- [Roteiro da sessão](roteiro-da-sessao.md): tempos e falas do facilitador.
- [Tarefas](tarefas.md): o enunciado entregue à pessoa.
- [Ficha do especialista](ficha-do-especialista.md): só para o facilitador.
- [Pré e pós-teste](pre-e-pos-teste.md): seis itens iguais nos dois momentos, com a chave de correção.
- [Folha de registro](folha-de-registro.md): um registro por pessoa.
- [Termo de consentimento](termo-de-consentimento.md): texto simples e lido em voz alta.
- [Pontuação](pontuacao.md): como cada texto é conferido pela IA.
- [Resultados](resultados.md): estado do piloto e a linha do critério do portão.

## Como o piloto vira portão da v1.0

A v1.0 só sai com o piloto registrado e citável ([ADR 0029](../adr/0029-agentes-e-prova.md)). O resultado é lido pelo mantenedor, que preenche a linha "Critério do portão" em [resultados.md](resultados.md). O plano geral de validação, com a parte da F2, está em [PLANO_VALIDACAO.md](../PLANO_VALIDACAO.md).
