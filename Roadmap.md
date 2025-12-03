# Roadmap Timesheet-SQL-APP

## Checklist inicial
- [ ] Registrar estado actual del backend FastAPI/SQLModel
- [ ] Identificar brechas funcionales pendientes
- [ ] Planificar fases técnicas con dependencias claras
- [ ] Priorizar tareas críticas para operatividad
- [ ] Establecer secuencia recomendada de ejecución

## 1. Resumen de Implementación Actual
- API FastAPI con routers para usuarios, cuentas/proyectos y timesheets montados en `app/main.py`.
- Modelos SQLModel para usuarios, cuentas, proyectos, estados y timesheets con relaciones y validaciones básicas.
- CRUD sin capas de servicio: operaciones directas para crear/listar/actualizar/eliminar usuarios, cuentas, proyectos, cabeceras e ítems de timesheet.
- Esquemas Pydantic v2 para entrada/salida en usuarios, cuentas/proyectos y timesheets.
- Inicialización de base con `init_db()` y dependencia `get_session()` centralizada para sesiones SQLModel.
- T1 (Autenticación JWT básica) ya está implementada en el repositorio: login con emisión/validación de tokens, hashing de contraseñas y dependencias de seguridad activas en los routers.

## 2. Faltantes del Backend
- Validaciones de negocio (cruces de estados, unicidad avanzada, rangos de horas, fechas futuras) y manejo de errores consistentes.
- Filtrados y paginación en listados; búsqueda por parámetros (cuenta, proyecto, rango de fechas, estado, usuario).
- Gestión de estados y flujo de timesheets (transiciones Draft/Submitted/Approved y acciones asociadas).
- Tests automatizados de routers/CRUD y configuración de CI para ejecutarlos.
- Documentación operacional (env vars, ejemplos de requests, swagger custom) y scripts de arranque (Docker/compose actualizados).

## 3. Roadmap en Fases

### Fase 1: Fundamentos operativos
Asegurar autenticación, seguridad y control de estados mínimos.

| ID  | Título                         | Descripción técnica                                                                 | Dependencias |
|-----|--------------------------------|-------------------------------------------------------------------------------------|--------------|
| T1  | Autenticación JWT básica (COMPLETADA) | Implementar login con emisión/validación de tokens, hashing de contraseñas y guardas de ruta. Implementado en el repositorio. | —            |
| T2  | Modelo de roles y permisos (COMPLETADA) | Definir roles (admin/user) y dependencias de autorización en routers sensibles.     | T1 (cumplida) |
| T3  | Gestión de estados iniciales (COMPLETADA)  | CRUD para tablas de estado (`user_status`, `project_status`, `timesheet_status`) y valores seed. | —            |
| T4  | Validación de transiciones (COMPLETADA)    | Reglas para mover timesheets entre estados permitidos (draft→submitted→approved) con errores claros. | T3 (cumplida) |

### Fase 2: Funcionalidad core
Añadir reglas de negocio y mejoras de datos.

| ID  | Título                               | Descripción técnica                                                             | Dependencias |
|-----|--------------------------------------|---------------------------------------------------------------------------------|--------------|
| T5  | Validaciones de dominio (COMPLETADA) | Chequear unicidad de IDs combinados, límites de horas (>0 y <=24/día), fechas no futuras. | T1 (cumplida), T3       |
| T6  | Filtrado y paginación de listados (COMPLETADA)   | Añadir query params por cuenta/proyecto/usuario/estado/fecha y paginación estándar. | T1 (cumplida)           |
| T7  | Relaciones y preload eficientes      | Incluir `joinload`/`selectinload` en queries para evitar N+1 y exponer anidados en schemas. | T6           |

### Fase 3: Calidad y entrega
Fortalecer pruebas, observabilidad y despliegue.

| ID  | Título                               | Descripción técnica                                                             | Dependencias |
|-----|--------------------------------------|---------------------------------------------------------------------------------|--------------|
| T8  | Pruebas automatizadas                | Tests unitarios/integ. para CRUD/routers con SQLite en memoria y fixtures de datos. | T5, T6       |
| T9  | Documentación y ejemplos de API      | Actualizar README/Swagger con flujos, auth y ejemplos curl/httpie.               | T1 (cumplida), T6       |
| T10 | Contenedorización y CI               | Revisar Docker/compose, agregar pipeline (lint+tests+migrations) en CI.          | T8, T9       |

## 4. Orden Recomendado
1. T1 (completada) → Autenticación JWT básica
2. T2 (completada) → Modelo de roles y permisos
3. T3 (completada) → Gestión de estados iniciales
4. T4 (completada) → Validación de transiciones
5. T5 (completada) → Validaciones de dominio
6. T6 (completada) → Filtrado y paginación de listados
7. T7 → Relaciones y preload eficientes
8. T8 → Pruebas automatizadas
9. T9 → Documentación y ejemplos de API
10. T10 → Contenedorización y CI
