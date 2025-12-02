from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import crud
from app.core.dependencies import get_session
from app.core.security import get_current_user, get_password_hash
from app.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    existing_email = crud.get_by_email(session, user_in.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo electrónico")

    existing_user_id = crud.get_by_user_id(session, user_in.user_id)
    if existing_user_id:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese código")

    hashed_password = get_password_hash(user_in.password)
    user = crud.create_user(session, user_in, hashed_password)
    return UserRead.model_validate(user)


@router.get("/", response_model=List[UserRead])
def list_users(
    session: Session = Depends(get_session), current_user=Depends(get_current_user)
) -> List[UserRead]:
    users = crud.list_users(session)
    return [UserRead.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: UUID, session: Session = Depends(get_session), current_user=Depends(get_current_user)
) -> UserRead:
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
) -> UserRead:
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if user_in.email:
        existing = crud.get_by_email(session, user_in.email)
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo electrónico")

    if user_in.user_id:
        existing_code = crud.get_by_user_id(session, user_in.user_id)
        if existing_code and existing_code.id != user_id:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con ese código")

    hashed_password = get_password_hash(user_in.password) if user_in.password else None

    updated_user = crud.update_user(session, user, user_in, hashed_password=hashed_password)
    return UserRead.model_validate(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID, session: Session = Depends(get_session), current_user=Depends(get_current_user)
) -> None:
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    crud.delete_user(session, user)
