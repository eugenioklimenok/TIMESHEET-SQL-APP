from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session

from app import crud
from app.models import TimesheetHeader, User
from app.models.timesheet import TimesheetStatus
from app.schemas import TimesheetCreate, TimesheetUpdate


def _validate_period(period_start, period_end) -> None:
    if period_start and period_end and period_start > period_end:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El periodo no es válido")


def _validate_transition(current_status: TimesheetStatus, new_status: TimesheetStatus | None) -> None:
    if new_status is None:
        return

    allowed = {
        TimesheetStatus.DRAFT: {TimesheetStatus.DRAFT, TimesheetStatus.SUBMITTED},
        TimesheetStatus.SUBMITTED: {TimesheetStatus.SUBMITTED, TimesheetStatus.APPROVED},
        TimesheetStatus.APPROVED: {TimesheetStatus.APPROVED},
    }
    if new_status not in allowed[current_status]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transición de estado inválida")


def _ensure_owner_or_admin(timesheet: TimesheetHeader, current_user: User) -> None:
    if current_user.role != "admin" and timesheet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el propietario o un admin puede acceder a este parte de horas",
        )


def create_timesheet(session: Session, current_user: User, timesheet_in: TimesheetCreate) -> TimesheetHeader:
    _validate_period(timesheet_in.period_start, timesheet_in.period_end)

    overlapping = crud.find_overlapping_timesheet(
        session, current_user.id, timesheet_in.period_start, timesheet_in.period_end
    )
    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un parte de horas para ese periodo",
        )

    return crud.create_timesheet(session, current_user.id, timesheet_in)


def list_timesheets(session: Session, current_user: User) -> list[TimesheetHeader]:
    user_id = None if current_user.role == "admin" else current_user.id
    return crud.list_timesheets(session, user_id=user_id)


def get_timesheet(session: Session, timesheet_id: UUID, current_user: User) -> TimesheetHeader:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parte de horas no encontrado")
    _ensure_owner_or_admin(timesheet, current_user)
    return timesheet


def update_timesheet(
    session: Session, timesheet_id: UUID, timesheet_in: TimesheetUpdate, current_user: User
) -> TimesheetHeader:
    timesheet = get_timesheet(session, timesheet_id, current_user)

    target_status = timesheet_in.status or timesheet.status
    _validate_transition(timesheet.status, timesheet_in.status)

    if timesheet.status != TimesheetStatus.DRAFT and not (
        timesheet.status == TimesheetStatus.SUBMITTED and timesheet_in.status == TimesheetStatus.APPROVED
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo puedes actualizar partes en Draft")

    new_period_start = timesheet_in.period_start or timesheet.period_start
    new_period_end = timesheet_in.period_end or timesheet.period_end
    _validate_period(new_period_start, new_period_end)

    overlapping = crud.find_overlapping_timesheet(
        session, timesheet.user_id, new_period_start, new_period_end, exclude_id=timesheet.id
    )
    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El periodo se solapa con otro parte de horas",
        )

    update_data = timesheet_in.model_dump(exclude_unset=True)
    if "status" not in update_data:
        update_data["status"] = target_status

    updated_timesheet = crud.update_timesheet(session, timesheet, TimesheetUpdate(**update_data))
    return updated_timesheet


def delete_timesheet(session: Session, timesheet_id: UUID, current_user: User) -> None:
    timesheet = get_timesheet(session, timesheet_id, current_user)
    if timesheet.status != TimesheetStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo puedes eliminar partes en estado Draft",
        )
    crud.delete_timesheet(session, timesheet)
