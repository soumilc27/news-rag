"""
Embedding generator using sentence-transformers.
Model: BAAI/bge-small-en-v1.5
"""
from typing import List, Union
from loguru import logger

_model = None


def get_model():
    """Lazy-load the embedding model."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading embedding model: BAAI/bge-small-en-v1.5")
        _model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        logger.info("Embedding model loaded.")
    return _model


def embed_text(text: str) -> List[float]:
    """Generate an embedding for a single text string."""
    model = get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of texts."""
    model = get_model()
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return embeddings.tolist()


def build_article_text(title: str, content: str) -> str:
    """Combine title and content for embedding."""
    content_snippet = content[:500] if content else ""
    return f"{title}. {content_snippet}".strip()
