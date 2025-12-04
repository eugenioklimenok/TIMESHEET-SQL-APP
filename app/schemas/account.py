from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_id: str
    name: str
    type: Optional[str] = None


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: UUID
    created_at: Optional[datetime] = None


class AccountUpdate(BaseModel):
    account_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
