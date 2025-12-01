from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.timesheet import TimesheetHeader


class UserStatus(SQLModel, table=True):
    __tablename__ = "user_status"

    id: int = Field(primary_key=True)
    status_name: str = Field(sa_column=Column(String(50), nullable=False, unique=True))

    users: List["User"] = Relationship(back_populates="status")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")),
    )
    user_id: str = Field(sa_column=Column(String(25), unique=True, nullable=False, index=True))
    name: Optional[str] = Field(default=None, sa_column=Column(String(100)))
    email: str = Field(sa_column=Column(String(150), unique=True, nullable=False))
    profile: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    role: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    status_id: int = Field(default=1, foreign_key="user_status.id")
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )

    status: Optional[UserStatus] = Relationship(back_populates="users")
    timesheets: List["TimesheetHeader"] = Relationship(back_populates="user")

