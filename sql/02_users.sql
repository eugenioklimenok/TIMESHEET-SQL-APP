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