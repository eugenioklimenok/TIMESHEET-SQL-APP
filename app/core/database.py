# app/core/database.py

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = os.getenv("DATABASE_URL") or (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Único engine/sesión centralizado para toda la app.
engine = create_engine(DATABASE_URL, echo=False)


def get_session() -> Generator[Session, None, None]:
    """Sesión de base de datos para inyección de dependencias."""
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """Validar la conexión y asegurar que los modelos estén registrados.

    Las tablas se crean y versionan vía migraciones de Alembic. Este
    helper solo comprueba la conectividad y carga los modelos para que el
    contexto de Alembic conozca el metadata de SQLModel.
    """

    import app.models  # noqa: WPS433 - registro de metadatos

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:  # pragma: no cover - fallback defensivo
        raise RuntimeError("No se pudo iniciar la conexión a la base de datos") from exc
