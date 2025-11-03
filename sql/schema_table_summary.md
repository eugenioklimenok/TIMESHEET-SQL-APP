
## 🗂️ Esquema de Tablas y Campos Clave (Resumen)

| Tabla              | Clave Primaria | ID legible     | FK UUIDs usados                          |
|-------------------|----------------|----------------|------------------------------------------|
| `users`           | `id` (UUID)    | `user_id`      | —                                        |
| `accounts`        | `id` (UUID)    | `account_id`   | —                                        |
| `projects`        | `id` (UUID)    | `project_id`   | `account_uuid` → `accounts.id`           |
| `timesheet_header`| `id` (UUID)    | —              | `user_uuid` → `users.id`<br>`project_uuid` → `projects.id` |
| `timesheet_item`  | `id` (UUID)    | —              | `header_uuid` → `timesheet_header.id`    |
| `user_status`     | `id` (SMALLINT)| —              | —                                        |
| `project_status`  | `id` (SMALLINT)| —              | —                                        |
| `timesheet_status`| `id` (SMALLINT)| —              | —                                        |

📌 **Notas:**
- Los campos `*_uuid` se utilizan para relaciones internas (FOREIGN KEYS).
- Los campos `*_id` son visibles para el usuario/API (códigos legibles).
- Todas las tablas tienen `created_at` como marca de tiempo estándar.
