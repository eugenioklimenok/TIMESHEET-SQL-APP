DROP TABLE IF EXISTS project_status CASCADE;


CREATE TABLE IF NOT EXISTS project_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL
);

INSERT INTO project_status (id, status_name) VALUES
  (1, 'Active'),
  (2, 'On Hold'),
  (3, 'Suspended'),
  (4, 'Completed'),
  (5, 'Cancelled')
ON CONFLICT DO NOTHING;
