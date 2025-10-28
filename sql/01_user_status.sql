-- ========================================
-- TABLA AUXILIAR: user_status
-- ========================================

CREATE TABLE IF NOT EXISTS user_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

-- Insert de valores base
INSERT INTO user_status (id, status_name)
VALUES
  (0, 'Inactivo'),
  (1, 'Activo'),
  (2, 'Suspendido'),
  (3, 'Desvinculado')
ON CONFLICT DO NOTHING;