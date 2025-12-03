from datetime import date
from uuid import UUID

from fastapi import status
from sqlmodel import Session

from app import crud
from app.core.errors import AuthorizationException, BusinessRuleException, NotFoundException
from app.models import User
from app.models.timesheet import TimesheetStatus
from app.schemas import (
    ProjectHoursReport,
    StatusSummary,
    SummaryReport,
    UserHoursReport,
    UserProjectHoursReport,
)


def _validate_period(period_start: date, period_end: date) -> None:
    if period_start > period_end:
        raise BusinessRuleException("El rango de fechas no es válido", status_code=status.HTTP_400_BAD_REQUEST)


def _ensure_admin_or_self(target_user_id: UUID, current_user: User) -> None:
    if current_user.role != "admin" and current_user.id != target_user_id:
        raise AuthorizationException("No tienes permiso para ver estos datos", status_code=status.HTTP_403_FORBIDDEN)


def _ensure_project_access(session: Session, project_id: UUID, current_user: User) -> None:
    project = crud.get_project_v2(session, project_id)
    if not project:
        raise NotFoundException("Proyecto no encontrado")

    if current_user.role == "admin":
        return

    membership = crud.get_membership(session, project_id, current_user.id)
    if not membership:
        raise AuthorizationException("No perteneces a este proyecto", status_code=status.HTTP_403_FORBIDDEN)


def get_user_hours_report(
    session: Session, period_start: date, period_end: date, current_user: User
) -> list[UserHoursReport]:
    _validate_period(period_start, period_end)

    user_filter = None if current_user.role == "admin" else current_user.id
    rows = crud.aggregate_hours_by_user(session, period_start, period_end, user_filter)

    if not rows:
        raise NotFoundException("No se encontraron horas en el período indicado")

    return [
        UserHoursReport(
            user_id=row.user_id,
            full_name=row.full_name,
            total_hours=float(row.total_hours or 0),
            period_start=period_start,
            period_end=period_end,
        )
        for row in rows
    ]


def get_project_hours_report(
    session: Session, project_id: UUID, period_start: date, period_end: date, current_user: User
) -> list[ProjectHoursReport]:
    _validate_period(period_start, period_end)
    _ensure_project_access(session, project_id, current_user)

    user_filter = None if current_user.role == "admin" else current_user.id
    rows = crud.aggregate_hours_by_project(session, project_id, period_start, period_end, user_filter)

    if not rows:
        raise NotFoundException("No se encontraron horas para este proyecto")

    return [
        ProjectHoursReport(
            project_id=row.project_id,
            project_name=row.project_name,
            total_hours=float(row.total_hours or 0),
            period_start=period_start,
            period_end=period_end,
        )
        for row in rows
    ]


def get_user_projects_report(
    session: Session, target_user_id: UUID, period_start: date, period_end: date, current_user: User
) -> list[UserProjectHoursReport]:
    _validate_period(period_start, period_end)
    _ensure_admin_or_self(target_user_id, current_user)

    user = crud.get_user(session, target_user_id)
    if not user:
        raise NotFoundException("Usuario no encontrado")

    rows = crud.aggregate_user_projects(session, target_user_id, period_start, period_end)
    if not rows:
        raise NotFoundException("No se encontraron horas para este usuario")

    return [
        UserProjectHoursReport(
            user_id=row.user_id,
            project_id=row.project_id,
            project_name=row.project_name,
            total_hours=float(row.total_hours or 0),
            period_start=period_start,
            period_end=period_end,
        )
        for row in rows
    ]


def get_status_summary(
    session: Session, period_start: date, period_end: date, current_user: User
) -> SummaryReport:
    _validate_period(period_start, period_end)

    if current_user.role != "admin":
        raise AuthorizationException(
            "Solo los administradores pueden ver el resumen", status_code=status.HTTP_403_FORBIDDEN
        )

    rows = crud.summarize_hours_by_status(session, period_start, period_end)
    if not rows:
        raise NotFoundException("No hay datos para este período")

    totals_map = {row.status: float(row.total_hours or 0) for row in rows}
    ordered_statuses = [TimesheetStatus.DRAFT, TimesheetStatus.SUBMITTED, TimesheetStatus.APPROVED]

    totals = [
        StatusSummary(status=status, total_hours=totals_map.get(status, 0.0))
        for status in ordered_statuses
    ]

    return SummaryReport(totals_by_status=totals)
