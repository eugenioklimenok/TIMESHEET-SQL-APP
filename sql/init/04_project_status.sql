-- Tabla auxiliar: project_status
CREATE TABLE IF NOT EXISTS project_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL
);
