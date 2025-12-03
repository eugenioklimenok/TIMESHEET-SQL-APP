from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.dependencies import get_session
from app.core.validators import validate_date_range, validate_project_id, validate_user_id
from app.core.security import get_current_user, role_required
from app.models import User
from app.schemas import (
    DateRange,
    ErrorResponse,
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


common_error_responses = {
    401: {"model": ErrorResponse, "description": "No autenticado"},
    403: {"model": ErrorResponse, "description": "No autorizado"},
    404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
    422: {"model": ErrorResponse, "description": "Entrada inválida"},
}


@router.get(
    "/user-hours",
    response_model=list[UserHoursReport],
    responses=common_error_responses,
)
def get_user_hours(
    date_range: DateRange = Depends(validate_date_range),
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> list[UserHoursReport]:
    return report_service.get_user_hours_report(
        session, date_range.period_start, date_range.period_end, current_user
    )


@router.get(
    "/project-hours/{project_id}",
    response_model=list[ProjectHoursReport],
    responses=common_error_responses,
)
def get_project_hours(
    project_id: UUID = Depends(validate_project_id),
    date_range: DateRange = Depends(validate_date_range),
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin", "user")),
) -> list[ProjectHoursReport]:
    return report_service.get_project_hours_report(
        session, project_id, date_range.period_start, date_range.period_end, current_user
    )


@router.get(
    "/user/{user_id}/projects",
    response_model=list[UserProjectHoursReport],
    responses=common_error_responses,
)
def get_user_project_hours(
    user_id: UUID = Depends(validate_user_id),
    date_range: DateRange = Depends(validate_date_range),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[UserProjectHoursReport]:
    return report_service.get_user_projects_report(
        session, user_id, date_range.period_start, date_range.period_end, current_user
    )


@router.get(
    "/summary",
    response_model=SummaryReport,
    responses=common_error_responses,
)
def get_summary(
    date_range: DateRange = Depends(validate_date_range),
    session: Session = Depends(get_session),
    current_user: User = Depends(role_required("admin")),
) -> SummaryReport:
    return report_service.get_status_summary(
        session, date_range.period_start, date_range.period_end, current_user
    )
