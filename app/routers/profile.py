from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import crud
from app.core.dependencies import get_session
from app.core.security import role_required
from app.models import UserProfile
from app.schemas import UserProfileRead, UserProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])


def _get_or_create_profile(session: Session, user_id: UUID) -> UserProfile:
    profile = crud.get_profile(session, user_id)
    if not profile:
        profile = crud.create_profile(session, user_id)
    return profile


@router.get("", response_model=UserProfileRead)
def get_profile(
    current_user=Depends(role_required("admin", "user")),
    session: Session = Depends(get_session),
) -> UserProfileRead:
    db_user = crud.get_user(session, current_user.id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    profile = _get_or_create_profile(session, current_user.id)
    return UserProfileRead.model_validate(profile)


@router.put("", response_model=UserProfileRead)
def update_profile(
    profile_in: UserProfileUpdate,
    current_user=Depends(role_required("admin", "user")),
    session: Session = Depends(get_session),
) -> UserProfileRead:
    db_user = crud.get_user(session, current_user.id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    update_data = profile_in.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe enviarse al menos un campo para actualizar el perfil",
        )

    profile = _get_or_create_profile(session, current_user.id)
    updated_profile = crud.update_profile(session, profile, profile_in)
    return UserProfileRead.model_validate(updated_profile)
