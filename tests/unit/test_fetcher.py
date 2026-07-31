import httpx
import pytest
import respx

from app.core.exceptions import WebsiteFetchError
from app.services.fetcher import WebsiteFetcher


@pytest.fixture
def fetcher() -> WebsiteFetcher:
    return WebsiteFetcher()


@pytest.mark.asyncio
@respx.mock
async def test_fetch_success(fetcher: WebsiteFetcher):
    """Returns extracted text from a valid HTML page."""

    html = """
    <html>
        <body>
            <h1>Hello World</h1>
            <p>This is a test page.</p>
        </body>
    </html>
    """

    respx.get("https://example.com").respond(
        status_code=200,
        text=html,
    )

    text = await fetcher.fetch("https://example.com")

    assert "Hello World" in text
    assert "This is a test page." in text


@pytest.mark.asyncio
@respx.mock
async def test_removes_unwanted_tags(fetcher: WebsiteFetcher):
    """Removes non-content HTML elements."""

    html = """
    <html>
        <body>

            <header>Header</header>

            <nav>Navigation</nav>

            <article>
                <h1>Main Content</h1>
                <p>Hello World</p>
            </article>

            <footer>Footer</footer>

            <script>
                alert("hello")
            </script>

        </body>
    </html>
    """

    respx.get("https://example.com").respond(
        status_code=200,
        text=html,
    )

    text = await fetcher.fetch("https://example.com")

    assert "Main Content" in text
    assert "Hello World" in text

    assert "Header" not in text
    assert "Navigation" not in text
    assert "Footer" not in text
    assert "alert" not in text


@pytest.mark.asyncio
@respx.mock
async def test_fetch_http_error(fetcher: WebsiteFetcher):
    """Raises WebsiteFetchError on HTTP errors."""

    respx.get("https://example.com").respond(
        status_code=404,
        text="Not Found",
    )

    with pytest.raises(WebsiteFetchError):
        await fetcher.fetch("https://example.com")


@pytest.mark.asyncio
@respx.mock
async def test_fetch_timeout(fetcher: WebsiteFetcher):
    """Raises WebsiteFetchError on request timeout."""

    route = respx.get("https://example.com")
    route.side_effect = httpx.TimeoutException("Timed out")

    with pytest.raises(WebsiteFetchError):
        await fetcher.fetch("https://example.com")


@pytest.mark.asyncio
@respx.mock
async def test_fetch_connection_error(fetcher: WebsiteFetcher):
    """Raises WebsiteFetchError on connection failure."""

    route = respx.get("https://example.com")
    route.side_effect = httpx.ConnectError("Connection failed")

    with pytest.raises(WebsiteFetchError):
        await fetcher.fetch("https://example.com")


@pytest.mark.asyncio
@respx.mock
async def test_fetch_empty_document(fetcher: WebsiteFetcher):
    """Returns an empty string for an empty HTML document."""

    respx.get("https://example.com").respond(
        status_code=200,
        text="<html></html>",
    )

    text = await fetcher.fetch("https://example.com")

    assert text == ""


@pytest.mark.asyncio
@respx.mock
async def test_truncates_large_document(fetcher: WebsiteFetcher):
    """Limits extracted content to 20,000 characters."""

    html = f"<html><body><p>{'A' * 25000}</p></body></html>"

    respx.get("https://example.com").respond(
        status_code=200,
        text=html,
    )

    text = await fetcher.fetch("https://example.com")

    assert len(text) == 20_000


@pytest.mark.asyncio
@respx.mock
async def test_sets_user_agent_header(fetcher: WebsiteFetcher):
    """Sends the expected User-Agent header."""

    captured_request = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_request
        captured_request = request
        return httpx.Response(
            status_code=200,
            text="<html><body>Hello</body></html>",
        )

    respx.get("https://example.com").mock(side_effect=handler)

    await fetcher.fetch("https://example.com")

    assert captured_request is not None
    assert captured_request.headers["User-Agent"].startswith("Mozilla/5.0")