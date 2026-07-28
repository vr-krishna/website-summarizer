import httpx
from bs4 import BeautifulSoup

from app.core.exceptions import WebsiteFetchError


class WebsiteFetcher:
    """Downloads and extracts readable content from webpages."""

    async def fetch(self, url: str) -> str:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        }

        try:
            async with httpx.AsyncClient(
                timeout=30,
                follow_redirects=True,
            ) as client:

                response = await client.get(
                    url,
                    headers=headers,
                )

                response.raise_for_status()

        except httpx.HTTPError as exc:
            raise WebsiteFetchError(str(exc)) from exc

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "svg",
            "canvas",
            "iframe",
            "noscript",
            "form",
        ]):
            tag.decompose()

        text = soup.get_text("\n")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return "\n".join(lines)[:20_000]