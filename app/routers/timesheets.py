from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app import crud
from app.core.dependencies import get_session
from app.core.security import role_required
from app.models import User
from app.services import timesheets as timesheet_service
from app.schemas import TimesheetCreate, TimesheetItemCreate, TimesheetItemRead, TimesheetRead, TimesheetUpdate

router = APIRouter(
    prefix="/timesheets",
    tags=["timesheets"],
)


@router.post("/", response_model=TimesheetRead, status_code=201)
def create_timesheet(
    timesheet_in: TimesheetCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> TimesheetRead:
    timesheet = timesheet_service.create_timesheet(session, current_user, timesheet_in)
    return TimesheetRead.model_validate(timesheet)


@router.get("/", response_model=List[TimesheetRead])
def list_timesheets(
    session: Session = Depends(get_session), current_user: User = Depends(role_required("admin", "user"))
) -> List[TimesheetRead]:
    timesheets = timesheet_service.list_timesheets(session, current_user)
    return [TimesheetRead.model_validate(timesheet) for timesheet in timesheets]


@router.get("/{timesheet_id}", response_model=TimesheetRead)
def get_timesheet(
    timesheet_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> TimesheetRead:
    timesheet = timesheet_service.get_timesheet(session, timesheet_id, current_user)
    return TimesheetRead.model_validate(timesheet)


@router.put("/{timesheet_id}", response_model=TimesheetRead)
def update_timesheet(
    timesheet_id: UUID,
    timesheet_in: TimesheetUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> TimesheetRead:
    updated_timesheet = timesheet_service.update_timesheet(session, timesheet_id, timesheet_in, current_user)
    return TimesheetRead.model_validate(updated_timesheet)


@router.delete("/{timesheet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_timesheet(
    timesheet_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> None:
    timesheet_service.delete_timesheet(session, timesheet_id, current_user)


@router.post("/{timesheet_id}/items", response_model=TimesheetItemRead, status_code=status.HTTP_201_CREATED)
def create_timesheet_item(
    timesheet_id: UUID,
    item_in: TimesheetItemCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> TimesheetItemRead:
    timesheet_service.get_timesheet(session, timesheet_id, current_user)
    item = crud.create_item(session, timesheet_id, item_in)
    return TimesheetItemRead.model_validate(item)


@router.get("/{timesheet_id}/items", response_model=List[TimesheetItemRead])
def list_timesheet_items(
    timesheet_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> List[TimesheetItemRead]:
    timesheet_service.get_timesheet(session, timesheet_id, current_user)
    items = crud.list_items(session, header_uuid=timesheet_id)
    return [TimesheetItemRead.model_validate(item) for item in items]
