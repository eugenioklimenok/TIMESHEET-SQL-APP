from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.dependencies import get_session
from app.core.security import role_required
from app.schemas import ErrorResponse, UserCreate, UserRead, UserUpdate
from app.services import users as user_service

router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(role_required("admin"))]
)

user_error_responses = {
    400: {"model": ErrorResponse, "description": "Error de validación"},
    401: {"model": ErrorResponse, "description": "No autenticado"},
    403: {"model": ErrorResponse, "description": "No autorizado"},
    404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
    422: {"model": ErrorResponse, "description": "Entrada inválida"},
}


@router.post("/", response_model=UserRead, status_code=201, responses=user_error_responses)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    user = user_service.create_user(session, user_in)
    return UserRead.model_validate(user)


@router.get("/", response_model=List[UserRead], responses=user_error_responses)
def list_users(session: Session = Depends(get_session)) -> List[UserRead]:
    users = user_service.list_users(session)
    return [UserRead.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserRead, responses=user_error_responses)
def get_user(user_id: UUID, session: Session = Depends(get_session)) -> UserRead:
    user = user_service.get_user(session, user_id)
    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead, responses=user_error_responses)
def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    session: Session = Depends(get_session),
) -> UserRead:
    updated_user = user_service.update_user(session, user_id, user_in)
    return UserRead.model_validate(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses=user_error_responses)
def delete_user(user_id: UUID, session: Session = Depends(get_session)) -> None:
    user_service.delete_user(session, user_id)
