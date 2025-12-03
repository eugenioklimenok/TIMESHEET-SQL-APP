# 📊 Reportes y Agregaciones (T8)

Endpoints de reporte basados en modelos Pydantic.

## `GET /reports/user-hours`
- Params: `from`, `to` (YYYY-MM-DD)
- Respuesta: `UserHoursReport[]` (ordenado por `total_hours` desc)

## `GET /reports/project-hours/{project_id}`
- Params: `from`, `to`
- Respuesta: `ProjectHoursReport[]` para el proyecto indicado, ordenado por `total_hours` desc

## `GET /reports/user/{user_id}/projects`
- Params: `from`, `to`
- Respuesta: `UserProjectHoursReport[]` agregando horas del usuario por proyecto

## `GET /reports/summary`
- Params: `from`, `to` (solo admins)
- Respuesta: `SummaryReport` con `totals_by_status` en orden Draft → Submitted → Approved
