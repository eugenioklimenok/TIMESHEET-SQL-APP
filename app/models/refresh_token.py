from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, String, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    jti: str = Field(sa_column=Column(String(64), unique=True, nullable=False, index=True))
    user_id: UUID = Field(nullable=False, foreign_key="users.id")
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=False), nullable=False))
    revoked: bool = Field(default=False, nullable=False)
    revoked_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=False)))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=False), server_default=text("CURRENT_TIMESTAMP")),
    )

    user: Optional["User"] = Relationship(back_populates="refresh_tokens")
