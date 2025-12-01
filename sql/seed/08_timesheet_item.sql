INSERT INTO timesheet_item (id, header_uuid, description, hours, billable) VALUES
  ('308e028c-1b94-415a-97ee-f7c98b8f7f3c', 'e33b11bb-d0fc-4338-8b79-efd394988251', 'CRM item setup', 3.5, TRUE),
  ('0ef8614d-3afd-4c2a-b24c-99cad958cf19', '0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', 'Testing timesheet module', 2.0, FALSE)
ON CONFLICT DO NOTHING;
