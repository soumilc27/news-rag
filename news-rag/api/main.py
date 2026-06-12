"""
NewsRAG FastAPI backend.
Exposes endpoints for search, ingestion status, and article retrieval.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from loguru import logger

from database.sqlite_manager import SQLiteManager
from retrieval.query_parser import parse_query
from retrieval.semantic_search import search_articles
from retrieval.reranker import rerank
from llm.summarizer import generate_summary
from embeddings.chroma_store import get_collection_count
from ingestion.sources import CATEGORIES

app = FastAPI(
    title="NewsRAG API",
    description="AI-powered news retrieval and summarization.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = SQLiteManager()


class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    source: Optional[str] = None
    days: Optional[int] = None
    n_results: int = 10


@app.get("/")
def root():
    """Serve Streamlit UI via an iframe.
    This embeds the internal Streamlit server so the public URL shows the UI.
    """
    iframe_html = """
    <style>
        html, body {margin:0;height:100%;overflow:hidden;background:#0d1117;}
        iframe {border:none;width:100%;height:100vh;}
    </style>
    <iframe src='http://127.0.0.1:8501' sandbox='allow-scripts allow-same-origin'></iframe>
    """
    return HTMLResponse(content=iframe_html, status_code=200)



@app.get("/health")
def health():
    article_count = db.get_article_count()
    vector_count = get_collection_count()
    return {
        "status": "ok",
        "articles_in_db": article_count,
        "articles_in_vector_db": vector_count,
    }


@app.post("/search")
def search(req: SearchRequest):
    """Full RAG pipeline: parse → search → rerank → summarize."""
    logger.info(f"Search request: '{req.query}'")

    # Parse query for implicit filters
    parsed = parse_query(req.query)
    category = req.category or parsed.get("category")
    source = req.source or parsed.get("source")
    days = req.days or parsed.get("days")

    # Semantic retrieval
    hits = search_articles(
        query=req.query,
        category=category,
        source=source,
        days=days,
        n_results=req.n_results,
    )

    # Rerank
    top_articles = rerank(req.query, hits, top_k=5)

    # Summarize
    result = generate_summary(req.query, top_articles)
    result["filters_applied"] = {
        "category": category,
        "source": source,
        "days": days,
    }

    return result


@app.get("/articles")
def get_articles(
    category: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    days: Optional[int] = Query(None),
    limit: int = Query(20, le=100),
):
    articles = db.get_articles(category=category, source=source, days=days, limit=limit)
    return {"articles": [a.to_dict() for a in articles], "count": len(articles)}


@app.get("/categories")
def get_categories():
    return {"categories": CATEGORIES}


@app.get("/sources")
def get_sources():
    sources = db.get_all_sources()
    return {"sources": ["All Sources"] + sorted(sources)}


@app.get("/stats")
def get_stats():
    return {
        "total_articles": db.get_article_count(),
        "vector_db_count": get_collection_count(),
        "category_counts": db.get_category_counts(),
        "source_counts": db.get_source_counts(),
    }


@app.post("/ingest")
def trigger_ingest(background_tasks: BackgroundTasks):
    """Trigger a manual ingestion run in the background."""
    background_tasks.add_task(_run_ingestion)
    return {"status": "Ingestion started in background"}


def _run_ingestion():
    try:
        from scheduler.update_news import run_ingestion_pipeline
        run_ingestion_pipeline()
    except Exception as e:
        logger.error(f"Background ingestion error: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
