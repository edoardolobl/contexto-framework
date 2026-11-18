-- Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
-- CONTEXTO: quais eventos do plano de mensuração pararam de coletar, por evento e operação.
-- Regra D+2: na consulta de 2026-11-17, só contam os dias completos até 2026-11-15.
-- Parte do plano (lab2_plano) e usa COALESCE: dia sem linha em lab2_eventos_diarios conta como zero.
-- Eventos inativos na operação (ativo = 0) saem com média nula e zero dias completos.
-- Resultado esperado: seis linhas, e add_to_cart no MX com 5 dias seguidos em zero.
WITH consulta AS (
  SELECT date('2026-11-17', '-2 days') AS ultimo_dia_completo
),
dias_completos AS (
  SELECT c.operation, c.event_date
  FROM lab2_carga AS c, consulta
  WHERE c.is_complete = 1
    AND c.event_date <= consulta.ultimo_dia_completo
),
contagem AS (
  SELECT p.event_name, p.operation, p.active, d.event_date,
         CASE WHEN d.event_date IS NULL THEN NULL
              ELSE COALESCE(e.event_count, 0) END AS n
  FROM lab2_plano AS p
  LEFT JOIN dias_completos AS d
    ON d.operation = p.operation AND d.event_date >= p.launch_date
  LEFT JOIN lab2_eventos_diarios AS e
    ON e.event_date = d.event_date
   AND e.operation = p.operation
   AND e.event_name = p.event_name
),
ultimo_disparo AS (
  SELECT event_name, operation,
         MAX(CASE WHEN n > 0 THEN event_date END) AS ultimo_dia
  FROM contagem
  GROUP BY event_name, operation
)
SELECT c.event_name,
       c.operation,
       c.active,
       ROUND(AVG(c.n), 1) AS avg_daily,
       COUNT(c.n) AS complete_days,
       COALESCE(SUM(c.n = 0), 0) AS zero_days,
       COALESCE(SUM(c.event_date IS NOT NULL
                    AND (u.ultimo_dia IS NULL OR c.event_date > u.ultimo_dia)), 0) AS current_zero_streak
FROM contagem AS c
JOIN ultimo_disparo AS u
  ON u.event_name = c.event_name AND u.operation = c.operation
GROUP BY c.event_name, c.operation, c.active
ORDER BY c.event_name, c.operation;
