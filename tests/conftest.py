from pathlib import Path

import pytest


@pytest.fixture
def article_html():
    return Path("tests/fixtures/article.html").read_text()


@pytest.fixture
def empty_html():
    return Path("tests/fixtures/empty.html").read_text()