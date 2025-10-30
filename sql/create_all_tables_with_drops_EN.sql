
-- ========================================
-- EXTENSIONS
-- ========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- DROP TABLES (IF EXISTS)
-- ========================================
DROP TABLE IF EXISTS timesheet_item CASCADE;
DROP TABLE IF EXISTS timesheet_header CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS timesheet_status CASCADE;
DROP TABLE IF EXISTS project_status CASCADE;
DROP TABLE IF EXISTS user_status CASCADE;

-- ========================================
-- LOOKUP TABLES (AUXILIARIES)
-- ========================================

CREATE TABLE IF NOT EXISTS user_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO user_status (id, status_name)
VALUES
  (0, 'Inactive'),
  (1, 'Active'),
  (2, 'Suspended'),
  (3, 'Terminated')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS project_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL
);

INSERT INTO project_status (id, status_name)
VALUES
    (1, 'Active'),
    (2, 'On Hold'),
    (3, 'Suspended'),
    (4, 'Completed'),
    (5, 'Cancelled')
ON CONFLICT DO NOTHING;

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
-- MAIN TABLES
-- ========================================

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

CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(150) NOT NULL,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    account_id UUID REFERENCES accounts(id),
    status_id SMALLINT REFERENCES project_status(id) DEFAULT 1,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS timesheet_header (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    project_id UUID NOT NULL REFERENCES projects(id),
    work_date DATE NOT NULL,
    status_id SMALLINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS timesheet_item (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    header_id UUID NOT NULL REFERENCES timesheet_header(id),
    description TEXT NOT NULL,
    hours NUMERIC(5,2) NOT NULL CHECK (hours >= 0),
    billable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- SAMPLE DATA (NO DUPLICATES)
-- ========================================

-- ACCOUNTS
INSERT INTO accounts (id, name, type) VALUES
  ('7a24d8d6-468a-4528-9b3c-4a428bcf4326', 'Canalt S.A.', 'External'),
  ('3a05f5a7-d820-463b-b909-7a9c7cefea59', 'Internal Use', 'Internal');

-- USERS
INSERT INTO users (id, username, name, email, profile, role, status_id)
VALUES
  ('7cc7272a-8fb8-4c0a-b847-289923f96578', 'euge', 'Alex Zajarov', 'alex@app.com', 'Consultant', 'Admin', 1),
  ('9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'claudia', 'Claudia Becker', 'claudia@app.com', 'Functional', 'User', 1);

-- PROJECTS
INSERT INTO projects (id, name, account_id, status_id, description)
VALUES
  ('1d1beda8-d885-4782-a316-c46fbc6d993b', 'CRM Implementation', '7a24d8d6-468a-4528-9b3c-4a428bcf4326', 1, 'Project for client Canalt'),
  ('da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', 'Internal Timesheet App', '3a05f5a7-d820-463b-b909-7a9c7cefea59', 2, 'Internal use of the timesheet tool');

-- TIMESHEET HEADERS
INSERT INTO timesheet_header (id, user_id, project_id, work_date, status_id)
VALUES
  ('e33b11bb-d0fc-4338-8b79-efd394988251', '7cc7272a-8fb8-4c0a-b847-289923f96578', '1d1beda8-d885-4782-a316-c46fbc6d993b', '2025-10-29', 0),
  ('0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', '9a2bb080-4da2-46ab-b0a8-ba651bca175b', 'da59f1d2-ec45-4ab9-beb0-8cc8b37fc71f', '2025-10-29', 2);

-- TIMESHEET ITEMS
INSERT INTO timesheet_item (id, header_id, description, hours, billable)
VALUES
  ('308e028c-1b94-415a-97ee-f7c98b8f7f3c', 'e33b11bb-d0fc-4338-8b79-efd394988251', 'CRM item setup', 3.5, TRUE),
  ('0ef8614d-3afd-4c2a-b24c-99cad958cf19', '0a5cf9dd-fa81-440d-9765-cde82d5d6b4a', 'Testing timesheet module', 2.0, FALSE);
