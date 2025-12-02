from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import User
from app.schemas import UserCreate, UserUpdate


def list_all(session: Session) -> List[User]:
    return list(session.exec(select(User)))


def get(session: Session, user_id: UUID) -> Optional[User]:
    return session.get(User, user_id)


def get_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def get_by_user_id(session: Session, user_id: str) -> Optional[User]:
    return session.exec(select(User).where(User.user_id == user_id)).first()


def create(session: Session, user_in: UserCreate, hashed_password: str) -> User:
    user = User(**user_in.model_dump(exclude={"password"}), hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update(session: Session, user: User, user_in: UserUpdate, hashed_password: str | None = None) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    update_data.pop("password", None)
    for field, value in update_data.items():
        setattr(user, field, value)
    if hashed_password:
        user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete(session: Session, user: User) -> None:
    session.delete(user)
    session.commit()
