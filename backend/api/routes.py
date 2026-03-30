# API routes - 3 essential endpoints only

from typing import Optional, List
import asyncio
import os
import tempfile
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import json


# Request/Response Models

class ConversationTurn(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class QueryRequest(BaseModel):
    query: str = Field(..., description="Your question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of sources to retrieve")
    conversation_history: List[ConversationTurn] = Field(default=[], description="Prior turns for memory")


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

# Global store for upload progress (filename -> {status, progress})
UPLOAD_PROGRESS = {}


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
        from mcp_server.web_search import web_search
        from mcp_server.llm import get_gemini_client
        from mcp_server.config import GEMINI_MODEL
        from google import genai
        from google.genai import types
        
        print(f"\n🤖 [AGENTIC RAG] Query: '{request.query}'")
        
        client = get_gemini_client()
        sources = []
        used_web = False
        tool_calls = []
        
        # Define Python functions that can be called
        def rag_retrieve_func(query: str, top_k: int = 5):
            """Search the multimodal RAG vector database for relevant documents, images, and tables. Use this first to find information from uploaded documents."""
            print(f"🔍 [TOOL] rag_retrieve | query: '{query}' | top_k: {top_k}")
            res = search_similar(query=query, top_k=int(top_k))
            for r in res:
                if r.get("content"):
                    sources.append(Source(
                        type=r.get("type", "unknown"),
                        content=r.get("content", "")[:500],
                        source=r.get("source"),
                        page=r.get("page"),
                        score=r.get("score", 0)
                    ))
            tool_calls.append("rag_retrieve")
            return res
        
        def web_search_func(query: str):
            """Search the web for information. Use this as fallback when RAG doesn't have sufficient information."""
            print(f"🌐 [TOOL] web_search | query: '{query}'")
            result = web_search(query=query, max_results=5, include_answer=True)
            nonlocal used_web
            used_web = True
            if result.get("success") and isinstance(result.get("results"), list):
                for r in result["results"][:5]:
                    sources.append(Source(
                        type="web",
                        content=r.get("content", "")[:500],
                        source=r.get("url"),
                        page=None,
                        score=r.get("score", 0)
                    ))
            tool_calls.append("web_search")
            return {"success": result.get("success"), "results": result.get("results"), "answer": result.get("answer")}
        
        # Build conversation memory context
        history_text = ""
        if request.conversation_history:
            history_lines = []
            for turn in request.conversation_history[-3:]:  # last 3 turns 
                role_label = "User" if turn.role == "user" else "Assistant"
                history_lines.append(f"{role_label}: {turn.content}")
            history_text = "\n".join(history_lines)

        history_section = f"\n\nCONVERSATION HISTORY (for context):\n{history_text}\n" if history_text else ""
        system_instruction = """You are an expert research assistant and data synthesizer.

TOOL SELECTION GUIDELINES:
1. First, try rag_retrieve to search the knowledge base
2. If the knowledge base results are NOT relevant or insufficient for the question, use web_search
3. Use web_search when asked about topics clearly outside your knowledge base (e.g., current events, general knowledge, frameworks, technologies not in your documents)
4. Use the conversation history to understand follow-up questions and resolve pronouns/references

RESPONSE GUIDELINES:
1. Provide highly detailed, comprehensive, and exhaustive answers. Never be brief unless explicitly asked.
2. Break down complex topics into clear, well-structured paragraphs using markdown headers, bold text, and bullet points.
3. Don't just summarize—explain the "why" and "how" deeply based on the retrieved context. Extensively detail methodology, logic, and reasoning.
4. Extract and highlight key metrics, qualitative results, and technical parameters whenever available. 
5. CRITICAL: If the retrieved information contains tabular data, you MUST convert and format it perfectly as a strict Markdown table so it renders correctly on the frontend!
6. IMPORTANT: Do NOT include source citations, file names, or page numbers in your answer. The sources will be provided separately."""

        prompt = f"""{history_section}
Question: {request.query}"""

        config = types.GenerateContentConfig(
            tools=[rag_retrieve_func, web_search_func],
            system_instruction=system_instruction,
            temperature=0.0
        )

        print("🤖 [AGENT] Gemini deciding which tools to use...")
        chat = client.chats.create(model=GEMINI_MODEL, config=config)
        response = chat.send_message(prompt)
        
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


@router.post("/query-stream")
async def query_stream(request: QueryRequest):
    """Ask a question with streaming response using Server-Sent Events (SSE)"""
    try:
        from mcp_server.retriever import search_similar
        from mcp_server.web_search import web_search
        from mcp_server.llm import get_gemini_client
        from mcp_server.config import GEMINI_MODEL
        from google import genai
        from google.genai import types
        
        print(f"\n🤖 [AGENTIC RAG STREAM] Query: '{request.query}'")
        
        # Build generator that yields SSE strings
        async def event_generator():
            client = get_gemini_client()
            sources = []
            used_web = False
            tool_calls = []
            
            def rag_retrieve_func(query: str, top_k: int = 5):
                """Search the multimodal RAG vector database for relevant documents, images, and tables. Use this first to find information from uploaded documents."""
                print(f"🔍 [TOOL] rag_retrieve | query: '{query}'")
                res = search_similar(query=query, top_k=int(top_k))
                for r in res:
                    if r.get("content"):
                        sources.append({
                            "type": r.get("type", "unknown"),
                            "content": r.get("content", "")[:500],
                            "source": r.get("source"),
                            "page": r.get("page"),
                            "score": r.get("score", 0)
                        })
                tool_calls.append("rag_retrieve")
                return res
            
            def web_search_func(query: str):
                """Search the web for information. Use this as fallback when RAG doesn't have sufficient information."""
                nonlocal used_web
                print(f"🌐 [TOOL] web_search | query: '{query}'")
                result = web_search(query=query, max_results=5, include_answer=True)
                used_web = True
                if result.get("success") and isinstance(result.get("results"), list):
                    for r in result["results"][:5]:
                        sources.append({
                            "type": "web",
                            "content": r.get("content", "")[:500],
                            "source": r.get("url"),
                            "score": r.get("score", 0)
                        })
                tool_calls.append("web_search")
                return {"success": result.get("success"), "results": result.get("results", []), "answer": result.get("answer")}
            
            history_text = ""
            if request.conversation_history:
                history_lines = [
                    f"{'User' if t.role == 'user' else 'Assistant'}: {t.content}" 
                    for t in request.conversation_history[-3:]
                ]
                history_text = "\n".join(history_lines)

            history_section = f"\n\nCONVERSATION HISTORY (for context):\n{history_text}\n" if history_text else ""
            system_instruction = """You are an expert research assistant and data synthesizer.

TOOL SELECTION GUIDELINES:
1. First, try rag_retrieve to search the knowledge base
2. If the knowledge base results are NOT relevant or insufficient for the question, use web_search
3. Use web_search when asked about topics clearly outside your knowledge base
4. Use the conversation history to understand follow-up questions

RESPONSE GUIDELINES:
1. Provide highly detailed, comprehensive, and exhaustive answers. Never be brief unless explicitly asked.
2. Break down complex topics into clear, well-structured paragraphs using markdown headers, bold text, and bullet points.
3. Don't just summarize—explain the "why" and "how" deeply based on the retrieved context. Extensively detail methodology, logic, and reasoning.
4. Extract and highlight key metrics, qualitative results, and technical parameters whenever available. 
5. CRITICAL: If the retrieved information contains tabular data, you MUST convert and format it perfectly as a strict Markdown table so it renders correctly on the frontend!
6. IMPORTANT: Do NOT include source citations, file names, or page numbers in your answer. The sources will be provided separately."""

            config = types.GenerateContentConfig(
                tools=[rag_retrieve_func, web_search_func],
                system_instruction=system_instruction,
                temperature=0.0
            )

            prompt = f"""{history_section}
Question: {request.query}"""
            
            try:
                chat = client.chats.create(model=GEMINI_MODEL, config=config)
                stream_response = chat.send_message_stream(prompt)
                
                metadata_sent = False
                
                for chunk in stream_response:
                    if chunk.text:
                        if not metadata_sent:
                            # Send metadata just before the first text chunk
                            meta_payload = json.dumps({"sources": sources, "used_web_search": used_web})
                            yield f"event: metadata\ndata: {meta_payload}\n\n"
                            yield "event: text\n\n"
                            metadata_sent = True
                            
                        chunk_payload = json.dumps({"text": chunk.text})
                        yield f"data: {chunk_payload}\n\n"
                        await asyncio.sleep(0.01)  # small breathing room
                        
                if not metadata_sent:
                    # If it somehow generated no text, still send metadata
                    meta_payload = json.dumps({"sources": sources, "used_web_search": used_web})
                    yield f"event: metadata\ndata: {meta_payload}\n\n"
                    yield "event: text\n\n"
                    
            except Exception as e:
                yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

            print(f"✅ [AGENT STR] Done. Tools: {tool_calls}")
            yield "event: done\ndata: {}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

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
            logger.info("🔄 Processing PDF in background thread...")
            loop = asyncio.get_event_loop()
            
            # Initialize progress state
            UPLOAD_PROGRESS[file.filename] = {"status": "Starting processing...", "progress": 0}
            
            def update_progress(msg: str, pct: int):
                UPLOAD_PROGRESS[file.filename] = {"status": msg, "progress": pct}
                
            texts_added, images_added, tables_added = await loop.run_in_executor(
                None, lambda: process_pdf(tmp_path, original_filename=file.filename, progress_callback=update_progress)
            )
            logger.info(f"✅ Done! Added {texts_added} texts, {images_added} images, {tables_added} tables")
            
            # Mark complete explicitly (just in case)
            UPLOAD_PROGRESS[file.filename] = {"status": "Upload complete!", "progress": 100}
            
            return UploadResponse(
                success=True,
                message=f"Processed {file.filename}",
                filename=file.filename,
                texts_added=texts_added,
                images_added=images_added,
                tables_added=tables_added
            )
        except Exception as process_err:
            UPLOAD_PROGRESS[file.filename] = {"status": f"Error: {process_err}", "progress": 100}
            raise process_err
        finally:
            os.unlink(tmp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/upload-progress/{filename}")
async def upload_progress_stream(filename: str):
    """Stream PDF processing progress over SSE"""
    async def event_generator():
        # Send an immediate connection confirmation
        yield f"data: {json.dumps({'status': 'Connected context stream...', 'progress': 0})}\n\n"
        
        while True:
            # Poll the global dictionary for this filename's state
            state = UPLOAD_PROGRESS.get(filename)
            if state:
                yield f"data: {json.dumps(state)}\n\n"
                
                # Stop if it reached completion or hit an error
                if state["progress"] >= 100 or "Error" in state["status"]:
                    break
            else:
                # If the key doesn't exist yet, it's just initializing
                yield f"data: {json.dumps({'status': 'Waiting for processor to begin...', 'progress': 0})}\n\n"
                
            await asyncio.sleep(0.5)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.delete("/reset")
async def reset_collection():
    """Reset Qdrant collection and clear all extracted images/tables"""
    try:
        from mcp_server.retriever import get_qdrant_client, create_collection, COLLECTION_NAME
        from mcp_server.config import IMAGES_FOLDER, TABLES_FOLDER

        # 1. Reset Qdrant collection
        client = get_qdrant_client()
        if client.collection_exists(COLLECTION_NAME):
            client.delete_collection(COLLECTION_NAME)
        create_collection(COLLECTION_NAME)

        # 2. Clear extracted images
        images_deleted = 0
        if IMAGES_FOLDER.exists():
            for f in IMAGES_FOLDER.iterdir():
                if f.is_file():
                    f.unlink()
                    images_deleted += 1

        # 3. Clear extracted tables
        tables_deleted = 0
        if TABLES_FOLDER.exists():
            for f in TABLES_FOLDER.iterdir():
                if f.is_file():
                    f.unlink()
                    tables_deleted += 1

        return {
            "success": True,
            "message": f"Reset complete — Qdrant collection recreated, {images_deleted} images and {tables_deleted} tables deleted.",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
