from __future__ import annotations

from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlmodel import Session, select

from app.models import Project, User, UserProjectMembership
from app.schemas.project import ProjectCreate, ProjectMemberCreate, ProjectUpdate


def get_project(session: Session, project_id: UUID) -> Optional[Project]:
    return session.get(Project, project_id)


def get_project_by_code(session: Session, code: str) -> Optional[Project]:
    return session.exec(select(Project).where(Project.code == code)).first()


def list_projects(
    session: Session,
    current_user: User,
    limit: int,
    offset: int,
    order_by: Any,
) -> tuple[List[Project], int]:
    base_query = select(Project)

    if current_user.role != "admin":
        base_query = (
            base_query.join(UserProjectMembership, UserProjectMembership.project_id == Project.id)
            .where(UserProjectMembership.user_id == current_user.id)
            .distinct()
        )

    total_query = select(func.count()).select_from(base_query.subquery())
    total_result = session.exec(total_query).one()
    total = total_result[0] if isinstance(total_result, tuple) else total_result

    projects = session.exec(base_query.order_by(order_by).offset(offset).limit(limit)).all()
    return projects, total


def create_project(session: Session, project_in: ProjectCreate) -> Project:
    project_data = project_in.model_dump()
    project_data["project_id"] = project_in.code
    project = Project(**project_data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def update_project(session: Session, project: Project, project_in: ProjectUpdate) -> Project:
    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
        if field == "code":
            project.project_id = value
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)
    session.commit()


def add_member(session: Session, project: Project, membership_in: ProjectMemberCreate) -> UserProjectMembership:
    membership = UserProjectMembership(**membership_in.model_dump(), project_id=project.id)
    session.add(membership)
    session.commit()
    session.refresh(membership)
    return membership


def get_membership(session: Session, project_id: UUID, user_id: UUID) -> Optional[UserProjectMembership]:
    return session.get(UserProjectMembership, (user_id, project_id))


def list_members(session: Session, project_id: UUID) -> List[tuple[UserProjectMembership, User]]:
    statement = (
        select(UserProjectMembership, User)
        .join(User, User.id == UserProjectMembership.user_id)
        .where(UserProjectMembership.project_id == project_id)
    )
    return session.exec(statement).all()


def remove_member(session: Session, membership: UserProjectMembership) -> None:
    session.delete(membership)
    session.commit()
