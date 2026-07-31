from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.markdown_renderer import render_markdown
from app.core.exceptions import WebsiteFetchError

from app.core.dependencies import get_summarizer
from app.services.summarizer import WebsiteSummarizer


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Website Summarizer",
        },
    )
@router.post("/summarize", response_class=HTMLResponse)
async def summarize(
    request: Request,
    url: str = Form(...),
    summarizer: WebsiteSummarizer = Depends(get_summarizer),
):
    try:
        summary = await summarizer.summarize(url)
        summary_html = render_markdown(summary)

        return templates.TemplateResponse(
            request=request,
            name="summary.html",
            context={
                "summary": summary_html,
            },
        )

    except WebsiteFetchError as exc:
        return templates.TemplateResponse(
            request=request,
            name="summary.html",
            context={
                "error": str(exc),
            },
            status_code=200,
        )

    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="summary.html",
            context={
                "error": "An unexpected error occurred. Please try again.",
            },
            status_code=500,
        )