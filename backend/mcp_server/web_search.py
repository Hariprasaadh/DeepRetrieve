# Web search fallback using Tavily API

from typing import List, Dict, Any
import json

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

from .config import TAVILY_API_KEY


# Global client instance (lazy loaded)
_tavily_client = None


def get_tavily_client():
    """Get or initialize Tavily client (lazy loading)"""
    global _tavily_client
    
    if _tavily_client is None:
        if TavilyClient is None:
            raise ImportError("tavily-python is not installed. Run: uv add tavily-python")
        
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY not set in environment")
        
        print("Initializing Tavily client...")
        _tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
        print("Tavily client ready!")
    
    return _tavily_client


def web_search(
    query: str,
    max_results: int = 5,
    search_depth: str = "basic",
    include_answer: bool = True
) -> Dict[str, Any]:
    """
    Perform web search using Tavily API
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        search_depth: "basic" or "advanced"
        include_answer: Whether to include AI-generated answer
    
    Returns:
        Dictionary with search results and optional answer
    """
    client = get_tavily_client()
    
    try:
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
    
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(e),
            "results": [],
            "source": "web_search"
        }


def format_web_results_as_context(search_results: Dict[str, Any]) -> str:
    """Format web search results as context for LLM"""
    if not search_results.get("success"):
        return f"Web search failed: {search_results.get('error', 'Unknown error')}"
    
    context_parts = []
    
    # Add the AI-generated answer if available
    if search_results.get("answer"):
        context_parts.append(f"Summary: {search_results['answer']}\n")
    
    # Add individual results
    context_parts.append("Web Sources:")
    for i, result in enumerate(search_results.get("results", []), 1):
        context_parts.append(f"\n[{i}] {result.get('title', 'Untitled')}")
        context_parts.append(f"URL: {result.get('url', '')}")
        context_parts.append(f"Content: {result.get('content', '')[:500]}...")
    
    return "\n".join(context_parts)
