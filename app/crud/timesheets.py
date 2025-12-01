from typing import List

from sqlmodel import Session, select

from app.models import Timesheet
from app.schemas import TimesheetCreate, TimesheetUpdate


def create(session: Session, timesheet_in: TimesheetCreate) -> Timesheet:
    timesheet = Timesheet(**timesheet_in.model_dump())
    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)
    return timesheet


def list_all(session: Session) -> List[Timesheet]:
    return list(session.exec(select(Timesheet)))


def update(session: Session, timesheet: Timesheet, timesheet_in: TimesheetUpdate) -> Timesheet:
    update_data = timesheet_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(timesheet, field, value)
    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)
    return timesheet
