from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Timesheet(SQLModel, table=True):
    __tablename__ = "timesheets"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(index=True, nullable=False)
    start_date: date = Field(nullable=False)
    end_date: date = Field(nullable=False)
    hours_worked: float = Field(nullable=False, ge=0)
