from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.timesheet import TimesheetStatus


class TimesheetItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: UUID
    date: date
    description: str
    hours: float


class TimesheetItemCreate(TimesheetItemBase):
    pass


class TimesheetItemUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: Optional[UUID] = None
    date: Optional[date] = None
    description: Optional[str] = None
    hours: Optional[float] = None


class TimesheetItemRead(TimesheetItemBase):
    id: UUID
    header_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TimesheetBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    period_start: date
    period_end: date


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetRead(TimesheetBase):
    id: UUID
    user_id: UUID
    status: TimesheetStatus
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TimesheetUpdate(BaseModel):
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    status: Optional[TimesheetStatus] = None


class TimesheetDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    owner: UUID = Field(alias="user_id")
    status: TimesheetStatus
    period_start: date
    period_end: date
    items: list[TimesheetItemRead] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TimesheetActionResponse(BaseModel):
    success: bool
    timesheet: TimesheetDetail
