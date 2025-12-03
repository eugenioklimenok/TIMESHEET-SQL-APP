"""Esquemas de validación compartida."""
from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class DateRange(BaseModel):
    period_start: date = Field(..., description="Fecha de inicio del periodo")
    period_end: date = Field(..., description="Fecha de fin del periodo")


class ErrorResponse(BaseModel):
    code: int = Field(..., description="Código de error HTTP o de aplicación")
    message: str = Field(..., description="Mensaje legible para el usuario")
    details: dict | list | None = Field(None, description="Detalles adicionales del error")
    timestamp: datetime = Field(..., description="Marca temporal en formato ISO8601 UTC")
    path: str = Field(..., description="Ruta del endpoint invocado")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 404,
                    "message": "Recurso no encontrado",
                    "details": None,
                    "timestamp": "2024-06-25T15:42:10Z",
                    "path": "/api/reports/generate",
                },
                {
                    "code": 422,
                    "message": "Input inválido",
                    "details": {"from": "La fecha 'from' no puede ser mayor que 'to'"},
                    "timestamp": "2024-06-25T15:42:10Z",
                    "path": "/reports/user-hours",
                },
            ]
        }
    }
