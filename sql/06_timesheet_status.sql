
-- 05_timesheet_status.sql
CREATE TABLE IF NOT EXISTS timesheet_status (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Inserts iniciales
INSERT INTO timesheet_status (id, name) VALUES
    (0, 'Draft'),
    (1, 'Submitted'),
    (2, 'Approved'),
    (3, 'Rejected'),
    (4, 'Billed')
ON CONFLICT DO NOTHING;
