DROP TABLE IF EXISTS user_status CASCADE;


CREATE TABLE IF NOT EXISTS user_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO user_status (id, status_name) VALUES
  (0, 'Inactive'),
  (1, 'Active'),
  (2, 'Suspended'),
  (3, 'Terminated')
ON CONFLICT DO NOTHING;
