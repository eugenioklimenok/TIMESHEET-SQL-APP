# app/core/database.py

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    if all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
        DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        DATABASE_URL = "sqlite:///./app.db"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Único engine/sesión centralizado para toda la app.
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def init_db() -> None:
    """Validar la conexión y asegurar que los modelos estén registrados.

    Las tablas se crean y versionan vía migraciones de Alembic en entornos
    de producción. Para entornos de desarrollo o pruebas se garantiza la
    creación del metadata para que el contexto de Alembic conozca los
    modelos y para habilitar SQLite en memoria durante los tests.
    """

    import app.models  # noqa: WPS433 - registro de metadatos

    SQLModel.metadata.create_all(engine)

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:  # pragma: no cover - fallback defensivo
        raise RuntimeError("No se pudo iniciar la conexión a la base de datos") from exc
