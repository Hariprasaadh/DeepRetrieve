# DeepRetrieve Model Context Protocol (MCP) Specifications

The DeepRetrieve backend natively exposes a **Model Context Protocol (MCP)** server interface. Compliant LLM clients (such as Claude Desktop or Cursor) can connect via stdio transport to autonomously run document retrieval, web searches, and visual reasoning tasks.

---

##  What is Model Context Protocol?

MCP is an open standard that enables models to connect to local and remote data stores and tools safely. In DeepRetrieve, the MCP server is built using the **FastMCP** Python SDK, turning RAG databases and web engines into modular client-accessible tools.

---

##  Exposed Tools Registry

The following tools are registered on the DeepRetrieve MCP server:

### 1. `rag_retrieve`
Queries the local Qdrant vector database for document chunks matching the query string.

- **Parameters**:
  - `query` (`str`, Required): The search query.
  - `top_k` (`int`, Optional, Default: `5`): Maximum context items to retrieve.
  - `content_type` (`str`, Optional): Filter results by type (`"text"`, `"table"`, or `"image"`).
- **Return Type**: `Dict[str, Any]` (Contains hits list with confidence scores, page numbers, and source filenames).

---

### 2. `web_search`
Performs a live query on the external internet using Tavily's search indexes.

- **Parameters**:
  - `query` (`str`, Required): The search query.
  - `max_results` (`int`, Optional, Default: `5`): Number of search hits to fetch.
  - `search_depth` (`str`, Optional, Default: `"basic"`): Search detail grade (`"basic"` or `"advanced"`).
- **Return Type**: `Dict[str, Any]` (Contains success state, answer summaries, and url list).

---

### 3. `hybrid_retrieve`
Performs an optimized retrieval flow. It queries the local document store first. If the similarity scores are lower than the threshold, it automatically falls back to internet search.

- **Parameters**:
  - `query` (`str`, Required): The query.
  - `top_k` (`int`, Optional, Default: `5`): Maximum items to fetch.
  - `relevance_threshold` (`float`, Optional, Default: `0.5`): Minimum score matching.
- **Return Type**: `Dict[str, Any]` (Contains combined sources and source origin tags).

---

### 4. `generate_answer`
Queries the Google Gemini model directly using the provided context block, yielding structured text responses.

- **Parameters**:
  - `query` (`str`, Required): User question.
  - `context` (`str`, Required): Text snippets to answer from.
  - `include_sources` (`bool`, Optional, Default: `True`): Directs model to add citation indexes like `[1]`, `[2]`.
- **Return Type**: `Dict[str, Any]` (Contains generated response text).

---

### 5. `get_knowledge_base_info`
Returns collection diagnostics, including indexed vector counts and storage status.

- **Parameters**: None
- **Return Type**: `Dict[str, Any]` (Contains total vectors and indexing state).

---

