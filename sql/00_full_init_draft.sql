-- DRAFT: Full initialization script for Timesheet SQL App
-- Generated on 2025-10-28 20:55:34

-- 01. Create user_status table
CREATE TABLE IF NOT EXISTS user_status (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO user_status (id, name) VALUES
    (0, 'inactive'),
    (1, 'active'),
    (2, 'suspended'),
    (3, 'offboarded')
ON CONFLICT DO NOTHING;

-- 02. Create users table
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    profile VARCHAR(50),
    role VARCHAR(50),
    status_id SMALLINT REFERENCES user_status(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, name, email, status_id) VALUES
    ('admin', 'admin', 'eugenioklimenok@gmail.com', 1),
    ('alex', 'alex', 'mundoerp.latam@gmail.com', 0)
ON CONFLICT DO NOTHING;

-- 03. Create accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounts (name) VALUES
    ('Softland Argentina'),
    ('Swissport'),
    ('CisLatam')
ON CONFLICT DO NOTHING;

-- 04. Create project_status table
CREATE TABLE IF NOT EXISTS project_status (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO project_status (id, name) VALUES
    (0, 'inactive'),
    (1, 'active'),
    (2, 'paused')
ON CONFLICT DO NOTHING;

-- 05. Create projects table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    account_id UUID REFERENCES accounts(id),
    status_id SMALLINT REFERENCES project_status(id),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INSERTs for projects pueden agregarse luego en otro archivo

-- DRAFT END: Más tablas pueden añadirse debajo para extender el modelo.
