# Roadmap del Proyecto

## Fase 1: Saneamiento y consistencia API

| Nº | Tarea | Prioridad | Dependencias | Resultados Esperados | Categoría |
|----|-------|-----------|--------------|----------------------|-----------|
| 1 | Unificar el manejo de errores en todos los routers usando las excepciones de `app.core.errors` y el esquema `ErrorResponse`, eliminando `HTTPException` ad-hoc. | Crítica | - | Respuestas coherentes, códigos HTTP alineados y trazabilidad centralizada en logs. | Estándares unificados de errores |
| 2 | Corregir inconsistencias de identificadores y unicidad en cuentas/proyectos/usuarios (campos `account_id`/`project_id` vs `code`) y validar duplicados a nivel de modelo y CRUD. | Alta | 1 | Datos normalizados sin colisiones y endpoints coherentes con el modelo SQL. | Corrección de inconsistencias detectadas |
| 3 | Reestructurar routers de usuarios/cuentas/proyectos para delegar reglas en una capa de servicios y reutilizar validaciones comunes. | Alta | 1, 2 | Lógica desacoplada, menor duplicidad y rutas listas para expandir reglas de negocio. | Reestructuración necesaria |

## Fase 2: Seguridad y configuración profesional

| Nº | Tarea | Prioridad | Dependencias | Resultados Esperados | Categoría |
|----|-------|-----------|--------------|----------------------|-----------|
| 4 | Implementar seguridad JWT profesional con PyJWT y passlib: firmas HS256/RS256 configurables por entorno, expiración, refresh tokens y revocación básica. | Crítica | 1, 3 | Autenticación robusta, claves rotables y tokens alineados a mejores prácticas. | Seguridad JWT profesional |
| 5 | Crear configuración profesional con `pydantic-settings`, `.env.example`, perfiles dev/test/prod y contenedores Docker/Compose para API + PostgreSQL + healthchecks. | Alta | 4 | Despliegues reproducibles, variables centralizadas y arranque local/CI consistente. | Configuración profesional (Docker, settings, etc.) |

## Fase 3: Reglas de negocio y experiencia de datos

| Nº | Tarea | Prioridad | Dependencias | Resultados Esperados | Categoría |
|----|-------|-----------|--------------|----------------------|-----------|
| 6 | Completar validaciones de negocio de timesheets: solapes de periodos, horas diarias y pertenencia a proyectos, con transiciones Draft/Submitted/Approved/Rejected cerradas. | Crítica | 1, 3 | Reglas consistentes, mensajes claros y prevención de registros inválidos. | Validaciones de negocio faltantes |
| 7 | Aplicar paginación y filtros coherentes en listados de usuarios, cuentas, proyectos, timesheets y reportes (fecha, estado, cuenta, proyecto, usuario). | Alta | 1, 6 | Consultas predecibles, escalabilidad en listados y contratos de API documentados. | Paginación y filtros coherentes en todos los listados |

## Fase 4: Calidad, pruebas y entrega

| Nº | Tarea | Prioridad | Dependencias | Resultados Esperados | Categoría |
|----|-------|-----------|--------------|----------------------|-----------|
| 8 | Ajustar la suite de tests para cubrir nuevos flujos JWT, validaciones de negocio, paginación y errores estandarizados; habilitar fixtures de datos y cobertura en CI. | Alta | 4, 6, 7 | Tests verdes reflejando las reglas actuales y pipeline de calidad confiable. | Ajustes necesarios en tests |
| 9 | Documentar y versionar el contrato de API (OpenAPI/README) alineado al nuevo manejo de errores, seguridad y configuración; preparar templates de despliegue. | Media | 5, 7, 8 | Documentación actualizada y lista para operaciones y handover. | Corrección de inconsistencias detectadas |
