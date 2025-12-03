# DeepRetrieve FastAPI Application

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .models import HealthResponse

from mcp_server.retriever import get_qdrant_client, create_collection
from mcp_server.embeddings import get_clip_model
from mcp_server.config import COLLECTION_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    print("🚀 Starting DeepRetrieve API...")
    
    # Initialize CLIP model (lazy load on first use)
    print("📦 CLIP model will be loaded on first use")
    
    # Initialize Qdrant connection
    try:
        client = get_qdrant_client()
        create_collection(COLLECTION_NAME)
        print("✅ Qdrant connected")
    except Exception as e:
        print(f"⚠️ Qdrant connection failed: {e}")
    
    yield
    
    print("👋 Shutting down DeepRetrieve API...")


# Create FastAPI app
app = FastAPI(
    title="DeepRetrieve API",
    description="MCP-Powered Agentic Multimodal RAG System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1", tags=["RAG"])


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    # Check services
    qdrant_ok = False
    clip_ok = False
    
    try:
        get_qdrant_client()
        qdrant_ok = True
    except:
        pass
    
    try:
        get_clip_model()
        clip_ok = True
    except:
        pass
    
    return HealthResponse(
        status="healthy" if qdrant_ok else "degraded",
        version="1.0.0",
        services={
            "qdrant": qdrant_ok,
            "clip": clip_ok
        }
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return await root()
