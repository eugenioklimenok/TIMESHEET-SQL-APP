from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status_name: str


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    name: Optional[str] = None
    email: EmailStr
    profile: Optional[str] = None
    account_uuid: Optional[UUID] = None
    role: Literal["admin", "user"] = "user"
    status_id: Optional[int] = 1


class UserCreate(UserBase):
    password: str
    status_id: Optional[int] = 1


class UserRead(UserBase):
    id: UUID
    created_at: Optional[datetime] = None
    status: Optional[UserStatusRead] = None


class UserUpdate(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile: Optional[str] = None
    account_uuid: Optional[UUID] = None
    role: Optional[Literal["admin", "user"]] = None
    status_id: Optional[int] = None
    password: Optional[str] = None
