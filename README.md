# ⏱️ TimeSheet App --- Backend (PostgreSQL + FastAPI + SQLModel)

Proyecto profesional creado por **Alex (ERP Insider LATAM)**.\
El objetivo es construir un backend moderno, modular y escalable para
gestionar:

-   Usuarios
-   Cuentas / Clientes
-   Proyectos
-   Partes de horas (Timesheets)
-   Estados y flujos (borrador → enviado → aprobado)

Este repositorio combina:

-   **Estructura SQL completa**
-   **Backend FastAPI + SQLModel**
-   **Migraciones con Alembic**
-   **Uso de IA local (Aider + Qwen2.5-coder)**
-   **Preparación para autenticación JWT**
-   **Base sólida para un MVP real y un portfolio profesional**

------------------------------------------------------------------------

## 🧱 1. Modelo de Base de Datos (SQL)

El proyecto incluye una estructura relacional robusta en PostgreSQL 16,
con organización modular en archivos `.sql`.

### Entidades principales

#### `user_status`

Estados posibles de un usuario.

#### `users`

Consultores o empleados que registran horas.\
Relación: - `status_id` → `user_status(id)`

#### `accounts`

Clientes o cuentas corporativas.

#### `project_status`

Estados posibles de un proyecto.

#### `projects`

Proyectos vinculados a una cuenta.\
Relaciones: - `account_id` → `accounts(id)` - `status_id` →
`project_status(id)`

#### `timesheet_status`

Estados de un parte de horas.

#### `timesheet_header`

Cabecera del parte: fecha, usuario, proyecto, estado.\
Relaciones: - `user_id` → `users(id)` - `project_id` → `projects(id)` -
`status_id` → `timesheet_status(id)`

#### `timesheet_item`

Detalle de tareas, duración y si son facturables.\
Relación: - `header_id` → `timesheet_header(id)`

------------------------------------------------------------------------

## 📁 2. Archivos SQL incluidos

Los scripts están divididos entre **inicialización** (`sql/init/`) y
**semillas** (`sql/seed/`).

**Orden recomendado para inicializar la estructura**

1. `sql/init/01_user_status.sql`
2. `sql/init/02_users.sql`
3. `sql/init/03_accounts.sql`
4. `sql/init/04_project_status.sql`
5. `sql/init/05_projects.sql`
6. `sql/init/06_timesheet_status.sql`
7. `sql/init/07_timesheet_header.sql`
8. `sql/init/08_timesheet_item.sql`

**Orden recomendado para seed de datos base** (mismo orden de dependencias):

1. `sql/seed/01_user_status.sql`
2. `sql/seed/02_users.sql`
3. `sql/seed/03_accounts.sql`
4. `sql/seed/04_project_status.sql`
5. `sql/seed/05_projects.sql`
6. `sql/seed/06_timesheet_status.sql`
7. `sql/seed/07_timesheet_header.sql`
8. `sql/seed/08_timesheet_item.sql`

Para un arranque rápido puedes usar el script completo con datos de ejemplo
en `sql/init/00_full_init_draft.sql`.

------------------------------------------------------------------------

## 🚀 3. Instalación rápida de la base de datos

Asegurate de tener PostgreSQL 16 con la extensión `uuid-ossp`.

``` bash
psql -U tu_usuario -d tu_base -f sql/init/00_full_init_draft.sql
```

Con esto tendrás toda la estructura + datos mínimos para comenzar.

------------------------------------------------------------------------

## 🧩 4. Arquitectura del Backend (FastAPI + SQLModel)

El proyecto usa una estructura limpia, escalable y orientada a
producción:

    app/
      main.py              # Punto de entrada FastAPI
      core/database.py     # Engine y sesiones centralizadas
      routers/             # Routers de usuarios, cuentas y timesheets
      schemas/             # Esquemas Pydantic para entrada/salida
      crud/                # Operaciones de acceso a datos
      models/              # Modelos SQLModel
    sql/                   # Scripts SQL raw
    migrations/            # Historial de Alembic
    tests/
    aider.conf.yml
    vibe_rules.md
    AIDER_CONTEXT.md
    continue_config.yaml
    README.md
    docker-compose.yml
    Dockerfile

El catálogo `migrations/` incluye la primera versión del esquema
(`migrations/versions/9c1e41e7a8b0_initial_schema.py`). Ajusta `alembic.ini`
o la variable de entorno `DATABASE_URL` para apuntar a tu base de datos y
ejecuta `alembic upgrade head` para aplicar la estructura.

Tecnologías principales:

-   **FastAPI** para el API REST
-   **SQLModel** (Pydantic v2 + SQLAlchemy)
-   **Alembic** para migraciones
-   **PostgreSQL** como motor principal
-   **Python 3.12**
-   **Docker** listo para uso futuro
-   **IA local** (Ollama + Qwen2.5-coder) para acelerar desarrollo

------------------------------------------------------------------------

## 🧪 5. Tests

Cada endpoint nuevo debe incluir una prueba en:

    tests/

------------------------------------------------------------------------

## 🤖 6. IA Integrada (Aider + Qwen2.5-coder)

El proyecto está optimizado para desarrollo asistido por IA usando:

-   **AIDER_CONTEXT.md**
-   **aider.conf.yml**
-   **vibe_rules.md**
-   **continue_config.yaml**

Modelo local recomendado:

``` bash
ollama pull qwen2.5-coder:7b
ollama serve
```

Para iniciar Aider:

``` bash
aider .
```

Esto habilita: - Commits automáticos - Cambios seguros y supervisados -
Respeto total de la estructura del proyecto - Generación de
CRUD/routers/migraciones siguiendo tus reglas - Actualización
inteligente basada en tus archivos de contexto

------------------------------------------------------------------------

## 📌 7. Roadmap del Proyecto

### ✔️ Base de datos completa (SQL)

### ✔️ Estados y relaciones principales

### ⬜ Modelos SQLModel

### ⬜ CRUD + routers FastAPI

### ⬜ Migraciones Alembic

### ⬜ Autenticación JWT + roles

### ⬜ Dockerización

### ⬜ Tests de endpoints

### ⬜ Ejemplos de requests (README)

### ⬜ Frontend mínimo (fase futura)

------------------------------------------------------------------------

## 🔗 8. Relación entre tablas (resumen gráfico)

    users → user_status
    projects → accounts, project_status
    timesheet_header → users, projects, timesheet_status
    timesheet_item → timesheet_header

------------------------------------------------------------------------

## © Autor

**Alex Klimenok (ERP Insider LATAM)**\
Consultor ERP • Backend Developer en evolución • LATAM\
2025

