#!/usr/bin/env bash
set -euo pipefail

uvicorn news-rag.api.main:app --host 0.0.0.0 --port 8000 &
uvicorn_pid=$!

streamlit run news-rag/frontend/streamlit_app.py \
    --server.port=10000 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.baseUrlPath=/ &
streamlit_pid=$!

cleanup() {
  kill $uvicorn_pid $streamlit_pid 2>/dev/null || true
  wait 2>/dev/null || true
}
trap cleanup SIGTERM SIGINT

wait -n || true
trap - SIGTERM SIGINT
cleanup
