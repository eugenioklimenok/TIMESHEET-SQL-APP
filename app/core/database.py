# app/core/database.py

import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

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
    """Crear las tablas registradas en los modelos."""
    # Registrar todos los modelos antes de crear las tablas.
    import app.models  # noqa: WPS433 - registro de metadatos

    SQLModel.metadata.create_all(engine)
