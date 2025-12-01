from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProjectStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status_name: str


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


class ProjectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: str
    name: str
    account_uuid: Optional[UUID] = None
    status_id: Optional[int] = 1
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: UUID
    created_at: Optional[datetime] = None
    status: Optional[ProjectStatusRead] = None


class ProjectUpdate(BaseModel):
    project_id: Optional[str] = None
    name: Optional[str] = None
    account_uuid: Optional[UUID] = None
    status_id: Optional[int] = None
    description: Optional[str] = None
