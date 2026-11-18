# 0013. Núcleo de entrada com cinco tipos

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 12; [12-incorporacoes.md](../../auditoria/12-incorporacoes.md), I-05

## Contexto

O portal oferece dez tipos de modelo lado a lado, sem dizer por onde começar (NAV-03, NAV-04). Com o foco em dados e mensuração ([0002](./0002-dados-e-mensuracao-como-trilho-principal.md)), as três pesquisas externas do mantenedor convergiram num conjunto menor de tipos para a porta de entrada (I-05). Esta é uma decisão nova, que não estava entre as perguntas da auditoria.

## Decisão

- **Porta de entrada, cinco tipos:** Indicador, Dataset com relacionamentos, Evento de coleta, Regra e decisão (inclui detecção de anomalia) e Perguntas de negócio.
- **Segundo nível:** Conceito, Política, Processo e Dashboard.
- **Trilha complementar:** Rubrica ([0003](./0003-rubrica-em-trilha-complementar.md)).
- Como os tipos atuais Dataset e Relacionamento se juntam em "Dataset com relacionamentos", e Decisão vira "Regra e decisão", fica em aberto até a F3.
  - **Fechado em 2026-11-17 pelo [ADR 0030](./0030-decisoes-do-mantenedor-depois-das-fases.md):** os tipos ficam separados. Dataset, Relacionamento e Decisão continuam como modelos próprios, sem fusão.

## Alternativas consideradas

- **Os dez tipos no mesmo nível, como hoje:** o leitor não sabe por onde começar.
- **Núcleo com mais tipos, incluindo Conceito e Política** (levantada na redação do ADR): afasta a entrada do caso de analytics, que é o trilho principal.
- **Um tipo de entrada só (Perguntas de negócio)** (levantada na redação do ADR): deixaria Indicador e Evento de coleta, que cobrem os casos reais, um nível abaixo.

## Consequências

- **Positivas:** a entrada fica curta e ligada aos casos reais; o menu ganha uma hierarquia clara.
- **Negativas:** Evento de coleta ainda não existe e precisa ser criado; fusões de tipos mudam nomes e endereços.
- **Fases afetadas:** F2 (menu e home, I-05, I-06); F3 (schemas dos tipos fundidos); F4 (Evento de coleta e Regra e decisão com detecção de anomalia, I-18 a I-20).
- **Breaking:** a fusão de tipos muda a chave `type` e os campos de quem já usa Dataset, Relacionamento ou Decisão. Entra com o schema 1.0, com redirecionamentos e tabela de migração.
