from datetime import datetime, timedelta
from uuid import UUID, uuid4

from sqlmodel import Session

from app import crud
from app.core.errors import AuthorizationException
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.schemas import Token


def authenticate_user(session: Session, email: str, password: str):
    user = crud.get_by_email(session, email)
    if not user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def _build_tokens(session: Session, user_id: UUID) -> Token:
    access_token = create_access_token(
        subject=str(user_id), expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_jti = uuid4().hex
    refresh_expires = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    crud.create_refresh_token(session, user_id=user_id, jti=refresh_jti, expires_at=refresh_expires)
    refresh_token = create_refresh_token(
        subject=str(user_id),
        jti=refresh_jti,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return Token(access_token=access_token, refresh_token=refresh_token)


def login(session: Session, email: str, password: str) -> Token:
    user = authenticate_user(session, email, password)
    if not user:
        raise AuthorizationException(
            "Credenciales incorrectas",
            details={"auth_scheme": "Bearer"},
        )
    return _build_tokens(session, user.id)


def refresh_session(session: Session, refresh_token: str) -> Token:
    payload = decode_token(refresh_token, expected_type="refresh")
    jti = payload.get("jti")
    if not jti:
        raise AuthorizationException("Token de refresco inválido")

    stored_token = crud.get_refresh_token_by_jti(session, jti)
    if not stored_token:
        raise AuthorizationException("Token de refresco no reconocido")

    if stored_token.revoked:
        raise AuthorizationException("Token de refresco revocado")

    if stored_token.expires_at < datetime.utcnow():
        raise AuthorizationException("Token de refresco expirado")

    if str(stored_token.user_id) != payload.get("sub"):
        raise AuthorizationException("Token de refresco no coincide con el usuario")

    crud.revoke_refresh_token(session, stored_token)
    return _build_tokens(session, UUID(payload["sub"]))


def revoke_token(session: Session, refresh_token: str) -> None:
    payload = decode_token(refresh_token, expected_type="refresh")
    jti = payload.get("jti")
    if not jti:
        raise AuthorizationException("Token de refresco inválido")

    stored_token = crud.get_refresh_token_by_jti(session, jti)
    if not stored_token or stored_token.revoked:
        return
    if str(stored_token.user_id) != payload.get("sub"):
        return
    crud.revoke_refresh_token(session, stored_token)
