# Importar librerías
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TypeDecorator
from sqlalchemy.schema import ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from src.database import get_db, engine, SessionLocal
from src.users.routes import users_router
from src.accounts.routes import accounts_router

    import asyncio

# Importar variables de entorno
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

# Crear una instancia de FastAPI
app = FastAPI()

# Crear una base de datos declarativa
Base = declarative_base()

# Definir la tabla de(users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Auditoria(Base):
    __tablename__ = "auditoria_timesheet"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario = Column(String, nullable=False)
    fecha = Column(String, nullable=False)
    entidad = Column(String, nullable=False)
    registro_id = Column(UUID(as_uuid=True), nullable=False)
    accion = Column(String, nullable=False)
    old_data = Column(JSON, nullable=False)
    new_data = Column(JSON, nullable=False)

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

def crear_propuestas_auditoria():
    # Propuesta de nuevos archivos SQL para auditoría
    print("Crear tabla para auditoría de transacciones del Timesheet")
    print("CREATE TABLE auditoria_timesheet (")
    print("  id uuid NOT NULL DEFAULT uuid_generate_v4(),")
    print("  usuario character varying NOT NULL,")
    print("  fecha timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,")
    print("  entidad character varying NOT NULL,")
    print("  registro_id uuid NOT NULL,")
    print("  accion character varying NOT NULL,")
    print("  old_data jsonb,")
    print("  new_data jsonb,")
    print("  PRIMARY KEY (id)")
    print(");")

    print("Crear función para insertar en auditoría")
    print("CREATE OR REPLACE FUNCTION insertar_auditoria (")
    print("  p_usuario character varying,")
    print("  p_entidad character varying,")
    print("  p_registro_id uuid,")
    print("  p_accion character varying,")
    print("  p_old_data jsonb,")
    print("  p_new_data jsonb")
    print(")")
    print("RETURNS void AS $$")
    print("BEGIN")
    print("  INSERT INTO auditoria_timesheet (")
    print("    usuario,")
    print("    fecha,")
    print("    entidad,")
    print("    registro_id,")
    print("    accion,")
    print("    old_data,")
    print("    new_data")
    print("  )")
    print("  VALUES (")
    print("    p_usuario,")
    print("    NOW(),")
    print("    p_entidad,")
    print("    p_registro_id,")
    print("    p_accion,")
    print("    p_old_data,")
    print("    p_new_data")
    print("  );")
    print("END;")
    print("$$ LANGUAGE plpgsql;")
crear_propuestas_auditoria()

