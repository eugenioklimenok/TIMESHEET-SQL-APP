# Importar librerías
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from src.database import get_db, engine, SessionLocal
from src.users.routes import users_router
from src.accounts.routes import accounts_router

# Importar variables de entorno
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

# Crear una instancia de FastAPI
app = FastAPI()

# Crear una base de datos declarativa
Base = declarative_base()

# Definir la tabla de users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Definir la ruta raíz
@app.get("/")
def read_root():
    return {"Hola": "Mundo"}

# Inicializar routers
app.include_router(users_router)
app.include_router(accounts_router)

# Manejar eventos de startup y shutdown de la base de datos
@app.on_event("startup")
def database_startup():
    import asyncio
    asyncio.get_event_loop().run_until_complete(engine.dispose())

@app.on_event("shutdown")
def database_shutdown():
    import asyncio
    asyncio.get_event_loop().run_until_complete(engine.dispose())

