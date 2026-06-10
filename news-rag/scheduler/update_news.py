"""
News ingestion pipeline and APScheduler setup.
Runs every 45 minutes by default.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ingestion.rss_fetcher import fetch_all_feeds
from ingestion.article_extractor import enrich_article
from ingestion.cleaner import clean_text
from ingestion.classifier import classify_articles_batch
from database.sqlite_manager import SQLiteManager
from embeddings.chroma_store import upsert_article

db_manager = SQLiteManager()


def run_ingestion_pipeline():
    """
    Full ingestion pipeline:
    1. Fetch RSS feeds
    2. Enrich with full article content
    3. Clean content
    4. Classify
    5. Store in SQLite
    6. Embed and store in ChromaDB
    """
    logger.info("=== Starting news ingestion pipeline ===")

    # Step 1: Fetch RSS
    articles = fetch_all_feeds()
    logger.info(f"Fetched {len(articles)} articles from RSS")

    # Step 2–4: Enrich, clean, classify
    new_count = 0
    for article in articles:
        url = article.get("url", "")
        if not url or db_manager.article_exists(url):
            continue

        # Enrich with full content
        article = enrich_article(article)

        # Clean content
        article["content"] = clean_text(article.get("content", ""))

        # Classify
        classify_articles_batch([article])

    # Step 5: Store in SQLite
    inserted_articles = []
    for article in articles:
        if not db_manager.article_exists(article.get("url", "")):
            saved = db_manager.insert_article(article)
            if saved:
                inserted_articles.append(saved)
                new_count += 1

    logger.info(f"Inserted {new_count} new articles into SQLite")

    # Step 6: Embed and store in ChromaDB
    embedded_count = 0
    for article in inserted_articles:
        try:
            upsert_article(
                article_id=article.id,
                title=article.title,
                content=article.content or "",
                metadata={
                    "source": article.source,
                    "category": article.category,
                    "published_date": article.published_date.isoformat() if article.published_date else "",
                    "url": article.url,
                },
            )
            embedded_count += 1
        except Exception as e:
            logger.error(f"Embedding error for article {article.id}: {e}")

    logger.info(f"Embedded {embedded_count} articles into ChromaDB")
    logger.info("=== Ingestion pipeline complete ===")
    return {"new_articles": new_count, "embedded": embedded_count}


_scheduler = None


def start_scheduler(interval_minutes: int = 45):
    """Start the background scheduler for periodic ingestion."""
    global _scheduler
    if _scheduler and _scheduler.running:
        logger.info("Scheduler already running.")
        return

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        run_ingestion_pipeline,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id="news_ingestion",
        name="News Ingestion",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info(f"Scheduler started — ingestion every {interval_minutes} minutes")


def stop_scheduler():
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    run_ingestion_pipeline()
