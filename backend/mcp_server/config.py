# Purpose: Configuration settings loader and schema constants.
# Responsibilities: Loads workspace variables from environment configurations, and defines 
# collection settings, embedding dimensions, relevance thresholds, and layout extraction directory paths.

import os

from pathlib import Path
from dotenv import load_dotenv

# Load workspace configuration environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Service credentials
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Vector index configurations
COLLECTION_NAME = "multimodal_rag"
EMBEDDING_DIM = 768  # Output dimension of local BAAI/bge-base-en-v1.5 model

# Model execution targets
GEMINI_MODEL = "gemini-2.5-flash"
BGE_MODEL_NAME = "BAAI/bge-base-en-v1.5"  # Locally run embedding model

# Ingestion & Retrieval thresholds
TOP_K = 5
RELEVANCE_THRESHOLD = 0.5  # Similarity threshold deciding if vector context is sufficient
MAX_RETRIES = 3

# Output paths for parsed PDF structures
OUTPUT_FOLDER = Path(__file__).parent.parent / "extracted_content"
IMAGES_FOLDER = OUTPUT_FOLDER / "images"
TABLES_FOLDER = OUTPUT_FOLDER / "tables"
