# 0007. Tipo Perguntas de negócio

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 6

## Contexto

O tipo que reúne as perguntas que a IA vai receber tem vários nomes: "Perguntas de referência", "casos de teste" e outros (MOD-15, EDI-08). Ele fica no fim de um grupo recolhido do menu, embora devesse abrir o percurso (NAV-03). O banco de perguntas e o gabarito (as respostas certas) são hoje coisas separadas, e o gabarito fixa só a versão do indicador, não a dos outros documentos de que depende (AUR-10).

## Decisão

- O banco de perguntas e o gabarito viram um tipo só, chamado **Perguntas de negócio**.
- Slug (o trecho do endereço da página): `templates/perguntas-de-negocio`.
- O endereço antigo `templates/casos-teste` redireciona para o novo.
- O mesmo documento serve de ficha de entrada (a pergunta que o leitor escreve primeiro) e de gabarito.
- Os campos novos sugeridos na auditoria (`phrasings`, `onboarding`, `reference_sql`, `depends_on_versions`) e a chave `type` do tipo ficam em aberto até a F3.

## Alternativas consideradas

- **Manter "Perguntas de referência":** é um dos nomes que já causam confusão e não diz que a pergunta é do negócio.
- **"Pergunta de negócio", no singular** (proposta Pedagogia): o documento reúne várias perguntas, então o plural descreve melhor.
- **Manter banco de perguntas e gabarito separados:** dois documentos para o mesmo conjunto de perguntas, com risco de divergirem.

## Consequências

- **Positivas:** um nome em todo lugar; o percurso pode começar pela pergunta de negócio (I-05, I-09).
- **Negativas:** links externos antigos dependem do redirecionamento; páginas, componentes e validador precisam trocar o nome.
- **Fases afetadas:** F2 (tipo novo, redirecionamento, banco de perguntas exemplares do I-09); F3 (campos no schema 1.0).
- **Breaking:** a mudança de nome e de slug é visível. URLs antigas continuam funcionando pelo redirecionamento. Mudanças de campo entram com o schema 1.0.
