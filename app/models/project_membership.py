from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:  # pragma: no cover - solo para type hints
    from app.models.account import Project
    from app.models.user import User


class UserProjectMembership(SQLModel, table=True):
    __tablename__ = "user_project_membership"

    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    project_id: UUID = Field(foreign_key="projects.id", primary_key=True)
    role_in_project: Optional[str] = Field(default=None, sa_column=Column(String(50)))

    user: Optional["User"] = Relationship(back_populates="project_memberships")
    project: Optional["Project"] = Relationship(back_populates="memberships")
