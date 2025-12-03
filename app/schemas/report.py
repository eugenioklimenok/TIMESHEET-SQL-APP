from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.timesheet import TimesheetStatus


class UserHoursReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    full_name: str | None = None
    total_hours: float
    period_start: date
    period_end: date


class ProjectHoursReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: UUID
    project_name: str | None = None
    total_hours: float
    period_start: date
    period_end: date


class UserProjectHoursReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    project_id: UUID
    project_name: str | None = None
    total_hours: float
    period_start: date
    period_end: date


class StatusSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: TimesheetStatus
    total_hours: float


class SummaryReport(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    totals_by_status: list[StatusSummary]
