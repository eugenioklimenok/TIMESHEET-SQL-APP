"""Validaciones reutilizables para la API."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import Path, Query, status

from app.core.errors import BusinessRuleException
from app.schemas.validation import DateRange


def validate_date_range(
    period_start: date = Query(..., alias="from", description="Fecha de inicio del reporte"),
    period_end: date = Query(..., alias="to", description="Fecha de fin del reporte"),
) -> DateRange:
    """Valida que el rango de fechas sea correcto."""

    if period_start > period_end:
        raise BusinessRuleException(
            "La fecha 'from' no puede ser mayor que 'to'",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"from": "La fecha 'from' no puede ser mayor que 'to'"},
        )

    return DateRange(period_start=period_start, period_end=period_end)


def validate_uuid_param(
    identifier: UUID = Path(..., description="Identificador UUID"), field_name: str = "id"
) -> UUID:
    """Valida identificadores UUID genéricos.

    Útil para asegurar que no se utilicen UUID vacíos.
    """

    if identifier.int == 0:
        raise BusinessRuleException(
            f"{field_name} es inválido",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={field_name: "El identificador no puede ser vacío"},
        )
    return identifier


def validate_user_id(user_id: UUID = Path(..., description="Identificador del usuario")) -> UUID:
    return validate_uuid_param(user_id, "user_id")


def validate_project_id(project_id: UUID = Path(..., description="Identificador del proyecto")) -> UUID:
    return validate_uuid_param(project_id, "project_id")


def validate_timesheet_id(timesheet_id: UUID = Path(..., description="Identificador del parte de horas")) -> UUID:
    return validate_uuid_param(timesheet_id, "timesheet_id")


def validate_item_id(item_id: UUID = Path(..., description="Identificador del ítem")) -> UUID:
    return validate_uuid_param(item_id, "item_id")
