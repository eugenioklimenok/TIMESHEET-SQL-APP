INSERT INTO user_status (id, status_name) VALUES
  (0, 'Inactive'),
  (1, 'Active'),
  (2, 'Suspended'),
  (3, 'Terminated')
ON CONFLICT DO NOTHING;
