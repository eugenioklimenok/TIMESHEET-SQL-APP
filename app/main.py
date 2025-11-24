# app/main.py

from fastapi import FastAPI
from app.core.database import init_db

app = FastAPI(
    title="TimeSheet App API",
    version="1.0.0",
    description="Backend profesional para gestión de timesheets (FastAPI + SQLModel + PostgreSQL)."
)

@app.on_event("startup")
def on_startup():
    """
    Se ejecuta cuando arranca la app.
    Inicializa tablas si aún no existen.
    """
    init_db()

@app.get("/")
def root():
    return {"status": "ok", "message": "TimeSheet App API funcionando"}
