# 📌 Resumen Ejecutivo
- **Objetivo general:** Consolidar un backend de timesheets listo para exponer APIs REST, con dominio modelado en SQLModel, SQL crudo organizado y migraciones reproducibles.
- **Problemas abordados:** Estructura de carpetas dispersa, SQL embebido sin aislamiento, ausencia de rutas de ampliación para endpoints y pipelines de migración claros.
- **Impacto esperado:** Mayor mantenibilidad, onboarding acelerado y capacidad de evolucionar el producto (nuevos endpoints, autenticación) sin duplicar lógica ni romper el esquema.

# 🧠 Contexto Técnico
- **Situación previa:** El proyecto contenía scripts SQL y código FastAPI, pero requería unificar la arquitectura y preparar la capa de dominio para uso real de API y migraciones. El README ya documenta el dominio y la organización esperada del backend.【F:README.md†L1-L152】
- **Deuda/limitaciones detectadas:** Necesidad de un único punto de entrada, centralizar la sesión/engine y garantizar que el esquema se gestione por migraciones (no `create_all` en producción).【F:app/main.py†L3-L26】【F:app/core/database.py†L32-L49】
- **Dependencias relevantes:**
  - Modelos y relaciones en `app/models/` (`User`, `Account`, `Project`, `TimesheetHeader/Item`, catálogos de estado).【F:app/models/user.py†L12-L36】【F:app/models/account.py†L12-L50】【F:app/models/timesheet.py†L13-L54】
  - Scripts SQL de init/seed organizados por dependencia para PostgreSQL 16 y extensión `uuid-ossp`.【F:README.md†L71-L112】
  - Migración inicial Alembic que replica el esquema completo con llaves, índices y restricciones.【F:README.md†L138-L141】【F:migrations/versions/9c1e41e7a8b0_initial_schema.py†L1-L82】

# 🛠️ Lista Detallada de Tareas Realizadas
- **Reorganización de la aplicación FastAPI**
  - **Propósito:** Unificar entrada y registro de routers en `app/` para facilitar el despliegue y la extensión de endpoints.【F:app/main.py†L6-L26】
  - **Archivos:** `app/main.py`, `app/core/database.py`.
  - **Cambios y razón técnica:** Se definió un `FastAPI` central, evento de startup que inicializa la conexión y routers cargados desde paquetes dedicados, evitando configuraciones duplicadas y preparando la inyección de dependencias comunes.【F:app/main.py†L6-L26】【F:app/core/database.py†L32-L49】
  - **Mejora obtenida:** Reduce acoplamiento y establece un contrato claro para futuros módulos (auth, healthchecks, nuevos recursos).

- **Separación y catalogación de lógica SQL**
  - **Propósito:** Aislar SQL crudo en carpetas dedicadas (`sql/init`, `sql/seed`) con orden de ejecución explícito para inicialización y datos base.【F:README.md†L71-L112】
  - **Archivos:** `sql/init/*.sql`, `sql/seed/*.sql`, `migrations/versions/9c1e41e7a8b0_initial_schema.py`.
  - **Cambios y razón técnica:** Se documentó la secuencia de dependencias y se creó una migración inicial que reproduce la estructura (extensión `uuid-ossp`, índices, llaves foráneas, constraints de horas).【F:README.md†L71-L112】【F:migrations/versions/9c1e41e7a8b0_initial_schema.py†L20-L82】
  - **Mejora obtenida:** Instalaciones reproducibles y trazabilidad del esquema mediante Alembic.

- **Modelado de dominio para endpoints**
  - **Propósito:** Definir entidades SQLModel y relaciones necesarias para CRUD y validaciones previas a exponer APIs de usuarios, cuentas/proyectos y timesheets.【F:app/models/user.py†L12-L36】【F:app/models/account.py†L12-L50】【F:app/models/timesheet.py†L13-L54】
  - **Archivos:** `app/models/user.py`, `app/models/account.py`, `app/models/timesheet.py`.
  - **Cambios y razón técnica:** Se implementaron modelos con UUID, catálogos de estado, constraints (`hours >= 0`), timestamps por defecto y relaciones bidireccionales para navegación ORM. Esto habilita esquemas Pydantic y capas CRUD/routers consistentes.
  - **Mejora obtenida:** Base coherente para endpoints y validaciones, con integridad referencial alineada al SQL y migraciones.

