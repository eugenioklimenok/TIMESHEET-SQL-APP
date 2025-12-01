from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TimesheetBase(BaseModel):
    user_uuid: UUID
    project_uuid: UUID
    work_date: date
    status_id: Optional[int] = 0


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetRead(TimesheetBase):
    id: UUID
    created_at: Optional[datetime] = None


class TimesheetUpdate(BaseModel):
    work_date: Optional[date] = None
    status_id: Optional[int] = None
