--USER STATUS TABLE
CREATE TABLE user_status (
    id SMALLINT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    LABEL VARCHAR(50) NOT NULL
);



 INSERT INTO user_status(id, code, label) VALUES
  (0, 'inactive', 'Inactivo'),
  (1, 'active', 'Activo'),
  (2, 'suspended', 'Suspendido'),
  (3, 'discontinued', 'Desvinculado');




select * from user_status

--drop TABLE user_status