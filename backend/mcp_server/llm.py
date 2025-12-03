# Gemini LLM integration for RAG responses

from typing import List, Dict, Optional, Any
import time
from threading import Lock

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from .config import (
    GOOGLE_API_KEY, 
    GEMINI_MODEL,
    RATE_LIMIT_WINDOW,
    MAX_CALLS_PER_WINDOW,
    MIN_DELAY_BETWEEN_CALLS,
    MAX_RETRIES
)


# Global model instance (lazy loaded)
_gemini_model = None

# Rate limiting state
_rate_limit_lock = Lock()
_last_call_time = 0
_call_count = 0


def get_gemini_model():
    """Get or initialize Gemini model (lazy loading)"""
    global _gemini_model
    
    if _gemini_model is None:
        if genai is None:
            raise ImportError("google-generativeai is not installed. Run: uv add google-generativeai")
        
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not set in environment")
        
        print(f"Initializing Gemini ({GEMINI_MODEL})...")
        genai.configure(api_key=GOOGLE_API_KEY)
        _gemini_model = genai.GenerativeModel(GEMINI_MODEL)
        print("Gemini model ready!")
    
    return _gemini_model


def _apply_rate_limit():
    """Apply rate limiting to prevent API quota exhaustion"""
    global _last_call_time, _call_count
    
    with _rate_limit_lock:
        current_time = time.time()
        
        # Reset counter if window has passed
        if current_time - _last_call_time > RATE_LIMIT_WINDOW:
            _call_count = 0
        
        # Check if we've exceeded max calls
        if _call_count >= MAX_CALLS_PER_WINDOW:
            wait_time = RATE_LIMIT_WINDOW - (current_time - _last_call_time)
            if wait_time > 0:
                print(f"Rate limit reached. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
                _call_count = 0
        
        # Ensure minimum delay between calls
        time_since_last = current_time - _last_call_time
        if time_since_last < MIN_DELAY_BETWEEN_CALLS and _last_call_time > 0:
            time.sleep(MIN_DELAY_BETWEEN_CALLS - time_since_last)
        
        _call_count += 1
        _last_call_time = time.time()


def prepare_context_from_results(results: List[Dict]) -> str:
    """Prepare context string from search results"""
    if not results:
        return ""
    
    context_parts = []
    
    for i, result in enumerate(results, 1):
        result_type = result.get("type", "unknown")
        score = result.get("score", 0)
        
        if result_type == "text":
            content = result.get("content", "")
            source = result.get("source", "unknown")
            page = result.get("page", "?")
            context_parts.append(f"[{i}] Text (score: {score:.3f})")
            context_parts.append(f"Source: {source}, Page: {page}")
            context_parts.append(f"Content: {content}\n")
        
        elif result_type == "image":
            content = result.get("content", "Image content")
            source = result.get("source", "unknown")
            context_parts.append(f"[{i}] Image (score: {score:.3f})")
            context_parts.append(f"Source: {source}")
            context_parts.append(f"Description: {content}\n")
        
        elif result_type == "table":
            content = result.get("content", "")
            source = result.get("source", "unknown")
            page = result.get("page", "?")
            context_parts.append(f"[{i}] Table (score: {score:.3f})")
            context_parts.append(f"Source: {source}, Page: {page}")
            context_parts.append(f"Data:\n{content}\n")
    
    return "\n".join(context_parts)


def generate_response(
    query: str,
    context: str,
    system_prompt: Optional[str] = None,
    max_retries: int = MAX_RETRIES
) -> Dict[str, Any]:
    """Generate response using Gemini with provided context (rate-limited)"""
    model = get_gemini_model()
    
    if system_prompt is None:
        system_prompt = """You are a helpful assistant that answers questions based on the provided context.
Use the context to answer the question accurately and comprehensively.
If the context doesn't contain enough information to answer the question, say so clearly.
Always cite the source numbers when using information from the context."""
    
    prompt = f"""{system_prompt}

Context:
{context}

Question: {query}

Answer:"""
    
    # Apply rate limiting before making the call
    _apply_rate_limit()
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return {
                "success": True,
                "response": response.text,
                "query": query
            }
        except Exception as e:
            error_str = str(e).lower()
            
            # Check if it's a rate limit error
            if "rate" in error_str or "quota" in error_str or "429" in error_str:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10  # Exponential backoff: 10s, 20s, 30s
                    print(f"Rate limit hit. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
            
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    return {
        "success": False,
        "error": "Max retries exceeded due to rate limiting",
        "query": query
    }


def check_context_relevance(
    query: str,
    results: List[Dict],
    threshold: float = 0.5
) -> bool:
    """Check if the search results are relevant enough for the query"""
    if not results:
        return False
    
    # Check if any result meets the threshold
    for result in results:
        if result.get("score", 0) >= threshold:
            return True
    
    return False
