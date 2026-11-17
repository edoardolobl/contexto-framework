-- CONTEXTO: taxa de sessões web convertidas na amostra Aurora.
-- Definição da Aurora (KPI-AURORA-001, versão 2.0); não equivale ao indicador de outra empresa.
-- Denominador: sessões web não internas em 2026-10-01.
-- Numerador: sessões elegíveis com pelo menos um pedido confirmado.
-- Resultado esperado: 25.0.
WITH eligible_sessions AS (
  SELECT session_id FROM demo_sessions
  WHERE channel = 'web'
    AND is_internal = 0
    AND session_date = '2026-10-01'
),
converted_sessions AS (
  SELECT DISTINCT o.session_id
  FROM demo_orders AS o
  JOIN eligible_sessions AS s
    ON s.session_id = o.session_id
  WHERE o.status_code = 'CONFIRMED'
)
SELECT ROUND(
  100.0 * (SELECT COUNT(*) FROM converted_sessions)
  / NULLIF((SELECT COUNT(*) FROM eligible_sessions), 0),
  2
) AS converted_session_rate;
