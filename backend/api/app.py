# DeepRetrieve FastAPI Application

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting DeepRetrieve API...")
    print("📦 Initializing services...")
    
    # Eagerly load Qdrant connection
    from mcp_server.retriever import get_qdrant_client, create_collection, COLLECTION_NAME
    client = get_qdrant_client()
    create_collection(COLLECTION_NAME)
    
    # Eagerly test HF Space connection if enabled
    from mcp_server.config import USE_HF_SPACE, HF_SPACE_URL
    if USE_HF_SPACE:
        print(f"Testing HuggingFace Space: {HF_SPACE_URL}")
        import requests
        try:
            resp = requests.get(HF_SPACE_URL, timeout=5)
            print(f"✅ HF Space connected! Status: {resp.status_code}")
        except Exception as e:
            print(f"⚠️ HF Space not reachable: {e}")
    
    print("✅ All services ready!")
    yield
    print("👋 Shutting down DeepRetrieve API...")


app = FastAPI(
    title="DeepRetrieve API",
    description="Multimodal RAG with automatic web search fallback",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["RAG"])


@app.get("/")
async def root():
    return {"status": "ok", "message": "DeepRetrieve API", "docs": "/docs"}
