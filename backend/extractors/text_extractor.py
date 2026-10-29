def extract_text(text: str, title: str = "Raw Text"):
    """
    Extract and structure metadata for plain text.

    Args:
        text: Input raw text string.
        title: Optional title identifier.

    Returns:
        Dictionary containing formatted metadata and text.
    """
    cleaned = text.strip() if text else ""
    return {
        "text": cleaned,
        "metadata": {
            "title": title,
            "character_count": len(cleaned),
            "word_count": len(cleaned.split()),
        }
    }
