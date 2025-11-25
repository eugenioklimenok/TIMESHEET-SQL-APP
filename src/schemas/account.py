from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str

class AccountRead(BaseModel):
    id: int
    email: str
    nombre: str
    apellido: str

class AccountUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None