from typing import Optional

from pydantic import BaseModel, EmailStr


class AccountBase(BaseModel):
    email: EmailStr
    nombre: Optional[str] = None
    apellido: Optional[str] = None


class AccountCreate(AccountBase):
    password: str


class AccountRead(AccountBase):
    id: int


class AccountUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    password: Optional[str] = None
