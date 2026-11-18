# 0010. Validação com pessoas

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 9

## Contexto

A eficácia do método nunca foi testada com pessoas, e o plano de validação está parado (MET-16). O roteiro usa dois testes como critério de saída: o da F2 (menu) e o portão da v1.0 (piloto na F7). Sem acesso a pessoas do público misto, as duas fases ficariam sem como terminar.

## Decisão

- O mantenedor tem acesso a **15 pessoas ou mais** para card sorting (as pessoas agrupam os temas como esperam encontrá-los) e tree test (elas tentam achar páginas num menu sem visual).
- E a **2 ou 3 pessoas** para o piloto, que reproduz os casos reais antes e depois de usar o Contexto.
- Quem são as pessoas, como são recrutadas e como os dados delas são tratados fica em aberto.

## Alternativas consideradas

- **Sem acesso a pessoas:** F2 e o portão da v1.0 ficariam sem critério de saída, e o roteiro precisaria de outro tipo de prova, mais fraca.
- **Só revisão por especialistas, sem o público** (levantada na redação do ADR): não mede se o leitor não técnico acha o caminho nem se aprende.

## Consequências

- **Positivas:** os critérios de saída da F2 e da F7 são viáveis. A v1.0 sai com prova própria, citável.
- **Negativas:** recrutar, agendar e registrar testes custa tempo do mantenedor. Testes com pessoas pedem cuidado com dados pessoais.
- **Fases afetadas:** F2 (card sorting com 15 pessoas ou mais e tree test com 5 a 8 tarefas, com pelo menos 80% de sucesso no percurso); F7 (piloto). O I-10 acrescenta rodadas de 5 a 8 pessoas que medem aprendizagem, não satisfação.
- **Breaking:** nenhum.
