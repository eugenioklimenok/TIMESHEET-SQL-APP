INSERT INTO timesheet_header (id, user_uuid, project_uuid, work_date, status_id) VALUES
  ('e33b11bb-d0fc-4338-8b79-efd394988251', '7cc7272a-8fb8-4c0a-b847-289923f96578', '1d1beda8-d885-4782-a316-c46fbc6d993b', '2025-10-29', 0),
  ('0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', '9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', '2025-10-29', 2)
ON CONFLICT DO NOTHING;
