-- Exemplo do Contexto. A Aurora é uma organização inventada; nomes, datas e aprovações fazem parte do caso.
-- Laboratório Aurora: 6 sessões e 6 pedidos, para refazer as contas à mão.
-- Dialeto: SQLite 3. Uma sessão pode produzir muitos pedidos.
-- Nomes no BigQuery: sessoes_web é aurora-analytics.web.sessoes_web; pedidos é aurora-analytics.vendas.pedidos.
-- O indicador usa só 01/10, canal web, sem sessões internas; S3 (interna) e S4 (app) estão na amostra para mostrar os filtros.
PRAGMA foreign_keys = ON;

CREATE TABLE sessoes_web (
  session_id TEXT PRIMARY KEY,
  channel TEXT NOT NULL,
  is_internal INTEGER NOT NULL CHECK (is_internal IN (0, 1)),
  session_date TEXT NOT NULL
);

CREATE TABLE pedidos (
  order_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessoes_web(session_id),
  status_code TEXT NOT NULL CHECK (status_code IN ('CONFIRMED', 'CANCELED', 'TEST'))
);

INSERT INTO sessoes_web (session_id, channel, is_internal, session_date) VALUES
 ('S1', 'web', 0, '2026-10-01'),
 ('S2', 'web', 0, '2026-10-01'),
 ('S3', 'web', 1, '2026-10-01'),
 ('S4', 'app', 0, '2026-10-01'),
 ('S5', 'web', 0, '2026-10-01'),
 ('S6', 'web', 0, '2026-10-01');

INSERT INTO pedidos (order_id, session_id, status_code) VALUES
 ('O1', 'S1', 'CONFIRMED'),
 ('O2', 'S1', 'CONFIRMED'),
 ('O3', 'S2', 'CANCELED'),
 ('O4', 'S3', 'CONFIRMED'),
 ('O5', 'S4', 'CONFIRMED'),
 ('O6', 'S5', 'TEST');
