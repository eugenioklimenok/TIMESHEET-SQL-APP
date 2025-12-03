import logging
from datetime import date
from uuid import UUID

from fastapi import status
from sqlalchemy import func
from sqlmodel import Session, select

from app import crud
from app.core.errors import AuthorizationException, BusinessRuleException, NotFoundException
from app.models import TimesheetHeader, TimesheetItem, User
from app.models.timesheet import TimesheetStatus
from app.schemas import (
    TimesheetActionResponse,
    TimesheetCreate,
    TimesheetDetail,
    TimesheetItemCreate,
    TimesheetItemUpdate,
    TimesheetUpdate,
)


logger = logging.getLogger(__name__)


def _validate_period(period_start, period_end) -> None:
    if period_start and period_end and period_start > period_end:
        raise BusinessRuleException("El periodo no es válido", status_code=status.HTTP_400_BAD_REQUEST)


def _build_action_response(timesheet: TimesheetHeader) -> TimesheetActionResponse:
    return TimesheetActionResponse(
        success=True,
        timesheet=TimesheetDetail.model_validate(timesheet),
    )


def _ensure_owner_or_admin(timesheet: TimesheetHeader, current_user: User) -> None:
    if current_user.role != "admin" and timesheet.user_id != current_user.id:
        raise AuthorizationException(
            "Solo el propietario o un admin puede acceder a este parte de horas",
            status_code=status.HTTP_403_FORBIDDEN,
        )


def _ensure_project_membership(session: Session, project_id: UUID, current_user: User) -> None:
    if current_user.role == "admin":
        return

    membership = crud.get_membership(session, project_id, current_user.id)
    if not membership:
        raise AuthorizationException("No perteneces al proyecto asignado", status_code=status.HTTP_403_FORBIDDEN)


