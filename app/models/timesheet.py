from datetime import date, datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Column, Date, DateTime, Numeric, String, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.account import Project
    from app.models.user import User


class TimesheetStatus(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class TimesheetHeader(SQLModel, table=True):
    __tablename__ = "timesheet_header"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="users.id")
    period_start: date = Field(sa_column=Column(Date, nullable=False))
    period_end: date = Field(sa_column=Column(Date, nullable=False))
    status: TimesheetStatus = Field(
        default=TimesheetStatus.DRAFT,
        sa_column=Column(String(20), nullable=False, server_default=text("'Draft'")),
    )
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP"),
        ),
    )

    user: Optional["User"] = Relationship(back_populates="timesheets")
    items: List["TimesheetItem"] = Relationship(back_populates="header")

    __table_args__ = (
        CheckConstraint("period_start <= period_end", name="ck_timesheet_period_valid"),
    )


class TimesheetItem(SQLModel, table=True):
    __tablename__ = "timesheet_item"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    header_id: UUID = Field(foreign_key="timesheet_header.id")
    project_id: UUID = Field(foreign_key="projects.id")
    date: date = Field(sa_column=Column(Date, nullable=False))
    description: str = Field(sa_column=Column(String, nullable=False))
    hours: float = Field(sa_column=Column(Numeric(5, 2), nullable=False))
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP"))
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP"),
        ),
    )

    header: Optional[TimesheetHeader] = Relationship(back_populates="items")
    project: Optional["Project"] = Relationship()

    __table_args__ = (
        CheckConstraint("hours > 0 AND hours <= 24", name="ck_timesheet_item_hours_range"),
    )
