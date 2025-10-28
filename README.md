# ⏱️ Timesheet SQL App — Backend PostgreSQL

Este proyecto define la estructura base de una aplicación de control de horas (Timesheet) usando **PostgreSQL**, pensada para luego ser conectada a una aplicación web, mobile o en la nube.

---

## 🧱 Estructura de la base de datos

La base de datos sigue un modelo relacional, modular y escalable. A continuación, se detallan las entidades principales y sus relaciones.

### 1. `user_status`
Tabla auxiliar que define los estados posibles de un usuario.

### 2. `users`
Lista de usuarios/consultores que cargan horas.

- FK: `status_id` → `user_status(id)`

### 3. `accounts`
Clientes o cuentas para las que se trabaja.

### 4. `project_status`
Estados posibles de un proyecto.

### 5. `projects`
Proyectos vinculados a cuentas.

- FK: `account_id` → `accounts(id)`
- FK: `status_id` → `project_status(id)`

### 6. `timesheet_status`
Estados posibles del parte diario (borrador, enviado, aprobado, etc.)

### 7. `timesheet_header`
Cabecera del parte diario/semanal.

- FK: `user_id` → `users(id)`
- FK: `project_id` → `projects(id)`
- FK: `status_id` → `timesheet_status(id)`

### 8. `timesheet_item`
Detalle de tareas, duración y si son facturables.

- FK: `header_id` → `timesheet_header(id)`

---

## 🚀 Instalación rápida

1. Aseguráte de tener una base de datos PostgreSQL funcional.
2. Ejecutá el siguiente comando desde consola:

```bash
psql -U tu_usuario -d tu_base -f 00_full_init_draft.sql
```

> 💡 Esto creará todas las tablas y datos base en el orden correcto.

---

## 📁 Archivos `.sql` incluidos

| Archivo | Contenido |
|--------|-----------|
| `00_full_init_draft.sql` | Script completo para inicializar la base |
| `01_user_status.sql` | Tabla y datos de estados de usuario |
| `02_users.sql` | Tabla de usuarios |
| `03_accounts.sql` | Tabla de cuentas/clientes |
| `04_project_status.sql` | Tabla de estados de proyectos |
| `05_projects.sql` | Tabla de proyectos |
| `06_timesheet_status.sql` | Tabla de estados de parte |
| `07_timesheet_header.sql` | Cabecera del parte de horas |
| `08_timesheet_item.sql` | Detalle de tareas en el parte |

---

## 🔗 Relación entre tablas (resumen)

```plaintext
users → user_status
projects → accounts, project_status
timesheet_header → users, projects, timesheet_status
timesheet_item → timesheet_header
```

---

## 🧠 Siguiente paso sugerido

Comenzar a trabajar en:

- Inserciones de prueba reales en `timesheet_header` y `timesheet_item`
- Validaciones de consistencia
- Desarrollo de vistas y reportes básicos (por usuario, por cuenta, por proyecto)
- Integración con app frontend

---

© Proyecto Timesheet SQL — Alex Zajarov, 2025