def _ensure_header_modifiable(timesheet: TimesheetHeader) -> None:
    if timesheet.status != TimesheetStatus.DRAFT:
        raise BusinessRuleException(
            "Solo puedes modificar ítems cuando el parte está en Draft",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def _ensure_date_in_period(timesheet: TimesheetHeader, item_date: date) -> None:
    if item_date < timesheet.period_start or item_date > timesheet.period_end:
        raise BusinessRuleException(
            "La fecha del ítem debe estar dentro del período del parte",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def _validate_hours_value(hours: float) -> None:
    if hours <= 0 or hours > 24:
        raise BusinessRuleException(
            "Las horas deben ser mayores a 0 y no exceder 24",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def _validate_daily_total(
    session: Session, timesheet: TimesheetHeader, item_date: date, hours: float, exclude_id: UUID | None = None
) -> None:
    statement = (
        select(func.coalesce(func.sum(TimesheetItem.hours), 0))
        .where(TimesheetItem.header_id == timesheet.id)
        .where(TimesheetItem.date == item_date)
    )
    if exclude_id:
        statement = statement.where(TimesheetItem.id != exclude_id)

    current_total = float(session.exec(statement).first() or 0)
    if current_total + hours > 24:
        raise BusinessRuleException(
            "El total de horas por día no puede exceder 24",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def create_timesheet(session: Session, current_user: User, timesheet_in: TimesheetCreate) -> TimesheetHeader:
    _validate_period(timesheet_in.period_start, timesheet_in.period_end)

    overlapping = crud.find_overlapping_timesheet(
        session, current_user.id, timesheet_in.period_start, timesheet_in.period_end
    )
    if overlapping:
        raise BusinessRuleException(
            "Ya existe un parte de horas para ese periodo",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return crud.create_timesheet(session, current_user.id, timesheet_in)


def list_timesheets(session: Session, current_user: User) -> list[TimesheetHeader]:
    user_id = None if current_user.role == "admin" else current_user.id
    return crud.list_timesheets(session, user_id=user_id)


def get_timesheet(session: Session, timesheet_id: UUID, current_user: User) -> TimesheetHeader:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise NotFoundException("Parte de horas no encontrado")
    _ensure_owner_or_admin(timesheet, current_user)
    return timesheet


def update_timesheet(
    session: Session, timesheet_id: UUID, timesheet_in: TimesheetUpdate, current_user: User
) -> TimesheetHeader:
    timesheet = get_timesheet(session, timesheet_id, current_user)

    if timesheet_in.status is not None:
        raise BusinessRuleException(
            "Las transiciones de estado deben usar los endpoints dedicados",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if timesheet.status != TimesheetStatus.DRAFT:
        raise BusinessRuleException(
            "Solo puedes actualizar partes en Draft", status_code=status.HTTP_400_BAD_REQUEST
        )

    new_period_start = timesheet_in.period_start or timesheet.period_start
    new_period_end = timesheet_in.period_end or timesheet.period_end
    _validate_period(new_period_start, new_period_end)

    overlapping = crud.find_overlapping_timesheet(
        session, timesheet.user_id, new_period_start, new_period_end, exclude_id=timesheet.id
    )
    if overlapping:
        raise BusinessRuleException(
            "El periodo se solapa con otro parte de horas",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    update_data = timesheet_in.model_dump(exclude_unset=True)
    updated_timesheet = crud.update_timesheet(session, timesheet, TimesheetUpdate(**update_data))
    return updated_timesheet


def delete_timesheet(session: Session, timesheet_id: UUID, current_user: User) -> None:
    timesheet = get_timesheet(session, timesheet_id, current_user)
    if timesheet.status != TimesheetStatus.DRAFT:
        raise BusinessRuleException(
            "Solo puedes eliminar partes en estado Draft", status_code=status.HTTP_400_BAD_REQUEST
        )
    crud.delete_timesheet(session, timesheet)


def submit_timesheet(
    session: Session, timesheet_id: UUID, current_user: User
) -> TimesheetActionResponse:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise NotFoundException("Parte de horas no encontrado")

    if timesheet.user_id != current_user.id:
        raise AuthorizationException(
            "Solo el dueño puede enviar este parte de horas", status_code=status.HTTP_403_FORBIDDEN
        )

    if timesheet.status != TimesheetStatus.DRAFT:
        raise BusinessRuleException(
            "Solo los partes en Draft pueden enviarse", status_code=status.HTTP_409_CONFLICT
        )

    updated = crud.update_timesheet(
        session, timesheet, TimesheetUpdate(status=TimesheetStatus.SUBMITTED)
    )
    logger.info("Timesheet %s enviado por usuario %s", timesheet.id, current_user.id)
    refreshed = crud.get_timesheet(session, updated.id) or updated
    return _build_action_response(refreshed)


def approve_timesheet(
    session: Session, timesheet_id: UUID, current_user: User
) -> TimesheetActionResponse:
    if current_user.role != "admin":
        raise AuthorizationException(
            "Solo un admin puede aprobar partes de horas", status_code=status.HTTP_403_FORBIDDEN
        )

    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise NotFoundException("Parte de horas no encontrado")

    if timesheet.status != TimesheetStatus.SUBMITTED:
        raise BusinessRuleException(
            "Solo puedes aprobar partes en estado Submitted", status_code=status.HTTP_409_CONFLICT
        )

    updated = crud.update_timesheet(
        session, timesheet, TimesheetUpdate(status=TimesheetStatus.APPROVED)
    )
    logger.info("Timesheet %s aprobado por admin %s", timesheet.id, current_user.id)
    refreshed = crud.get_timesheet(session, updated.id) or updated
    return _build_action_response(refreshed)


def reject_timesheet(
    session: Session, timesheet_id: UUID, current_user: User
) -> TimesheetActionResponse:
    if current_user.role != "admin":
        raise AuthorizationException(
            "Solo un admin puede rechazar partes de horas", status_code=status.HTTP_403_FORBIDDEN
        )

    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise NotFoundException("Parte de horas no encontrado")

    if timesheet.status != TimesheetStatus.SUBMITTED:
        raise BusinessRuleException(
            "Solo puedes rechazar partes en estado Submitted", status_code=status.HTTP_409_CONFLICT
        )

    updated = crud.update_timesheet(
        session, timesheet, TimesheetUpdate(status=TimesheetStatus.REJECTED)
    )
    logger.info("Timesheet %s rechazado por admin %s", timesheet.id, current_user.id)
    refreshed = crud.get_timesheet(session, updated.id) or updated
    return _build_action_response(refreshed)


def create_timesheet_item(
    session: Session, timesheet_id: UUID, item_in: TimesheetItemCreate, current_user: User
) -> TimesheetItem:
    timesheet = get_timesheet(session, timesheet_id, current_user)
    _ensure_header_modifiable(timesheet)

    if not crud.get_project(session, item_in.project_id):
        raise NotFoundException("Proyecto no encontrado")

    _ensure_project_membership(session, item_in.project_id, current_user)
    _ensure_date_in_period(timesheet, item_in.date)
    _validate_hours_value(item_in.hours)
    _validate_daily_total(session, timesheet, item_in.date, item_in.hours)

    return crud.create_item(session, timesheet.id, item_in)


def list_timesheet_items(session: Session, timesheet_id: UUID, current_user: User) -> list[TimesheetItem]:
    timesheet = get_timesheet(session, timesheet_id, current_user)
    return crud.list_items(session, header_id=timesheet.id)


def get_timesheet_item(
    session: Session, timesheet_id: UUID, item_id: UUID, current_user: User
) -> TimesheetItem:
    timesheet = get_timesheet(session, timesheet_id, current_user)

    item = crud.get_item(session, item_id)
    if not item or item.header_id != timesheet.id:
        raise NotFoundException("Ítem no encontrado")

    return item


def update_timesheet_item(
    session: Session, timesheet_id: UUID, item_id: UUID, item_in: TimesheetItemUpdate, current_user: User
) -> TimesheetItem:
    timesheet = get_timesheet(session, timesheet_id, current_user)
    _ensure_header_modifiable(timesheet)

    item = crud.get_item(session, item_id)
    if not item or item.header_id != timesheet.id:
        raise NotFoundException("Ítem no encontrado")

    new_project_id = item_in.project_id or item.project_id
    new_date = item_in.date or item.date
    new_hours = float(item_in.hours) if item_in.hours is not None else float(item.hours)

    if not crud.get_project(session, new_project_id):
        raise NotFoundException("Proyecto no encontrado")

    _ensure_project_membership(session, new_project_id, current_user)
    _ensure_date_in_period(timesheet, new_date)
    _validate_hours_value(new_hours)
    _validate_daily_total(session, timesheet, new_date, new_hours, exclude_id=item.id)

    return crud.update_item(session, item, item_in)


def delete_timesheet_item(session: Session, timesheet_id: UUID, item_id: UUID, current_user: User) -> None:
    timesheet = get_timesheet(session, timesheet_id, current_user)
    _ensure_header_modifiable(timesheet)

    item = crud.get_item(session, item_id)
    if not item or item.header_id != timesheet.id:
        raise NotFoundException("Ítem no encontrado")

    crud.delete_item(session, item)
