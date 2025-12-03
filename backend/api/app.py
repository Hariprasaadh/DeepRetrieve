# DeepRetrieve FastAPI Application

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .models import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    print("🚀 Starting DeepRetrieve API...")
    print("📦 Services will be initialized on first use (lazy loading)")
    
    # Don't initialize heavy services at startup - let them lazy load
    # This prevents memory issues on free tier hosting
    
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
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={
            "api": True
        }
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check - checks all services"""
    qdrant_ok = False
    clip_ok = False
    
    try:
        from mcp_server.retriever import get_qdrant_client
        get_qdrant_client()
        qdrant_ok = True
    except:
        pass
    
    try:
        from mcp_server.embeddings import get_clip_model
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
