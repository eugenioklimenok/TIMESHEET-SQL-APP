from typing import List, Optional

from sqlmodel import Session, select

from app.models import Account
from app.schemas import AccountCreate, AccountUpdate


def get_by_email(session: Session, email: str) -> Optional[Account]:
    return session.exec(select(Account).where(Account.email == email)).first()


def create(session: Session, account_in: AccountCreate) -> Account:
    account = Account(**account_in.model_dump())
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


def list_all(session: Session) -> List[Account]:
    return list(session.exec(select(Account)))


def update(session: Session, account: Account, account_in: AccountUpdate) -> Account:
    update_data = account_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account
