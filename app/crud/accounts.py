from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import Account
from app.schemas import AccountCreate, AccountUpdate


def get_by_account_id(session: Session, account_id: str) -> Optional[Account]:
    return session.exec(select(Account).where(Account.account_id == account_id)).first()


def create(session: Session, account_in: AccountCreate) -> Account:
    account = Account(**account_in.model_dump())
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def list_all(session: Session) -> List[Account]:
    return list(session.exec(select(Account)))


def get(session: Session, account_uuid: UUID) -> Optional[Account]:
    return session.get(Account, account_uuid)


def update(session: Session, account: Account, account_in: AccountUpdate) -> Account:
    update_data = account_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account
