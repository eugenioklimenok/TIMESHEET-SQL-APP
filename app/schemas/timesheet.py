from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TimesheetStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TimesheetItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description: str
    hours: float
    billable: Optional[bool] = True


class TimesheetItemCreate(TimesheetItemBase):
    pass


class TimesheetItemRead(TimesheetItemBase):
    id: UUID
    header_uuid: UUID
    created_at: Optional[datetime] = None


class TimesheetBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_uuid: UUID
    project_uuid: UUID
    work_date: date
    status_id: Optional[int] = 0


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetRead(TimesheetBase):
    id: UUID
    created_at: Optional[datetime] = None
    status: Optional[TimesheetStatusRead] = None


class TimesheetUpdate(BaseModel):
    work_date: Optional[date] = None
    status_id: Optional[int] = None
