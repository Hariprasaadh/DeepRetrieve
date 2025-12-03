# DeepRetrieve MCP Server
# Exposes RAG retriever and web search as MCP tools

from .server import mcp as mcp_app, run_server
from .retriever import search_similar, get_collection_info, create_collection
from .web_search import web_search, format_web_results_as_context
from .embeddings import embed_text, embed_image, embed_image_base64
from .llm import generate_response, prepare_context_from_results, check_context_relevance

__all__ = [
    "mcp_app",
    "run_server",
    "search_similar",
    "get_collection_info",
    "create_collection",
    "web_search",
    "format_web_results_as_context",
    "embed_text",
    "embed_image",
    "embed_image_base64",
    "generate_response",
    "prepare_context_from_results",
    "check_context_relevance"
]
