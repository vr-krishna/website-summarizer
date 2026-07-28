from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

app.include_router(router)