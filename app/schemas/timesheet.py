from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class TimesheetBase(BaseModel):
    project_id: int
    start_date: date
    end_date: date
    hours_worked: float = Field(gt=0)


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetRead(TimesheetBase):
    id: int


class TimesheetUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    hours_worked: Optional[float] = Field(default=None, gt=0)
