-- Laboratório Aurora: 6 sessões e 6 pedidos, para refazer as contas à mão.
-- Dialeto: SQLite 3. Uma sessão pode produzir muitos pedidos.
-- O exemplo está restrito a 2026-10-01, no canal WEB, sem tráfego interno.
PRAGMA foreign_keys = ON;

CREATE TABLE demo_sessions (
  session_id TEXT PRIMARY KEY,
  channel TEXT NOT NULL,
  is_internal INTEGER NOT NULL CHECK (is_internal IN (0, 1)),
  session_date TEXT NOT NULL
);

CREATE TABLE demo_orders (
  order_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES demo_sessions(session_id),
  status_code TEXT NOT NULL CHECK (status_code IN ('CONFIRMED', 'CANCELED', 'TEST'))
);

INSERT INTO demo_sessions (session_id, channel, is_internal, session_date) VALUES
 ('S1', 'web', 0, '2026-10-01'),
 ('S2', 'web', 0, '2026-10-01'),
 ('S3', 'web', 1, '2026-10-01'),
 ('S4', 'app', 0, '2026-10-01'),
 ('S5', 'web', 0, '2026-10-01'),
 ('S6', 'web', 0, '2026-10-01');

INSERT INTO demo_orders (order_id, session_id, status_code) VALUES
 ('O1', 'S1', 'CONFIRMED'),
 ('O2', 'S1', 'CONFIRMED'),
 ('O3', 'S2', 'CANCELED'),
 ('O4', 'S3', 'CONFIRMED'),
 ('O5', 'S4', 'CONFIRMED'),
 ('O6', 'S5', 'TEST');
