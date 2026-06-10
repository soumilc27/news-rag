"""
Prompt builder for NewsRAG LLM summarization.
"""
from typing import List, Dict


def build_summarization_prompt(query: str, articles: List[Dict]) -> str:
    """
    Build a RAG prompt for news summarization.
    """
    if not articles:
        return ""

    context_parts = []
    for i, article in enumerate(articles, 1):
        pub_date = article.get("published_date", "")[:10] if article.get("published_date") else "Unknown"
        snippet = article.get("preview") or article.get("content", "")[:400]
        context_parts.append(
            f"[Article {i}]\n"
            f"Title: {article['title']}\n"
            f"Source: {article['source']} | Date: {pub_date}\n"
            f"URL: {article['url']}\n"
            f"Content: {snippet}\n"
        )

    context = "\n---\n".join(context_parts)

    prompt = f"""You are NewsRAG, an AI-powered news research assistant.

Your task is to summarize the most important news based on the user's query, using ONLY the provided articles below. Never invent facts. Always cite the source for each point you make.

User Query: "{query}"

Retrieved Articles:
---
{context}
---

Instructions:
1. Write a concise, informative summary (3-5 sentences) of the major developments relevant to the query.
2. Highlight 2-4 key events or announcements, each attributed to a specific source.
3. Keep a neutral, factual tone.
4. End with a one-line "Key Takeaway".

Format your response as:

**Summary**
[Your summary here]

**Key Developments**
- [Point 1] (Source: [Source Name])
- [Point 2] (Source: [Source Name])
- [Point 3] (Source: [Source Name])

**Key Takeaway**
[One sentence]
"""
    return prompt


def build_system_prompt() -> str:
    return (
        "You are a professional news research assistant. "
        "Summarize news accurately, cite sources for every claim, "
        "and never fabricate information. Be concise and factual."
    )
