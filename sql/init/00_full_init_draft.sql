-- Script integral de referencia: crea estructura completa y datos mínimos
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 01 USER STATUS
CREATE TABLE IF NOT EXISTS user_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO user_status (id, status_name) VALUES
  (0, 'Inactive'),
  (1, 'Active'),
  (2, 'Suspended'),
  (3, 'Terminated')
ON CONFLICT DO NOTHING;

-- 02 USERS
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(25) NOT NULL UNIQUE,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    profile VARCHAR(50),
    role VARCHAR(50),
    status_id SMALLINT DEFAULT 1 REFERENCES user_status(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (id, user_id, name, email, profile, role, status_id) VALUES
  ('7cc7272a-8fb8-4c0a-b847-289923f96578', 'Azajarov', 'Alex Zajarov', 'mundoerp.latam@gmail.com', 'Consultant', 'Admin', 1),
  ('9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'Eklimenok', 'Eugenio Klimenok', 'eugenioklimenok@gmail.com', 'Functional', 'User', 1)
ON CONFLICT DO NOTHING;

-- 03 ACCOUNTS
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id VARCHAR(25) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounts (id, account_id, name, type) VALUES
  ('7a24d8d6-468a-4528-9b3c-4a428bcf4326', 'CL011120251', 'Canalt S.A.', 'External'),
  ('3a05f5a7-d820-463b-b909-7a9c7cefea59', 'CL011120252', 'Internal Use', 'Internal')
ON CONFLICT DO NOTHING;

-- 04 PROJECT STATUS
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

-- 05 PROJECTS
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id VARCHAR(25) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    account_uuid UUID REFERENCES accounts(id),
    status_id SMALLINT REFERENCES project_status(id) DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO projects (id, project_id, name, account_uuid, status_id, description) VALUES
  ('1d1beda8-d885-4782-a316-c46fbc6d993b', 'PROY01112025A1', 'CRM Implementation', '7a24d8d6-468a-4528-9b3c-4a428bcf4326', 1, 'Project for client Canalt'),
  ('da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', 'PROY01112025A2', 'Internal Timesheet App', '3a05f5a7-d820-463b-b909-7a9c7cefea59', 2, 'Internal use of the timesheet tool')
ON CONFLICT DO NOTHING;

-- 06 TIMESHEET STATUS
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

-- 07 TIMESHEET HEADER
CREATE TABLE IF NOT EXISTS timesheet_header (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_uuid UUID NOT NULL REFERENCES users(id),
    project_uuid UUID NOT NULL REFERENCES projects(id),
    work_date DATE NOT NULL,
    status_id SMALLINT NOT NULL DEFAULT 0 REFERENCES timesheet_status(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO timesheet_header (id, user_uuid, project_uuid, work_date, status_id) VALUES
  ('e33b11bb-d0fc-4338-8b79-efd394988251', '7cc7272a-8fb8-4c0a-b847-289923f96578', '1d1beda8-d885-4782-a316-c46fbc6d993b', '2025-10-29', 0),
  ('0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', '9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', '2025-10-29', 2)
ON CONFLICT DO NOTHING;

-- 08 TIMESHEET ITEM
CREATE TABLE IF NOT EXISTS timesheet_item (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    header_uuid UUID NOT NULL REFERENCES timesheet_header(id),
    description TEXT NOT NULL,
    hours NUMERIC(5,2) NOT NULL CHECK (hours >= 0),
    billable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO timesheet_item (id, header_uuid, description, hours, billable) VALUES
  ('308e028c-1b94-415a-97ee-f7c98b8f7f3c', 'e33b11bb-d0fc-4338-8b79-efd394988251', 'CRM item setup', 3.5, TRUE),
  ('0ef8614d-3afd-4c2a-b24c-99cad958cf19', '0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', 'Testing timesheet module', 2.0, FALSE)
ON CONFLICT DO NOTHING;
