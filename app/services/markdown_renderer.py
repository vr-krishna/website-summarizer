import markdown


def render_markdown(content: str) -> str:
    """Convert Markdown to HTML."""

    return markdown.markdown(
        content,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "toc",
            "admonition",
            "pymdownx.tasklist",
            "pymdownx.superfences",
        ],
    )