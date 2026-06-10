"""
RSS feed sources configuration for NewsRAG.
"""

RSS_SOURCES = [
    # Technology
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "category": "Technology"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "category": "Technology"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "category": "Technology"},
    {"name": "Wired", "url": "https://www.wired.com/feed/rss", "category": "Technology"},

    # AI / Machine Learning
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "category": "Artificial Intelligence"},
    {"name": "MIT Tech Review AI", "url": "https://www.technologyreview.com/feed/", "category": "Artificial Intelligence"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "category": "Artificial Intelligence"},

    # General / World News
    {"name": "Reuters", "url": "https://feeds.reuters.com/reuters/topNews", "category": "Politics"},
    {"name": "BBC News", "url": "https://feeds.bbci.co.uk/news/rss.xml", "category": "Politics"},
    {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "category": "Politics"},

    # Business
    {"name": "Bloomberg", "url": "https://feeds.bloomberg.com/technology/news.rss", "category": "Business"},
    {"name": "CNBC Tech", "url": "https://www.cnbc.com/id/19854910/device/rss/rss.html", "category": "Business"},

    # Science
    {"name": "ScienceDaily", "url": "https://www.sciencedaily.com/rss/all.xml", "category": "Science"},
    {"name": "Nature News", "url": "https://www.nature.com/nature.rss", "category": "Science"},
    {"name": "NASA", "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss", "category": "Science"},

    # Cybersecurity
    {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "category": "Cybersecurity"},
    {"name": "The Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews", "category": "Cybersecurity"},
    {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml", "category": "Cybersecurity"},

    # Sports
    {"name": "ESPN", "url": "https://www.espn.com/espn/rss/news", "category": "Sports"},
    {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/rss.xml?edition=int", "category": "Sports"},
]

CATEGORIES = [
    "All",
    "Technology",
    "Artificial Intelligence",
    "Politics",
    "Business",
    "Science",
    "Cybersecurity",
    "Sports",
    "General",
]

TIME_RANGES = {
    "Last 24 Hours": 1,
    "Last 3 Days": 3,
    "Last 7 Days": 7,
    "Last 30 Days": 30,
    "All Time": None,
}
