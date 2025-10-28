
# 📘 Tabla Auxiliar: `timesheet_status`

Contiene los posibles estados de una carga de horas (`timesheet_header`), permitiendo controlar el flujo de validación.

## 📌 Campos:
- `id`: Clave primaria (`SMALLINT`).
- `name`: Descripción del estado (`VARCHAR(50)`)

## ✅ Valores iniciales:
- `0` → Borrador
- `1` → Enviado
- `2` → Aprobado
- `3` → Rechazado
- `4` → Facturado

## 🔗 Relación:
- Referenciado por `timesheet_header.status_id`
