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
REQUEST_TIMEOUT = 10


def fetch_url(url: str) -> Optional[str]:
    """Download raw HTML from a URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logger.debug(f"Failed to fetch {url}: {e}")
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
        )
        return content
    except Exception as e:
        logger.debug(f"Trafilatura extraction failed for {url}: {e}")
        return None


def enrich_article(article: dict) -> dict:
    """
    Attempt to replace/enhance article content with full extracted text.
    Falls back to existing content (RSS summary) if extraction fails.
    """
    url = article.get("url", "")
    if not url:
        return article

    full_content = extract_content(url)
    if full_content and len(full_content) > len(article.get("content", "")):
        article["content"] = full_content
        logger.debug(f"Enriched content for: {article['title'][:50]}")
    else:
        logger.debug(f"Using RSS summary for: {article['title'][:50]}")

    return article
