from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import (
    SummarizationError,
    WebsiteFetchError,
)
from app.services.summarizer import WebsiteSummarizer


@pytest.fixture
def fetcher():
    mock = AsyncMock()
    mock.fetch.return_value = "Website content"
    return mock


@pytest.fixture
def ai():
    mock = AsyncMock()
    mock.summarize.return_value = "Generated summary"
    return mock


@pytest.fixture
def summarizer(fetcher, ai):
    return WebsiteSummarizer(
        fetcher=fetcher,
        ai=ai,
    )


@pytest.mark.asyncio
async def test_summarize_success(
    summarizer,
    fetcher,
    ai,
):
    """Fetches webpage content and generates a summary."""

    result = await summarizer.summarize(
        "https://example.com"
    )

    fetcher.fetch.assert_awaited_once_with(
        "https://example.com"
    )

    ai.summarize.assert_awaited_once_with(
        "Website content"
    )

    assert result == "Generated summary"


@pytest.mark.asyncio
async def test_fetcher_error_propagates(
    summarizer,
    fetcher,
):
    """Propagates WebsiteFetchError."""

    fetcher.fetch.side_effect = WebsiteFetchError(
        "Unable to fetch webpage"
    )

    with pytest.raises(WebsiteFetchError):
        await summarizer.summarize(
            "https://example.com"
        )


@pytest.mark.asyncio
async def test_ai_error_propagates(
    summarizer,
    ai,
):
    """Propagates SummarizationError."""

    ai.summarize.side_effect = SummarizationError(
        "OpenAI unavailable"
    )

    with pytest.raises(SummarizationError):
        await summarizer.summarize(
            "https://example.com"
        )


@pytest.mark.asyncio
async def test_fetcher_called_once(
    summarizer,
    fetcher,
):
    """Fetcher is called exactly once."""

    await summarizer.summarize(
        "https://example.com"
    )

    fetcher.fetch.assert_awaited_once()


@pytest.mark.asyncio
async def test_ai_called_once(
    summarizer,
    ai,
):
    """AI service is called exactly once."""

    await summarizer.summarize(
        "https://example.com"
    )

    ai.summarize.assert_awaited_once()