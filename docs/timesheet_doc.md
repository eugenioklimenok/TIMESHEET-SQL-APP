
# 🕒 Timesheet Tables: Header & Item

Estas dos tablas forman el núcleo de la aplicación de registro de horas.

---

## 📌 `timesheet_header`

Representa una carga de horas hecha por un usuario para un proyecto en una fecha determinada.

### Campos:
- `id`: UUID, PK autogenerado.
- `user_id`: FK a `users(id)`.
- `project_id`: FK a `projects(id)`.
- `work_date`: Fecha del trabajo realizado.
- `status_id`: Estado de la carga (ej: 0 = borrador, 1 = enviado, etc.).
- `created_at`: Timestamp automático.

---

## 🧾 `timesheet_item`

Detalle de cada actividad dentro de una carga de horas (header).

### Campos:
- `id`: UUID, PK autogenerado.
- `header_id`: FK a `timesheet_header(id)`.
- `description`: Texto libre de la tarea.
- `hours`: Horas trabajadas (hasta 2 decimales).
- `billable`: Booleano (si es facturable).
- `created_at`: Timestamp automático.

---

## 🔗 Relación
Un `timesheet_header` puede tener múltiples `timesheet_item`.

Ideal para controlar horas por jornada, y tareas asociadas.
