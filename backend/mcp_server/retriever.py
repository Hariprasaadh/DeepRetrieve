# Qdrant vector database operations

from typing import List, Dict, Optional
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct, BinaryQuantization, BinaryQuantizationConfig

from .config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMBEDDING_DIM
from .embeddings import embed_text, embed_image

# Connect to Qdrant immediately
print(f"Connecting to Qdrant Cloud at {QDRANT_URL}...")
import time
start = time.time()

_qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=10,
    prefer_grpc=False,
)

# Test connection
_qdrant_client.get_collections()

elapsed = time.time() - start
print(f"✅ Qdrant Cloud connected! ({elapsed:.2f}s)")


def get_qdrant_client() -> QdrantClient:
    """Get Qdrant client instance"""
    return _qdrant_client


def create_collection(collection_name: str = COLLECTION_NAME, recreate: bool = False):
    """Create a Qdrant collection with Binary Quantization"""
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
    """Search for similar content in Qdrant"""
    client = get_qdrant_client()
    
    # Embed the query
    query_embedding = embed_text(query)
    
    # Build filter if content type specified
    query_filter = None
    if content_type:
        query_filter = models.Filter(
            must=[models.FieldCondition(key="type", match=models.MatchValue(value=content_type))]
        )
    
    # Search using query_points (new API)
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k,
        query_filter=query_filter
    )
    
    # Format results
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
            "csv_path": result.payload.get("csv_path"),
            "table_index": result.payload.get("table_index")
        })
    
    return formatted_results


def search_by_image(
    image_input,
    top_k: int = 5,
    collection_name: str = COLLECTION_NAME
) -> List[Dict]:
    """Search using an image as query"""
    client = get_qdrant_client()
    
    # Embed the image
    query_embedding = embed_image(image_input)
    
    # Search using query_points (new API)
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k
    )
    
    # Format results
    formatted_results = []
    for result in results.points:
        formatted_results.append({
            "score": result.score,
            "type": result.payload.get("type"),
            "content": result.payload.get("content"),
            "image_base64": result.payload.get("image_base64"),
            "source": result.payload.get("source"),
            "page": result.payload.get("page"),
            "csv_path": result.payload.get("csv_path"),
            "table_index": result.payload.get("table_index")
        })
    
    return formatted_results


def get_collection_info(collection_name: str = COLLECTION_NAME) -> Dict:
    """Get information about the collection"""
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
