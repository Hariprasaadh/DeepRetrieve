# DeepRetrieve MCP Server

MCP (Model Context Protocol) server that exposes the RAG retriever and web search as formal tools, allowing LLMs to autonomously orchestrate multi-step retrieval with fallback logic.

## Tools

### 1. `rag_retrieve`
Search the multimodal vector database for relevant documents, images, and tables.

```python
rag_retrieve(
    query: str,           # Natural language search query
    top_k: int = 5,       # Number of results
    content_type: str     # Optional filter: "text", "image", or "table"
)
```

### 2. `fallback_web_search`
Web search fallback when RAG context is insufficient.

```python
fallback_web_search(
    query: str,           # Search query
    max_results: int = 5  # Number of web results
)
```

### 3. `hybrid_search`
Intelligent hybrid search that automatically falls back to web search if RAG results are insufficient.

```python
hybrid_search(
    query: str,           # Search query
    top_k: int = 5,       # RAG results count
    web_fallback: bool    # Enable web fallback (default: True)
)
```

### 4. `generate_answer`
Generate an answer using Gemini LLM with provided context.

```python
generate_answer(
    query: str,           # User's question
    context: str,         # Context from retrieval
    include_sources: bool # Cite sources (default: True)
)
```

### 5. `get_knowledge_base_info`
Get statistics about the vector database collection.

## Running the Server

### Using uv
```bash
cd backend
uv run python -m mcp_server.server
```

### Using the script entry point
```bash
cd backend
uv run deepretrieve
```

## Configuration

Set these environment variables in `.env`:

```env
GOOGLE_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "deepretrieve": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/backend", "deepretrieve"]
    }
  }
}
```

## Orchestration Logic

The MCP server is designed for agentic workflows:

1. **First attempt**: Use `rag_retrieve` to search the knowledge base
2. **Check relevance**: If average score < 0.5, results are insufficient
3. **Fallback**: Use `fallback_web_search` for additional context
4. **Generate**: Use `generate_answer` to produce the final response

Or use `hybrid_search` which handles this logic automatically.

## Architecture

```
mcp_server/
├── __init__.py      # Module exports
├── config.py        # Configuration and environment variables
├── embeddings.py    # CLIP embedding functions
├── retriever.py     # Qdrant vector search
├── web_search.py    # Tavily web search fallback
├── llm.py           # Gemini LLM integration
└── server.py        # FastMCP server with tool definitions
```
