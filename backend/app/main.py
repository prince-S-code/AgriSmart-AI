from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(crop_router)
app.include_router(disease_router)
app.include_router(dashboard_router)
app.include_router(health_router)
