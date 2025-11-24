# vibe_rules.md — TimeSheet App (Alex • ERP Insider LATAM)

Reglas adicionales para agentes autónomos (Aider + Continue.dev).

## 1. Antes de actuar
- Leer `AIDER_CONTEXT.md` completo.
- Identificar la carpeta correcta según estructura.
- Detectar duplicados o archivos similares.
- No inventar carpetas ni rutas.

## 2. Creación de archivos
Permitir crear archivos SOLO en:
- /sql
- /app/main.py
- /app/routers
- /app/models
- /app/crud
- /app/schemas
- /app/core
- /app/dependencies.py
- /migrations
- /tests

Nunca crear fuera de estas carpetas.

## 3. Modelo mental obligatorio
Router → Crud → Modelo → Schema → SQL
Sigue esta cadena SIEMPRE.

## 4. Validaciones obligatorias
- Snake_case.
- UUID con gen_random_uuid().
- TIMESTAMPTZ.
- Índices con CONCURRENTLY.
- Tests auto-generados cuando se crea un endpoint.

## 5. Lógica
- Routers sin lógica de negocio.
- CRUD con SQLModel.
- Alembic para cada cambio de DB.
- No borrar columnas sin aprobación explícita.

## 6. Manejo de SQL
- No SELECT *.
- Joins explícitos.
- Validar que las columnas existan.
- No modificar tablas críticas sin plan previo.

## 7. Comunicación del agente
- Mensajes cortos.
- Advertir antes de cambios grandes.
- Explicar riesgos solo si existen.

## 8. Autenticación
- No implementar JWT sin que Alex lo pida directamente.

Fin del archivo.
