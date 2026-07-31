import logging

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.exceptions import (
    SummarizationError,
    WebsiteFetchError,
)

logger = logging.getLogger(__name__)

templates = Jinja2Templates(
    directory="app/templates",
)


async def website_fetch_exception_handler(
    request: Request,
    exc: WebsiteFetchError,
) -> HTMLResponse:
    """Handle website fetch errors."""

    logger.exception(
        "Website fetch failed: %s",
        exc,
    )

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "title": "Unable to Fetch Website",
            "error": str(exc),
        },
        status_code=502,
    )


async def summarization_exception_handler(
    request: Request,
    exc: SummarizationError,
) -> HTMLResponse:
    """Handle AI summarization errors."""

    logger.exception(
        "Summary generation failed: %s",
        exc,
    )

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "title": "Unable to Generate Summary",
            "error": str(exc),
        },
        status_code=503,
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> HTMLResponse:
    """Handle unexpected application errors."""

    logger.exception(
        "Unexpected server error: %s",
        exc,
    )

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "title": "Unexpected Error",
            "error": (
                "Something went wrong while processing your request. "
                "Please try again later."
            ),
        },
        status_code=500,
    )