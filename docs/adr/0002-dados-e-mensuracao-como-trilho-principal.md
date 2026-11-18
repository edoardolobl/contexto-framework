# 0002. Dados e mensuração como trilho principal

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 1

## Contexto

Cinco dos dez tipos de modelo usam exemplos fora de dados e analytics (MOD-22). Os casos reais que motivaram o projeto (evento raro tratado como quebrado, indicador calculado com a definição genérica) não têm caminho no portal: uma busca por "GA4", "GTM" e "tag plan" não achou nada (NAV-01, EDI-31). Era preciso escolher se o produto prioriza dados e mensuração ou se mantém os dois trilhos com o mesmo peso.

## Decisão

- Dados e mensuração são o trilho principal do Contexto.
- Conceito, Política, Processo e Decisão continuam, mas como apoio aos casos de analytics: seus exemplos passam a se ligar a esse universo.
- Quais tipos ficam na porta de entrada está em [0013](./0013-nucleo-de-entrada-com-cinco-tipos.md). O destino da Rubrica está em [0003](./0003-rubrica-em-trilha-complementar.md).

## Alternativas consideradas

- **Dois trilhos com peso igual** (dados e documentos de negócio): mantém a dispersão atual (MOD-22) e não resolve a falta de caminho para quem trabalha com eventos e indicadores (NAV-01).
- **Tirar Conceito, Política, Processo e Decisão do produto** (levantada na redação do ADR): perderia tipos que os casos de analytics usam, como a política que define uma exceção ou o conceito com `not_synonyms`.

## Consequências

- **Positivas:** o portal fala com o público que trouxe os casos reais; exemplos e laboratórios ganham um fio único.
- **Negativas:** quem chegou ao Contexto por Política ou Processo encontra esses tipos em segundo plano. Os exemplos desses tipos precisam ser reescritos.
- **Fases afetadas:** F2 (porta de entrada e menu), F4 (Evento de coleta, Lab 2 Aurora; I-18 a I-23), F5 (moldes ligados a analytics, AUR-02 e MOD-22).
- **Breaking:** nenhum no formato dos modelos. Pode haver mudança de URL no menu, tratada com redirecionamento (o servidor leva o endereço antigo ao novo).
