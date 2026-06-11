FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    SENTENCE_TRANSFORMERS_HOME=/tmp/sentence_transformers \
    CHROMA_DB_PATH=/tmp/chroma_db \
    OLLAMA_MODEL=gemma3:27b
    OLLAMA_BASE_URL=https://ollama.com/v1

WORKDIR /app

COPY start.sh ./
RUN chmod +x start.sh

COPY news-rag/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY news-rag/ ./news-rag/

RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

ENV PYTHONPATH=/app

RUN mkdir -p /tmp/sentence_transformers /tmp/chroma_db

EXPOSE 8000 10000

CMD ["bash", "./start.sh"]
