# Purpose: FastMCP tool definition and server entrypoint.
# Responsibilities: Exposes RAG retrieval, fallback web search, and hybrid retrieval tools
# to Model Context Protocol clients for agent orchestration.

from typing import Optional, Dict, Any
from fastmcp import FastMCP

from .config import COLLECTION_NAME, TOP_K, RELEVANCE_THRESHOLD
from .retriever import search_similar, get_collection_info
from .web_search import web_search, format_web_results_as_context
from .llm import prepare_context_from_results, generate_response, check_context_relevance


# FastMCP instance defining agent tools
mcp = FastMCP(
    name="deepretrieve",
    instructions="""
    DeepRetrieve MCP Server - Agentic Multimodal RAG System
    
    This server provides two main tools:
    1. rag_retrieve - Search the vector database for relevant documents, images, and tables
    2. web_search - Fallback web search when RAG context is insufficient
    
    Orchestration Logic:
    - First, use rag_retrieve to search the knowledge base
    - If the relevance scores are low (< 0.5), use web_search as fallback
    - Combine results for comprehensive answers
    """
)


@mcp.tool()
def rag_retrieve(
    query: str,
    top_k: int = TOP_K,
    content_type: Optional[str] = None
) -> Dict[str, Any]:
    """Queries the local vector database for document chunks matching the query string."""
    print(f"🔍 [TOOL CALL] rag_retrieve | query: '{query}' | top_k: {top_k}")
    
    results = search_similar(
        query=query,
        top_k=top_k,
        content_type=content_type
    )
    
    is_relevant = check_context_relevance(query, results, RELEVANCE_THRESHOLD)
    context = prepare_context_from_results(results)
    avg_score = sum(r.get("score", 0) for r in results) / len(results) if results else 0
    
    return {
        "success": True,
        "query": query,
        "results_count": len(results),
        "results": results,
        "is_relevant": is_relevant,
        "average_score": avg_score,
        "relevance_threshold": RELEVANCE_THRESHOLD,
        "context": context,
        "suggestion": None if is_relevant else "Consider using web_search for additional context"
    }


@mcp.tool()
def fallback_web_search(
    query: str,
    max_results: int = 5
) -> Dict[str, Any]:
    """Queries external web indices when local vector search results fail relevance checks."""
    print(f"🌐 [TOOL CALL] fallback_web_search | query: '{query}' | max_results: {max_results}")
    
    search_results = web_search(
        query=query,
        max_results=max_results,
        include_answer=True
    )
    context = format_web_results_as_context(search_results)
    
    return {
        "success": search_results.get("success", False),
        "query": query,
        "answer": search_results.get("answer"),
        "results": search_results.get("results", []),
        "context": context,
        "source": "web_search"
    }


@mcp.tool()
def hybrid_search(
    query: str,
    top_k: int = TOP_K,
    web_fallback: bool = True
) -> Dict[str, Any]:
    """Performs local retrieval and falls back to web search if local context is insufficient."""
    print(f"🔀 [TOOL CALL] hybrid_search | query: '{query}' | top_k: {top_k} | fallback: {web_fallback}")
    
    rag_results = rag_retrieve(query=query, top_k=top_k)
    
    combined = {
        "query": query,
        "rag_results": rag_results,
        "web_results": None,
        "used_fallback": False,
        "combined_context": rag_results.get("context", "")
    }
    
    if web_fallback and not rag_results.get("is_relevant", False):
        web_results = fallback_web_search(query=query)
        combined["web_results"] = web_results
        combined["used_fallback"] = True
        
        if web_results.get("success"):
            combined["combined_context"] = f"""
RAG Context:
{rag_results.get('context', 'No RAG results')}

Web Context:
{web_results.get('context', 'No web results')}
"""
    
    return combined


@mcp.tool()
def generate_answer(
    query: str,
    context: str,
    include_sources: bool = True
) -> Dict[str, Any]:
    """Synthesizes a final reply to the user prompt using the provided context blocks via the LLM."""
    print(f"💬 [TOOL CALL] generate_answer | query: '{query}' | context_len: {len(context)}")
    
    system_prompt = """You are a helpful assistant that answers questions based on the provided context.
Use the context to answer the question accurately and comprehensively."""
    
    if include_sources:
        system_prompt += "\nAlways cite the source numbers [1], [2], etc. when using information from the context."
    
    return generate_response(
        query=query,
        context=context,
        system_prompt=system_prompt
    )


@mcp.tool()
def get_knowledge_base_info() -> Dict[str, Any]:
    """Fetches vector store diagnostic status and record counts."""
    print("📊 [TOOL CALL] get_knowledge_base_info")
    return get_collection_info()


def run_server():
    """Starts the MCP server process loop."""
    print("Starting DeepRetrieve MCP Server...")
    mcp.run()


if __name__ == "__main__":
    run_server()
