from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app import crud
from app.core.errors import BusinessRuleException, NotFoundException
from app.core.dependencies import get_session
from app.core.security import role_required
from app.models import UserProfile
from app.schemas import ErrorResponse, UserProfileRead, UserProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])


profile_error_responses = {
    400: {"model": ErrorResponse, "description": "Error de validación"},
    401: {"model": ErrorResponse, "description": "No autenticado"},
    403: {"model": ErrorResponse, "description": "No autorizado"},
    404: {"model": ErrorResponse, "description": "Recurso no encontrado"},
    422: {"model": ErrorResponse, "description": "Entrada inválida"},
}


def _get_or_create_profile(session: Session, user_id: UUID) -> UserProfile:
    profile = crud.get_profile(session, user_id)
    if not profile:
        profile = crud.create_profile(session, user_id)
    return profile


@router.get("", response_model=UserProfileRead, responses=profile_error_responses)
def get_profile(
    current_user=Depends(role_required("admin", "user")),
    session: Session = Depends(get_session),
) -> UserProfileRead:
    db_user = crud.get_user(session, current_user.id)
    if db_user is None:
        raise NotFoundException("Usuario no encontrado")

    profile = _get_or_create_profile(session, current_user.id)
    return UserProfileRead.model_validate(profile)


@router.put("", response_model=UserProfileRead, responses=profile_error_responses)
def update_profile(
    profile_in: UserProfileUpdate,
    current_user=Depends(role_required("admin", "user")),
    session: Session = Depends(get_session),
) -> UserProfileRead:
    db_user = crud.get_user(session, current_user.id)
    if db_user is None:
        raise NotFoundException("Usuario no encontrado")

    update_data = profile_in.model_dump(exclude_unset=True)
    if not update_data:
        raise BusinessRuleException(
            "Debe enviarse al menos un campo para actualizar el perfil",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    profile = _get_or_create_profile(session, current_user.id)
    updated_profile = crud.update_profile(session, profile, profile_in)
    return UserProfileRead.model_validate(updated_profile)
