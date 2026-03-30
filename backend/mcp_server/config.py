# Configuration for MCP Server and RAG components

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Tavily API for web search (get free key at https://tavily.com)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Qdrant Configuration
COLLECTION_NAME = "multimodal_rag"
EMBEDDING_DIM = 768  # BAAI/bge-base-en-v1.5 output dimension


# Gemini Configuration (LLM only — embeddings are handled locally)
GEMINI_MODEL = "gemini-2.5-flash"

# Local Embedding Model
BGE_MODEL_NAME = "BAAI/bge-base-en-v1.5"  # ~438 MB, 768 dims

# RAG Configuration
TOP_K = 5
RELEVANCE_THRESHOLD = 0.5  # Minimum score to consider context sufficient

MAX_RETRIES = 3  # Max retries on transient errors

# Output Paths
OUTPUT_FOLDER = Path(__file__).parent.parent / "extracted_content"
IMAGES_FOLDER = OUTPUT_FOLDER / "images"
TABLES_FOLDER = OUTPUT_FOLDER / "tables"
