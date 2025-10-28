-- Tabla auxiliar de estados de proyectos
CREATE TABLE IF NOT EXISTS project_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL
);

-- Estados posibles para proyectos
INSERT INTO project_status (id, status_name)
VALUES
    (1, 'Activo'),
    (2, 'En espera'),
    (3, 'Suspendido'),
    (4, 'Finalizado'),
    (5, 'Cancelado')
ON CONFLICT DO NOTHING;