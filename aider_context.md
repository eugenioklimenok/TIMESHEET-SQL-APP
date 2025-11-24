# AIDER_CONTEXT.md — TimeSheet App (Alex • ERP Insider LATAM)
¡Este archivo es leído automáticamente por Aider en cada sesión!
Nunca lo borres ni lo renombres.

## 1. Identidad y objetivo
- Nombre: TimeSheet App
- Dominio: Gestión de horas trabajadas, proyectos, clientes y usuarios (ERP ligero LATAM)
- Estado actual: solo definición de base de datos (SQL puro) + README
- Objetivo final: API REST completa con FastAPI + autenticación JWT + frontend mínimo
- Uso real: portfolio + MVP + proyecto educativo

## 2. Stack definitivo (2025)
- Python 3.12
- FastAPI + Uvicorn
- PostgreSQL 16 + extensión uuid-ossp
- SQLModel (SQLAlchemy + Pydantic v2)
- Alembic para migraciones
- Docker + docker-compose
- qwen2.5-coder:7b local como agente principal (Aider)

## 3. Estructura de carpetas OBLIGATORIA
/ (raíz)
├── sql/                  ← todos los .sql (schema, vistas, funciones)
├── app/
│   ├── main.py
│   ├── routers/
│   ├── schemas/
│   ├── crud/
│   ├── models/
│   ├── dependencies.py
│   └── core/
├── migrations/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── README.md
└── AIDER_CONTEXT.md      ← este archivo


## 4. Reglas INQUEBRANTABLES (obedecer siempre)
1. Nunca romper compatibilidad existente
2. Antes de cambios grandes → explicar el plan en 2-3 líneas
3. Cada cambio = un commit separado con mensaje perfecto:
   - feat: agrega endpoint GET /timesheets
   - refactor: optimiza vista horas por proyecto
   - fix: corrige cálculo de totales
   - chore: actualiza dependencias
4. Usar siempre snake_case en DB y Python
5. Primary keys → UUID (gen_random_uuid())
6. Fechas → TIMESTAMP WITH TIME ZONE
7. Índices → CREATE INDEX CONCURRENTLY
8. Solo crear archivos dentro de la estructura definida arriba
9. Todo endpoint debe tener test en /tests
10. Si no estás 100 % seguro → NO tocar y avisarme

## 5. Convenciones de código
- Archivos SQL: nombre descriptivo + .sql
- Vistas: prefijo v_
- Modelos SQLModel: singular (User, Project, Timesheet)
- Rutas API: plural (/users, /projects, /timesheets)
- Paginación: limit-offset por defecto

## 6. Próximos pasos priorizados (actualizar cuando se completen)
- [ ] Crear carpetas y estructura inicial
- [ ] Convertir SQL actual a modelos SQLModel
- [ ] Generar migraciones Alembic
- [ ] API completa: users → projects → timesheets (CRUD + filtros)
- [ ] Autenticación JWT + roles (admin/employee)
- [ ] Dockerizar todo
- [ ] Tests + README con ejemplos

Última actualización: 2025-11-24