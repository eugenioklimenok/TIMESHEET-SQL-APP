from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import TimesheetHeader, TimesheetItem
from app.schemas import TimesheetCreate, TimesheetItemCreate, TimesheetUpdate


# Timesheet headers

def list_timesheets(session: Session) -> List[TimesheetHeader]:
    return list(session.exec(select(TimesheetHeader)))


def get_timesheet(session: Session, timesheet_id: UUID) -> Optional[TimesheetHeader]:
    return session.get(TimesheetHeader, timesheet_id)


def create_timesheet(session: Session, timesheet_in: TimesheetCreate) -> TimesheetHeader:
    timesheet = TimesheetHeader(**timesheet_in.model_dump())
    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)
    return timesheet


def update_timesheet(
    session: Session, timesheet: TimesheetHeader, timesheet_in: TimesheetUpdate
) -> TimesheetHeader:
    update_data = timesheet_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(timesheet, field, value)
    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)
    return timesheet


def delete_timesheet(session: Session, timesheet: TimesheetHeader) -> None:
    session.delete(timesheet)
    session.commit()


# Timesheet items

def list_items(session: Session, header_uuid: Optional[UUID] = None) -> List[TimesheetItem]:
    statement = select(TimesheetItem)
    if header_uuid:
        statement = statement.where(TimesheetItem.header_uuid == header_uuid)
    return list(session.exec(statement))


def get_item(session: Session, item_uuid: UUID) -> Optional[TimesheetItem]:
    return session.get(TimesheetItem, item_uuid)


def create_item(session: Session, header_uuid: UUID, item_in: TimesheetItemCreate) -> TimesheetItem:
    item = TimesheetItem(header_uuid=header_uuid, **item_in.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def delete_item(session: Session, item: TimesheetItem) -> None:
    session.delete(item)
    session.commit()
