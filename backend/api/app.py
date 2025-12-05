# DeepRetrieve FastAPI Application

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting DeepRetrieve API...")
    print("📦 Services will be initialized on first use (lazy loading)")
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
