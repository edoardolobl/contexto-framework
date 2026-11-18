-- Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
-- CONTEXTO: implementa KPI-AURORA-002@1.0, receita de purchase por operação e dia. Dialeto: SQLite 3.
-- A receita mora no pedido: somar sempre em lab2_pedidos, sem JOIN com os itens (lab2_itens),
-- porque a junção repete cada pedido uma vez por item e infla o total.
-- Resultado esperado: BR em 2026-11-02 = 500 (e não 1100, como dá depois da junção).
SELECT
  operation,
  order_date,
  SUM(revenue) AS receita
FROM lab2_pedidos
GROUP BY operation, order_date
ORDER BY operation, order_date;
