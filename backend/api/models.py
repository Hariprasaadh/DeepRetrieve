# Pydantic models for API requests and responses

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


# ============== Request Models ==============

class SearchRequest(BaseModel):
    """Request model for text search"""
    query: str = Field(..., description="Search query text")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")
    content_type: Optional[str] = Field(
        default=None, 
        description="Filter by content type: 'text', 'image', or 'table'"
    )


class ImageSearchRequest(BaseModel):
    """Request model for image-based search"""
    image_base64: str = Field(..., description="Base64 encoded image")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")


class HybridSearchRequest(BaseModel):
    """Request model for hybrid search (RAG + Web)"""
    query: str = Field(..., description="Search query text")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of RAG results")
    web_fallback: bool = Field(default=True, description="Use web search as fallback")


class GenerateRequest(BaseModel):
    """Request model for answer generation"""
    query: str = Field(..., description="User's question")
    context: str = Field(..., description="Context for the LLM")
    include_sources: bool = Field(default=True, description="Include source citations")


class RAGQueryRequest(BaseModel):
    """Request model for complete RAG pipeline"""
    query: str = Field(..., description="User's question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results")
    use_web_fallback: bool = Field(default=True, description="Use web search if RAG insufficient")


class UploadPDFRequest(BaseModel):
    """Metadata for PDF upload"""
    source_name: Optional[str] = Field(default=None, description="Custom name for the source")


# ============== Response Models ==============

class SearchResult(BaseModel):
    """Single search result"""
    score: float
    type: Optional[str]
    content: Optional[str]
    image_base64: Optional[str] = None
    source: Optional[str]
    page: Optional[int] = None
    path: Optional[str] = None
    csv_path: Optional[str] = None
    table_index: Optional[int] = None


class SearchResponse(BaseModel):
    """Response model for search operations"""
    success: bool
    query: str
    results_count: int
    results: List[SearchResult]
    is_relevant: bool
    average_score: float
    context: Optional[str] = None


class WebSearchResult(BaseModel):
    """Single web search result"""
    title: str
    url: str
    content: str
    score: float


class WebSearchResponse(BaseModel):
    """Response model for web search"""
    success: bool
    query: str
    answer: Optional[str]
    results: List[WebSearchResult]
    context: str


class HybridSearchResponse(BaseModel):
    """Response model for hybrid search"""
    query: str
    rag_results: SearchResponse
    web_results: Optional[WebSearchResponse]
    used_fallback: bool
    combined_context: str


class GenerateResponse(BaseModel):
    """Response model for answer generation"""
    success: bool
    query: str
    response: Optional[str] = None
    error: Optional[str] = None


class RAGQueryResponse(BaseModel):
    """Response model for complete RAG pipeline"""
    success: bool
    query: str
    answer: Optional[str] = None
    sources: List[SearchResult] = []
    used_web_fallback: bool = False
    error: Optional[str] = None


class CollectionInfoResponse(BaseModel):
    """Response model for collection info"""
    exists: bool
    points_count: Optional[int] = None
    vectors_count: Optional[int] = None
    status: Optional[str] = None
    message: Optional[str] = None


class UploadResponse(BaseModel):
    """Response model for file uploads"""
    success: bool
    message: str
    filename: str
    texts_added: int = 0
    images_added: int = 0
    tables_added: int = 0


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    version: str
    services: Dict[str, bool]
