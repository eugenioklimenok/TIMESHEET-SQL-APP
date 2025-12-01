from fastapi import FastAPI

from app.core.database import init_db
from app.routers import accounts_router, timesheets_router, users_router

app = FastAPI(
    title="TimeSheet App API",
    version="1.0.0",
    description="Backend profesional para gestión de timesheets (FastAPI + SQLModel + PostgreSQL).",
)


@app.on_event("startup")
def on_startup() -> None:
    """Crear tablas y preparar la base de datos en el arranque."""
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "message": "TimeSheet App API funcionando"}


app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(timesheets_router)
