from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.dependencies import get_session
from app.core.errors import AuthorizationException
from app.core.security import authenticate_user, create_access_token, get_current_user
from app.schemas import ErrorResponse, Token, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


auth_error_responses = {
    401: {"model": ErrorResponse, "description": "No autenticado"},
    422: {"model": ErrorResponse, "description": "Entrada inválida"},
}


@router.post("/login", response_model=Token, responses=auth_error_responses)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise AuthorizationException(
            "Credenciales incorrectas",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details={"auth_scheme": "Bearer"},
        )

    access_token = create_access_token(subject=user.email)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead, responses=auth_error_responses)
def read_users_me(current_user=Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)
