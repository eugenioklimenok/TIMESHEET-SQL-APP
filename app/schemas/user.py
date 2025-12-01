from datetime import datetime
from typing import Optional
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
    role: Optional[str] = None
    status_id: Optional[int] = 1


class UserCreate(UserBase):
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
    role: Optional[str] = None
    status_id: Optional[int] = None
