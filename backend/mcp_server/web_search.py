# Purpose: External web search integration using Tavily API.
# Responsibilities: Connects to Tavily API to fetch real-time search results, returns structured query results, 
# and formats search hits into formatted text snippets for LLM prompting.

from typing import List, Dict, Any

import json
from tavily import TavilyClient

from .config import TAVILY_API_KEY

# Initialize Tavily search client on module load
print("Initializing Tavily client...")
_tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
print("✅ Tavily client ready!")


def get_tavily_client():
    """Returns the shared TavilyClient instance."""
    return _tavily_client


def web_search(
    query: str,
    max_results: int = 5,
    search_depth: str = "basic",
    include_answer: bool = True
) -> Dict[str, Any]:
    """Performs an external web search query using the Tavily client."""
    client = get_tavily_client()
    
    response = client.search(
        query=query,
        max_results=max_results,
        search_depth=search_depth,
        include_answer=include_answer
    )
    
    results = []
    for result in response.get("results", []):
        results.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
            "score": result.get("score", 0)
        })
    
    return {
        "success": True,
        "query": query,
        "answer": response.get("answer"),
        "results": results,
        "source": "web_search"
    }


def format_web_results_as_context(search_results: Dict[str, Any]) -> str:
    """Formats Tavily web search results into structured text passages for LLM prompt insertion."""
    if not search_results.get("success"):
        return f"Web search failed: {search_results.get('error', 'Unknown error')}"
    
    context_parts = []
    
    if search_results.get("answer"):
        context_parts.append(f"Summary: {search_results['answer']}\n")
    
    context_parts.append("Web Sources:")
    for i, result in enumerate(search_results.get("results", []), 1):
        context_parts.append(f"\n[{i}] {result.get('title', 'Untitled')}")
        context_parts.append(f"URL: {result.get('url', '')}")
        context_parts.append(f"Content: {result.get('content', '')[:500]}...")
    
    return "\n".join(context_parts)


