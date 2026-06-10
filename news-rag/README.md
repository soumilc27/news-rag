# 📰 NewsRAG – AI Powered News Retrieval & Summarization

> An AI-powered real-time news retrieval and summarization platform built using Retrieval-Augmented Generation (RAG). Automatically ingests news from multiple sources, performs semantic indexing, retrieves relevant articles via vector search, and generates grounded summaries using a local LLM.

![NewsRAG Screenshot](docs/screenshot.png)

---

## 🏗️ Architecture

```
RSS Feeds → Article Fetcher → Content Extractor → Classifier
    → SQLite DB → Embedding Generator → ChromaDB Vector Store
    → User Query → Metadata Filtering → Semantic Search
    → Reranker → Local LLM (Ollama) → AI Summary → Streamlit UI
```

---

## ✨ Features

- 📡 **Automatic RSS ingestion** from 20+ trusted sources (TechCrunch, BBC, Reuters, NASA, etc.)
- 🧠 **Semantic search** using `BAAI/bge-small-en-v1.5` embeddings + ChromaDB
- 🏷️ **Auto-classification** into 8 categories (Technology, AI, Politics, Business, Science, etc.)
- 🔁 **Reranking** with `BAAI/bge-reranker-base` cross-encoder
- 🤖 **Local LLM summarization** via Ollama (qwen2.5:7b-instruct)
- 🌐 **Modern dark UI** built with Streamlit
- ⚡ **FastAPI backend** with full REST API
- ⏰ **Scheduled ingestion** every 45 minutes (APScheduler)
- 🗄️ **Persistent storage** in SQLite + ChromaDB

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/news-rag
cd news-rag
pip install -r requirements.txt
```

### 2. Install & Start Ollama (for AI Summaries)

```bash
# Install Ollama from https://ollama.com
ollama pull qwen2.5:7b-instruct
ollama serve
```

> **Note:** Without Ollama, the app still works — it falls back to a rule-based summary.

### 3. Run Initial Ingestion

Populate the database with articles before searching:

```bash
python run.py --ingest
```

This will:
- Fetch articles from all configured RSS feeds
- Extract full article content
- Classify articles by topic
- Generate embeddings
- Store everything in SQLite + ChromaDB

### 4. Start the Application

```bash
# Start both API + Frontend
python run.py

# Or start individually:
python run.py --api         # FastAPI at http://localhost:8000
python run.py --frontend    # Streamlit at http://localhost:8501
```

Open **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
news-rag/
├── ingestion/
│   ├── rss_fetcher.py        # RSS feed fetching
│   ├── article_extractor.py  # Full content extraction via trafilatura
│   ├── cleaner.py            # Text normalization
│   ├── classifier.py         # Keyword-based topic classification
│   └── sources.py            # RSS source configuration
│
├── database/
│   ├── models.py             # SQLAlchemy Article model
│   └── sqlite_manager.py     # CRUD operations
│
├── embeddings/
│   ├── embedder.py           # sentence-transformers (BAAI/bge-small-en-v1.5)
│   └── chroma_store.py       # ChromaDB vector store
│
├── retrieval/
│   ├── query_parser.py       # NL query → filters extraction
│   ├── semantic_search.py    # Vector search + SQLite enrichment
│   └── reranker.py           # BAAI/bge-reranker-base cross-encoder
│
├── llm/
│   ├── prompt_builder.py     # RAG prompt construction
│   └── summarizer.py         # Ollama integration + fallback
│
├── api/
│   └── main.py               # FastAPI REST API
│
├── frontend/
│   └── streamlit_app.py      # Streamlit dark UI
│
├── scheduler/
│   └── update_news.py        # APScheduler + ingestion pipeline
│
├── requirements.txt
├── run.py                    # Main entry point
└── README.md
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | System health + article counts |
| `POST` | `/search` | Full RAG pipeline search |
| `GET` | `/articles` | Browse articles with filters |
| `GET` | `/stats` | Category & source statistics |
| `GET` | `/sources` | List all available sources |
| `POST` | `/ingest` | Trigger manual ingestion |

### Search Example

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest AI breakthroughs", "days": 7}'
```

---

## ⚙️ Configuration

### Adding RSS Sources

Edit `ingestion/sources.py`:

```python
RSS_SOURCES.append({
    "name": "My Blog",
    "url": "https://myblog.com/feed.xml",
    "category": "Technology"
})
```

### Changing the LLM

Edit `llm/summarizer.py`:

```python
OLLAMA_MODEL = "llama3.2:3b"  # or any other Ollama model
```

### Ingestion Interval

Edit `scheduler/update_news.py`:

```python
start_scheduler(interval_minutes=30)  # Every 30 minutes
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit + Plotly |
| **API** | FastAPI + Uvicorn |
| **Database** | SQLite + SQLAlchemy |
| **Embeddings** | sentence-transformers (BAAI/bge-small-en-v1.5) |
| **Vector DB** | ChromaDB |
| **Reranker** | BAAI/bge-reranker-base |
| **LLM** | Ollama (qwen2.5:7b-instruct) |
| **Ingestion** | feedparser + trafilatura |
| **Scheduler** | APScheduler |

---

## 🎯 Skills Demonstrated

- Python · FastAPI · Streamlit
- RAG Architecture · Vector Databases · Embeddings
- Semantic Search · Information Retrieval
- Local LLM Deployment (Ollama)
- NLP · API Development · AI System Design

---

## 📈 Roadmap (v2)

- [ ] Multi-label article classification
- [ ] Hybrid BM25 + vector retrieval
- [ ] Personalized news recommendations  
- [ ] Daily AI-generated digest emails
- [ ] Sentiment analysis + trend visualization
- [ ] User accounts & bookmarks
- [ ] Deploy to Render / Railway

---

## 📄 License

MIT License — free to use for portfolio and learning purposes.
