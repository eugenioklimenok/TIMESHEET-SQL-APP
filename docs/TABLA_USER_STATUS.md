# Tabla: user_status

Tabla auxiliar que define los distintos estados que puede tener un usuario. Mejora la escalabilidad y claridad del modelo frente a un simple campo booleano.

## Estructura

- `id` (SMALLINT): Identificador del estado.
- `code` (VARCHAR): Código corto para el estado (ej. `ACTIVE`, `SUSPENDED`, etc).
- `description` (VARCHAR): Descripción larga del estado.

## Estados sugeridos

| id | code        | description           |
|----|-------------|------------------------|
| 0  | INACTIVE    | Usuario inactivo       |
| 1  | ACTIVE      | Usuario activo         |
| 2  | SUSPENDED   | Usuario suspendido     |
| 3  | UNASSIGNED  | Usuario desvinculado   |

## Ventajas

- Permite agregar nuevos estados sin modificar la tabla principal.
- Facilita validaciones y reportes.

## Consulta recomendada con JOIN

```sql
SELECT u.username, u.email, s.description as estado
FROM users u
JOIN user_status s ON u.status_id = s.id;
```