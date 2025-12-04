from uuid import UUID

from sqlmodel import Session

from app import crud
from app.core.errors import NotFoundException
from app.core.security import get_password_hash
from app.schemas import UserCreate, UserUpdate


def _get_user_or_404(session: Session, user_id: UUID):
    user = crud.get_user(session, user_id)
    if not user:
        raise NotFoundException("Usuario no encontrado")
    return user


def create_user(session: Session, user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)
    return crud.create_user(session, user_in, hashed_password)


def list_users(session: Session):
    return crud.list_users(session)


def get_user(session: Session, user_id: UUID):
    return _get_user_or_404(session, user_id)


def update_user(session: Session, user_id: UUID, user_in: UserUpdate):
    user = _get_user_or_404(session, user_id)
    hashed_password = get_password_hash(user_in.password) if user_in.password else None
    return crud.update_user(session, user, user_in, hashed_password=hashed_password)


def delete_user(session: Session, user_id: UUID) -> None:
    user = _get_user_or_404(session, user_id)
    crud.delete_user(session, user)
