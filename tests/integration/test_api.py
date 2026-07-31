import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import get_summarizer
from app.main import app


class FakeSummarizer:
    async def summarize(self, url: str) -> str:
        return "# Test Summary\n\nThis is a fake summary."


class FailingSummarizer:
    async def summarize(self, url: str) -> str:
        raise Exception("Service unavailable")


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Website Summarizer" in response.text


def test_summarize_success(client):
    app.dependency_overrides[get_summarizer] = (
        lambda: FakeSummarizer()
    )

    response = client.post(
        "/summarize",
        data={
            "url": "https://example.com",
        },
    )

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    # Markdown should be rendered into HTML.
    assert "<h1" in response.text
    assert "Test Summary" in response.text
    assert "This is a fake summary." in response.text


def test_invalid_form_data(client):
    app.dependency_overrides[get_summarizer] = (
        lambda: FakeSummarizer()
    )

    response = client.post(
        "/summarize",
        data={},
    )

    assert response.status_code == 422


def test_summarizer_failure(client):
    app.dependency_overrides[get_summarizer] = (
        lambda: FailingSummarizer()
    )

    with pytest.raises(Exception, match="Service unavailable"):
        client.post(
            "/summarize",
            data={
                "url": "https://example.com",
            },
        )