from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, String, Text, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.timesheet import TimesheetHeader


class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")),
    )
    account_id: str = Field(sa_column=Column(String(25), unique=True, nullable=False, index=True))
    name: str = Field(sa_column=Column(String(150), nullable=False))
    type: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )

    projects: List["Project"] = Relationship(back_populates="account")


class ProjectStatus(SQLModel, table=True):
    __tablename__ = "project_status"

    id: int = Field(primary_key=True)
    status_name: str = Field(sa_column=Column(String(50), nullable=False))

    projects: List["Project"] = Relationship(back_populates="status")


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")),
    )
    project_id: str = Field(sa_column=Column(String(25), unique=True, nullable=False, index=True))
    name: str = Field(sa_column=Column(String(100), nullable=False))
    account_uuid: Optional[UUID] = Field(default=None, foreign_key="accounts.id")
    status_id: Optional[int] = Field(default=1, foreign_key="project_status.id")
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )

    account: Optional[Account] = Relationship(back_populates="projects")
    status: Optional[ProjectStatus] = Relationship(back_populates="projects")
    timesheets: List["TimesheetHeader"] = Relationship(back_populates="project")

