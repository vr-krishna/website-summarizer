from app.services.fetcher import WebsiteFetcher
from app.services.openai_service import OpenAIService


class WebsiteSummarizer:
    def __init__(
        self,
        fetcher: WebsiteFetcher,
        ai: OpenAIService,
    ):
        self.fetcher = fetcher
        self.ai = ai

    async def summarize(self, url: str) -> str:
        webpage = await self.fetcher.fetch(url)
        return await self.ai.summarize(webpage)