"""
ChromaDB vector store for NewsRAG.
Manages article embeddings and semantic search.
"""
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
import chromadb
from chromadb.config import Settings

from embeddings.embedder import embed_text, build_article_text

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "news_articles"

_client = None
_collection = None


def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def upsert_article(article_id: int, title: str, content: str, metadata: dict):
    """
    Generate embedding and upsert an article into ChromaDB.
    """
    try:
        collection = get_collection()
        text = build_article_text(title, content)
        embedding = embed_text(text)

        # ChromaDB metadata must be str/int/float/bool
        safe_meta = {
            "article_id": article_id,
            "source": str(metadata.get("source", "")),
            "category": str(metadata.get("category", "General")),
            "published_date": str(metadata.get("published_date", "")),
            "url": str(metadata.get("url", "")),
            "title": str(title[:200]),
        }

        collection.upsert(
            ids=[str(article_id)],
            embeddings=[embedding],
            metadatas=[safe_meta],
            documents=[text[:1000]],
        )
        logger.debug(f"Upserted article {article_id} into ChromaDB")
    except Exception as e:
        logger.error(f"ChromaDB upsert error for article {article_id}: {e}")


def semantic_search(
    query: str,
    n_results: int = 10,
    category_filter: Optional[str] = None,
    source_filter: Optional[str] = None,
    days_filter: Optional[int] = None,
) -> List[Dict]:
    """
    Perform semantic search in ChromaDB.
    Returns list of metadata dicts for top matches.
    """
    collection = get_collection()
    total_docs = collection.count()
    if total_docs == 0:
        logger.warning("ChromaDB collection is empty — no articles indexed yet.")
        return []

    query_embedding = embed_text(query)

    # Build where filter
    where = {}
    if category_filter and category_filter.lower() not in ("all", ""):
        where["category"] = category_filter
    if source_filter and source_filter.lower() not in ("all sources", "all", ""):
        where["source"] = source_filter

    actual_n = min(n_results, total_docs)

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=actual_n,
            where=where if where else None,
            include=["metadatas", "distances", "documents"],
        )
    except Exception as e:
        # Retry without filter if filter causes an error
        logger.warning(f"Filtered search failed ({e}), retrying without filter")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=actual_n,
            include=["metadatas", "distances", "documents"],
        )

    hits = []
    if results and results["metadatas"]:
        for meta, dist, doc in zip(
            results["metadatas"][0],
            results["distances"][0],
            results["documents"][0],
        ):
            hits.append({
                **meta,
                "score": float(1 - dist),
                "snippet": doc,
            })

    return hits


def get_collection_count() -> int:
    try:
        return get_collection().count()
    except Exception:
        return 0
