from fastapi import FastAPI

from app.core.database import init_db
from app.core.errors import register_exception_handlers
from app.utils.logging import setup_logging
from app.routers import (
    accounts_router,
    auth_router,
    profile_router,
    projects_router,
    reports_router,
    timesheets_router,
    users_router,
)

# Inicializar logging antes de crear la app
setup_logging()

app = FastAPI(
    title="TimeSheet App API",
    version="1.0.0",
    description="Backend profesional para gestión de timesheets (FastAPI + SQLModel + PostgreSQL).",
)

# Registrar manejadores globales
register_exception_handlers(app)


@app.on_event("startup")
def on_startup() -> None:
    """Validar conexión y registrar metadata para migraciones."""
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "message": "TimeSheet App API funcionando"}


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(accounts_router)
app.include_router(projects_router)
app.include_router(reports_router)
app.include_router(timesheets_router)
