from typing import Any, Optional
from uuid import UUID

from fastapi import status
from sqlmodel import Session

from app import crud
from app.core.errors import AuthorizationException, BusinessRuleException, NotFoundException
from app.models import Project, User
from app.schemas import ProjectCreate, ProjectMemberCreate, ProjectUpdate


def _require_admin(user: User) -> None:
    if user.role != "admin":
        raise AuthorizationException(
            "Only admins can perform this action", status_code=status.HTTP_403_FORBIDDEN
        )


def _get_project_or_404(session: Session, project_id: UUID) -> Project:
    project = crud.get_project_v2(session, project_id)
    if not project:
        raise NotFoundException("Project not found")
    return project


def _get_ordering(ordering: Optional[str]) -> Any:
    column_map = {
        "created_at": Project.created_at,
        "updated_at": Project.updated_at,
        "name": Project.name,
        "code": Project.code,
    }
    value = ordering or "-created_at"
    descending = value.startswith("-")
    column = column_map.get(value.lstrip("-"), Project.created_at)
    return column.desc() if descending else column.asc()


def create_project(session: Session, current_user: User, project_in: ProjectCreate) -> Project:
    _require_admin(current_user)
    return crud.create_project_v2(session, project_in)


def list_projects(
    session: Session,
    current_user: User,
    limit: int,
    offset: int,
    ordering: Optional[str],
) -> tuple[list[Project], int]:
    order_by = _get_ordering(ordering)
    return crud.list_projects_v2(session, current_user, limit, offset, order_by)


def get_project(session: Session, current_user: User, project_id: UUID) -> Project:
    project = _get_project_or_404(session, project_id)
    if current_user.role != "admin":
        membership = crud.get_membership(session, project_id, current_user.id)
        if not membership:
            raise AuthorizationException(
                "Not authorized to view this project", status_code=status.HTTP_403_FORBIDDEN
            )
    return project


def update_project(
    session: Session, current_user: User, project_id: UUID, project_in: ProjectUpdate
) -> Project:
    _require_admin(current_user)
    project = _get_project_or_404(session, project_id)
    return crud.update_project_v2(session, project, project_in)


def delete_project(session: Session, current_user: User, project_id: UUID) -> None:
    _require_admin(current_user)
    project = _get_project_or_404(session, project_id)
    crud.delete_project_v2(session, project)


def add_member(
    session: Session, current_user: User, project_id: UUID, member_in: ProjectMemberCreate
) -> None:
    _require_admin(current_user)
    project = _get_project_or_404(session, project_id)

    user = crud.get_user(session, member_in.user_id)
    if not user:
        raise NotFoundException("User not found")

    if crud.get_membership(session, project_id, member_in.user_id):
        raise BusinessRuleException(
            "User already assigned to this project",
            status_code=status.HTTP_409_CONFLICT,
            details={"user_id": str(member_in.user_id)},
        )

    crud.add_member(session, project, member_in)


def list_members(session: Session, current_user: User, project_id: UUID):
    project = _get_project_or_404(session, project_id)
    if current_user.role != "admin":
        membership = crud.get_membership(session, project_id, current_user.id)
        if not membership:
            raise AuthorizationException(
                "Not authorized to view members", status_code=status.HTTP_403_FORBIDDEN
            )

    return crud.list_members(session, project_id)


def remove_member(session: Session, current_user: User, project_id: UUID, user_id: UUID) -> None:
    _require_admin(current_user)
    _get_project_or_404(session, project_id)

    membership = crud.get_membership(session, project_id, user_id)
    if not membership:
        raise NotFoundException("User not found in this project")

    crud.remove_member(session, membership)
