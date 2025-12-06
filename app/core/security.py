"""Utilidades de seguridad y autenticación JWT sin dependencias externas."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app import crud
from app.core.dependencies import get_session
from app.core.errors import AuthorizationException
from app.models import User
from app.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(data: bytes) -> str:
    if ALGORITHM != "HS256":  # pragma: no cover - placeholder para futuros algoritmos
        raise AuthorizationException("Algoritmo de firma no soportado")
    signature = hmac.new(SECRET_KEY.encode(), data, hashlib.sha256).digest()
    return _b64encode(signature)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt, stored_hash = hashed_password.split("$", 1)
    except ValueError:
        return False

    new_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt.encode(), 100_000)
    return hmac.compare_digest(_b64encode(new_hash), stored_hash)


def get_password_hash(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}${_b64encode(hashed)}"


def create_token(
    *, subject: str, expires_delta: timedelta, token_type: str, jti: str | None = None
) -> str:
    expire_time = datetime.now(timezone.utc) + expires_delta
    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = {"sub": subject, "exp": int(expire_time.timestamp()), "type": token_type}
    if jti:
        payload["jti"] = jti

    header_b64 = _b64encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature_b64 = _sign(signing_input)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    return create_token(
        subject=subject,
        expires_delta=expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(subject: str, jti: str, expires_delta: Optional[timedelta] = None) -> str:
    return create_token(
        subject=subject,
        expires_delta=expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
        jti=jti,
    )


def decode_token(token: str, *, expected_type: str | None = None) -> dict:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise AuthorizationException("Token inválido") from exc

    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected_signature = _sign(signing_input)
    if not hmac.compare_digest(expected_signature, signature_b64):
        raise AuthorizationException("Firma del token inválida")

    try:
        payload = json.loads(_b64decode(payload_b64))
    except json.JSONDecodeError as exc:
        raise AuthorizationException("Payload del token inválido") from exc

    exp = payload.get("exp")
    if exp is not None and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
        raise AuthorizationException("Token expirado")

    if expected_type and payload.get("type") != expected_type:
        raise AuthorizationException("Tipo de token inválido")

    return payload


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    credentials_exception = AuthorizationException("No se pudieron validar las credenciales")

    try:
        payload = decode_token(token, expected_type="access")
        subject: Optional[str] = payload.get("sub")
        if subject is None:
            raise credentials_exception
        token_data = TokenData(sub=subject, token_type="access", jti=payload.get("jti"))
    except AuthorizationException:
        raise credentials_exception

    try:
        user_id = UUID(subject)
    except ValueError:
        raise credentials_exception

    user = crud.get_user(session, user_id)
    if not user:
        raise credentials_exception
    return user


def role_required(*allowed_roles: str):
    """Dependencia para validar que el usuario tenga uno de los roles permitidos."""

    def _require_role(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise AuthorizationException("No tienes permisos suficientes", status_code=status.HTTP_403_FORBIDDEN)
        return current_user

    return _require_role
