from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import TimesheetHeader
from app.schemas import TimesheetCreate, TimesheetUpdate


def create(session: Session, timesheet_in: TimesheetCreate) -> TimesheetHeader:
    timesheet = TimesheetHeader(**timesheet_in.model_dump())
    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)
    return timesheet


def list_all(session: Session) -> List[TimesheetHeader]:
    return list(session.exec(select(TimesheetHeader)))


def get(session: Session, timesheet_id: UUID) -> Optional[TimesheetHeader]:
    return session.get(TimesheetHeader, timesheet_id)


def update(session: Session, timesheet: TimesheetHeader, timesheet_in: TimesheetUpdate) -> TimesheetHeader:
    update_data = timesheet_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(timesheet, field, value)
    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)
    return timesheet
