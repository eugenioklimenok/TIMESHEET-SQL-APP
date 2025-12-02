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

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app import crud
from app.core.dependencies import get_session
from app.models import User
from app.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(data: bytes) -> str:
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


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire_time = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": subject, "exp": int(expire_time.timestamp())}

    header_b64 = _b64encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature_b64 = _sign(signing_input)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_token(token: str) -> dict:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido") from exc

    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected_signature = _sign(signing_input)
    if not hmac.compare_digest(expected_signature, signature_b64):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Firma del token inválida")

    try:
        payload = json.loads(_b64decode(payload_b64))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Payload del token inválido") from exc

    exp = payload.get("exp")
    if exp is not None and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")

    return payload


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = crud.get_by_email(session, email)
    if not user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        subject: Optional[str] = payload.get("sub")
        if subject is None:
            raise credentials_exception
        token_data = TokenData(sub=subject)
    except HTTPException:
        raise credentials_exception

    user = crud.get_by_email(session, token_data.sub)
    if not user:
        raise credentials_exception
    return user
