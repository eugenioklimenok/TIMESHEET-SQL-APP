from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app import crud
from app.core.errors import AuthorizationException, BusinessRuleException, NotFoundException
from app.core.dependencies import get_session
from app.core.security import get_current_user, role_required
from app.models import Project, User
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


def _require_admin(user: User) -> None:
    if user.role != "admin":
        raise AuthorizationException("Only admins can perform this action", status_code=status.HTTP_403_FORBIDDEN)


def _get_ordering(ordering: Optional[str]):
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


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED, responses=project_error_responses)
def create_project(
    project_in: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    _require_admin(current_user)

    if crud.get_project_by_code(session, project_in.code):
        raise BusinessRuleException(
            "Project code already exists",
            status_code=status.HTTP_409_CONFLICT,
            details={"code": project_in.code},
        )

    project = crud.create_project_v2(session, project_in)
    return ProjectRead.model_validate(project)


@router.get("/", response_model=ProjectListResponse, responses=project_error_responses)
def list_projects(
    limit: int = Query(25, gt=0),
    offset: int = Query(0, ge=0),
    ordering: Optional[str] = Query("-created_at"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectListResponse:
    order_by = _get_ordering(ordering)
    projects, total = crud.list_projects_v2(session, current_user, limit, offset, order_by)
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
    project = crud.get_project_v2(session, project_id)
    if not project:
        raise NotFoundException("Project not found")

    if current_user.role != "admin":
        membership = crud.get_membership(session, project_id, current_user.id)
        if not membership:
            raise AuthorizationException("Not authorized to view this project", status_code=status.HTTP_403_FORBIDDEN)

    return ProjectRead.model_validate(project)


@router.put("/{project_id}", response_model=ProjectRead, responses=project_error_responses)
def update_project(
    project_id: UUID,
    project_in: ProjectUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    _require_admin(current_user)

    project = crud.get_project_v2(session, project_id)
    if not project:
        raise NotFoundException("Project not found")

    if project_in.code:
        existing = crud.get_project_by_code(session, project_in.code)
        if existing and existing.id != project_id:
            raise BusinessRuleException(
                "Project code already exists",
                status_code=status.HTTP_409_CONFLICT,
                details={"code": project_in.code},
            )

    updated = crud.update_project_v2(session, project, project_in)
    return ProjectRead.model_validate(updated)


@router.delete(
    "/{project_id}", status_code=status.HTTP_204_NO_CONTENT, responses=project_error_responses
)
def delete_project(
    project_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    _require_admin(current_user)

    project = crud.get_project_v2(session, project_id)
    if not project:
        raise NotFoundException("Project not found")

    crud.delete_project_v2(session, project)


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
    _require_admin(current_user)

    project = crud.get_project_v2(session, project_id)
    if not project:
        raise NotFoundException("Project not found")

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
    return {"detail": "User added"}


@router.get("/{project_id}/members", response_model=ProjectMemberList, responses=project_error_responses)
def list_members(
    project_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectMemberList:
    project = crud.get_project_v2(session, project_id)
    if not project:
        raise NotFoundException("Project not found")

    if current_user.role != "admin":
        membership = crud.get_membership(session, project_id, current_user.id)
        if not membership:
            raise AuthorizationException("Not authorized to view members", status_code=status.HTTP_403_FORBIDDEN)

    memberships = crud.list_members(session, project_id)
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
    _require_admin(current_user)

    project = crud.get_project_v2(session, project_id)
    if not project:
        raise NotFoundException("Project not found")

    membership = crud.get_membership(session, project_id, user_id)
    if not membership:
        raise NotFoundException("User not found in this project")

    crud.remove_member(session, membership)
    return {"detail": "User removed"}
