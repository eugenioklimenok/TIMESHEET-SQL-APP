from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.dependencies import get_session
from app.core.security import get_current_user, role_required
from app.models import User
from app.schemas import (
    ProjectHoursReport,
    SummaryReport,
    UserHoursReport,
    UserProjectHoursReport,
)
from app.services import reports as report_service

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.get("/user-hours", response_model=list[UserHoursReport])
def get_user_hours(
    period_start: date = Query(..., alias="from"),
    period_end: date = Query(..., alias="to"),
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> list[UserHoursReport]:
    return report_service.get_user_hours_report(session, period_start, period_end, current_user)


@router.get("/project-hours/{project_id}", response_model=list[ProjectHoursReport])
def get_project_hours(
    project_id: UUID,
    period_start: date = Query(..., alias="from"),
    period_end: date = Query(..., alias="to"),
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> list[ProjectHoursReport]:
    return report_service.get_project_hours_report(session, project_id, period_start, period_end, current_user)


@router.get("/user/{user_id}/projects", response_model=list[UserProjectHoursReport])
def get_user_project_hours(
    user_id: UUID,
    period_start: date = Query(..., alias="from"),
    period_end: date = Query(..., alias="to"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[UserProjectHoursReport]:
    return report_service.get_user_projects_report(session, user_id, period_start, period_end, current_user)


@router.get("/summary", response_model=SummaryReport)
def get_summary(
    period_start: date = Query(..., alias="from"),
    period_end: date = Query(..., alias="to"),
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin")),
) -> SummaryReport:
    return report_service.get_status_summary(session, period_start, period_end, current_user)
