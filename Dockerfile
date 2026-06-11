FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY start.sh ./
RUN chmod +x start.sh

COPY news-rag/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY news-rag/ ./news-rag/

ENV PYTHONPATH=/app

EXPOSE 10000

CMD ["bash", "./start.sh"]
