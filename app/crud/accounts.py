from typing import List, Optional
from uuid import UUID

from fastapi import status
from sqlmodel import Session, select

from app.core.errors import BusinessRuleException
from app.crud.projects import get_project_by_code
from app.models import Account, Project
from app.schemas.account import AccountCreate, AccountUpdate
from app.schemas.project import ProjectCreate, ProjectUpdate


# Account operations

def list_accounts(session: Session) -> List[Account]:
    return list(session.exec(select(Account)))


def get_account(session: Session, account_uuid: UUID) -> Optional[Account]:
    return session.get(Account, account_uuid)


def get_by_account_id(session: Session, account_id: str) -> Optional[Account]:
    return session.exec(select(Account).where(Account.account_id == account_id)).first()


def create_account(session: Session, account_in: AccountCreate) -> Account:
    if get_by_account_id(session, account_in.account_id):
        raise BusinessRuleException(
            "Ya existe una cuenta con ese identificador",
            status_code=status.HTTP_409_CONFLICT,
            details={"account_id": account_in.account_id},
        )
    account = Account(**account_in.model_dump())
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def update_account(session: Session, account: Account, account_in: AccountUpdate) -> Account:
    update_data = account_in.model_dump(exclude_unset=True)
    if "account_id" in update_data:
        existing = get_by_account_id(session, update_data["account_id"])
        if existing and existing.id != account.id:
            raise BusinessRuleException(
                "Ya existe una cuenta con ese identificador",
                status_code=status.HTTP_409_CONFLICT,
                details={"account_id": update_data["account_id"]},
            )
    for field, value in update_data.items():
        setattr(account, field, value)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def delete_account(session: Session, account: Account) -> None:
    session.delete(account)
    session.commit()


# Project operations

def list_projects(session: Session) -> List[Project]:
    return list(session.exec(select(Project)))


def get_project(session: Session, project_uuid: UUID) -> Optional[Project]:
    return session.get(Project, project_uuid)


def create_project(session: Session, project_in: ProjectCreate) -> Project:
    if get_project_by_code(session, project_in.code):
        raise BusinessRuleException(
            "Ya existe un proyecto con ese código",
            status_code=status.HTTP_409_CONFLICT,
            details={"code": project_in.code},
        )
    project = Project(**project_in.model_dump())
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def update_project(session: Session, project: Project, project_in: ProjectUpdate) -> Project:
    update_data = project_in.model_dump(exclude_unset=True)
    if "code" in update_data:
        existing = get_project_by_code(session, update_data["code"])
        if existing and existing.id != project.id:
            raise BusinessRuleException(
                "Ya existe un proyecto con ese código",
                status_code=status.HTTP_409_CONFLICT,
                details={"code": update_data["code"]},
            )
    for field, value in update_data.items():
        setattr(project, field, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)
    session.commit()
