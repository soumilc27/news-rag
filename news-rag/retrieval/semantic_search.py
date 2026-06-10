"""
Semantic search pipeline for NewsRAG.
Combines ChromaDB vector search with SQLite metadata enrichment.
"""
from typing import List, Dict, Optional
from loguru import logger

from embeddings.chroma_store import semantic_search as chroma_search
from database.sqlite_manager import SQLiteManager
from ingestion.cleaner import get_preview

db_manager = SQLiteManager()


def search_articles(
    query: str,
    category: Optional[str] = None,
    source: Optional[str] = None,
    days: Optional[int] = None,
    n_results: int = 10,
) -> List[Dict]:
    """
    Run semantic search and enrich results with full article data from SQLite.
    """
    hits = chroma_search(
        query=query,
        n_results=n_results,
        category_filter=category,
        source_filter=source,
        days_filter=days,
    )

    if not hits:
        logger.info("No vector search results; falling back to SQLite query.")
        return _fallback_db_search(category=category, source=source, days=days)

    # Enrich with full content from SQLite
    enriched = []
    for hit in hits:
        article_id = hit.get("article_id")
        if article_id:
            article = db_manager.get_article_by_id(int(article_id))
            if article:
                enriched.append({
                    "id": article.id,
                    "title": article.title,
                    "content": article.content or "",
                    "preview": get_preview(article.content or hit.get("snippet", ""), 200),
                    "source": article.source,
                    "url": article.url,
                    "category": article.category,
                    "published_date": article.published_date.isoformat() if article.published_date else "",
                    "score": hit.get("score", 0.0),
                })

    logger.info(f"Semantic search returned {len(enriched)} enriched articles")
    return enriched


def _fallback_db_search(
    category: Optional[str] = None,
    source: Optional[str] = None,
    days: Optional[int] = None,
) -> List[Dict]:
    """Fallback: return recent articles from SQLite when vector DB is empty."""
    articles = db_manager.get_articles(
        category=category,
        source=source,
        days=days or 7,
        limit=10,
    )
    from ingestion.cleaner import get_preview
    return [
        {
            "id": a.id,
            "title": a.title,
            "content": a.content or "",
            "preview": get_preview(a.content or "", 200),
            "source": a.source,
            "url": a.url,
            "category": a.category,
            "published_date": a.published_date.isoformat() if a.published_date else "",
            "score": 0.5,
        }
        for a in articles
    ]
