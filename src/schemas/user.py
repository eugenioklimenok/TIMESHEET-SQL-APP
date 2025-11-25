from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    nombre: str
    apellido: str

class UserRead(BaseModel):
    id: int
    email: str
    nombre: str
    apellido: str

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None