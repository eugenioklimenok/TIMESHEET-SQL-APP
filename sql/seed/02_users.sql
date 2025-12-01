INSERT INTO users (id, user_id, name, email, profile, role, status_id) VALUES
  ('7cc7272a-8fb8-4c0a-b847-289923f96578', 'Azajarov', 'Alex Zajarov', 'mundoerp.latam@gmail.com', 'Consultant', 'Admin', 1),
  ('9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'Eklimenok', 'Eugenio Klimenok', 'eugenioklimenok@gmail.com', 'Functional', 'User', 1)
ON CONFLICT DO NOTHING;
