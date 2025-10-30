
-- ========================================
-- EXTENSIONES
-- ========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- TABLAS AUXILIARES
-- ========================================

-- Estados de usuario
CREATE TABLE IF NOT EXISTS user_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO user_status (id, status_name)
VALUES
  (0, 'Inactivo'),
  (1, 'Activo'),
  (2, 'Suspendido'),
  (3, 'Desvinculado')
ON CONFLICT DO NOTHING;

-- Estados de proyecto
CREATE TABLE IF NOT EXISTS project_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL
);

INSERT INTO project_status (id, status_name)
VALUES
    (1, 'Activo'),
    (2, 'En espera'),
    (3, 'Suspendido'),
    (4, 'Finalizado'),
    (5, 'Cancelado')
ON CONFLICT DO NOTHING;

-- Estados de timesheet
CREATE TABLE IF NOT EXISTS timesheet_status (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

INSERT INTO timesheet_status (id, name) VALUES
    (0, 'Draft'),
    (1, 'Submitted'),
    (2, 'Approved'),
    (3, 'Rejected'),
    (4, 'Billed')
ON CONFLICT DO NOTHING;

-- ========================================
-- TABLAS PRINCIPALES
-- ========================================

-- Usuarios
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    profile VARCHAR(50),
    role VARCHAR(50),
    status_id SMALLINT DEFAULT 1 REFERENCES user_status(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, name, email)
VALUES 
  ('admin', 'Administrador General', 'admin@app.com'),
  ('alex', 'Alex Zajarov', 'alex@app.com');

-- Cuentas / Clientes
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(150) NOT NULL,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounts (name, type) VALUES
    ('Cliente A', 'Externo'),
    ('Cliente B', 'Externo'),
    ('Uso Interno', 'Interno');

-- Proyectos
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    account_id UUID REFERENCES accounts(id),
    status_id SMALLINT REFERENCES project_status(id) DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- PARTE HORARIO: CABECERA + ÍTEMS
-- ========================================

-- Cabecera
CREATE TABLE IF NOT EXISTS timesheet_header (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    project_id UUID NOT NULL REFERENCES projects(id),
    work_date DATE NOT NULL,
    status_id SMALLINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ítems
CREATE TABLE IF NOT EXISTS timesheet_item (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    header_id UUID NOT NULL REFERENCES timesheet_header(id),
    description TEXT NOT NULL,
    hours NUMERIC(5,2) NOT NULL CHECK (hours >= 0),
    billable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
