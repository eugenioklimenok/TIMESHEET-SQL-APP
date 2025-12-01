-- Tabla principal: users
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
