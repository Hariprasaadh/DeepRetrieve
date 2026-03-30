# Gemini LLM integration for RAG responses

from typing import List, Dict, Optional, Any
from google import genai

from .config import GOOGLE_API_KEY, GEMINI_MODEL, MAX_RETRIES

# Initialize Gemini immediately
print(f"Initializing Gemini ({GEMINI_MODEL})...")
_gemini_client = genai.Client(api_key=GOOGLE_API_KEY)
print("✅ Gemini client ready!")


def get_gemini_client():
    """Get Gemini client instance"""
    return _gemini_client


def prepare_context_from_results(results: List[Dict]) -> str:
    """Prepare clean context string from search results"""
    if not results:
        return ""
    
    context_parts = []
    
    for i, result in enumerate(results, 1):
        result_type = result.get("type", "unknown")
        content = result.get("content", "").strip()
        source = result.get("source", "unknown")
        page = result.get("page")
        
        if not content:
            continue
        
        # Clean up content - remove excessive whitespace
        content = " ".join(content.split())
        
        if result_type == "text":
            location = f"{source}" + (f", Page {page}" if page else "")
            context_parts.append(f"[Source {i}] ({location})\n{content}")
        
        elif result_type == "image":
            context_parts.append(f"[Image {i}] ({source})\nDescription: {content}")
        
        elif result_type == "table":
            location = f"{source}" + (f", Page {page}" if page else "")
            context_parts.append(f"[Table {i}] ({location})\n{content}")
        
        elif result_type == "web":
            context_parts.append(f"[Web {i}] ({source})\n{content}")
    
    return "\n\n".join(context_parts)


def generate_response(
    query: str,
    context: str,
    system_prompt: Optional[str] = None,
    max_retries: int = MAX_RETRIES
) -> Dict[str, Any]:
    """Generate response using Gemini with provided context (rate-limited)"""
    client = get_gemini_client()
    
    if system_prompt is None:
        system_prompt = """You are an expert research assistant. Your task is to answer questions using ONLY the provided context.

INSTRUCTIONS:
1. VERIFY: Check if the context contains relevant information to answer the question
2. If context is RELEVANT: Provide a clear, accurate answer based on the context
3. If context is NOT RELEVANT or INSUFFICIENT: Say "I couldn't find specific information about this in the provided documents."
4. NEVER make up information not present in the context
5. Format your response clearly with proper paragraphs
6. If citing specific facts, mention the source (e.g., "According to the document...")

RESPONSE FORMAT:
- Start with a direct answer to the question
- Provide supporting details from the context
- Keep the response concise but comprehensive
- Use bullet points for lists when appropriate"""
    
    prompt = f"""{system_prompt}

---
CONTEXT:
{context}
---

USER QUESTION: {query}

ANSWER:"""
    
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return {
        "success": True,
        "response": response.text,
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
    
    # Must have at least one result above threshold
    has_good_score = any(r.get("score", 0) >= threshold for r in results)
    if not has_good_score:
        return False
    
    # Check content quality - reject junk content
    for result in results:
        content = result.get("content", "")
        # Check for corrupted content (repeated tokens, too many newlines)
        if "<EOS>" in content or "<pad>" in content:
            return False
        # Check if content is mostly newlines (corrupted)
        if content.count('\n') > len(content.split()) * 0.5:
            return False
    
    # Generic document queries - trust the vector score
    query_lower = query.lower()
    generic_queries = ['document', 'pdf', 'file', 'paper', 'content', 'summary', 'summarize', 'overview']
    if any(g in query_lower for g in generic_queries):
        return has_good_score
    
    # For specific queries, check keyword overlap
    query_words = set(query.lower().split())
    stopwords = {'what', 'is', 'the', 'a', 'an', 'how', 'why', 'when', 'where', 'who', 'about', 
                 'explain', 'tell', 'me', 'can', 'you', 'do', 'does', 'did', 'will', 'would', 
                 'could', 'should', 'to', 'for', 'of', 'in', 'on', 'at', 'with', 'and', 'or', 
                 'but', 'this', 'that', 'these', 'those', 'it', 'its', 'my', 'your'}
    query_keywords = query_words - stopwords
    
    # If no specific keywords, trust vector score
    if not query_keywords:
        return has_good_score
    
    # Check if any keyword appears in any result
    for result in results:
        content = result.get("content", "").lower()
        for keyword in query_keywords:
            if len(keyword) > 2 and keyword in content:
                return True
    
    return False
