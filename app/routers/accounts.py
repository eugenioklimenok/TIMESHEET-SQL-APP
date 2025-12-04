from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.dependencies import get_session
from app.core.security import role_required
from app.schemas import ErrorResponse, ProjectCreate, ProjectRead, ProjectUpdate
from app.schemas.account import AccountCreate, AccountRead, AccountUpdate
from app.services import accounts as account_service

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[Depends(role_required("admin"))],
)


account_error_responses = {
    400: {"model": ErrorResponse, "description": "Error de validación"},
    401: {"model": ErrorResponse, "description": "No autenticado"},
    403: {"model": ErrorResponse, "description": "No autorizado"},
    404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
    409: {"model": ErrorResponse, "description": "Conflicto de negocio"},
    422: {"model": ErrorResponse, "description": "Entrada inválida"},
}


@router.post("/", response_model=AccountRead, status_code=201, responses=account_error_responses)
def create_account(account_in: AccountCreate, session: Session = Depends(get_session)) -> AccountRead:
    account = account_service.create_account(session, account_in)
    return AccountRead.model_validate(account)


@router.get("/", response_model=List[AccountRead], responses=account_error_responses)
def list_accounts(session: Session = Depends(get_session)) -> List[AccountRead]:
    accounts = account_service.list_accounts(session)
    return [AccountRead.model_validate(account) for account in accounts]


@router.get("/{account_id}", response_model=AccountRead, responses=account_error_responses)
def get_account(account_id: UUID, session: Session = Depends(get_session)) -> AccountRead:
    account = account_service.get_account(session, account_id)
    return AccountRead.model_validate(account)


@router.patch("/{account_id}", response_model=AccountRead, responses=account_error_responses)
def update_account(account_id: UUID, account_in: AccountUpdate, session: Session = Depends(get_session)) -> AccountRead:
    account = account_service.update_account(session, account_id, account_in)
    return AccountRead.model_validate(account)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT, responses=account_error_responses)
def delete_account(account_id: UUID, session: Session = Depends(get_session)) -> None:
    account_service.delete_account(session, account_id)


@router.post(
    "/{account_id}/projects",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    responses=account_error_responses,
)
def create_project(
    account_id: UUID, project_in: ProjectCreate, session: Session = Depends(get_session)
) -> ProjectRead:
    project = account_service.create_project_for_account(session, account_id, project_in)
    return ProjectRead.model_validate(project)


@router.get("/{account_id}/projects", response_model=List[ProjectRead], responses=account_error_responses)
def list_projects(account_id: UUID, session: Session = Depends(get_session)) -> List[ProjectRead]:
    projects = account_service.list_projects_for_account(session, account_id)
    return [ProjectRead.model_validate(project) for project in projects]


@router.patch(
    "/{account_id}/projects/{project_id}",
    response_model=ProjectRead,
    responses=account_error_responses,
)
def update_project(
    account_id: UUID, project_id: UUID, project_in: ProjectUpdate, session: Session = Depends(get_session)
) -> ProjectRead:
    project = account_service.update_project_for_account(session, account_id, project_id, project_in)
    return ProjectRead.model_validate(project)


@router.delete(
    "/{account_id}/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=account_error_responses,
)
def delete_project(account_id: UUID, project_id: UUID, session: Session = Depends(get_session)) -> None:
    account_service.delete_project_for_account(session, account_id, project_id)
