from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.dependencies import get_session
from app.core.security import get_current_user
from app.schemas import ErrorResponse, Token, TokenRefreshRequest, UserRead
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


auth_error_responses = {
    401: {"model": ErrorResponse, "description": "No autenticado"},
    422: {"model": ErrorResponse, "description": "Entrada inválida"},
}


@router.post("/login", response_model=Token, responses=auth_error_responses)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
) -> Token:
    return auth_service.login(session, form_data.username, form_data.password)


@router.post("/refresh", response_model=Token, responses=auth_error_responses)
def refresh_tokens(payload: TokenRefreshRequest, session: Session = Depends(get_session)) -> Token:
    return auth_service.refresh_session(session, payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, responses=auth_error_responses)
def logout(payload: TokenRefreshRequest, session: Session = Depends(get_session)) -> None:
    auth_service.revoke_token(session, payload.refresh_token)


@router.get("/me", response_model=UserRead, responses=auth_error_responses)
def read_users_me(current_user=Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)
