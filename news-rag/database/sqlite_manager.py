"""
SQLite database manager for article CRUD operations.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from loguru import logger

from database.models import Article, SessionLocal, init_db


class SQLiteManager:
    def __init__(self):
        init_db()

    def get_session(self) -> Session:
        return SessionLocal()

    def article_exists(self, url: str) -> bool:
        db = self.get_session()
        try:
            return db.query(Article).filter(Article.url == url).first() is not None
        finally:
            db.close()

    def insert_article(self, article_data: dict) -> Optional[Article]:
        db = self.get_session()
        try:
            if self.article_exists(article_data["url"]):
                return None
            article = Article(**article_data)
            db.add(article)
            db.commit()
            db.refresh(article)
            logger.info(f"Inserted article: {article_data['title'][:60]}...")
            return article
        except Exception as e:
            db.rollback()
            logger.error(f"Error inserting article: {e}")
            return None
        finally:
            db.close()

    def get_articles(
        self,
        category: Optional[str] = None,
        source: Optional[str] = None,
        days: Optional[int] = None,
        limit: int = 50,
    ) -> List[Article]:
        db = self.get_session()
        try:
            query = db.query(Article)
            if category and category.lower() != "all":
                query = query.filter(Article.category == category)
            if source and source.lower() != "all sources":
                query = query.filter(Article.source == source)
            if days:
                from datetime import timedelta
                cutoff = datetime.utcnow() - timedelta(days=days)
                query = query.filter(Article.published_date >= cutoff)
            return query.order_by(Article.published_date.desc()).limit(limit).all()
        finally:
            db.close()

    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        db = self.get_session()
        try:
            return db.query(Article).filter(Article.id == article_id).first()
        finally:
            db.close()

    def get_all_sources(self) -> List[str]:
        db = self.get_session()
        try:
            sources = db.query(Article.source).distinct().all()
            return [s[0] for s in sources if s[0]]
        finally:
            db.close()

    def get_article_count(self) -> int:
        db = self.get_session()
        try:
            return db.query(Article).count()
        finally:
            db.close()

    def get_category_counts(self) -> dict:
        db = self.get_session()
        try:
            from sqlalchemy import func
            results = db.query(Article.category, func.count(Article.id)).group_by(Article.category).all()
            return {cat: count for cat, count in results}
        finally:
            db.close()

    def get_source_counts(self) -> dict:
        db = self.get_session()
        try:
            from sqlalchemy import func
            results = db.query(Article.source, func.count(Article.id)).group_by(Article.source).all()
            return {src: count for src, count in results}
        finally:
            db.close()
