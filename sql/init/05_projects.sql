-- Tabla de proyectos vinculada a cuentas y estados
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id VARCHAR(25) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    account_uuid UUID REFERENCES accounts(id),
    status_id SMALLINT REFERENCES project_status(id) DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
