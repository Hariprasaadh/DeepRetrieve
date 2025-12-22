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


@router.get("/tools")
async def list_tools():
    """List available MCP tools"""
    try:
        from mcp_server.server import mcp
        
        tools_list = []
        for tool_name in mcp._tool_manager._tools.keys():
            tool_func = mcp._tool_manager._tools[tool_name]
            tools_list.append({
                "name": tool_name,
            })
        
        return {"tools": tools_list, "count": len(tools_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Ask a question - Truly Agentic RAG where Gemini decides which tools to use"""
    try:
        from mcp_server.retriever import search_similar
        from mcp_server.web_search import web_search, format_web_results_as_context
        from mcp_server.llm import prepare_context_from_results, get_gemini_model, _apply_rate_limit
        import google.generativeai as genai
        
        print(f"\n🤖 [AGENTIC RAG] Query: '{request.query}'")
        
        # Define tools for Gemini
        tools = [
            genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name="rag_retrieve",
                        description="Search the multimodal RAG vector database for relevant documents, images, and tables. Use this first to find information from uploaded documents.",
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={
                                "query": genai.protos.Schema(type=genai.protos.Type.STRING, description="The search query"),
                                "top_k": genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Number of results (default: 5)")
                            },
                            required=["query"]
                        )
                    ),
                    genai.protos.FunctionDeclaration(
                        name="web_search",
                        description="Search the web for information. Use this as fallback when RAG doesn't have sufficient information.",
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={
                                "query": genai.protos.Schema(type=genai.protos.Type.STRING, description="The search query"),
                            },
                            required=["query"]
                        )
                    )
                ]
            )
        ]
        
        # Initialize agent 
        model = get_gemini_model()
        
        # Define Python functions that can be called
        def rag_retrieve_func(query: str, top_k: int = 5):
            print(f"🔍 [TOOL] rag_retrieve | query: '{query}' | top_k: {top_k}")
            return search_similar(query=query, top_k=int(top_k))
        
        def web_search_func(query: str):
            print(f"🌐 [TOOL] web_search | query: '{query}'")
            result = web_search(query=query, max_results=5, include_answer=True)
            return {"success": result.get("success"), "results": result.get("results", []), "answer": result.get("answer")}
        
        # Map function names to actual functions
        available_functions = {
            "rag_retrieve": rag_retrieve_func,
            "web_search": web_search_func
        }
        
        sources = []
        used_web = False
        tool_calls = []
        
        # Agent loop - let Gemini decide which tools to use
        prompt = f"""You are a helpful research assistant with access to a knowledge base and web search.

Question: {request.query}

TOOL SELECTION GUIDELINES:
1. First, try rag_retrieve to search the knowledge base
2. If the knowledge base results are NOT relevant or insufficient for the question, use web_search
3. Use web_search when asked about topics clearly outside your knowledge base (e.g., current events, general knowledge, frameworks, technologies not in your documents)

IMPORTANT: Do NOT include source citations, file names, or page numbers in your answer. The sources will be provided separately. Focus only on delivering a well-structured, informative response."""

        print("🤖 [AGENT] Gemini deciding which tools to use...")
        _apply_rate_limit()
        
        chat = model.start_chat()
        response = chat.send_message(prompt, tools=tools)
        
        # Process function calls manually
        while response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            func_name = function_call.name
            func_args = dict(function_call.args)
            
            print(f"🔧 [AGENT] Gemini called: {func_name}({func_args})")
            tool_calls.append(func_name)
            
            # Execute the function
            if func_name in available_functions:
                func_result = available_functions[func_name](**func_args)
                
                # Collect sources
                if func_name == "rag_retrieve" and isinstance(func_result, list):
                    for r in func_result:
                        if r.get("content"):
                            sources.append(Source(
                                type=r.get("type", "unknown"),
                                content=r.get("content", "")[:500],
                                source=r.get("source"),
                                page=r.get("page"),
                                score=r.get("score", 0)
                            ))
                
                elif func_name == "web_search":
                    used_web = True
                    if func_result.get("success") and isinstance(func_result.get("results"), list):
                        for r in func_result["results"][:5]:
                            sources.append(Source(
                                type="web",
                                content=r.get("content", "")[:500],
                                source=r.get("url"),
                                page=None,
                                score=r.get("score", 0)
                            ))
                
                # Send function response back to Gemini
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=func_name,
                                response={"result": func_result}
                            )
                        )]
                    )
                )
            else:
                print(f"⚠️ [AGENT] Unknown function: {func_name}")
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=func_name,
                                response={"error": "Function not found"}
                            )
                        )]
                    )
                )
        
        # Get final answer from agent
        answer = response.text if response.text else "I couldn't generate an answer."
        
        print(f"✅ [AGENT] Completed. Tools used: {tool_calls}")
        
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
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"📄 Starting upload: {file.filename}")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        logger.info(f"💾 Saved to temp: {tmp_path}")
        
        try:
            logger.info("🔄 Processing PDF (this may take 2-5 minutes on free tier)...")
            texts_added, images_added, tables_added = process_pdf(tmp_path)
            logger.info(f"✅ Done! Added {texts_added} texts, {images_added} images, {tables_added} tables")
            
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
