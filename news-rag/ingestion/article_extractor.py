"""
Article content extractor using trafilatura.
Visits article URLs and extracts clean text content.
"""
import requests
import trafilatura
from typing import Optional
from loguru import logger


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
REQUEST_TIMEOUT = 8
MAX_CONTENT_LENGTH = 3000


def fetch_url(url: str) -> Optional[str]:
    """Download raw HTML from a URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None


def extract_content(url: str) -> Optional[str]:
    """
    Extract clean article content from a URL using trafilatura.
    Falls back to None if extraction fails.
    """
    html = fetch_url(url)
    if not html:
        return None

    try:
        content = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
            max_text_size=MAX_CONTENT_LENGTH,
        )
        return content
    except Exception:
        return None


def enrich_article(article: dict) -> dict:
    """
    Skip full-text enrichment — too slow on hosted environments.
    RSS feed summaries are sufficient for search and summarization.
    """
    return article
