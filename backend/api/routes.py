# API route handlers

from typing import Optional
import os
import tempfile
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from .models import (
    SearchRequest, SearchResponse, SearchResult,
    ImageSearchRequest,
    HybridSearchRequest, HybridSearchResponse,
    GenerateRequest, GenerateResponse,
    RAGQueryRequest, RAGQueryResponse,
    WebSearchResponse, WebSearchResult,
    CollectionInfoResponse,
    UploadResponse
)

from mcp_server.retriever import search_similar, search_by_image, get_collection_info
from mcp_server.web_search import web_search, format_web_results_as_context
from mcp_server.llm import (
    generate_response, 
    prepare_context_from_results, 
    check_context_relevance
)
from mcp_server.config import RELEVANCE_THRESHOLD, TOP_K


router = APIRouter()


# Search Endpoints
@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """Search the vector database for relevant documents"""
    try:
        results = search_similar(
            query=request.query,
            top_k=request.top_k,
            content_type=request.content_type
        )
        
        is_relevant = check_context_relevance(request.query, results, RELEVANCE_THRESHOLD)
        avg_score = sum(r.get("score", 0) for r in results) / len(results) if results else 0
        context = prepare_context_from_results(results)
        
        return SearchResponse(
            success=True,
            query=request.query,
            results_count=len(results),
            results=[SearchResult(**r) for r in results],
            is_relevant=is_relevant,
            average_score=avg_score,
            context=context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/image", response_model=SearchResponse)
async def search_by_image_endpoint(request: ImageSearchRequest):
    """Search using an image as query"""
    try:
        results = search_by_image(
            image_input=request.image_base64,
            top_k=request.top_k
        )
        
        avg_score = sum(r.get("score", 0) for r in results) / len(results) if results else 0
        
        return SearchResponse(
            success=True,
            query="[Image Query]",
            results_count=len(results),
            results=[SearchResult(**r) for r in results],
            is_relevant=avg_score >= RELEVANCE_THRESHOLD,
            average_score=avg_score,
            context=prepare_context_from_results(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/web", response_model=WebSearchResponse)
async def web_search_endpoint(query: str, max_results: int = 5):
    """Search the web for information"""
    try:
        results = web_search(query=query, max_results=max_results)
        context = format_web_results_as_context(results)
        
        return WebSearchResponse(
            success=results.get("success", False),
            query=query,
            answer=results.get("answer"),
            results=[WebSearchResult(**r) for r in results.get("results", [])],
            context=context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/hybrid", response_model=HybridSearchResponse)
async def hybrid_search_endpoint(request: HybridSearchRequest):
    """Hybrid search combining RAG and web search"""
    try:
        # First, RAG search
        rag_results = search_similar(query=request.query, top_k=request.top_k)
        is_relevant = check_context_relevance(request.query, rag_results, RELEVANCE_THRESHOLD)
        avg_score = sum(r.get("score", 0) for r in rag_results) / len(rag_results) if rag_results else 0
        rag_context = prepare_context_from_results(rag_results)
        
        rag_response = SearchResponse(
            success=True,
            query=request.query,
            results_count=len(rag_results),
            results=[SearchResult(**r) for r in rag_results],
            is_relevant=is_relevant,
            average_score=avg_score,
            context=rag_context
        )
        
        web_response = None
        combined_context = rag_context
        used_fallback = False
        
        # Web fallback if needed
        if request.web_fallback and not is_relevant:
            web_results = web_search(query=request.query, max_results=5)
            web_context = format_web_results_as_context(web_results)
            
            web_response = WebSearchResponse(
                success=web_results.get("success", False),
                query=request.query,
                answer=web_results.get("answer"),
                results=[WebSearchResult(**r) for r in web_results.get("results", [])],
                context=web_context
            )
            
            combined_context = f"RAG Context:\n{rag_context}\n\nWeb Context:\n{web_context}"
            used_fallback = True
        
        return HybridSearchResponse(
            query=request.query,
            rag_results=rag_response,
            web_results=web_response,
            used_fallback=used_fallback,
            combined_context=combined_context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Generation Endpoints 

@router.post("/generate", response_model=GenerateResponse)
async def generate_answer(request: GenerateRequest):
    """Generate an answer using the LLM"""
    try:
        result = generate_response(
            query=request.query,
            context=request.context
        )
        
        return GenerateResponse(
            success=result.get("success", False),
            query=request.query,
            response=result.get("response"),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    """Complete RAG pipeline: search + generate"""
    try:
        # Search
        results = search_similar(query=request.query, top_k=request.top_k)
        is_relevant = check_context_relevance(request.query, results, RELEVANCE_THRESHOLD)
        context = prepare_context_from_results(results)
        
        used_web = False
        
        # Web fallback
        if request.use_web_fallback and not is_relevant:
            web_results = web_search(query=request.query, max_results=5)
            if web_results.get("success"):
                web_context = format_web_results_as_context(web_results)
                context = f"{context}\n\nWeb Search Results:\n{web_context}"
                used_web = True
        
        # Generate response
        llm_result = generate_response(query=request.query, context=context)
        
        return RAGQueryResponse(
            success=llm_result.get("success", False),
            query=request.query,
            answer=llm_result.get("response"),
            sources=[SearchResult(**r) for r in results],
            used_web_fallback=used_web,
            error=llm_result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Upload Endpoints       

@router.post("/upload/pdf", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    source_name: Optional[str] = Form(None)
):
    """Upload and process a PDF file"""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Import here to avoid circular imports
        from .pdf_processor import process_pdf
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        try:
            # Process the PDF
            texts_added, images_added, tables_added = process_pdf(tmp_path)
            
            return UploadResponse(
                success=True,
                message=f"Successfully processed {file.filename}",
                filename=file.filename,
                texts_added=texts_added,
                images_added=images_added,
                tables_added=tables_added
            )
        finally:
            # Clean up temp file
            os.unlink(tmp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Info Endpoints       
@router.get("/collection/info", response_model=CollectionInfoResponse)
async def get_collection_info_endpoint():
    """Get information about the vector database collection"""
    try:
        info = get_collection_info()
        return CollectionInfoResponse(**info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
