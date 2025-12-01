"""Dependencias comunes de la aplicación."""
from typing import Generator

from sqlmodel import Session

from app.core.database import engine


def get_session() -> Generator[Session, None, None]:
    """Sesión de base de datos para inyección de dependencias."""
    with Session(engine) as session:
        yield session
