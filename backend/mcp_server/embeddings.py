# Purpose: Local dense embedding model interface.
# Responsibilities: Loads the BAAI/bge-base-en-v1.5 sentence-transformers model locally on 
# CPU or GPU, generates query/document vector representations, and formats text-search inputs.

import torch

from typing import List
from sentence_transformers import SentenceTransformer

from .config import BGE_MODEL_NAME

_device = "cuda" if torch.cuda.is_available() else "cpu"

# Singleton initialization of local SentenceTransformer
print(f"Loading embedding model: {BGE_MODEL_NAME} on {_device.upper()}...")
_model = SentenceTransformer(BGE_MODEL_NAME, device=_device)
print(f"✅ Embedding model ready! (dim={_model.get_sentence_embedding_dimension()}, device={_device})")


def embed_text(text: str) -> List[float]:
    """Generates normalized dense vector embeddings for document text chunks."""
    embedding = _model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embed_query(query: str) -> List[float]:
    """Generates normalized dense vector embeddings for a query.

    Appends the specific task-related instruction prefix required by BGE models
    to align the query vector with the document chunk vector space.
    """
    prefixed = f"Represent this sentence for searching relevant passages: {query}"
    embedding = _model.encode(prefixed, normalize_embeddings=True)
    return embedding.tolist()


def embed_image_base64(base64_string: str) -> List[float]:
    """Base64 image embedding. Not supported by the text-only BGE model."""
    raise NotImplementedError(
        "Image byte embedding is not supported with the local bge model. "
        "Embed the image caption text using embed_text() instead."
    )


def embed_image(image_input) -> List[float]:
    """Direct image embedding. Not supported by the text-only BGE model."""
    raise NotImplementedError(
        "Image embedding is not supported with the local bge model. "
        "Use embed_text() on a text description instead."
    )
