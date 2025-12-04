from typing import List, Optional
from uuid import UUID

from fastapi import status
from sqlmodel import Session, select

from app.core.errors import BusinessRuleException
from app.models import User, UserProfile
from app.schemas import UserCreate, UserProfileUpdate, UserUpdate


def list_all(session: Session) -> List[User]:
    return list(session.exec(select(User)))


def get(session: Session, user_id: UUID) -> Optional[User]:
    return session.get(User, user_id)


def get_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def get_by_user_id(session: Session, user_id: str) -> Optional[User]:
    return session.exec(select(User).where(User.user_id == user_id)).first()


def create(session: Session, user_in: UserCreate, hashed_password: str) -> User:
    if get_by_email(session, user_in.email):
        raise BusinessRuleException(
            "Ya existe un usuario con ese correo electrónico",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"email": user_in.email},
        )
    if get_by_user_id(session, user_in.user_id):
        raise BusinessRuleException(
            "Ya existe un usuario con ese código",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"user_id": user_in.user_id},
        )
    user = User(**user_in.model_dump(exclude={"password"}), hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update(session: Session, user: User, user_in: UserUpdate, hashed_password: str | None = None) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    update_data.pop("password", None)
    if "email" in update_data:
        existing_email = get_by_email(session, update_data["email"])
        if existing_email and existing_email.id != user.id:
            raise BusinessRuleException(
                "Ya existe un usuario con ese correo electrónico",
                status_code=status.HTTP_400_BAD_REQUEST,
                details={"email": update_data["email"]},
            )
    if "user_id" in update_data:
        existing_user_id = get_by_user_id(session, update_data["user_id"])
        if existing_user_id and existing_user_id.id != user.id:
            raise BusinessRuleException(
                "Ya existe un usuario con ese código",
                status_code=status.HTTP_400_BAD_REQUEST,
                details={"user_id": update_data["user_id"]},
            )
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


def get_profile(session: Session, user_uuid: UUID) -> Optional[UserProfile]:
    return session.exec(select(UserProfile).where(UserProfile.user_uuid == user_uuid)).first()


def create_profile(session: Session, user_uuid: UUID) -> UserProfile:
    profile = UserProfile(user_uuid=user_uuid)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def update_profile(session: Session, profile: UserProfile, profile_in: UserProfileUpdate) -> UserProfile:
    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
