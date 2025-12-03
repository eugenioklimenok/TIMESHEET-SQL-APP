from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import Account, Project
from app.schemas.account import AccountCreate, AccountUpdate, ProjectCreate, ProjectUpdate


# Account operations

def list_accounts(session: Session) -> List[Account]:
    return list(session.exec(select(Account)))


def get_account(session: Session, account_uuid: UUID) -> Optional[Account]:
    return session.get(Account, account_uuid)


def get_by_account_id(session: Session, account_id: str) -> Optional[Account]:
    return session.exec(select(Account).where(Account.account_id == account_id)).first()


def create_account(session: Session, account_in: AccountCreate) -> Account:
    account = Account(**account_in.model_dump())
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def update_account(session: Session, account: Account, account_in: AccountUpdate) -> Account:
    update_data = account_in.model_dump(exclude_unset=True)
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


def get_by_project_id(session: Session, project_id: str) -> Optional[Project]:
    return session.exec(select(Project).where(Project.project_id == project_id)).first()


def create_project(session: Session, project_in: ProjectCreate) -> Project:
    project_data = project_in.model_dump()
    project_data["code"] = project_in.project_id
    project = Project(**project_data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def update_project(session: Session, project: Project, project_in: ProjectUpdate) -> Project:
    update_data = project_in.model_dump(exclude_unset=True)
    if "project_id" in update_data:
        update_data["code"] = update_data.get("project_id")
    for field, value in update_data.items():
        setattr(project, field, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def delete_project(session: Session, project: Project) -> None:
    session.delete(project)
    session.commit()
