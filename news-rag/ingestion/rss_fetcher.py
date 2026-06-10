"""
RSS feed fetcher for NewsRAG.
Fetches articles from configured RSS sources.
"""
import feedparser
from datetime import datetime
from typing import List, Dict, Optional
from loguru import logger

from ingestion.sources import RSS_SOURCES


def parse_date(entry) -> Optional[datetime]:
    """Try to extract and parse a published date from a feed entry."""
    for attr in ("published_parsed", "updated_parsed", "created_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6])
            except Exception:
                continue
    return datetime.utcnow()


def fetch_feed(source: Dict) -> List[Dict]:
    """Fetch and parse a single RSS feed source."""
    articles = []
    try:
        feed = feedparser.parse(source["url"])
        if feed.bozo and not feed.entries:
            logger.warning(f"Feed parse issue for {source['name']}: {feed.bozo_exception}")
            return []

        for entry in feed.entries[:20]:  # Cap at 20 per feed
            url = entry.get("link", "")
            if not url:
                continue

            title = entry.get("title", "No Title").strip()
            summary = entry.get("summary", "") or entry.get("description", "")
            published_date = parse_date(entry)

            articles.append({
                "title": title,
                "content": summary,  # Will be enriched by extractor
                "source": source["name"],
                "url": url,
                "category": source.get("category", "General"),
                "published_date": published_date,
            })

        logger.info(f"Fetched {len(articles)} articles from {source['name']}")
    except Exception as e:
        logger.error(f"Error fetching {source['name']}: {e}")

    return articles


def fetch_all_feeds(sources: List[Dict] = None) -> List[Dict]:
    """Fetch articles from all configured RSS sources."""
    if sources is None:
        sources = RSS_SOURCES

    all_articles = []
    for source in sources:
        articles = fetch_feed(source)
        all_articles.extend(articles)

    logger.info(f"Total fetched: {len(all_articles)} articles from {len(sources)} sources")
    return all_articles
