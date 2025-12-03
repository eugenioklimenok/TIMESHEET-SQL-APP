"""Manejo centralizado de errores y excepciones personalizadas."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.logging import get_logger


logger = get_logger(__name__)


class BusinessRuleException(Exception):
    """Errores de negocio y validaciones personalizadas."""

    def __init__(self, message: str, *, status_code: int = status.HTTP_400_BAD_REQUEST, details: Any | None = None) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFoundException(BusinessRuleException):
    """Excepción para recursos no encontrados."""

    def __init__(self, message: str, *, details: Any | None = None) -> None:
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND, details=details)


class AuthorizationException(BusinessRuleException):
    """Excepción para errores de autenticación o autorización."""

    def __init__(self, message: str, *, status_code: int = status.HTTP_401_UNAUTHORIZED, details: Any | None = None) -> None:
        super().__init__(message, status_code=status_code, details=details)


# Helpers


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _format_error_response(request: Request, code: int, message: str, details: Any | None = None) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "details": details,
        "timestamp": _utc_timestamp(),
        "path": request.url.path,
    }


# Exception handlers


async def business_rule_exception_handler(request: Request, exc: BusinessRuleException) -> JSONResponse:
    logger.warning("Business rule error at %s: %s", request.url.path, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=_format_error_response(request, exc.status_code, exc.message, exc.details),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    detail = exc.detail
    message = "Error en la solicitud"
    details: Any | None = None

    if isinstance(detail, str):
        message = detail
    elif isinstance(detail, dict):
        message = detail.get("message") or detail.get("detail") or message
        details = detail.get("details") or {k: v for k, v in detail.items() if k not in {"message", "detail"}}
    elif isinstance(detail, list):
        details = detail

    logger.warning("HTTP exception at %s: %s", request.url.path, message)
    return JSONResponse(
        status_code=exc.status_code,
        content=_format_error_response(request, exc.status_code, message, details),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Validation error at %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_format_error_response(
            request,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Input inválido",
            details=exc.errors(),
        ),
    )


async def unexpected_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unexpected error at %s", request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_format_error_response(
            request,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error interno del servidor",
            details=None,
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registra manejadores globales de excepciones en la aplicación."""

    app.add_exception_handler(BusinessRuleException, business_rule_exception_handler)
    app.add_exception_handler(NotFoundException, business_rule_exception_handler)
    app.add_exception_handler(AuthorizationException, business_rule_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
