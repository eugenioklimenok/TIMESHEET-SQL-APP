-- ========== ACCOUNTS ==========
INSERT INTO accounts (id, name, type) VALUES
  ('7a24d8d6-468a-4528-9b3c-4a428bcf4326', 'Canalt S.A.', 'Externo'),
  ('3a05f5a7-d820-463b-b909-7a9c7cefea59', 'Uso Interno', 'Interno');

-- ========== USERS ==========
INSERT INTO users (id, username, name, email, profile, role, status_id)
VALUES
  ('7cc7272a-8fb8-4c0a-b847-289923f96578', 'alex', 'Alex Zajarov', 'alex@app.com', 'Consultor', 'Admin', 1),
  ('9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'claudia', 'Claudia Becker', 'claudia@app.com', 'Funcional', 'User', 1);

-- ========== PROJECTS ==========
INSERT INTO projects (id, name, account_id, status_id, description)
VALUES
  ('1d1beda8-d885-4782-a316-c46fbc6d993b', 'Implementación CRM', '7a24d8d6-468a-4528-9b3c-4a428bcf4326', 1, 'Proyecto para cliente Canalt'),
  ('da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', 'App Interna Timesheet', '3a05f5a7-d820-463b-b909-7a9c7cefea59', 2, 'Uso interno de la herramienta');

-- ========== TIMESHEET HEADER ==========
INSERT INTO timesheet_header (id, user_id, project_id, work_date, status_id)
VALUES
  ('e33b11bb-d0fc-4338-8b79-efd394988251', '7cc7272a-8fb8-4c0a-b847-289923f96578', '1d1beda8-d885-4782-a316-c46fbc6d993b', '2025-10-29', 0),
  ('0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', '9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', '2025-10-29', 2);

-- ========== TIMESHEET ITEM ==========
INSERT INTO timesheet_item (id, header_id, description, hours, billable)
VALUES
  ('308e028c-1b94-415a-97ee-f7c98b8f7f3c', 'e33b11bb-d0fc-4338-8b79-efd394988251', 'Carga de artículos en CRM', 3.5, TRUE),
  ('0ef8614d-3afd-4c2a-b24c-99cad958cf19', '0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', 'Testing módulo de tiempos', 2.0, FALSE);