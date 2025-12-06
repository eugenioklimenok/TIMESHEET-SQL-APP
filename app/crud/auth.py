from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models import RefreshToken


def create_refresh_token(session: Session, user_id: UUID, jti: str, expires_at: datetime) -> RefreshToken:
    token = RefreshToken(user_id=user_id, jti=jti, expires_at=expires_at)
    session.add(token)
    session.commit()
    session.refresh(token)
    return token


def get_refresh_token_by_jti(session: Session, jti: str) -> Optional[RefreshToken]:
    return session.exec(select(RefreshToken).where(RefreshToken.jti == jti)).first()


def revoke_refresh_token(session: Session, token: RefreshToken) -> RefreshToken:
    token.revoked = True
    token.revoked_at = datetime.utcnow()
    session.add(token)
    session.commit()
    session.refresh(token)
    return token
