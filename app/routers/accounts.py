from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import crud
from app.core.dependencies import get_session
from app.core.security import get_current_user
from app.schemas import AccountCreate, AccountRead, AccountUpdate, ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/accounts", tags=["accounts"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=AccountRead, status_code=201)
def create_account(account_in: AccountCreate, session: Session = Depends(get_session)) -> AccountRead:
    existing = crud.get_by_account_id(session, account_in.account_id)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese identificador")
    account = crud.create_account(session, account_in)
    return AccountRead.model_validate(account)


@router.get("/", response_model=List[AccountRead])
def list_accounts(session: Session = Depends(get_session)) -> List[AccountRead]:
    accounts = crud.list_accounts(session)
    return [AccountRead.model_validate(account) for account in accounts]


@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: UUID, session: Session = Depends(get_session)) -> AccountRead:
    account = crud.get_account(session, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
    return AccountRead.model_validate(account)


@router.patch("/{account_id}", response_model=AccountRead)
def update_account(account_id: UUID, account_in: AccountUpdate, session: Session = Depends(get_session)) -> AccountRead:
    account = crud.get_account(session, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if account_in.account_id:
        existing = crud.get_by_account_id(session, account_in.account_id)
        if existing and existing.id != account_id:
            raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese identificador")

    updated_account = crud.update_account(session, account, account_in)
    return AccountRead.model_validate(updated_account)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: UUID, session: Session = Depends(get_session)) -> None:
    account = crud.get_account(session, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")
    crud.delete_account(session, account)


@router.post("/{account_id}/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    account_id: UUID, project_in: ProjectCreate, session: Session = Depends(get_session)
) -> ProjectRead:
    account = crud.get_account(session, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")

    if project_in.project_id and crud.get_by_project_id(session, project_in.project_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un proyecto con ese identificador")

    project = crud.create_project(
        session,
        ProjectCreate(
            **project_in.model_dump(exclude={"account_uuid"}),
            account_uuid=project_in.account_uuid or account.id,
        ),
    )
    return ProjectRead.model_validate(project)


@router.get("/{account_id}/projects", response_model=List[ProjectRead])
def list_projects(account_id: UUID, session: Session = Depends(get_session)) -> List[ProjectRead]:
    account = crud.get_account(session, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")

    projects = [project for project in crud.list_projects(session) if project.account_uuid == account.id]
    return [ProjectRead.model_validate(project) for project in projects]


@router.patch("/{account_id}/projects/{project_id}", response_model=ProjectRead)
def update_project(
    account_id: UUID, project_id: UUID, project_in: ProjectUpdate, session: Session = Depends(get_session)
) -> ProjectRead:
    account = crud.get_account(session, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")

    project = crud.get_project(session, project_id)
    if not project or project.account_uuid != account.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")

    updated_project = crud.update_project(session, project, project_in)
    return ProjectRead.model_validate(updated_project)


@router.delete("/{account_id}/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(account_id: UUID, project_id: UUID, session: Session = Depends(get_session)) -> None:
    account = crud.get_account(session, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada")

    project = crud.get_project(session, project_id)
    if not project or project.account_uuid != account.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")

    crud.delete_project(session, project)
