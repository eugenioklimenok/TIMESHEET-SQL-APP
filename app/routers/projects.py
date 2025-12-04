from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.dependencies import get_session
from app.core.security import get_current_user, role_required
from app.models import User
from app.schemas import (
    ErrorResponse,
    ProjectCreate,
    ProjectListResponse,
    ProjectMemberCreate,
    ProjectMemberList,
    ProjectMemberRead,
    ProjectRead,
    ProjectUpdate,
)
from app.services import projects as project_service

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    dependencies=[Depends(role_required("admin", "user"))],
)


project_error_responses = {
    400: {"model": ErrorResponse, "description": "Error de validación"},
    401: {"model": ErrorResponse, "description": "No autenticado"},
    403: {"model": ErrorResponse, "description": "No autorizado"},
    404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
    409: {"model": ErrorResponse, "description": "Conflicto de negocio"},
    422: {"model": ErrorResponse, "description": "Entrada inválida"},
}


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED, responses=project_error_responses)
def create_project(
    project_in: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    project = project_service.create_project(session, current_user, project_in)
    return ProjectRead.model_validate(project)


@router.get("/", response_model=ProjectListResponse, responses=project_error_responses)
def list_projects(
    limit: int = Query(25, gt=0),
    offset: int = Query(0, ge=0),
    ordering: Optional[str] = Query("-created_at"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectListResponse:
    projects, total = project_service.list_projects(
        session, current_user, limit, offset, ordering
    )
    return ProjectListResponse(
        results=[ProjectRead.model_validate(project) for project in projects],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{project_id}", response_model=ProjectRead, responses=project_error_responses)
def get_project(
    project_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    project = project_service.get_project(session, current_user, project_id)
    return ProjectRead.model_validate(project)


@router.put("/{project_id}", response_model=ProjectRead, responses=project_error_responses)
def update_project(
    project_id: UUID,
    project_in: ProjectUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    updated = project_service.update_project(session, current_user, project_id, project_in)
    return ProjectRead.model_validate(updated)


@router.delete(
    "/{project_id}", status_code=status.HTTP_204_NO_CONTENT, responses=project_error_responses
)
def delete_project(
    project_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    project_service.delete_project(session, current_user, project_id)


@router.post(
    "/{project_id}/members",
    status_code=status.HTTP_201_CREATED,
    responses=project_error_responses,
)
def add_member(
    project_id: UUID,
    member_in: ProjectMemberCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    project_service.add_member(session, current_user, project_id, member_in)
    return {"detail": "User added"}


@router.get("/{project_id}/members", response_model=ProjectMemberList, responses=project_error_responses)
def list_members(
    project_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectMemberList:
    memberships = project_service.list_members(session, current_user, project_id)
    results = [
        ProjectMemberRead(
            user_id=membership.user_id,
            role_in_project=membership.role_in_project,
            username=user.name or user.user_id,
            email=user.email,
        )
        for membership, user in memberships
    ]
    return ProjectMemberList(results=results, total=len(results))


@router.delete(
    "/{project_id}/members/{user_id}",
    status_code=status.HTTP_200_OK,
    responses=project_error_responses,
)
def remove_member(
    project_id: UUID,
    user_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    project_service.remove_member(session, current_user, project_id, user_id)
    return {"detail": "User removed"}
