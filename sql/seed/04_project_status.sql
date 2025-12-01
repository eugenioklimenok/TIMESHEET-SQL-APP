INSERT INTO project_status (id, status_name) VALUES
  (1, 'Active'),
  (2, 'On Hold'),
  (3, 'Suspended'),
  (4, 'Completed'),
  (5, 'Cancelled')
ON CONFLICT DO NOTHING;
