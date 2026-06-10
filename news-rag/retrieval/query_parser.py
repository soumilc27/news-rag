"""
Query parser for NewsRAG.
Extracts intent, category, source, and date filters from natural language queries.
"""
import re
from typing import Dict, Optional
from ingestion.sources import CATEGORIES


SOURCE_NAMES = [
    "techcrunch", "ars technica", "the verge", "hacker news", "wired",
    "hugging face", "mit tech review", "venturebeat",
    "reuters", "bbc", "al jazeera",
    "bloomberg", "cnbc",
    "sciencedaily", "nature", "nasa",
    "krebs on security", "the hacker news", "dark reading",
    "espn", "bbc sport",
]

DATE_PATTERNS = {
    r"\blast\s+24\s+hours?\b": 1,
    r"\btoday\b": 1,
    r"\byesterday\b": 2,
    r"\blast\s+(\d+)\s+days?\b": None,  # dynamic
    r"\blast\s+week\b": 7,
    r"\bthis\s+week\b": 7,
    r"\blast\s+3\s+days?\b": 3,
    r"\blast\s+month\b": 30,
    r"\bthis\s+month\b": 30,
}

CATEGORY_ALIASES = {
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "machine learning": "Artificial Intelligence",
    "ml": "Artificial Intelligence",
    "tech": "Technology",
    "technology": "Technology",
    "politics": "Politics",
    "political": "Politics",
    "business": "Business",
    "finance": "Business",
    "economy": "Business",
    "science": "Science",
    "cyber": "Cybersecurity",
    "cybersecurity": "Cybersecurity",
    "security": "Cybersecurity",
    "sports": "Sports",
    "sport": "Sports",
}


def parse_query(query: str) -> Dict:
    """
    Parse a natural language query and extract filters.
    Returns dict with keys: query, category, source, days.
    """
    lower = query.lower()

    # Extract category
    category = None
    for alias, cat in CATEGORY_ALIASES.items():
        if alias in lower:
            category = cat
            break

    # Extract source
    source = None
    for src in SOURCE_NAMES:
        if src in lower:
            source = src.title()
            break

    # Extract days
    days = None
    for pattern, day_val in DATE_PATTERNS.items():
        match = re.search(pattern, lower)
        if match:
            if day_val is None:
                # Dynamic: "last N days"
                try:
                    days = int(match.group(1))
                except Exception:
                    days = 7
            else:
                days = day_val
            break

    return {
        "query": query,
        "category": category,
        "source": source,
        "days": days,
    }
