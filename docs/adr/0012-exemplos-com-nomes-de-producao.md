# 0012. Exemplos com nomes plausíveis de produção

- **Estado:** Aceito
- **Data:** 2026-11-17
- **Decisão:** do mantenedor em 2026-11-17 (auditoria/11-decisoes.md); texto aprovado pelo mantenedor em 2026-11-17
- **Decidido por:** mantenedor (texto redigido pela auditoria)
- **Origem:** [11-decisoes.md](../../auditoria/11-decisoes.md), decisão 11

## Contexto

Os exemplos da Aurora usam nomes genéricos, que não se parecem com o que o leitor vê no trabalho (AUR-02, MOD-09). Os arquivos .sql de exemplo não trazem o aviso de que a Aurora é inventada, e outras páginas repetem o aviso fora dos lugares previstos (AUR-21). O contrato editorial hoje limita o aviso a três lugares: a home, a seção de autoria e a primeira linha de cada YAML de exemplo.

## Decisão

- Os exemplos usam nomes plausíveis de produção: projeto BigQuery, catálogo Databricks, propriedade GA4, contêiner GTM, operações BR e MX e eventos GA4 reais.
- Todo arquivo de exemplo baixável traz o aviso de ficção, em qualquer formato, inclusive .sql.
- A organização continua sendo a Aurora.
- A lista exata de nomes e o texto do aviso em cada formato ficam em aberto.

## Alternativas consideradas

- **Manter nomes genéricos:** mais seguro contra cópia por engano, mas não ensina como o documento fica no ambiente real.
- **Aviso só no YAML, como hoje:** o .sql circula sozinho, sem o site e sem o YAML ao lado.

## Consequências

- **Positivas:** o leitor reconhece o próprio ambiente nos exemplos; os casos reais (eventos GA4, operações por país) cabem no Lab 2.
- **Negativas:** aumenta o risco de alguém copiar um nome inventado achando que é real. O aviso em todos os formatos reduz, sem eliminar.
- **Fases afetadas:** F1 (aviso nos .sql); F4 (Lab 2 Aurora com 2 operações e eventos GA4, I-22); F5 (valores com cara de produção nos moldes). A seção "O aviso de que a Aurora é inventada" do contrato muda antes.
- **Breaking:** nenhum no formato. Os nomes dentro dos exemplos mudam.
