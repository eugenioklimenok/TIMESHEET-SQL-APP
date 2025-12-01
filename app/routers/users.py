from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud
from app.core.database import get_session
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    existing = crud.get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo electrónico")
    user = crud.create_user(session, user_in)
    return UserRead.model_validate(user)


@router.get("/", response_model=List[UserRead])
def list_users(session: Session = Depends(get_session)) -> List[UserRead]:
    users = crud.list_users(session)
    return [UserRead.model_validate(user) for user in users]


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_in: UserUpdate, session: Session = Depends(get_session)) -> UserRead:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user_in.email:
        existing = crud.get_user_by_email(session, user_in.email)
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo electrónico")
    updated_user = crud.update_user(session, user, user_in)
    return UserRead.model_validate(updated_user)
