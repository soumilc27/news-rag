"""
LLM summarizer for NewsRAG using Ollama (self-hosted or Ollama Cloud).
Falls back to a rule-based summary if Ollama is unavailable.
"""
import os
from typing import List, Dict, Optional
from loguru import logger

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from llm.prompt_builder import build_summarization_prompt, build_system_prompt

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "").strip()


def _is_cloud() -> bool:
    return "ollama.com" in OLLAMA_BASE_URL or OLLAMA_BASE_URL.startswith("https://")


def _get_headers() -> Dict[str, str]:
    headers: Dict[str, str] = {"Content-Type": "application/json"}
    if OLLAMA_API_KEY:
        headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"
    return headers


def _check_ollama() -> bool:
    """Check if Ollama is reachable at the configured base URL."""
    try:
        import httpx
        if _is_cloud():
            resp = httpx.get(
                f"{OLLAMA_BASE_URL}/models",
                headers=_get_headers(),
                timeout=5,
            )
            return resp.status_code == 200
        resp = httpx.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            headers=_get_headers(),
            timeout=5,
        )
        return resp.status_code == 200
    except Exception:
        return False


def summarize_with_ollama(query: str, articles: List[Dict]) -> Optional[str]:
    """Call Ollama to generate a summary."""
    try:
        import httpx
        prompt = build_summarization_prompt(query, articles)
        if not prompt:
            return None

        if _is_cloud():
            endpoint = f"{OLLAMA_BASE_URL}/chat/completions"
            body = {
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": build_system_prompt()},
                    {"role": "user", "content": prompt},
                ],
            }
        else:
            endpoint = f"{OLLAMA_BASE_URL}/api/chat"
            body = {
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": build_system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
            }

        resp = httpx.post(
            endpoint,
            headers=_get_headers(),
            json=body,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()

        if _is_cloud():
            return data.get("choices", [{}])[0].get("message", {}).get("content")
        return data.get("message", {}).get("content")
    except Exception as e:
        logger.warning(f"Ollama summarization failed: {e}")
        return None


def _rule_based_summary(query: str, articles: List[Dict]) -> str:
    """Fallback rule-based summary when LLM is unavailable."""
    if not articles:
        return "No relevant articles were found for your query."

    lines = [f"**Summary**\nHere are the top news results for: *{query}*\n"]
    lines.append("**Key Developments**")
    for a in articles[:5]:
        pub = a.get("published_date", "")[:10] if a.get("published_date") else ""
        preview = a.get("preview", a.get("content", ""))[:150]
        lines.append(f"- **{a['title']}** ({a['source']}, {pub})\n  {preview}...")
    lines.append(
        "\n**Key Takeaway**\n"
        "These results were retrieved via semantic search. "
        "Enable Ollama with qwen2.5:7b-instruct for AI-generated summaries."
    )
    return "\n".join(lines)


def generate_summary(query: str, articles: List[Dict]) -> Dict:
    """
    Generate a news summary for the given query and articles.
    Returns dict with 'summary', 'powered_by', and 'articles'.
    """
    if not articles:
        return {
            "summary": "No relevant articles found. Try broadening your search or adding more RSS feeds.",
            "powered_by": "System",
            "articles": [],
        }

    ollama_ok = _check_ollama()

    if ollama_ok:
        summary = summarize_with_ollama(query, articles)
        powered_by = f"Local LLM ({OLLAMA_MODEL})"
    else:
        summary = None
        powered_by = "Rule-based (Ollama not running)"

    if not summary:
        summary = _rule_based_summary(query, articles)

    return {
        "summary": summary,
        "powered_by": powered_by,
        "articles": articles,
        "ollama_active": ollama_ok,
    }
