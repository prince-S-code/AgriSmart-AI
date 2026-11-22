from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.sqlite import init_db
from app.api.auth import router as auth_router
from app.api.crop import router as crop_router
from app.api.disease import router as disease_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="AgriSmart AI", version="1.0.0", lifespan=lifespan)
cors_origins = [
    origin.strip().rstrip("/")
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(crop_router)
app.include_router(disease_router)
app.include_router(dashboard_router)
app.include_router(health_router)


@app.get("/", include_in_schema=False)
def root():
    return {
        "name": "AgriSmart AI API",
        "status": "running",
        "health": "/api/health",
        "documentation": "/docs",
    }
