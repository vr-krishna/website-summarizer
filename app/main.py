from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings
from app.core.exception_handlers import (
    generic_exception_handler,
    summarization_exception_handler,
    website_fetch_exception_handler,
)
from app.core.exceptions import (
    SummarizationError,
    WebsiteFetchError,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.app_name,
    description="AI-powered website summarizer built with FastAPI and OpenAI.",
    version=settings.app_version,
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

app.include_router(router)

app.add_exception_handler(
    WebsiteFetchError,
    website_fetch_exception_handler,
)

app.add_exception_handler(
    SummarizationError,
    summarization_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)