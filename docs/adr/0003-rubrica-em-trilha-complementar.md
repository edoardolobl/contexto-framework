# 0003. Rubrica em trilha complementar

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 2

## Contexto

A Rubrica aparece em lugares diferentes conforme o documento: README e ROADMAP a classificam como Dados, e o menu como Documentos do negócio (NAV-16, EDI-20). Com o foco em dados e mensuração ([0002](./0002-dados-e-mensuracao-como-trilho-principal.md)), ela não é um dos documentos que o leitor precisa para começar.

## Decisão

- A Rubrica sai do núcleo de tipos e vai para uma trilha complementar.
- O uso de referência dessa trilha é, por exemplo, avaliar respostas da IA.
- Como a trilha complementar aparece no menu fica em aberto, para o card sorting da F2 ([0010](./0010-validacao-com-pessoas.md)).

## Alternativas consideradas

- **Manter a Rubrica no núcleo:** ela ocuparia lugar na porta de entrada sem servir aos casos de analytics, e a classificação confusa continuaria.
- **Fundir a Rubrica com Decisão:** as duas comparam critérios, mas uma avalia trabalho já feito e a outra decide um caso. A fusão misturaria dois propósitos num tipo só.

## Consequências

- **Positivas:** o núcleo fica menor; a Rubrica ganha um uso claro (avaliar respostas da IA), ligado ao gabarito.
- **Negativas:** quem já usa a Rubrica para outros fins a encontra mais longe da entrada.
- **Fases afetadas:** F2 (menu e núcleo de entrada; I-05); F3 (a Rubrica ainda precisa do schema 1.0, mesmo fora do núcleo).
- **Breaking:** nenhum no formato. Mudança de URL, se houver, com redirecionamento.
