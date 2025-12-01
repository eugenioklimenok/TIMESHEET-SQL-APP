INSERT INTO projects (id, project_id, name, account_uuid, status_id, description) VALUES
  ('1d1beda8-d885-4782-a316-c46fbc6d993b', 'PROY01112025A1', 'CRM Implementation', '7a24d8d6-468a-4528-9b3c-4a428bcf4326', 1, 'Project for client Canalt'),
  ('da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', 'PROY01112025A2', 'Internal Timesheet App', '3a05f5a7-d820-463b-b909-7a9c7cefea59', 2, 'Internal use of the timesheet tool')
ON CONFLICT DO NOTHING;
