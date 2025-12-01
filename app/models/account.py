from typing import Optional

from sqlmodel import Column, Field, SQLModel, String


class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False)
    )
    password: str = Field(nullable=False)
    nombre: Optional[str] = Field(default=None)
    apellido: Optional[str] = Field(default=None)
