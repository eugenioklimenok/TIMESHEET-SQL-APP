from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Importar variables de entorno
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

# Crear una instancia de FastAPI
app = FastAPI()

# Crear una conexión a la base de datos
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear una base de datos declarativa
Base = declarative_base()

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(SQLALCHEMY_DATABASE_URL))

# Definir la tabla de users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Crear todas las tablas
Base.metadata.create_all(bind=create_engine(SQLALCHEMY_DATABASE_URL))

# Definir la ruta raíz
@app.get("/")
def read_root():
    return {"Hola": "Mundo"}
