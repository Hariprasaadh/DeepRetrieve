# API routes - 3 essential endpoints only

from typing import Optional, List
import os
import tempfile
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field


# Request/Response Models

class QueryRequest(BaseModel):
    query: str = Field(..., description="Your question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of sources to retrieve")


class Source(BaseModel):
    type: str
    content: str
    source: Optional[str] = None
    page: Optional[int] = None
    score: float


class QueryResponse(BaseModel):
    success: bool
    query: str
    answer: Optional[str] = None
    sources: List[Source] = []
    used_web_search: bool = False
    error: Optional[str] = None


class UploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    texts_added: int = 0
    images_added: int = 0
    tables_added: int = 0


# Lazy imports
def get_retriever():
    from mcp_server.retriever import search_similar
    return search_similar

def get_web_search():
    from mcp_server.web_search import web_search, format_web_results_as_context
    return web_search, format_web_results_as_context

def get_llm():
    from mcp_server.llm import generate_response, prepare_context_from_results, check_context_relevance
    from mcp_server.config import RELEVANCE_THRESHOLD
    return generate_response, prepare_context_from_results, check_context_relevance, RELEVANCE_THRESHOLD


router = APIRouter()


@router.get("/ping")
async def ping():
    """Check if API is running"""
    return {"status": "ok", "message": "DeepRetrieve API is running!"}


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Ask a question - RAG first, LLM decides if web search needed"""
    try:
        search_similar = get_retriever()
        web_search, format_web_results = get_web_search()
        generate_response, prepare_context, _, _ = get_llm()
        
        # Step 1: Always get RAG results first
        results = search_similar(query=request.query, top_k=request.top_k)
        rag_context = prepare_context(results)
        
        sources = []
        for r in results:
            if r.get("content"):
                sources.append(Source(
                    type=r.get("type", "unknown"),
                    content=r.get("content", "")[:500],
                    source=r.get("source"),
                    page=r.get("page"),
                    score=r.get("score", 0)
                ))
        
        # Step 2: Ask LLM to answer with RAG context, or request web search
        llm_prompt = f"""Answer the user's question using the provided context.

If the context contains relevant information: Answer the question directly.
If the context is NOT sufficient or irrelevant: Reply EXACTLY with "NEED_WEB_SEARCH" (nothing else).

CONTEXT:
{rag_context if rag_context else "No documents found."}

QUESTION: {request.query}

ANSWER:"""

        from mcp_server.llm import get_gemini_model, _apply_rate_limit
        model = get_gemini_model()
        _apply_rate_limit()
        
        first_response = model.generate_content(llm_prompt)
        answer = first_response.text.strip()
        used_web = False
        
        # Step 3: If LLM says it needs web search, do it
        if "NEED_WEB_SEARCH" in answer:
            web_results = web_search(query=request.query, max_results=5)
            
            if web_results.get("success"):
                web_context = format_web_results(web_results)
                used_web = True
                
                # Add web sources
                sources = []  # Replace with web sources
                for r in web_results.get("results", [])[:5]:
                    sources.append(Source(
                        type="web",
                        content=r.get("content", "")[:500],
                        source=r.get("url"),
                        page=None,
                        score=r.get("score", 0)
                    ))
                
                # Ask LLM again with web context
                _apply_rate_limit()
                web_response = model.generate_content(
                    f"Answer this question using the web search results:\n\n{web_context}\n\nQuestion: {request.query}"
                )
                answer = web_response.text.strip()
        
        return QueryResponse(
            success=True,
            query=request.query,
            answer=answer,
            sources=sources,
            used_web_search=used_web,
            error=None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF to the knowledge base"""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        from .pdf_processor import process_pdf
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        try:
            texts_added, images_added, tables_added = process_pdf(tmp_path)
            
            return UploadResponse(
                success=True,
                message=f"Processed {file.filename}",
                filename=file.filename,
                texts_added=texts_added,
                images_added=images_added,
                tables_added=tables_added
            )
        finally:
            os.unlink(tmp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/reset")
async def reset_collection():
    """Reset the vector database (delete all documents)"""
    try:
        from mcp_server.retriever import get_qdrant_client, create_collection, COLLECTION_NAME
        client = get_qdrant_client()
        
        if client.collection_exists(COLLECTION_NAME):
            client.delete_collection(COLLECTION_NAME)
        
        create_collection(COLLECTION_NAME)
        
        return {"success": True, "message": "Collection reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
