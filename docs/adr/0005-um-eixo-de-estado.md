# 0005. Um eixo só de estado do documento

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 4

## Contexto

Hoje o contrato editorial aceita quatro estados no campo `status`: `draft`, `pending_approval`, `approved` e `deprecated`. Os exemplos com lacunas usam `pending_approval` onde a página "Como ler os campos" descreve o rascunho como `draft`, e as cópias históricas que não valem mais seguem com `approved`, embora `deprecated` exista para isso (AUR-09). Também não há como dizer que uma versão foi substituída por outra (MET-08). A proposta Governança sugeria dois eixos separados, um para aprovação e outro para ciclo de vida; a Pedagogia, um eixo só.

## Decisão

- O campo `status` tem um eixo só, com cinco valores: `draft`, `pending_approval`, `approved`, `superseded` e `deprecated`.
- `superseded` é o valor novo, para a versão cujo lugar foi tomado por outra.
- A fronteira exata entre `superseded` e `deprecated` e o rótulo em português de `superseded` ficam em aberto e vão para a seção "Estados" do contrato editorial.

## Alternativas consideradas

- **Dois eixos, aprovação e ciclo de vida** (proposta Governança, por exemplo `approval_status` e `lifecycle`): mais preciso, mas dobra o que o leitor não técnico precisa entender e combinar.
- **Manter os quatro estados atuais:** não distingue a versão substituída da que deixou de valer.

## Consequências

- **Positivas:** um campo, uma lista curta, fácil de explicar e de validar.
- **Negativas:** alguns casos raros (um documento aprovado que já tem data para deixar de valer) ficam sem estado próprio e dependem de `valid_to`.
- **Fases afetadas:** F0 (vocabulário e validador); F1 (estados dos exemplos corrigidos, AUR-09); F3 (lista de valores no schema 1.0).
- **Breaking:** acrescentar `superseded` não quebra nada, porque nenhum documento atual o usa. O que pode quebrar é reclassificar cópias históricas (por exemplo, de `approved` para `superseded` ou `deprecated`), porque quem lê o campo passa a ver outro estado. A reclassificação entra com o schema 1.0 ([0009](./0009-versao-do-produto-separada-do-schema.md)).
