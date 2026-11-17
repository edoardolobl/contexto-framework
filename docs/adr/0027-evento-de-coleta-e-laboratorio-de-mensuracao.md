# 0027. Evento de coleta e laboratório de mensuração

- **Estado:** Proposto
- **Data:** 2026-11-17
- **Proposto por:** F4 (fase Mensuração; quando aceito, vira "**Decidido por:** mantenedor")
- **Origem:** [10-direcao-proposta.md](../../auditoria/10-direcao-proposta.md), fase F4; [09-casos-de-uso.md](../../auditoria/09-casos-de-uso.md), casos 1 e 3; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-18 a I-23

## Contexto

Um evento raro com zero disparos num dia foi lido como quebra de coleta (USO-01), e a documentação não tinha onde dizer o que é esperado por operação, qual o histórico normal e quando um dia está completo. Cruzar mídia, GA4 e pedidos também ficou sem molde: não há atribuição, fuso por fonte nem junção por agregado (USO-02), e nenhum modelo mostra a faixa plausível de um número (USO-05). O [ADR 0022](./0022-laboratorio-pequeno-verificado-em-sqlite.md) deixou em aberto o tamanho do laboratório, e a F4 precisava fechar isso antes de escrever o Lab 2.

## Decisão

1. **Tipo Evento de coleta**, com slug `evento-coleta` e página em `templates/evento-coleta`, no núcleo de entrada ([ADR 0013](./0013-nucleo-de-entrada-com-cinco-tipos.md)). O núcleo para sair do rascunho é o das oito chaves do [ADR 0026](./0026-schema-1-0-e-fonte-unica.md). Os campos de expectativa seguem a incorporação I-18: `expected_frequency`, `active_scopes` (operação, país, marca), `expected_zero_conditions`, `launch_date`, `retirement_date`, `renamed_from` (com vigência), `consent_requirements`, `late_arrival_window`, `deduplication_key`, `downstream_kpis`, `known_exceptions` e `validation_query`. Somam-se `grain_note` (o que uma linha representa) e `missing_days_policy` (o que significa um dia sem linha). O bloco `context.instructions` já vem preenchido no modelo, com a instrução mínima ao agente ([ADR 0025](./0025-instrucao-minima-ao-agente.md)).
2. **Regra canônica de evento quebrado como exemplo do tipo Regra e decisão.** A regra só declara candidato a falha quando o evento está ativo no escopo, com frequência esperada na janela, janela de ingestão completa e desvio por N períodos seguidos, avaliado por operação e depois das exceções conhecidas. O N fica no Evento de coleta, não na regra. Limiares são escolha do time, nunca valor universal (I-19).
3. **Triagem na página do tipo Evento de coleta.** A triagem de anomalia em cinco passos (delimitar o escopo, datar o início e cruzar com deploys, checar sazonalidade, cruzar fonte externa, testar o fluxo à mão) entra como tabela de decisão de exemplo, em seção opcional da página do tipo (I-20).
4. **Reconciliação como exemplo do tipo Política.** A ficha de regras de reconciliação entre Meta, Google Ads, GA4, BigQuery e ERP é um exemplo completo do tipo Política, com uma posição por fonte e a configuração de janela, modelo, data e fuso de cada uma. Fica na página de cenários de mensuração (I-21).
5. **Limite fixo do Lab 2.** O laboratório de eventos tem 2 operações, 3 eventos, 1 evento raro presente só numa das operações, 1 incidente, 28 dias de histórico e 1 dia ainda incompleto em D+2. Os números são recalculados em SQLite. Esta decisão fecha o ponto em aberto do ADR 0022.
6. **Validador próprio do Lab 2.** `scripts/check_lab2_mensuracao.py` recalcula a amostra e confere o texto da página. Ele não substitui o validador do Lab 1 e não chama nenhum LLM (ADR 0022).
7. **Cenários só com fonte primária.** O banco de cenários (`referencias/cenarios-de-mensuracao`) só entra com documentação oficial lida, do Google Analytics Help ou do Google for Developers. Cenário sem confirmação nessas fontes fica de fora e aparece na lista de pendências do relatório, não no portal (I-22).

Em aberto: os nomes finais dos campos do Evento de coleta dependem da revisão do mantenedor antes da F5. A escolha de cada limiar de alerta continua sendo do time que a adota.

## Alternativas consideradas

- **Alternativa A:** manter a regra só no modelo de decisão, como no esboço A1 da auditoria. Não foi escolhida: ensina a tratar zero como quebra, não separa operação e não tem onde registrar histórico nem dia incompleto.
- **Alternativa B:** fundir Evento de coleta com Dataset. Não foi escolhida: o Dataset descreve uma tabela, e o evento descreve uma implementação por operação e por período de vida. Os dois ficam separados, com o Dataset apontando para o evento.
- **Alternativa C:** deixar o Lab 2 crescer conforme a necessidade. Não foi escolhida: o ADR 0022 pede um laboratório pequeno e verificável por máquina, e um tamanho aberto impede o teste de recálculo.
- **Alternativa D:** usar um LLM como juiz das respostas do laboratório. Não foi escolhida, pelo mesmo motivo do ADR 0022: o resultado deixa de ser reproduzível.
- **Alternativa E:** incluir cenários de blogs e de fornecedores. Não foi escolhida: são números de terceira mão, e a regra de cenários só com fonte primária protege o leitor de citações que não se sustentam.

## Consequências

- **Positivas:** o caso 1 e o caso 3 ganham molde no portal; o Lab 2 tem limite fixo e recalculo verificável; cada cenário tem fonte que o leitor pode abrir.
- **Negativas:** o tipo novo tem mais campos que os outros, e a F5 precisa de moldes didáticos para ele. O laboratório fica pequeno, o que mostra a diferença entre definições e não a taxa de acerto de um sistema.
- **Fases afetadas:** F4 (este ADR, o tipo, o Lab 2, o banco de cenários e o protocolo do caso 1 em `docs/experimentos/caso-1.md`); F5 (sequência didática do tipo Evento de coleta); F7 (piloto com o caso 1, antes e depois).
- **Breaking:** nenhum. Os tipos existentes não mudam de chave nem de campo; o tipo novo só acrescenta um nível de entrada.
