"""
NewsRAG – Main entry point.

Usage:
  python run.py              # Start API + Frontend
  python run.py --ingest     # Run ingestion pipeline once
  python run.py --api        # Start FastAPI backend only
  python run.py --frontend   # Start Streamlit frontend only
"""
import sys
import os
import subprocess
import threading
import time

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_api():
    """Start FastAPI backend."""
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
    ])


def run_frontend():
    """Start Streamlit frontend."""
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "frontend/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
    ])


def run_ingestion():
    """Run one-off ingestion pipeline."""
    from scheduler.update_news import run_ingestion_pipeline
    print("Starting ingestion pipeline...")
    result = run_ingestion_pipeline()
    print(f"Done! New articles: {result['new_articles']}, Embedded: {result['embedded']}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--ingest" in args:
        run_ingestion()

    elif "--api" in args:
        run_api()

    elif "--frontend" in args:
        run_frontend()

    else:
        # Run both API and frontend
        print("Starting NewsRAG...")
        print("API:      http://localhost:8000")
        print("Frontend: http://localhost:8501")
        print()
        print("Run 'python run.py --ingest' first to populate the database.")
        print("Press Ctrl+C to stop.\n")

        # Start API in background thread
        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()
        time.sleep(2)

        # Run frontend in main thread
        run_frontend()
