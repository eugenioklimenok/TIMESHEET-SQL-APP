from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import aliased
from sqlmodel import Session, select

from app.models import Project, TimesheetHeader, TimesheetItem, User
from app.models.timesheet import TimesheetStatus


ALLOWED_STATUSES = [
    TimesheetStatus.DRAFT,
    TimesheetStatus.SUBMITTED,
    TimesheetStatus.APPROVED,
]


def aggregate_hours_by_user(
    session: Session, period_start: date, period_end: date, user_id: Optional[UUID] = None
):
    statement = (
        select(
            TimesheetHeader.user_id.label("user_id"),
            User.name.label("full_name"),
            func.coalesce(func.sum(TimesheetItem.hours), 0).label("total_hours"),
        )
        .select_from(TimesheetItem)
        .join(TimesheetHeader, TimesheetHeader.id == TimesheetItem.header_id)
        .join(User, User.id == TimesheetHeader.user_id)
        .where(
            TimesheetItem.date >= period_start,
            TimesheetItem.date <= period_end,
            TimesheetHeader.status.in_(ALLOWED_STATUSES),
        )
        .group_by(TimesheetHeader.user_id, User.name)
        .order_by(func.sum(TimesheetItem.hours).desc())
    )

    if user_id:
        statement = statement.where(TimesheetHeader.user_id == user_id)

    return session.exec(statement).all()


def aggregate_hours_by_project(
    session: Session,
    project_id: UUID,
    period_start: date,
    period_end: date,
    user_id: Optional[UUID] = None,
):
    project_alias = aliased(Project)
    statement = (
        select(
            TimesheetItem.project_id.label("project_id"),
            project_alias.name.label("project_name"),
            func.coalesce(func.sum(TimesheetItem.hours), 0).label("total_hours"),
        )
        .select_from(TimesheetItem)
        .join(TimesheetHeader, TimesheetHeader.id == TimesheetItem.header_id)
        .join(project_alias, project_alias.id == TimesheetItem.project_id)
        .where(
            TimesheetItem.project_id == project_id,
            TimesheetItem.date >= period_start,
            TimesheetItem.date <= period_end,
            TimesheetHeader.status.in_(ALLOWED_STATUSES),
        )
        .group_by(TimesheetItem.project_id, project_alias.name)
        .order_by(func.sum(TimesheetItem.hours).desc())
    )

    if user_id:
        statement = statement.where(TimesheetHeader.user_id == user_id)

    return session.exec(statement).all()


def aggregate_user_projects(
    session: Session, user_id: UUID, period_start: date, period_end: date
):
    project_alias = aliased(Project)
    statement = (
        select(
            TimesheetHeader.user_id.label("user_id"),
            TimesheetItem.project_id.label("project_id"),
            project_alias.name.label("project_name"),
            func.coalesce(func.sum(TimesheetItem.hours), 0).label("total_hours"),
        )
        .select_from(TimesheetItem)
        .join(TimesheetHeader, TimesheetHeader.id == TimesheetItem.header_id)
        .join(project_alias, project_alias.id == TimesheetItem.project_id)
        .where(
            TimesheetHeader.user_id == user_id,
            TimesheetItem.date >= period_start,
            TimesheetItem.date <= period_end,
            TimesheetHeader.status.in_(ALLOWED_STATUSES),
        )
        .group_by(TimesheetHeader.user_id, TimesheetItem.project_id, project_alias.name)
        .order_by(func.sum(TimesheetItem.hours).desc())
    )

    return session.exec(statement).all()


def summarize_hours_by_status(session: Session, period_start: date, period_end: date):
    statement = (
        select(
            TimesheetHeader.status.label("status"),
            func.coalesce(func.sum(TimesheetItem.hours), 0).label("total_hours"),
        )
        .select_from(TimesheetItem)
        .join(TimesheetHeader, TimesheetHeader.id == TimesheetItem.header_id)
        .where(
            TimesheetItem.date >= period_start,
            TimesheetItem.date <= period_end,
            TimesheetHeader.status.in_(ALLOWED_STATUSES),
        )
        .group_by(TimesheetHeader.status)
    )

    return session.exec(statement).all()
