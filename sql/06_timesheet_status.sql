
-- 05_timesheet_status.sql
CREATE TABLE IF NOT EXISTS timesheet_status (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Inserts iniciales
INSERT INTO timesheet_status (id, name) VALUES
    (0, 'Borrador'),
    (1, 'Enviado'),
    (2, 'Aprobado'),
    (3, 'Rechazado'),
    (4, 'Facturado')
ON CONFLICT DO NOTHING;
