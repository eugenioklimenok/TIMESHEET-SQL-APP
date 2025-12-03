from app.routers.accounts import router as accounts_router
from app.routers.auth import router as auth_router
from app.routers.profile import router as profile_router
from app.routers.projects import router as projects_router
from app.routers.reports import router as reports_router
from app.routers.timesheets import router as timesheets_router
from app.routers.users import router as users_router

__all__ = [
    "accounts_router",
    "auth_router",
    "profile_router",
    "projects_router",
    "reports_router",
    "timesheets_router",
    "users_router",
]
