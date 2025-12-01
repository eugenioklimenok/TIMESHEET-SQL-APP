from datetime import date, datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, Column, Date, DateTime, Numeric, String, Text, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.account import Project
    from app.models.user import User


class TimesheetStatus(SQLModel, table=True):
    __tablename__ = "timesheet_status"

    id: int = Field(primary_key=True)
    name: str = Field(sa_column=Column(String(50), nullable=False))

    headers: List["TimesheetHeader"] = Relationship(back_populates="status")


class TimesheetHeader(SQLModel, table=True):
    __tablename__ = "timesheet_header"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")),
    )
    user_uuid: UUID = Field(foreign_key="users.id")
    project_uuid: UUID = Field(foreign_key="projects.id")
    work_date: date = Field(sa_column=Column(Date, nullable=False))
    status_id: int = Field(default=0, foreign_key="timesheet_status.id")
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )

    user: Optional["User"] = Relationship(back_populates="timesheets")
    project: Optional["Project"] = Relationship(back_populates="timesheets")
    status: Optional[TimesheetStatus] = Relationship(back_populates="headers")
    items: List["TimesheetItem"] = Relationship(back_populates="header")


class TimesheetItem(SQLModel, table=True):
    __tablename__ = "timesheet_item"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PGUUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")),
    )
    header_uuid: UUID = Field(foreign_key="timesheet_header.id")
    description: str = Field(sa_column=Column(Text, nullable=False))
    hours: float = Field(sa_column=Column(Numeric(5, 2), nullable=False))
    billable: Optional[bool] = Field(default=True, sa_column=Column(Boolean, server_default=text("TRUE")))
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )

    header: Optional[TimesheetHeader] = Relationship(back_populates="items")

    __table_args__ = (CheckConstraint("hours >= 0", name="ck_timesheet_item_hours_positive"),)

