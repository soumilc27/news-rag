"""
NewsRAG Streamlit Frontend
Dark, modern UI matching the reference design.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NewsRAG – AI Powered News",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label {
    color: #8b949e !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* Logo */
.news-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #e6edf3;
    padding: 12px 0 20px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.news-logo span {
    color: #7c3aed;
}

/* Header */
.page-header {
    text-align: center;
    padding: 20px 0 28px 0;
}
.page-header h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #e6edf3;
    margin-bottom: 6px;
}
.page-header h1 span { color: #7c3aed; }
.page-header p {
    color: #8b949e;
    font-size: 14px;
    margin: 0;
}

/* Search bar */
.stTextInput > div > div > input {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    color: #e6edf3 !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #484f58 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 0 24px !important;
    height: 50px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.35) !important;
}

/* Select boxes */
.stSelectbox > div > div {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
}
.stSelectbox > div > div:hover {
    border-color: #7c3aed !important;
}

/* Summary card */
.summary-card {
    background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%);
    border: 1px solid #30363d;
    border-left: 3px solid #7c3aed;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 24px;
}
.summary-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}
.summary-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 17px;
    font-weight: 600;
    color: #e6edf3;
}
.llm-badge {
    background: rgba(34, 197, 94, 0.12);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.25);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
}
.llm-badge-offline {
    background: rgba(234, 179, 8, 0.12);
    color: #eab308;
    border: 1px solid rgba(234, 179, 8, 0.25);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
}
.summary-text {
    color: #c9d1d9;
    font-size: 14px;
    line-height: 1.75;
}

/* Article cards */
.article-card {
    background-color: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
    display: flex;
    gap: 18px;
    align-items: flex-start;
}
.article-card:hover {
    border-color: #7c3aed;
    background-color: #1a1f2e;
    transform: translateX(2px);
}
.article-img-placeholder {
    width: 80px;
    height: 70px;
    border-radius: 8px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
}
.article-body { flex: 1; min-width: 0; }
.article-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 5px;
    line-height: 1.4;
}
.article-meta {
    font-size: 12px;
    color: #7c3aed;
    margin-bottom: 8px;
    font-weight: 500;
}
.article-meta span { color: #484f58; margin: 0 4px; }
.article-preview {
    font-size: 13px;
    color: #8b949e;
    line-height: 1.6;
    margin-bottom: 10px;
}
.category-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.02em;
}

/* Category tag colors */
.cat-technology { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.cat-ai { background: rgba(124,58,237,0.15); color: #a78bfa; border: 1px solid rgba(124,58,237,0.3); }
.cat-politics { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.cat-business { background: rgba(234,179,8,0.15); color: #fbbf24; border: 1px solid rgba(234,179,8,0.3); }
.cat-science { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.cat-cyber { background: rgba(249,115,22,0.15); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }
.cat-sports { background: rgba(20,184,166,0.15); color: #2dd4bf; border: 1px solid rgba(20,184,166,0.3); }
.cat-general { background: rgba(107,114,128,0.15); color: #9ca3af; border: 1px solid rgba(107,114,128,0.3); }

/* Right panel cards */
.panel-card {
    background-color: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 16px;
}
.panel-card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 14px;
}
.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    font-size: 13px;
    color: #c9d1d9;
    border-bottom: 1px solid #21262d;
}
.status-row:last-child { border-bottom: none; }
.status-active { color: #22c55e; font-size: 12px; font-weight: 600; }
.status-inactive { color: #ef4444; font-size: 12px; font-weight: 600; }

/* Quick category buttons */
.quick-cat {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 12px;
    border-radius: 8px;
    font-size: 13px;
    color: #8b949e;
    cursor: pointer;
    margin-bottom: 2px;
    transition: all 0.15s ease;
}
.quick-cat:hover, .quick-cat.active {
    background-color: rgba(124,58,237,0.15);
    color: #a78bfa;
}

/* Pipeline bar */
.pipeline-bar {
    background-color: #161b22;
    border-top: 1px solid #21262d;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    flex-wrap: wrap;
}
.pipeline-step {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: #484f58;
    font-weight: 500;
}
.pipeline-step .icon {
    width: 30px;
    height: 30px;
    background: #21262d;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}
.pipeline-arrow { color: #30363d; font-size: 12px; }

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #e6edf3;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Dividers */
hr { border-color: #21262d; margin: 20px 0; }

/* Dark mode scrollbars */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #484f58; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ────────────────────────────────────────────────────────────────

CATEGORY_ICONS = {
    "All": "📰",
    "Technology": "💻",
    "Artificial Intelligence": "🤖",
    "Politics": "🏛️",
    "Business": "💼",
    "Science": "🔬",
    "Cybersecurity": "🛡️",
    "Sports": "⚽",
    "General": "🌐",
}

CATEGORY_CSS = {
    "Technology": "cat-technology",
    "Artificial Intelligence": "cat-ai",
    "Politics": "cat-politics",
    "Business": "cat-business",
    "Science": "cat-science",
    "Cybersecurity": "cat-cyber",
    "Sports": "cat-sports",
    "General": "cat-general",
}

SOURCE_LOGOS = {
    "TechCrunch": "🟢",
    "Ars Technica": "🔵",
    "The Verge": "🟣",
    "Reuters": "🔴",
    "BBC": "🟡",
    "BBC News": "🟡",
    "Wired": "⚫",
    "NASA": "🚀",
    "Nature": "🌿",
    "ESPN": "🏅",
}


def get_source_emoji(source_name: str) -> str:
    for k, v in SOURCE_LOGOS.items():
        if k.lower() in source_name.lower():
            return v
    return "📄"


def format_date(date_str: str) -> str:
    if not date_str:
        return "Unknown date"
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", ""))
        delta = datetime.utcnow() - dt
        if delta.days == 0:
            hours = delta.seconds // 3600
            return f"{hours}h ago" if hours > 0 else "Just now"
        elif delta.days == 1:
            return "Yesterday"
        elif delta.days < 7:
            return f"{delta.days} days ago"
        else:
            return dt.strftime("%b %d, %Y")
    except Exception:
        return date_str[:10]


def get_category_css(category: str) -> str:
    return CATEGORY_CSS.get(category, "cat-general")


def load_backend():
    """Lazy-import backend modules to avoid import errors in UI."""
    try:
        from database.sqlite_manager import SQLiteManager
        from retrieval.query_parser import parse_query
        from retrieval.semantic_search import search_articles
        from retrieval.reranker import rerank
        from llm.summarizer import generate_summary, _check_ollama
        from embeddings.chroma_store import get_collection_count
        return {
            "db": SQLiteManager(),
            "parse_query": parse_query,
            "search_articles": search_articles,
            "rerank": rerank,
            "generate_summary": generate_summary,
            "check_ollama": _check_ollama,
            "get_collection_count": get_collection_count,
        }
    except Exception as e:
        return {"error": str(e)}


@st.cache_resource
def get_backend():
    return load_backend()


# ─── Session State ───────────────────────────────────────────────────────────
if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"


# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>News<span>RAG</span> – AI Powered News Search & Summarization</h1>
    <p>Search. Filter. Summarize. Stay Informed.</p>
</div>
""", unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="news-logo">
        📰 News<span>RAG</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="color:#8b949e;font-size:11px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:12px;">▼ FILTERS</p>', unsafe_allow_html=True)

    st.markdown('<p style="color:#8b949e;font-size:11px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px;">NEWS CATEGORY</p>', unsafe_allow_html=True)
    categories = ["All", "Technology", "Artificial Intelligence", "Politics", "Business", "Science", "Cybersecurity", "Sports"]
    category_filter = st.selectbox(
        "Category",
        options=categories,
        index=0,
        label_visibility="collapsed",
        key="cat_filter",
    )

    st.markdown('<p style="color:#8b949e;font-size:11px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px;margin-top:14px;">TIME RANGE</p>', unsafe_allow_html=True)
    time_range = st.selectbox(
        "Time Range",
        options=["All Time", "Last 24 Hours", "Last 3 Days", "Last 7 Days", "Last 30 Days"],
        index=0,
        label_visibility="collapsed",
        key="time_filter",
    )
    days_map = {"All Time": None, "Last 24 Hours": 1, "Last 3 Days": 3, "Last 7 Days": 7, "Last 30 Days": 30}
    days_filter = days_map[time_range]

    st.markdown('<p style="color:#8b949e;font-size:11px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px;margin-top:14px;">SOURCE</p>', unsafe_allow_html=True)

    backend = get_backend()
    if "db" in backend:
        try:
            all_sources = ["All Sources"] + sorted(backend["db"].get_all_sources())
        except Exception:
            all_sources = ["All Sources"]
    else:
        all_sources = ["All Sources"]

    source_filter = st.selectbox(
        "Source",
        options=all_sources,
        index=0,
        label_visibility="collapsed",
        key="src_filter",
    )

    if st.button("🔍  Apply Filters", key="apply_btn"):
        st.session_state["trigger_search"] = True

    # Quick categories
    st.markdown('<hr style="border-color:#21262d;margin:20px 0 14px 0;">', unsafe_allow_html=True)
    st.markdown('<p style="color:#484f58;font-size:10px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">QUICK CATEGORIES</p>', unsafe_allow_html=True)

    for cat in categories:
        icon = CATEGORY_ICONS.get(cat, "📰")
        is_active = st.session_state.selected_category == cat
        color = "#a78bfa" if is_active else "#8b949e"
        bg = "background-color:rgba(124,58,237,0.15);" if is_active else ""
        if st.button(f"{icon}  {cat}", key=f"qcat_{cat}"):
            st.session_state.selected_category = cat


