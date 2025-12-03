from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_uuid: UUID = Field(foreign_key="users.id", sa_column=Column(String, unique=True, nullable=False))
    first_name: Optional[str] = Field(default=None, sa_column=Column(String(100)))
    last_name: Optional[str] = Field(default=None, sa_column=Column(String(100)))
    phone: Optional[str] = Field(default=None, sa_column=Column(String(30)))
    country: Optional[str] = Field(default=None, sa_column=Column(String(2)))
    time_zone: Optional[str] = Field(default=None, sa_column=Column(String(100)))
    avatar_url: Optional[str] = Field(default=None, sa_column=Column(String(500)))

    user: "User" = Relationship(back_populates="user_profile")


from app.models.user import User  # noqa: E402  # isort:skip
