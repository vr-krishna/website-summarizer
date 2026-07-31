from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import SummarizationError
from app.services.openai_service import OpenAIService


@pytest.fixture
def mock_client():
    client = AsyncMock()

    client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock()
        )
    )

    return client


@pytest.fixture
def service(mock_client):
    return OpenAIService(client=mock_client)


@pytest.mark.asyncio
async def test_summarize_success(service, mock_client):
    expected = "Generated summary"

    mock_client.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=expected
                    )
                )
            ]
        )
    )

    result = await service.summarize("Website")

    assert result == expected
    mock_client.chat.completions.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_summarize_uses_correct_messages(
    service,
    mock_client,
):
    mock_client.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="Summary"
                    )
                )
            ]
        )
    )

    webpage = "FastAPI"

    await service.summarize(webpage)

    _, kwargs = (
        mock_client.chat.completions.create.call_args
    )

    assert len(kwargs["messages"]) == 2
    assert kwargs["messages"][0]["role"] == "system"
    assert kwargs["messages"][1]["role"] == "user"
    assert webpage in kwargs["messages"][1]["content"]


@pytest.mark.asyncio
async def test_summarize_raises_error(
    service,
    mock_client,
):
    mock_client.chat.completions.create.side_effect = (
        Exception("API unavailable")
    )

    with pytest.raises(SummarizationError):
        await service.summarize("Website")


@pytest.mark.asyncio
async def test_empty_response(
    service,
    mock_client,
):
    mock_client.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=None
                    )
                )
            ]
        )
    )

    with pytest.raises(SummarizationError):
        await service.summarize("Website")