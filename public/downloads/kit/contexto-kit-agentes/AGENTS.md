# Instruções do kit Contexto para agentes

Versão alvo: formato AGENTS.md conforme agents.md, conferido em 17/11/2026.
Licença deste kit: CC BY 4.0.

Estas instruções orientam o agente. Elas não garantem que ele as siga: cada ferramenta decide como lê o arquivo e como responde.

## Onde fica cada coisa

- [Glossário](glossario.md): termos, sinônimos e o que não confundir com outro termo.
- [Contratos](contratos/): a definição aprovada de cada assunto, com id e versão atual.
- [Histórico de contratos](contratos/historico/): versões anteriores, usadas só para perguntas sobre o passado.
- [Gabaritos](gabaritos/): respostas esperadas, para conferir se o entendimento está certo.
- [Dados](dados/): a amostra do laboratório, para conferir contas. A amostra não é definição.
- [Skill auditar-coleta](skills/auditar-coleta/SKILL.md): passos para perguntas sobre evento de coleta que parou, quebrou ou está zerado.

## Arquivos do kit

- [Glossário](glossario.md)
- [Participante ativo: programa de integração Aurora (CONCEPT-ONBOARDING-001@2.0)](contratos/CONCEPT-ONBOARDING-001@2.0.md)
- [Acompanhamento de sessões convertidas: Aurora (DASH-AURORA-WEB@2.1)](contratos/DASH-AURORA-WEB@2.1.md)
- [Pedidos: Aurora (DATASET-AURORA-ORDERS@1.0)](contratos/DATASET-AURORA-ORDERS@1.0.md)
- [Sessões web e app: Aurora (DATASET-AURORA-SESSIONS@1.2)](contratos/DATASET-AURORA-SESSIONS@1.2.md)
- [Evento quebrado: Aurora (DECISION-AURORA-EVENTO-QUEBRADO@1.1)](contratos/DECISION-AURORA-EVENTO-QUEBRADO@1.1.md)
- [Triagem de campanha: Aurora (DECISION-CAMPAIGN-001@2.0)](contratos/DECISION-CAMPAIGN-001@2.0.md)
- [Evento generate_lead: Aurora (EVENT-AURORA-GENERATE-LEAD@1.1)](contratos/EVENT-AURORA-GENERATE-LEAD@1.1.md)
- [Taxa de sessões convertidas: loja web Aurora (KPI-AURORA-001@2.0)](contratos/KPI-AURORA-001@2.0.md)
- [Ficha de reconciliação entre mídia, GA4, pedidos e ERP: Aurora (POLICY-AURORA-RECONCILIACAO-MIDIA@1.1)](contratos/POLICY-AURORA-RECONCILIACAO-MIDIA@1.1.md)
- [Despesas em eventos: Aurora (POLICY-EVENTS-001@1.1)](contratos/POLICY-EVENTS-001@1.1.md)
- [Solicitar e publicar campanha: Aurora (PROCESS-CAMPAIGN-001@2.0)](contratos/PROCESS-CAMPAIGN-001@2.0.md)
- [Sessões para pedidos: Aurora (REL-AURORA-SESSIONS-ORDERS@2.0)](contratos/REL-AURORA-SESSIONS-ORDERS@2.0.md)
- [Rubrica de revisão de material de campanha: Aurora (RUBRIC-CAMPAIGN-001@2.0)](contratos/RUBRIC-CAMPAIGN-001@2.0.md)
- [Participante ativo: programa de integração Aurora (CONCEPT-ONBOARDING-001@1.0)](contratos/historico/CONCEPT-ONBOARDING-001@1.0.md)
- [Taxa de sessões convertidas: loja web Aurora (KPI-AURORA-001@1.0)](contratos/historico/KPI-AURORA-001@1.0.md)
- [Dados: aurora-fixture.sql](dados/aurora-fixture.sql)
- [Dados: aurora-lab2-fixture.sql](dados/aurora-lab2-fixture.sql)
- [Dados: aurora-lab2-reference-query.sql](dados/aurora-lab2-reference-query.sql)
- [Dados: aurora-reference-query.sql](dados/aurora-reference-query.sql)
- [Gabarito documental: sessões convertidas Aurora (QA-AURORA-001@1.1)](gabaritos/QA-AURORA-001@1.1.md)
- [Gabarito documental: quais eventos pararam de coletar (QA-AURORA-002@1.0)](gabaritos/QA-AURORA-002@1.0.md)
- [Skill `auditar-coleta`](skills/auditar-coleta/SKILL.md)
- [Evento quebrado: Aurora (DECISION-AURORA-EVENTO-QUEBRADO@1.1)](skills/auditar-coleta/references/DECISION-AURORA-EVENTO-QUEBRADO@1.1.md)
- [Evento generate_lead: Aurora (EVENT-AURORA-GENERATE-LEAD@1.1)](skills/auditar-coleta/references/EVENT-AURORA-GENERATE-LEAD@1.1.md)
- [Skill `contexto-consultar`](skills/contexto-consultar/SKILL.md)
- [Skill `contexto-elicitar`](skills/contexto-elicitar/SKILL.md)
- [Referência da Skill `contexto-elicitar`: references/perguntas-por-incidente.md](skills/contexto-elicitar/references/perguntas-por-incidente.md)
- [Referência da Skill `contexto-elicitar`: references/tipos.md](skills/contexto-elicitar/references/tipos.md)
- [Skill `importar-plano-de-mensuracao`](skills/importar-plano-de-mensuracao/SKILL.md)
- [Evento generate_lead: Aurora (EVENT-AURORA-GENERATE-LEAD@1.1)](skills/importar-plano-de-mensuracao/references/EVENT-AURORA-GENERATE-LEAD@1.1.md)
- [Referência da Skill `importar-plano-de-mensuracao`: references/colunas.md](skills/importar-plano-de-mensuracao/references/colunas.md)

## Ordem de leitura

1. Este arquivo.
2. O glossário, para os termos da pergunta.
3. O contrato do assunto, pelo id.
4. O gabarito, para conferir a resposta esperada, se a pergunta estiver nele.
5. A Skill auditar-coleta, quando a pergunta for sobre evento de coleta que parou.

## Regras

- Nunca calcule um indicador sem consultar a definição aprovada; se não houver, pergunte.
- Zero em um dia não é quebra; compare com a linha de base por operação.
- Use só o que está neste kit. Não complete a resposta com definição de mercado ou de outra operação.
- Só o estado approved (aprovado) vale como regra.
- draft (rascunho) e pending_approval (pendente de aprovação) são rascunho e não valem como definição.
- superseded (substituído) serve só para perguntas sobre o passado: escolha a versão cuja vigência cobre a data da pergunta.
- deprecated (obsoleto) quer dizer que o assunto deixou de valer. Diga isso.
- valid_from é o primeiro dia de vigência. valid_to é o fim exclusivo: o dia de valid_to já não conta.
- Em toda resposta, cite o id e a versão de cada documento usado, no formato id@versão.
- Termine toda resposta em um destes três desfechos:
  - Responder: há definição aprovada que cobre a pergunta.
  - Pedir esclarecimento: a pergunta é ambígua, porque falta operação, canal, período ou unidade. Mostre as opções que existem.
  - Abster-se: não há base aprovada. Diga isso e aponte quem pode resolver.
