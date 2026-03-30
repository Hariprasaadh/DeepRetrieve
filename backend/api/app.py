# DeepRetrieve FastAPI Application

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting DeepRetrieve API (Local Mode)...")
    print("📦 Initializing services...")
    
    # Initialize Qdrant connection
    from mcp_server.retriever import get_qdrant_client, create_collection, COLLECTION_NAME
    client = get_qdrant_client()
    create_collection(COLLECTION_NAME)
    
    print("✅ All services ready!")
    yield
    print("👋 Shutting down...")


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

from fastapi.staticfiles import StaticFiles
from mcp_server.config import IMAGES_FOLDER

app.include_router(router, prefix="/api/v1", tags=["RAG"])
app.mount("/images", StaticFiles(directory=str(IMAGES_FOLDER)), name="images")

@app.get("/")
async def root():
    return {"status": "ok", "message": "DeepRetrieve API", "docs": "/docs"}
