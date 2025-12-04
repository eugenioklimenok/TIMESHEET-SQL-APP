from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, String, Text, text
from sqlmodel import Field, Relationship, SQLModel

from app.models.project_membership import UserProjectMembership

if TYPE_CHECKING:
    from app.models.user import User


class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    account_id: str = Field(sa_column=Column(String(25), unique=True, nullable=False, index=True))
    name: str = Field(sa_column=Column(String(150), nullable=False))
    type: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )

    projects: List["Project"] = Relationship(back_populates="account")
    users: List["User"] = Relationship(back_populates="account")


class ProjectStatus(SQLModel, table=True):
    __tablename__ = "project_status"

    id: int | None = Field(default=None, primary_key=True)
    status_name: str = Field(sa_column=Column(String(50), nullable=False))

    projects: List["Project"] = Relationship(back_populates="status")


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    code: str = Field(sa_column=Column(String(16), unique=True, nullable=False, index=True))
    name: str = Field(sa_column=Column(String(100), nullable=False))
    account_uuid: Optional[UUID] = Field(default=None, foreign_key="accounts.id")
    status_id: Optional[int] = Field(default=1, foreign_key="project_status.id")
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    client_name: Optional[str] = Field(default=None, sa_column=Column(String(150)))
    is_active: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, server_default=text("TRUE")),
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP"),
        ),
    )

    account: Optional[Account] = Relationship(back_populates="projects")
    status: Optional[ProjectStatus] = Relationship(back_populates="projects")
    memberships: List["UserProjectMembership"] = Relationship(back_populates="project")
    members: List["User"] = Relationship(back_populates="projects", link_model=UserProjectMembership)

