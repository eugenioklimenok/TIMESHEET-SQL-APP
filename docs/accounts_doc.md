# Tabla `accounts`

Esta tabla almacena las cuentas o clientes asociadas a los proyectos.

## Estructura de la tabla

| Campo       | Tipo        | Descripción                                      |
|-------------|-------------|--------------------------------------------------|
| id          | UUID        | Identificador único (PK) generado automáticamente |
| name        | VARCHAR(150)| Nombre de la cuenta o cliente                    |
| type        | VARCHAR(50) | Tipo de cuenta (Ej: Interno, Externo)            |
| created_at  | TIMESTAMP   | Fecha de creación del registro                   |

## Inserts de ejemplo

```sql
INSERT INTO accounts (name, type) VALUES
    ('Cliente A', 'Externo'),
    ('Cliente B', 'Externo'),
    ('Uso Interno', 'Interno');
```

## Relaciones

- Esta tabla se relaciona con `projects` mediante la columna `account_id`.
