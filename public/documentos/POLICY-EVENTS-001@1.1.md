---
# Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
id: POLICY-EVENTS-001
schema_version: "1.1.0"
type: politica
title: "Despesas em eventos: Aurora"
version: "1.1"
revision_id: "POLICY-EVENTS-001@1.1" # versão específica; id = assunto estável
status: approved
owner: "Controladoria (Aurora)"
approver: "Diretoria Financeira (Aurora)"
valid_from: "2026-10-01"
valid_to: null               # fim exclusivo da vigência; null = sem fim documentado
version_date: "2026-10-01"
last_reviewed: "2026-10-01"
review_interval: null
source_of_truth: "POL-FIN-014, versão 3, publicada na intranet em Políticas > Finanças"
supersedes_revision: "POLICY-EVENTS-001@1.0"
superseded_by_revision: null
license: CC-BY-4.0
source_url: "https://edoardolobl.github.io/contexto-framework/documentos/POLICY-EVENTS-001@1.1.md"
intent:
  question: "Qual regra de despesas de evento está valendo na Aurora?"
  audience: ["Equipe de eventos", "Quem aprova despesas", Controladoria]
  purpose: "Dizer qual regra de despesas de evento está valendo e onde ela está escrita"
  decisions: ["Exigir ou não aprovação prévia de uma despesa de evento"]
plain_summary: "Vale a POL-FIN-014 versão 3: despesa de evento acima de R$ 500 precisa de aprovação prévia. E-mails e resumos não mudam a política."
open_questions: []
version_history:
  - version: "1.1"
    date: "2026-10-01"
    change: "Incluído o gatilho de revisão anual, a pedido da Diretoria Financeira"
    approved_by: "Diretoria Financeira (Aurora)"
  - version: "1.0"
    date: "2026-08-18"
    change: "Conflito entre fontes resolvido: a Controladoria confirmou a POL-FIN-014 versão 3 como fonte oficial. Registradas obrigações, permissões e exceção"
    approved_by: "Diretoria Financeira (Aurora)"
  - version: "0.1"
    date: "2026-08-11"
    change: "Primeiro rascunho, com três fontes em conflito e nenhuma autoridade confirmada"
    approved_by: null

context:
  instructions: null
  verifiedStatements: []
  constraints: []
authoritativeDefinitions: []

scope:
  audiences: ["Equipe de eventos da Aurora", "Quem aprova despesas"]
  activities: ["Registro e reembolso de despesas de evento"]
  localities: ["Todas as unidades da Aurora"]
  exclusions: ["Viagens sem relação com eventos, cobertas por outra política"]
# A política subjacente tem effective_date 01/07. A versão documental 1.1
# foi emitida e passou a vigorar em 01/10: são duas datas diferentes.
# Atenção: "version" no cabeçalho é a versão DESTE REGISTRO. A versão da política em si
# está em authority.version. São coisas diferentes e mudam em momentos diferentes.
authority:
  issuing_body: "Controladoria (Aurora)"
  approver_role: "Diretoria Financeira (Aurora)"
  version: "3"
  effective_date: "2026-07-01"
  expiry_date: null
  supersedes: "POL-FIN-014, versão 2: aprovação prévia acima de R$ 300, vigente até 30/06/2026"
obligations:
  - "Toda despesa precisa de comprovante fiscal anexado ao pedido de reembolso"
  - "Despesa de evento acima de R$ 500 por evento exige aprovação prévia da liderança da área"
permissions: ["Despesas até R$ 500 por evento podem ser reembolsadas sem aprovação prévia"]
prohibitions: ["Não reembolsar despesa sem comprovante fiscal"]
exceptions:
  - condition: "Evento contratado em emergência, sem tempo para aprovação prévia"
    approval_role: "Diretoria Financeira (Aurora)"
    evidence_needed: "Justificativa escrita em até 5 dias úteis após o evento"
conflicting_sources:
  - id: CONFLICT-001
    sources: [POL-FIN-014, E-MAIL-EVENTOS, INTRANET-EVENTOS]
    description: "Três limites diferentes para aprovação prévia de despesa de evento"
    positions:
      - source: "POL-FIN-014 versão 3, em Políticas > Finanças, com vigência desde 01/07/2026"
        says: "Aprovação prévia para despesa de evento acima de R$ 500"
      - source: "E-mail da equipe de eventos, 03/08/2026"
        says: "Aprovação prévia só acima de R$ 1.000"
      - source: "Resumo na intranet, atualizado em 15/03/2026"
        says: "Aprovação prévia acima de R$ 300"
    impact: "Uma despesa de R$ 800 precisa ou não de aprovação prévia, conforme a fonte consultada"
    state: resolved
    resolution: "Vale a POL-FIN-014 versão 3: R$ 500. O e-mail era um comunicado sem força de política e não mudou o limite. O resumo da intranet repetia a versão 2 (R$ 300, vigente até 30/06/2026) e foi corrigido em 14/08."
    resolution_owner: "Controladoria (Aurora)"
    resolved_at: "2026-08-14"
source_precedence_rule: "A política publicada em Políticas > Finanças prevalece sobre e-mails, resumos e apresentações. Comunicados não alteram a política."
how_to_verify: "Conferir o número da versão e a data de vigência no cabeçalho da POL-FIN-014"
review_trigger: "Revisão anual em julho, ou antes se a POL-FIN-014 ganhar nova versão"

related_documents: []
---

# Despesas em eventos: Aurora (POLICY-EVENTS-001@1.1)

> **Estado:** Aprovado
>
> **Vigência:** de 01/10/2026, sem fim previsto
>
> **Licença:** CC-BY-4.0
>
> **Endereço:** https://edoardolobl.github.io/contexto-framework/documentos/POLICY-EVENTS-001@1.1.md

## Pergunta que este documento responde (POLICY-EVENTS-001@1.1, de 01/10/2026, sem fim previsto)

Qual regra de despesas de evento está valendo na Aurora?

## Em poucas palavras (POLICY-EVENTS-001@1.1, de 01/10/2026, sem fim previsto)

Vale a POL-FIN-014 versão 3: despesa de evento acima de R$ 500 precisa de aprovação prévia. E-mails e resumos não mudam a política.

## Comentário (POLICY-EVENTS-001@1.1, de 01/10/2026, sem fim previsto)

O conflito foi resolvido por quem tem autoridade: vale a política publicada, e o e-mail era só um comunicado. A resolução fica registrada com a data e com quem resolveu.

O que observar: há duas versões diferentes neste documento. `version` é a versão deste registro; `authority.version` é a versão da própria política. Elas mudam em momentos diferentes.
