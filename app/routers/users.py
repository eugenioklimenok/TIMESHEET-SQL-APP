from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app import crud
from app.core.errors import BusinessRuleException, NotFoundException
from app.core.dependencies import get_session
from app.core.security import get_password_hash, role_required
from app.schemas import ErrorResponse, UserCreate, UserRead, UserUpdate

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
    existing_email = crud.get_by_email(session, user_in.email)
    if existing_email:
        raise BusinessRuleException(
            "Ya existe un usuario con ese correo electrónico",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"email": user_in.email},
        )

    existing_user_id = crud.get_by_user_id(session, user_in.user_id)
    if existing_user_id:
        raise BusinessRuleException(
            "Ya existe un usuario con ese código",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"user_id": user_in.user_id},
        )

    hashed_password = get_password_hash(user_in.password)
    user = crud.create_user(session, user_in, hashed_password)
    return UserRead.model_validate(user)


@router.get("/", response_model=List[UserRead], responses=user_error_responses)
def list_users(
    session: Session = Depends(get_session)
) -> List[UserRead]:
    users = crud.list_users(session)
    return [UserRead.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserRead, responses=user_error_responses)
def get_user(user_id: UUID, session: Session = Depends(get_session)) -> UserRead:
    user = crud.get_user(session, user_id)
    if not user:
        raise NotFoundException("Usuario no encontrado")
    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead, responses=user_error_responses)
def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    session: Session = Depends(get_session),
) -> UserRead:
    user = crud.get_user(session, user_id)
    if not user:
        raise NotFoundException("Usuario no encontrado")

    if user_in.email:
        existing = crud.get_by_email(session, user_in.email)
        if existing and existing.id != user_id:
            raise BusinessRuleException(
                "Ya existe un usuario con ese correo electrónico",
                status_code=status.HTTP_400_BAD_REQUEST,
                details={"email": user_in.email},
            )

    if user_in.user_id:
        existing_code = crud.get_by_user_id(session, user_in.user_id)
        if existing_code and existing_code.id != user_id:
            raise BusinessRuleException(
                "Ya existe un usuario con ese código",
                status_code=status.HTTP_400_BAD_REQUEST,
                details={"user_id": user_in.user_id},
            )

    hashed_password = get_password_hash(user_in.password) if user_in.password else None

    updated_user = crud.update_user(session, user, user_in, hashed_password=hashed_password)
    return UserRead.model_validate(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses=user_error_responses)
def delete_user(user_id: UUID, session: Session = Depends(get_session)) -> None:
    user = crud.get_user(session, user_id)
    if not user:
        raise NotFoundException("Usuario no encontrado")
    crud.delete_user(session, user)
