FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        bash \
    && rm -rf /var/lib/apt/lists/*

COPY start.sh ./
RUN chmod +x start.sh

COPY news-rag/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY news-rag/ ./

ENV PYTHONPATH=/app

EXPOSE 8501
EXPOSE 8000

CMD ["bash", "./start.sh"]
