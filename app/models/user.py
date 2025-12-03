from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, String, text
from sqlmodel import Field, Relationship, SQLModel

from app.models.project_membership import UserProjectMembership

if TYPE_CHECKING:
    from app.models.account import Account, Project
    from app.models.timesheet import TimesheetHeader
    from app.models.user_profile import UserProfile


class UserStatus(SQLModel, table=True):
    __tablename__ = "user_status"

    id: int | None = Field(default=None, primary_key=True)
    status_name: str = Field(sa_column=Column(String(50), nullable=False, unique=True))

    users: List["User"] = Relationship(back_populates="status")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: str = Field(sa_column=Column(String(25), unique=True, nullable=False, index=True))
    name: Optional[str] = Field(default=None, sa_column=Column(String(100)))
    email: str = Field(sa_column=Column(String(150), unique=True, nullable=False))
    profile: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    account_uuid: Optional[UUID] = Field(default=None, foreign_key="accounts.id")
    role: str = Field(
        default="user",
        sa_column=Column(String(50), nullable=False, server_default=text("'user'")),
    )
    hashed_password: str = Field(sa_column=Column(String(255), nullable=False))
    status_id: int = Field(default=1, foreign_key="user_status.id")
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )

    status: Optional[UserStatus] = Relationship(back_populates="users")
    account: Optional["Account"] = Relationship(back_populates="users")
    timesheets: List["TimesheetHeader"] = Relationship(back_populates="user")
    user_profile: Optional["UserProfile"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
    project_memberships: List["UserProjectMembership"] = Relationship(back_populates="user")
    projects: List["Project"] = Relationship(back_populates="members", link_model=UserProjectMembership)