# 🗂️ Archivos Modificados / Creados
- `app/main.py`: Punto de entrada FastAPI con registro de routers y hook de startup para la base de datos.【F:app/main.py†L6-L26】
- `app/core/database.py`: Configuración centralizada de engine/sesión y validación de conexión al iniciar la app.【F:app/core/database.py†L19-L49】
- `app/models/user.py`: Modelos `User` y `UserStatus` con claves únicas e índices para identificadores y correo.【F:app/models/user.py†L12-L36】
- `app/models/account.py`: Modelos `Account`, `ProjectStatus`, `Project` con relaciones y metadatos de auditoría.【F:app/models/account.py†L12-L50】
- `app/models/timesheet.py`: Modelos `TimesheetStatus`, `TimesheetHeader`, `TimesheetItem` con constraint de horas y enlaces a usuario/proyecto.【F:app/models/timesheet.py†L13-L54】
- `migrations/versions/9c1e41e7a8b0_initial_schema.py`: Migración Alembic que crea tablas, índices y extension `uuid-ossp`.【F:migrations/versions/9c1e41e7a8b0_initial_schema.py†L20-L82】
- `sql/init/*.sql`, `sql/seed/*.sql`: Scripts ordenados por dependencias para bootstrap y datos base (catalogados en README).【F:README.md†L71-L112】

# 🧪 Pruebas Sugeridas
- **Smoke API:** Levantar la app (`uvicorn app.main:app`) y verificar `GET /` retorna `{status:"ok"}` tras inicializar la DB.【F:app/main.py†L6-L26】
- **Migraciones:** Ejecutar `alembic upgrade head` sobre una base vacía y confirmar creación de tablas e índices definidos en la migración inicial.【F:migrations/versions/9c1e41e7a8b0_initial_schema.py†L20-L82】
- **Integridad referencial:** Insertar users/accounts/projects antes de crear `timesheet_header` y `timesheet_item` para validar llaves foráneas y el constraint de horas ≥ 0.【F:app/models/timesheet.py†L22-L54】
- **Seeds:** Aplicar scripts en el orden indicado y verificar datos mínimos (catálogos de estado y registros de ejemplo).【F:README.md†L71-L112】

# ⚠️ Riesgos / Dependencias
- **Dependencia de PostgreSQL 16 y extensión `uuid-ossp`:** requerida por la migración inicial y scripts SQL.【F:migrations/versions/9c1e41e7a8b0_initial_schema.py†L20-L82】【F:README.md†L103-L112】
- **Diferencias entre `create_all` y migraciones:** En producción debe usarse Alembic; `create_all` se mantiene para entornos de desarrollo/test y puede divergir si no se actualizan migraciones junto con modelos.【F:app/core/database.py†L32-L49】
- **Integridad de datos:** Claves únicas (user_id, account_id, project_id, email) y constraint de horas pueden generar errores si los seeds o pruebas no respetan el dominio.【F:app/models/user.py†L24-L36】【F:app/models/account.py†L15-L50】【F:app/models/timesheet.py†L22-L54】

# 🚀 Recomendaciones y Próximos Pasos
- Añadir esquemas Pydantic y operaciones CRUD alineadas con los modelos para exponer endpoints versionados.
- Implementar tests automáticos en `tests/` usando SQLite en memoria o contenedor PostgreSQL para validar rutas y reglas de negocio.【F:README.md†L155-L160】
- Incorporar autenticación JWT y dependencias comunes en `app/core/` para proteger endpoints sensibles.
- Automatizar seeds/migraciones en CI/CD (scripts `make` o pipelines) y documentar variables de entorno (`DATABASE_URL`, credenciales).
- Completar el roadmap marcando modelos CRUD/routers como entregados y agregando healthchecks y métricas básicas.【F:README.md†L192-L200】

# 🧬 Impacto en la Arquitectura
- **Estructura lógica:** Proyecto consolidado bajo `app/` con capas explícitas (`core`, `models`, `routers`, `crud`, `schemas`) y SQL aislado en `sql/` + migraciones en `migrations/`.【F:README.md†L120-L141】
- **Responsabilidades:** `app/core/database.py` asume la orquestación del engine y registro de metadata; los modelos encapsulan relaciones y constraints, habilitando CRUD/routers desacoplados.【F:app/core/database.py†L19-L49】【F:app/models/timesheet.py†L13-L54】
- **Mantenibilidad y escalabilidad:** Migraciones versionadas y modelos tipados reducen riesgo de drift de esquema y facilitan extensiones (nuevas entidades, estados, procesos de aprobación).

# 📄 Anexo
- **Migración inicial (fragmento):** creación de catálogos de estado, tablas principales y constraint `ck_timesheet_item_hours_positive` para horas no negativas.【F:migrations/versions/9c1e41e7a8b0_initial_schema.py†L20-L82】
- **Estructura y orden de scripts SQL:** secuencia recomendada para init/seed documentada en README para reproducir entornos desde cero.【F:README.md†L71-L112】
