from uuid import UUID

from sqlmodel import Session

from app import crud
from app.core.errors import NotFoundException
from app.schemas.account import AccountCreate, AccountUpdate
from app.schemas.project import ProjectCreate, ProjectUpdate


def _get_account_or_404(session: Session, account_id: UUID):
    account = crud.get_account(session, account_id)
    if not account:
        raise NotFoundException("Cuenta no encontrada")
    return account


def create_account(session: Session, account_in: AccountCreate):
    return crud.create_account(session, account_in)


def list_accounts(session: Session):
    return crud.list_accounts(session)


def get_account(session: Session, account_id: UUID):
    return _get_account_or_404(session, account_id)


def update_account(session: Session, account_id: UUID, account_in: AccountUpdate):
    account = _get_account_or_404(session, account_id)
    return crud.update_account(session, account, account_in)


def delete_account(session: Session, account_id: UUID) -> None:
    account = _get_account_or_404(session, account_id)
    crud.delete_account(session, account)


def create_project_for_account(session: Session, account_id: UUID, project_in: ProjectCreate):
    account = _get_account_or_404(session, account_id)
    payload = ProjectCreate(
        **project_in.model_dump(exclude={"account_uuid"}),
        account_uuid=project_in.account_uuid or account.id,
    )
    return crud.create_project(session, payload)


def list_projects_for_account(session: Session, account_id: UUID):
    account = _get_account_or_404(session, account_id)
    return [
        project
        for project in crud.list_projects(session)
        if project.account_uuid == account.id
    ]


def update_project_for_account(
    session: Session, account_id: UUID, project_id: UUID, project_in: ProjectUpdate
):
    account = _get_account_or_404(session, account_id)
    project = crud.get_project(session, project_id)
    if not project or project.account_uuid != account.id:
        raise NotFoundException("Proyecto no encontrado")
    return crud.update_project(session, project, project_in)


def delete_project_for_account(session: Session, account_id: UUID, project_id: UUID) -> None:
    account = _get_account_or_404(session, account_id)
    project = crud.get_project(session, project_id)
    if not project or project.account_uuid != account.id:
        raise NotFoundException("Proyecto no encontrado")
    crud.delete_project(session, project)
