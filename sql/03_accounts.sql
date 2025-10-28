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
