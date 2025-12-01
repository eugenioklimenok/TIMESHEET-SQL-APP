from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud
from app.core.database import get_session
from app.schemas import TimesheetCreate, TimesheetRead, TimesheetUpdate

router = APIRouter(prefix="/timesheets", tags=["timesheets"])


@router.post("/", response_model=TimesheetRead, status_code=201)
def create_timesheet(timesheet_in: TimesheetCreate, session: Session = Depends(get_session)) -> TimesheetRead:
    timesheet = crud.create_timesheet(session, timesheet_in)
    return TimesheetRead.model_validate(timesheet)


@router.get("/", response_model=List[TimesheetRead])
def list_timesheets(session: Session = Depends(get_session)) -> List[TimesheetRead]:
    timesheets = crud.list_timesheets(session)
    return [TimesheetRead.model_validate(timesheet) for timesheet in timesheets]


@router.patch("/{timesheet_id}", response_model=TimesheetRead)
def update_timesheet(
    timesheet_id: UUID, timesheet_in: TimesheetUpdate, session: Session = Depends(get_session)
) -> TimesheetRead:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=404, detail="Parte de horas no encontrado")
    updated_timesheet = crud.update_timesheet(session, timesheet, timesheet_in)
    return TimesheetRead.model_validate(updated_timesheet)
