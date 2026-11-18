# Colunas da planilha de plano de mensuração

A planilha tem uma linha por evento e operação, com separador ponto e vírgula. Linhas com o mesmo Evento formam um documento só. Colunas de nível do evento valem para o documento todo: se duas linhas do mesmo evento trazem valores diferentes, é erro. Célula vazia numa linha e preenchida na outra não é conflito. Colunas de nível da operação valem só para a linha.

Datas podem vir como DD/MM/AAAA ou AAAA-MM-DD. Cabeçalho e ordem das colunas: o nome casa sem diferença de maiúsculas, e coluna desconhecida é ignorada com aviso.

| Coluna | Campo do Evento de coleta | Nível | Como preencher | Se a célula ficar vazia |
|---|---|---|---|---|
| Evento | title ("Evento valor") e chave de agrupamento | evento | Nome do evento como chega na ferramenta, por exemplo generate_lead | Erro na linha: sem o nome, não há documento |
| Identificador | id (e revision_id, id@0.1) | evento | Código em maiúsculas com hífens, por exemplo EVENT-AURORA-GENERATE-LEAD | Pergunta em aberto; id fica em branco |
| Pergunta de negócio | intent.question | evento | A pergunta que o documento responde | Pergunta em aberto |
| Responsável | owner e quem resolve as perguntas em aberto | evento | Cargo ou área, nunca nome de pessoa | Pergunta em aberto |
| Gatilho | trigger | evento | A ação que faz o evento disparar | Pergunta em aberto |
| Frequência esperada | expected_behavior.expected_frequency | evento | O ritmo normal, em palavras | Pergunta em aberto |
| Prazo para os dados chegarem | late_arrival_window | evento | Quando o dia fica completo, com fuso | Pergunta em aberto |
| Data de lançamento | launch_date | evento | DD/MM/AAAA ou AAAA-MM-DD | Pergunta em aberto |
| Consentimento exigido | consent_requirements | evento | O consentimento que o disparo exige | Pergunta em aberto |
| Indicadores que dependem do evento | downstream_kpis | evento | Nomes separados por vírgula (entre aspas se o separador for vírgula) | Pergunta em aberto |
| Operação | active_scopes[].operation, silence_tolerance[].operation | operação | Código da operação, por exemplo BR | Pergunta em aberto; a pergunta cita a linha |
| País | active_scopes[].country | operação | País da operação | Pergunta em aberto |
| Marca | active_scopes[].brand | operação | Marca da operação | Pergunta em aberto |
| Ativo na operação | active_scopes[].active | operação | sim, não, true ou false; outro valor é erro | Pergunta em aberto |
| Ativo desde | active_scopes[].since | operação | DD/MM/AAAA ou AAAA-MM-DD | Pergunta em aberto |
| Motivo | active_scopes[].reason | operação | Por que está ativo ou inativo ali | Pergunta em aberto, exceto quando Ativo na operação é sim |
| Tolerância ao silêncio | expected_behavior.silence_tolerance[].rule | operação | Quantos dias completos seguidos em zero levantam suspeita | Pergunta em aberto |
| Ferramenta de destino | destination[].platform | operação | Ferramenta que recebe o disparo, como GA4 | Pergunta em aberto |
| Onde dentro da ferramenta | destination[].object | operação | Propriedade, tabela ou contêiner | Pergunta em aberto |
| Fuso horário | destination[].timezone | operação | Fuso em que o dia é contado, por exemplo America/Sao_Paulo | Pergunta em aberto |

## O que o rascunho nunca traz

- status é sempre draft.
- quem aprova, vigência (início e fim), última revisão, licença e endereço ficam em branco.
- approved_by do histórico fica em branco.
- Todo rascunho ganha a pergunta "Quem aprova o documento do evento X?".

Nunca preencha uma célula vazia por conta própria: ela vira pergunta em aberto para quem responde pelo evento.
