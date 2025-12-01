INSERT INTO timesheet_status (id, name) VALUES
  (0, 'Draft'),
  (1, 'Submitted'),
  (2, 'Approved'),
  (3, 'Rejected'),
  (4, 'Billed')
ON CONFLICT DO NOTHING;
