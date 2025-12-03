from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    code: str = Field(max_length=16)
    description: Optional[str] = None
    client_name: Optional[str] = None
    is_active: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    code: Optional[str] = Field(default=None, max_length=16)
    description: Optional[str] = None
    client_name: Optional[str] = None
    is_active: Optional[bool] = None


class ProjectRead(ProjectBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProjectListResponse(BaseModel):
    results: List[ProjectRead]
    total: int
    limit: int
    offset: int


class ProjectMemberBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    role_in_project: Optional[str] = None


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberRead(ProjectMemberBase):
    username: str
    email: str


class ProjectMemberList(BaseModel):
    results: List[ProjectMemberRead]
    total: int
