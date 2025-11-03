DROP TABLE IF EXISTS accounts CASCADE;


CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id VARCHAR(25) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounts (id, account_id, name, type) VALUES
  ('7a24d8d6-468a-4528-9b3c-4a428bcf4326', 'CL011120251', 'Canalt S.A.', 'External'),
  ('3a05f5a7-d820-463b-b909-7a9c7cefea59', 'CL011120252', 'Internal Use', 'Internal');



