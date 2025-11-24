# app/core/database.py

from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    """
    Devuelve un Session para FastAPI (inyección de dependencias).
    Usar como: Depends(get_session)
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Crear tablas automáticamente si no existen.
    Lo vas a llamar desde main.py en el evento startup.
    """
    SQLModel.metadata.create_all(engine)
