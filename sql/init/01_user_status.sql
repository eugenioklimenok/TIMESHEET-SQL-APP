CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla auxiliar: user_status
CREATE TABLE IF NOT EXISTS user_status (
    id SMALLINT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
);
