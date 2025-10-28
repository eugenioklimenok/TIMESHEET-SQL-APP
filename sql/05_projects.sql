-- Tabla de proyectos vinculada a cuentas y estados
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    account_id UUID REFERENCES accounts(id),
    status_id SMALLINT REFERENCES project_status(id) DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ⚠️ Los siguientes inserts requieren UUIDs reales de cuentas existentes
-- INSERT INTO projects (name, account_id, status_id, description)
-- VALUES
--   ('Implementación CRM', 'UUID_ACME', 1, 'Proyecto para cliente Acme'),
--   ('App Interna Timesheet', 'UUID_INTERNO', 2, 'Desarrollo de app interna');