# ─── Main Layout ─────────────────────────────────────────────────────────────
main_col, right_col = st.columns([3, 1], gap="large")

with main_col:
    # ── Search Bar ──────────────────────────────────────────────────────────
    search_col, btn_col = st.columns([5, 1])

    with search_col:
        query = st.text_input(
            "search",
            placeholder='Search news... (e.g. "OpenAI new update", "election results", "AI breakthroughs")',
            label_visibility="collapsed",
            key="search_query",
        )

    with btn_col:
        search_clicked = st.button("🔍  Search", key="search_btn")

    # ── Trigger search ───────────────────────────────────────────────────────
    should_search = search_clicked or st.session_state.get("trigger_search", False)
    st.session_state["trigger_search"] = False

    if should_search and query.strip():
        st.session_state.last_query = query

        with st.spinner("🔍 Running semantic search..."):
            if "error" in backend:
                st.error(f"Backend error: {backend['error']}")
                st.info("Run `python run.py --ingest` first to populate the database.")
                st.stop()

            try:
                # Parse, search, rerank, summarize
                parsed = backend["parse_query"](query)
                eff_category = category_filter if category_filter != "All" else parsed.get("category")
                eff_source = source_filter if source_filter != "All Sources" else parsed.get("source")
                eff_days = days_filter or parsed.get("days")

                hits = backend["search_articles"](
                    query=query,
                    category=eff_category,
                    source=eff_source,
                    days=eff_days,
                    n_results=10,
                )

                top_articles = backend["rerank"](query, hits, top_k=5)
                result = backend["generate_summary"](query, top_articles)
                st.session_state.search_results = top_articles
                st.session_state.summary = result
            except Exception as e:
                st.error(f"Search error: {e}")
                st.info("Make sure you've run the ingestion pipeline first: `python run.py --ingest`")

    # ── AI Summary Card ──────────────────────────────────────────────────────
    if st.session_state.summary:
        result = st.session_state.summary
        ollama_on = result.get("ollama_active", False)
        powered_by = result.get("powered_by", "System")

        badge_cls = "llm-badge" if ollama_on else "llm-badge-offline"
        badge_icon = "✅" if ollama_on else "⚠️"

        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-header">
                <span style="font-size:20px;">✨</span>
                <span class="summary-title">AI Summary</span>
                <span class="{badge_cls}">{badge_icon} {powered_by}</span>
            </div>
            <div class="summary-text">
        """, unsafe_allow_html=True)

        summary_text = result.get("summary", "")
        st.markdown(summary_text)

        st.markdown("</div></div>", unsafe_allow_html=True)

        if st.button("↻  Regenerate Summary", key="regen_btn"):
            if st.session_state.search_results:
                with st.spinner("Regenerating..."):
                    result = backend["generate_summary"](
                        st.session_state.last_query,
                        st.session_state.search_results
                    )
                    st.session_state.summary = result
                    st.rerun()

    elif not query:
        # Welcome state
        st.markdown("""
        <div style="text-align:center; padding: 60px 20px; color: #484f58;">
            <div style="font-size: 56px; margin-bottom: 16px;">📰</div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 20px; color: #8b949e; margin-bottom: 8px;">
                Search for any news topic
            </div>
            <div style="font-size: 14px; line-height: 1.8;">
                Try: "Latest AI breakthroughs" &nbsp;·&nbsp; "Cybersecurity incidents this week"<br>
                "Political news from last 3 days" &nbsp;·&nbsp; "Space discoveries"
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Article Results ──────────────────────────────────────────────────────
    articles = st.session_state.search_results
    if articles:
        st.markdown(f"""
        <div class="section-header">
            <div class="section-title">
                📋 Top News Articles
                <span style="color:#484f58;font-size:13px;font-weight:400;">({len(articles)} results)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for i, article in enumerate(articles):
            cat = article.get("category", "General")
            cat_css = get_category_css(cat)
            emoji = get_source_emoji(article.get("source", ""))
            date_str = format_date(article.get("published_date", ""))
            preview = article.get("preview", article.get("content", "")[:180])
            if len(preview) > 180:
                preview = preview[:180] + "..."
            url = article.get("url", "#")
            title = article.get("title", "Untitled")
            source = article.get("source", "Unknown")
            score = article.get("score", 0)

            st.markdown(f"""
            <div class="article-card">
                <div class="article-img-placeholder" style="background:rgba(124,58,237,0.1);">{emoji}</div>
                <div class="article-body">
                    <div class="article-title">{title}</div>
                    <div class="article-meta">
                        {source} <span>·</span> {date_str}
                        <span>·</span>
                        <span class="category-tag {cat_css}">{cat}</span>
                    </div>
                    <div class="article-preview">{preview}</div>
                    <a href="{url}" target="_blank" style="color:#7c3aed;font-size:12px;font-weight:600;text-decoration:none;">
                        ↗ Read Original Article
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Pipeline Bar ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline-bar">
        <span style="color:#484f58;font-size:11px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;margin-right:12px;">HOW IT WORKS</span>
        <div class="pipeline-step"><div class="icon">📡</div><div>RSS Feeds</div></div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-step"><div class="icon">📥</div><div>Article Fetcher</div></div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-step"><div class="icon">🧹</div><div>Content Extractor</div></div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-step"><div class="icon">🏷️</div><div>Classifier</div></div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-step"><div class="icon">⚡</div><div>Embeddings</div></div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-step"><div class="icon">🗄️</div><div>Vector DB</div></div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-step"><div class="icon">🔍</div><div>Retrieval</div></div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-step"><div class="icon">🦙</div><div>LLM (Ollama)</div></div>
        <span class="pipeline-arrow">→</span>
        <div class="pipeline-step"><div class="icon">📊</div><div>Summary + Sources</div></div>
    </div>
    """, unsafe_allow_html=True)


# ─── Right Panel ─────────────────────────────────────────────────────────────
with right_col:
    # Source distribution chart
    st.markdown("""
    <div class="panel-card">
        <div class="panel-card-title">📊 Sources Distribution</div>
    """, unsafe_allow_html=True)

    if "db" in backend:
        try:
            source_counts = backend["db"].get_source_counts()
            if source_counts:
                # Top 5 sources
                top_sources = dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5])
                labels = list(top_sources.keys())
                values = list(top_sources.values())

                colors = ["#7c3aed", "#5b21b6", "#6d28d9", "#4c1d95", "#8b5cf6"]

                fig = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.6,
                    marker=dict(colors=colors, line=dict(color="#0d1117", width=2)),
                    textinfo="none",
                    hovertemplate="<b>%{label}</b><br>%{value} articles<br>%{percent}<extra></extra>",
                )])
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    margin=dict(t=0, b=0, l=0, r=0),
                    height=160,
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                # Legend
                for label, val, color in zip(labels, values, colors):
                    total = sum(values)
                    pct = int(val / total * 100) if total else 0
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:3px 0;font-size:12px;color:#c9d1d9;">
                        <div style="width:10px;height:10px;border-radius:50%;background:{color};flex-shrink:0;"></div>
                        <div style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{label}</div>
                        <div style="color:#484f58;">{pct}%</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#484f58;font-size:13px;">No data yet. Run ingestion first.</p>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<p style="color:#484f58;font-size:12px;">Chart unavailable</p>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # About card
    st.markdown("""
    <div class="panel-card">
        <div class="panel-card-title">ℹ️ About NewsRAG</div>
        <p style="font-size:12px;color:#8b949e;line-height:1.7;margin:0;">
            NewsRAG is an AI-powered news retrieval and summarization platform 
            that helps you discover and understand the latest happenings from 
            trusted news sources around the world using RAG architecture.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # System status
    st.markdown("""<div class="panel-card"><div class="panel-card-title">⚙️ System Status</div>""", unsafe_allow_html=True)

    if "db" in backend:
        try:
            article_count = backend["db"].get_article_count()
            vector_count = backend["get_collection_count"]()
            ollama_ok = backend["check_ollama"]()

            rss_ok = article_count > 0
            vdb_ok = vector_count > 0

            rss_status = "Active" if rss_ok else "No data"
            vdb_status = "Active" if vdb_ok else "Empty"
            llm_status = "Active" if ollama_ok else "Offline"
            rss_cls = "status-active" if rss_ok else "status-inactive"
            vdb_cls = "status-active" if vdb_ok else "status-inactive"
            llm_cls = "status-active" if ollama_ok else "status-inactive"

            st.markdown(f"""
            <div class="status-row">
                <span>RSS Feeds</span>
                <span class="{rss_cls}">● {rss_status}</span>
            </div>
            <div class="status-row">
                <span>Vector DB</span>
                <span class="{vdb_cls}">● {vdb_status}</span>
            </div>
            <div class="status-row">
                <span>LLM (Local)</span>
                <span class="{llm_cls}">● {llm_status}</span>
            </div>
            <div class="status-row" style="border-bottom:none;">
                <span>Articles</span>
                <span style="color:#22c55e;font-size:12px;font-weight:600;">{article_count:,}</span>
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            st.markdown('<p style="color:#484f58;font-size:12px;">Status unavailable</p>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-row"><span>RSS Feeds</span><span class="status-inactive">● Offline</span></div>
        <div class="status-row"><span>Vector DB</span><span class="status-inactive">● Offline</span></div>
        <div class="status-row"><span>LLM (Local)</span><span class="status-inactive">● Offline</span></div>
        """, unsafe_allow_html=True)

    now = datetime.utcnow().strftime("%d %b %Y, %I:%M %p")
    st.markdown(f"""
    </div>
    <p style="color:#484f58;font-size:11px;text-align:center;margin-top:8px;">
        Last updated: {now} UTC
    </p>
    """, unsafe_allow_html=True)

    # Ingest button
    if st.button("🔄  Fetch Latest News", key="ingest_btn"):
        with st.spinner("Ingesting news..."):
            try:
                from scheduler.update_news import run_ingestion_pipeline
                result = run_ingestion_pipeline()
                st.success(f"✅ Ingested {result['new_articles']} new articles!")
                st.rerun()
            except Exception as e:
                st.error(f"Ingestion error: {e}")
