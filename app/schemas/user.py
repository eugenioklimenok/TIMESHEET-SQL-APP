from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    nombre: Optional[str] = None
    apellido: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    password: Optional[str] = None
