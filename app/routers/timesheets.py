from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import crud
from app.core.dependencies import get_session
from app.schemas import TimesheetCreate, TimesheetItemCreate, TimesheetItemRead, TimesheetRead, TimesheetUpdate

router = APIRouter(prefix="/timesheets", tags=["timesheets"])


@router.post("/", response_model=TimesheetRead, status_code=201)
def create_timesheet(timesheet_in: TimesheetCreate, session: Session = Depends(get_session)) -> TimesheetRead:
    timesheet = crud.create_timesheet(session, timesheet_in)
    return TimesheetRead.model_validate(timesheet)


@router.get("/", response_model=List[TimesheetRead])
def list_timesheets(session: Session = Depends(get_session)) -> List[TimesheetRead]:
    timesheets = crud.list_timesheets(session)
    return [TimesheetRead.model_validate(timesheet) for timesheet in timesheets]


@router.get("/{timesheet_id}", response_model=TimesheetRead)
def get_timesheet(timesheet_id: UUID, session: Session = Depends(get_session)) -> TimesheetRead:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parte de horas no encontrado")
    return TimesheetRead.model_validate(timesheet)


@router.patch("/{timesheet_id}", response_model=TimesheetRead)
def update_timesheet(
    timesheet_id: UUID, timesheet_in: TimesheetUpdate, session: Session = Depends(get_session)
) -> TimesheetRead:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=404, detail="Parte de horas no encontrado")
    updated_timesheet = crud.update_timesheet(session, timesheet, timesheet_in)
    return TimesheetRead.model_validate(updated_timesheet)


@router.delete("/{timesheet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_timesheet(timesheet_id: UUID, session: Session = Depends(get_session)) -> None:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parte de horas no encontrado")
    crud.delete_timesheet(session, timesheet)


@router.post("/{timesheet_id}/items", response_model=TimesheetItemRead, status_code=status.HTTP_201_CREATED)
def create_timesheet_item(
    timesheet_id: UUID, item_in: TimesheetItemCreate, session: Session = Depends(get_session)
) -> TimesheetItemRead:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parte de horas no encontrado")

    item = crud.create_item(session, timesheet_id, item_in)
    return TimesheetItemRead.model_validate(item)


@router.get("/{timesheet_id}/items", response_model=List[TimesheetItemRead])
def list_timesheet_items(timesheet_id: UUID, session: Session = Depends(get_session)) -> List[TimesheetItemRead]:
    timesheet = crud.get_timesheet(session, timesheet_id)
    if not timesheet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parte de horas no encontrado")

    items = crud.list_items(session, header_uuid=timesheet_id)
    return [TimesheetItemRead.model_validate(item) for item in items]
