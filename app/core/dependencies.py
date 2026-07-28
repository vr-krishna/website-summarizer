from app.services.fetcher import WebsiteFetcher
from app.services.openai_service import OpenAIService
from app.services.summarizer import WebsiteSummarizer


def get_summarizer() -> WebsiteSummarizer:
    return WebsiteSummarizer(
        fetcher=WebsiteFetcher(),
        ai=OpenAIService(),
    )