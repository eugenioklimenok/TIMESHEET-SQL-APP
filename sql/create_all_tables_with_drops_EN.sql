
-- ===========================================================
-- 🧭 CONVENCIÓN DE NOMBRES (NAMING) – UUID + CÓDIGOS LEIBLES
-- ===========================================================
-- Esta tabla sigue el estándar moderno de naming del proyecto:
-- 
-- ▸ 'id'             → UUID como clave primaria (PK técnica)
-- ▸ '*_id'           → Código legible para humanos (ej. 'user_id' = 'Eklimenok')
-- ▸ '*_uuid'         → Clave foránea (FK) que apunta a la PK de otra tabla (UUID)
-- 
-- Ejemplo: 
--    user_uuid → FK hacia users.id (UUID técnico)
--    user_id   → Código legible que ve el usuario final o API
--
-- No se usan nombres como 'username', 'account_name', etc.
-- No se recomienda usar 'fk_user_id' o similares.
-- 
-- Objetivo: Que el diseño sea autoexplicativo, moderno y fácil de mantener.
-- ===========================================================


-- ========================================
-- EXTENSIONS
-- ========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- ========================================
-- 01 USER STATUS
-- ========================================
DROP TABLE IF EXISTS user_status CASCADE;

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

-- ========================================
-- 02 USERS
-- ========================================
DROP TABLE IF EXISTS users CASCADE;

-- ========================================
-- TABLA PRINCIPAL: users
-- ========================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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

-- Insert de usuarios de prueba
INSERT INTO users (username, name, email)
VALUES 
  ('admin', 'Administrador General', 'admin@app.com'),
  ('alex', 'Alex Zajarov', 'alex@app.com');

-- ========================================
-- 03 ACCOUNTS
-- ========================================
DROP TABLE IF EXISTS accounts CASCADE;

-- 01_accounts.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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

-- ========================================
-- 04 PROJECT STATUS
-- ========================================
DROP TABLE IF EXISTS project_status CASCADE;

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

-- ========================================
-- 05 PROJECTS
-- ========================================
DROP TABLE IF EXISTS projects CASCADE;

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

-- ========================================
-- 06 TIMESHEET STATUS
-- ========================================
DROP TABLE IF EXISTS timesheet_status CASCADE;

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

-- ========================================
-- 07 TIMESHEET HEADER
-- ========================================
DROP TABLE IF EXISTS timesheet_header CASCADE;

-- 06_timesheet_header.sql
CREATE TABLE IF NOT EXISTS timesheet_header (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    project_id UUID NOT NULL REFERENCES projects(id),
    work_date DATE NOT NULL,
    status_id SMALLINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 08 TIMESHEET ITEM
-- ========================================
DROP TABLE IF EXISTS timesheet_item CASCADE;

-- 07_timesheet_item.sql
CREATE TABLE IF NOT EXISTS timesheet_item (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    header_id UUID NOT NULL REFERENCES timesheet_header(id),
    description TEXT NOT NULL,
    hours NUMERIC(5,2) NOT NULL CHECK (hours >= 0),
    billable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- SAMPLE DATA
-- ========================================
-- ========== ACCOUNTS ==========
INSERT INTO accounts (id, name, type) VALUES
  ('7a24d8d6-468a-4528-9b3c-4a428bcf4326', 'Canalt S.A.', 'Externo'),
  ('3a05f5a7-d820-463b-b909-7a9c7cefea59', 'Uso Interno', 'Interno');

-- ========== USERS ==========
INSERT INTO users (id, username, name, email, profile, role, status_id)
VALUES
  ('7cc7272a-8fb8-4c0a-b847-289923f96578', 'alex', 'Alex Zajarov', 'alex@app.com', 'Consultor', 'Admin', 1),
  ('9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'claudia', 'Claudia Becker', 'claudia@app.com', 'Funcional', 'User', 1);

-- ========== PROJECTS ==========
INSERT INTO projects (id, name, account_id, status_id, description)
VALUES
  ('1d1beda8-d885-4782-a316-c46fbc6d993b', 'Implementación CRM', '7a24d8d6-468a-4528-9b3c-4a428bcf4326', 1, 'Proyecto para cliente Canalt'),
  ('da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', 'App Interna Timesheet', '3a05f5a7-d820-463b-b909-7a9c7cefea59', 2, 'Uso interno de la herramienta');

-- ========== TIMESHEET HEADER ==========
INSERT INTO timesheet_header (id, user_id, project_id, work_date, status_id)
VALUES
  ('e33b11bb-d0fc-4338-8b79-efd394988251', '7cc7272a-8fb8-4c0a-b847-289923f96578', '1d1beda8-d885-4782-a316-c46fbc6d993b', '2025-10-29', 0),
  ('0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', '9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', '2025-10-29', 2);

-- ========== TIMESHEET ITEM ==========
INSERT INTO timesheet_item (id, header_id, description, hours, billable)
VALUES
  ('308e028c-1b94-415a-97ee-f7c98b8f7f3c', 'e33b11bb-d0fc-4338-8b79-efd394988251', 'Carga de artículos en CRM', 3.5, TRUE),
  ('0ef8614d-3afd-4c2a-b24c-99cad958cf19', '0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', 'Testing módulo de tiempos', 2.0, FALSE);
