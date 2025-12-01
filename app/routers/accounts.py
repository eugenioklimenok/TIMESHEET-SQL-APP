from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud
from app.core.database import get_session
from app.schemas import AccountCreate, AccountRead, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["accounts"])


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
