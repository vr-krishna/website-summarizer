from app.services.markdown_renderer import render_markdown


def test_render_heading():
    html = render_markdown("# Hello")

    assert "<h1" in html
    assert "Hello" in html


def test_render_bold_text():
    html = render_markdown("**Bold**")

    assert "<strong>Bold</strong>" in html


def test_render_unordered_list():
    html = render_markdown("- One\n- Two")

    assert "<ul>" in html
    assert "<li>One</li>" in html
    assert "<li>Two</li>" in html


def test_render_table():
    markdown = (
        "| Name | Age |\n"
        "|------|-----|\n"
        "| Alice | 30 |"
    )

    html = render_markdown(markdown)

    assert "<table>" in html
    assert "<td>Alice</td>" in html


def test_render_fenced_code():
    markdown = (
        "```python\n"
        "print('Hello')\n"
        "```"
    )

    html = render_markdown(markdown)

    assert "<code" in html
    assert "print" in html


def test_render_task_list():
    markdown = (
        "- [x] Complete tests\n"
        "- [ ] Deploy app"
    )

    html = render_markdown(markdown)

    assert "Complete tests" in html
    assert "Deploy app" in html


def test_render_empty_string():
    assert render_markdown("") == ""


def test_render_plain_text():
    html = render_markdown("Hello World")

    assert "<p>Hello World</p>" == html


def test_render_preserves_line_breaks():
    html = render_markdown("Line 1\n\nLine 2")

    assert "<p>Line 1</p>" in html
    assert "<p>Line 2</p>" in html