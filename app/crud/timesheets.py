from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import TimesheetHeader, TimesheetItem
from app.models.timesheet import TimesheetStatus
from app.schemas import TimesheetCreate, TimesheetItemCreate, TimesheetItemUpdate, TimesheetUpdate


# Timesheet headers

def list_timesheets(session: Session, user_id: Optional[UUID] = None) -> List[TimesheetHeader]:
    statement = select(TimesheetHeader)
    if user_id:
        statement = statement.where(TimesheetHeader.user_id == user_id)
    return list(session.exec(statement))


def get_timesheet(session: Session, timesheet_id: UUID) -> Optional[TimesheetHeader]:
    return session.get(TimesheetHeader, timesheet_id)


def find_overlapping_timesheet(
    session: Session, user_id: UUID, period_start: date, period_end: date, exclude_id: Optional[UUID] = None
) -> Optional[TimesheetHeader]:
    statement = select(TimesheetHeader).where(
        TimesheetHeader.user_id == user_id,
        TimesheetHeader.period_start <= period_end,
        TimesheetHeader.period_end >= period_start,
    )
    if exclude_id:
        statement = statement.where(TimesheetHeader.id != exclude_id)
    return session.exec(statement).first()


def create_timesheet(session: Session, user_id: UUID, timesheet_in: TimesheetCreate) -> TimesheetHeader:
    timesheet = TimesheetHeader(user_id=user_id, status=TimesheetStatus.DRAFT, **timesheet_in.model_dump())
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

def list_items(session: Session, header_id: Optional[UUID] = None) -> List[TimesheetItem]:
    statement = select(TimesheetItem)
    if header_id:
        statement = statement.where(TimesheetItem.header_id == header_id)
    return list(session.exec(statement))


def get_item(session: Session, item_uuid: UUID) -> Optional[TimesheetItem]:
    return session.get(TimesheetItem, item_uuid)


def create_item(session: Session, header_id: UUID, item_in: TimesheetItemCreate) -> TimesheetItem:
    item = TimesheetItem(header_id=header_id, **item_in.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def update_item(session: Session, item: TimesheetItem, item_in: TimesheetItemCreate | TimesheetItemUpdate) -> TimesheetItem:
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def delete_item(session: Session, item: TimesheetItem) -> None:
    session.delete(item)
    session.commit()
