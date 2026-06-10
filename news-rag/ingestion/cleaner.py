"""
Content cleaner for article text.
Removes noise, ads, and normalizes text.
"""
import re
from typing import Optional


def clean_text(text: Optional[str]) -> str:
    """Clean and normalize article text."""
    if not text:
        return ""

    # Remove HTML tags (shouldn't be many after trafilatura, but just in case)
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove common ad/footer patterns
    patterns_to_remove = [
        r"Subscribe to.*?newsletter",
        r"Click here to.*?\.",
        r"Advertisement\s*",
        r"ADVERTISEMENT\s*",
        r"Share this article.*",
        r"Follow us on.*",
        r"\[.*?\]",  # Remove bracketed content like [Reuters]
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Truncate to reasonable length (first ~3000 chars for embedding)
    if len(text) > 5000:
        text = text[:5000] + "..."

    return text


def get_preview(text: str, max_chars: int = 200) -> str:
    """Get a short preview snippet from article content."""
    cleaned = clean_text(text)
    if len(cleaned) <= max_chars:
        return cleaned
    # Cut at sentence boundary if possible
    truncated = cleaned[:max_chars]
    last_period = truncated.rfind(". ")
    if last_period > 80:
        return truncated[:last_period + 1]
    return truncated + "..."
