"""
Article topic classifier for NewsRAG.
Uses keyword-based classification with a fallback to the RSS source category.
Can be upgraded to use a zero-shot model or local LLM.
"""
from typing import Optional
from loguru import logger


# Keyword mapping for categories
CATEGORY_KEYWORDS = {
    "Artificial Intelligence": [
        "artificial intelligence", "machine learning", "deep learning", "neural network",
        "llm", "gpt", "chatgpt", "openai", "gemini", "claude", "transformer",
        "generative ai", "ai model", "language model", "diffusion", "stable diffusion",
        "reinforcement learning", "nlp", "computer vision", "robotics", "automation",
        "hugging face", "anthropic", "mistral", "llama", "copilot"
    ],
    "Technology": [
        "software", "hardware", "smartphone", "iphone", "android", "apple", "google",
        "microsoft", "amazon", "meta", "nvidia", "chip", "semiconductor", "gpu", "cpu",
        "cloud", "saas", "startup", "app", "developer", "programming", "code",
        "cybersecurity", "hack", "data breach", "privacy", "encryption",
        "5g", "quantum", "blockchain", "web3", "vr", "ar", "metaverse"
    ],
    "Cybersecurity": [
        "hack", "breach", "vulnerability", "exploit", "ransomware", "malware",
        "phishing", "cybercrime", "security", "cve", "zero-day", "patch",
        "threat", "cyber attack", "ddos", "botnet", "spyware", "data leak"
    ],
    "Business": [
        "ipo", "acquisition", "merger", "revenue", "earnings", "stock", "market",
        "investor", "venture capital", "funding", "startup", "valuation",
        "economy", "inflation", "gdp", "trade", "tariff", "finance", "bank",
        "interest rate", "recession", "layoff", "hiring", "ceo", "executive"
    ],
    "Science": [
        "research", "study", "scientists", "nasa", "space", "astronomy", "climate",
        "biology", "physics", "chemistry", "medicine", "vaccine", "disease",
        "experiment", "discovery", "fossil", "genome", "dna", "protein",
        "climate change", "global warming", "environment", "ocean", "earthquake"
    ],
    "Politics": [
        "president", "congress", "senate", "election", "vote", "government",
        "policy", "law", "legislation", "democrat", "republican", "white house",
        "parliament", "prime minister", "war", "military", "ukraine", "russia",
        "china", "geopolitics", "sanction", "treaty", "un", "nato"
    ],
    "Sports": [
        "football", "basketball", "soccer", "baseball", "tennis", "golf",
        "nfl", "nba", "mlb", "nhl", "fifa", "olympics", "championship",
        "tournament", "athlete", "player", "coach", "team", "match", "game",
        "score", "league", "playoffs"
    ],
}


def classify_article(title: str, content: str, fallback_category: str = "General") -> str:
    """
    Classify an article into a category based on keyword matching.
    Returns the highest-scoring category, or fallback_category if no match.
    """
    text = f"{title} {content}".lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[category] = score

    if not scores:
        return fallback_category

    best_category = max(scores, key=scores.get)
    logger.debug(f"Classified '{title[:40]}' as {best_category} (score: {scores[best_category]})")
    return best_category


def classify_articles_batch(articles: list) -> list:
    """Classify a batch of articles in place."""
    for article in articles:
        rss_category = article.get("category", "General")
        title = article.get("title", "")
        content = article.get("content", "")

        # Keyword classification takes priority
        predicted = classify_article(title, content, fallback_category=rss_category)
        article["category"] = predicted

    return articles
