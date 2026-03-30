# Embedding functions — powered by BAAI/bge-base-en-v1.5 

import torch
from typing import List
from sentence_transformers import SentenceTransformer

from .config import BGE_MODEL_NAME

# Use GPU if available
_device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model once at startup (singleton) — ~438 MB, cached after first download
print(f"Loading embedding model: {BGE_MODEL_NAME} on {_device.upper()}...")
_model = SentenceTransformer(BGE_MODEL_NAME, device=_device)
print(f"✅ Embedding model ready! (dim={_model.get_sentence_embedding_dimension()}, device={_device})")



def embed_text(text: str) -> List[float]:
    """Embed a document text chunk for indexing."""
    embedding = _model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embed_query(query: str) -> List[float]:
    """Embed a search query.
    
    BGE models benefit from an instruction prefix for queries.
    """
    prefixed = f"Represent this sentence for searching relevant passages: {query}"
    embedding = _model.encode(prefixed, normalize_embeddings=True)
    return embedding.tolist()


def embed_image_base64(base64_string: str) -> List[float]:
    """Not supported with text-only model — use embed_text on the image caption instead."""
    raise NotImplementedError(
        "Image byte embedding is not supported with the local bge model. "
        "Embed the image caption text using embed_text() instead."
    )


def embed_image(image_input) -> List[float]:
    """Not supported with text-only model."""
    raise NotImplementedError(
        "Image embedding is not supported with the local bge model. "
        "Use embed_text() on a text description instead."
    )
