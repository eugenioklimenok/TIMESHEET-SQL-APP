from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud
from app.core.database import get_session
from app.models import Account
from app.schemas import AccountCreate, AccountRead, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/", response_model=AccountRead, status_code=201)
def create_account(account_in: AccountCreate, session: Session = Depends(get_session)) -> AccountRead:
    existing = crud.get_account_by_email(session, account_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese correo electrónico")
    account = crud.create_account(session, account_in)
    return AccountRead.model_validate(account)


@router.get("/", response_model=List[AccountRead])
def list_accounts(session: Session = Depends(get_session)) -> List[AccountRead]:
    accounts = crud.list_accounts(session)
    return [AccountRead.model_validate(account) for account in accounts]


@router.patch("/{account_id}", response_model=AccountRead)
def update_account(account_id: int, account_in: AccountUpdate, session: Session = Depends(get_session)) -> AccountRead:
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    if account_in.email:
        existing = crud.get_account_by_email(session, account_in.email)
        if existing and existing.id != account_id:
            raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese correo electrónico")
    updated_account = crud.update_account(session, account, account_in)
    return AccountRead.model_validate(updated_account)
