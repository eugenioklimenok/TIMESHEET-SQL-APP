# 📁 Tabla `projects` y `project_status`

## 🧱 Tabla `project_status`

Define los estados posibles que puede tener un proyecto en el sistema:

| id | status_name |
|----|-------------|
| 1  | Activo      |
| 2  | En espera   |
| 3  | Suspendido  |
| 4  | Finalizado  |
| 5  | Cancelado   |

Esta tabla es auxiliar y se relaciona con `projects.status_id`.

---

## 📁 Tabla `projects`

Representa los proyectos asociados a una cuenta (cliente o área interna).

### Estructura:

- `id`: UUID único autogenerado.
- `name`: Nombre del proyecto.
- `account_id`: FK a `accounts.id`.
- `status_id`: FK a `project_status.id` (por defecto: Activo).
- `description`: Texto libre con más info.
- `created_at`: Timestamp automático.

### Relaciones:

- **1:N** con `accounts`
- **N:1** con `project_status`

---

## 🧪 Inserts sugeridos

Para insertar proyectos, necesitás los `UUID` reales de cuentas:

```sql
INSERT INTO projects (name, account_id, status_id, description)
VALUES
  ('Implementación CRM', 'UUID_ACME', 1, 'Proyecto para cliente Acme'),
  ('App Interna Timesheet', 'UUID_INTERNO', 2, 'Desarrollo de app interna');
```