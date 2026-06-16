# Purpose: Qdrant Vector Database connection management and indexing interfaces.
# Responsibilities: Initializes the Qdrant Cloud client, registers collections configured
# with Binary Quantization indices, and handles vector similarity lookups.

import time
from typing import List, Dict, Optional
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct, BinaryQuantization, BinaryQuantizationConfig

from .config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_DIM
from .embeddings import embed_text, embed_query, embed_image

print(f"Connecting to Qdrant Cloud at {QDRANT_URL}...")
start = time.time()

# Establish Qdrant database connection on module import
_qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=10,
    prefer_grpc=False,
)

# Verify link viability
_qdrant_client.get_collections()

elapsed = time.time() - start
print(f"✅ Qdrant Cloud connected! ({elapsed:.2f}s)")


def get_qdrant_client() -> QdrantClient:
    """Returns the shared Qdrant client instance."""
    return _qdrant_client


def create_collection(collection_name: str = COLLECTION_NAME, recreate: bool = False):
    """Initializes the target collection in Qdrant with cosine distance metric and on-disk payload storage.

    Uses Binary Quantization (BQ) configured to cache vectors in RAM for faster index queries,
    mitigating network retrieval latencies.
    """
    client = get_qdrant_client()
    
    if recreate and client.collection_exists(collection_name=collection_name):
        print(f"Deleting existing collection: {collection_name}")
        client.delete_collection(collection_name)
    
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE,
                on_disk=True
            ),
            quantization_config=BinaryQuantization(
                binary=BinaryQuantizationConfig(
                    always_ram=True
                )
            ),
        )
        print(f"Created collection: {collection_name}")
    else:
        print(f"Collection '{collection_name}' already exists")


def search_similar(
    query: str,
    top_k: int = 5,
    collection_name: str = COLLECTION_NAME,
    content_type: Optional[str] = None
) -> List[Dict]:
    """Queries Qdrant for items matching the semantic embedding of the query string.

    Supports categorical filtering (e.g. text, image, table) through payload matching.
    """
    client = get_qdrant_client()
    query_embedding = embed_query(query)
    
    query_filter = None
    if content_type:
        query_filter = models.Filter(
            must=[models.FieldCondition(key="type", match=models.MatchValue(value=content_type))]
        )
    
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k,
        query_filter=query_filter
    )
    
    formatted_results = []
    for result in results.points:
        formatted_results.append({
            "score": result.score,
            "type": result.payload.get("type"),
            "content": result.payload.get("content"),
            "image_base64": result.payload.get("image_base64"),
            "source": result.payload.get("source"),
            "page": result.payload.get("page"),
            "path": result.payload.get("path"),
            "json_path": result.payload.get("json_path"),
            "headers": result.payload.get("headers"),
            "table_index": result.payload.get("table_index")
        })
    
    return formatted_results


def search_by_image(
    image_input,
    top_k: int = 5,
    collection_name: str = COLLECTION_NAME
) -> List[Dict]:
    """Retrieves payload objects utilizing an image embedding as the query vector."""
    client = get_qdrant_client()
    query_embedding = embed_image(image_input)
    
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k
    )
    
    formatted_results = []
    for result in results.points:
        formatted_results.append({
            "score": result.score,
            "type": result.payload.get("type"),
            "content": result.payload.get("content"),
            "image_base64": result.payload.get("image_base64"),
            "source": result.payload.get("source"),
            "page": result.payload.get("page"),
            "json_path": result.payload.get("json_path"),
            "headers": result.payload.get("headers"),
            "table_index": result.payload.get("table_index")
        })
    
    return formatted_results


def get_collection_info(collection_name: str = COLLECTION_NAME) -> Dict:
    """Fetches diagnostic statistics and record counts for the target Qdrant collection."""
    client = get_qdrant_client()
    
    if not client.collection_exists(collection_name):
        return {"exists": False, "message": f"Collection '{collection_name}' does not exist"}
    
    info = client.get_collection(collection_name)
    return {
        "exists": True,
        "points_count": info.points_count,
        "indexed_vectors_count": getattr(info, 'indexed_vectors_count', None),
        "status": str(info.status)
    }
