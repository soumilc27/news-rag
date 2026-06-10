"""
Reranker for NewsRAG using BAAI/bge-reranker-base.
Falls back to score-based sorting if model unavailable.
"""
from typing import List, Dict
from loguru import logger

_reranker = None
RERANKER_AVAILABLE = False


def _load_reranker():
    global _reranker, RERANKER_AVAILABLE
    if _reranker is not None:
        return _reranker
    try:
        from sentence_transformers import CrossEncoder
        logger.info("Loading reranker model: BAAI/bge-reranker-base")
        _reranker = CrossEncoder("BAAI/bge-reranker-base", max_length=512)
        RERANKER_AVAILABLE = True
        logger.info("Reranker model loaded.")
    except Exception as e:
        logger.warning(f"Reranker not available: {e}. Using score-based fallback.")
        RERANKER_AVAILABLE = False
    return _reranker


def rerank(query: str, articles: List[Dict], top_k: int = 5) -> List[Dict]:
    """
    Rerank articles using cross-encoder or fall back to relevance score.
    Returns top_k articles sorted by relevance.
    """
    if not articles:
        return []

    reranker = _load_reranker()

    if reranker and RERANKER_AVAILABLE:
        try:
            pairs = [(query, f"{a['title']}. {a.get('preview', '')}") for a in articles]
            scores = reranker.predict(pairs)
            for article, score in zip(articles, scores):
                article["rerank_score"] = float(score)
            reranked = sorted(articles, key=lambda x: x.get("rerank_score", 0), reverse=True)
            logger.info(f"Reranked {len(articles)} articles → returning top {top_k}")
            return reranked[:top_k]
        except Exception as e:
            logger.warning(f"Reranker inference failed: {e}. Using score fallback.")

    # Fallback: sort by original similarity score
    sorted_articles = sorted(articles, key=lambda x: x.get("score", 0), reverse=True)
    return sorted_articles[:top_k]
