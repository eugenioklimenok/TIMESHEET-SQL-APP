# Tabla: users

Esta tabla almacena la información básica de cada usuario del sistema.

## Estructura

- `id` (UUID): Identificador único generado automáticamente (`uuid_generate_v4()`).
- `username` (VARCHAR 50): Nombre de usuario, único y obligatorio.
- `name` (VARCHAR 100): Nombre completo del usuario.
- `email` (VARCHAR 150): Correo electrónico, único.
- `profile` (VARCHAR 50): Perfil o descripción del usuario (opcional).
- `role` (VARCHAR 50): Rol del usuario (opcional).
- `status_id` (SMALLINT): Relación con la tabla `user_status`, representa el estado actual del usuario.
- `created_at` (TIMESTAMP): Fecha de creación, se completa automáticamente.

## Ejemplo de inserción

```sql
INSERT INTO users (username, name, email)
VALUES 
('admin', 'Administrador General', 'admin@app.com'),
('alex', 'Alex Zajarov', 'alex@app.com');
```

## Ejemplo de actualización de estado

```sql
UPDATE users
SET status_id = 2
WHERE username = 'alex';
```