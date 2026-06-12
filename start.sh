#!/usr/bin/env bash
set -euo pipefail


cd /app

    # Start Streamlit first (internal UI)
    streamlit run frontend/streamlit_app.py \
        --server.port=8501 \
        --server.address=0.0.0.0 \
        --server.headless=true \
        --server.enableCORS=false \
        --server.enableXsrfProtection=false &
    streamlit_pid=$!

    # Then start FastAPI on the public Render port
    uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} &
    uvicorn_pid=$!

cleanup() {
  kill $uvicorn_pid $streamlit_pid 2>/dev/null || true
  wait 2>/dev/null || true
}
trap cleanup SIGTERM SIGINT

wait -n || true
trap - SIGTERM SIGINT
cleanup
