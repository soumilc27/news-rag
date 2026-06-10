"""
LLM summarizer for NewsRAG using Ollama (qwen2.5:7b-instruct).
Falls back to a rule-based summary if Ollama is unavailable.
"""
from typing import List, Dict, Optional
from loguru import logger

from llm.prompt_builder import build_summarization_prompt, build_system_prompt

OLLAMA_MODEL = "qwen2.5:7b-instruct"
OLLAMA_BASE_URL = "http://localhost:11434"


def _check_ollama() -> bool:
    """Check if Ollama is running locally."""
    try:
        import httpx
        resp = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def summarize_with_ollama(query: str, articles: List[Dict]) -> Optional[str]:
    """Call Ollama to generate a summary."""
    try:
        import ollama
        prompt = build_summarization_prompt(query, articles)
        if not prompt:
            return None

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": build_system_prompt()},
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]
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
