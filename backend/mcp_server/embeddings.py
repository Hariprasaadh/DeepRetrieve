# Embedding functions

import base64
import time
from typing import List

from google import genai
from google.genai import types

from .config import GOOGLE_API_KEY, GEMINI_EMBEDDING_MODEL

# Initialize Gemini client
_client = genai.Client(api_key=GOOGLE_API_KEY)


def _embed_with_retry(contents, task_type: str = None, max_retries: int = 3) -> List[float]:
    """Call Gemini embed_content with exponential-backoff retry on rate errors."""
    config = types.EmbedContentConfig(task_type=task_type) if task_type else None
    delay = 5
    for attempt in range(max_retries):
        try:
            kwargs = {"model": GEMINI_EMBEDDING_MODEL, "contents": contents}
            if config:
                kwargs["config"] = config
            result = _client.models.embed_content(**kwargs)
            return list(result.embeddings[0].values)
        except Exception as e:
            err = str(e).lower()
            if "quota" in err or "rate" in err or "429" in err or "resource" in err:
                if attempt < max_retries - 1:
                    print(f"⏳ Gemini embed rate limited, retrying in {delay}s... (attempt {attempt + 1})")
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise
            else:
                raise



def embed_text(text: str) -> List[float]:
    """Embed a document text chunk for indexing (RETRIEVAL_DOCUMENT task type)."""
    return _embed_with_retry(contents=text, task_type="RETRIEVAL_DOCUMENT")


def embed_query(query: str) -> List[float]:
    """Embed a search query (RETRIEVAL_QUERY task type — optimised for search)."""
    return _embed_with_retry(contents=query, task_type="RETRIEVAL_QUERY")


def embed_image_base64(base64_string: str) -> List[float]:
    """Embed a base64-encoded image (PNG) using Gemini multimodal embeddings."""
    image_bytes = base64.b64decode(base64_string)
    image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/png")
    return _embed_with_retry(contents=[image_part])


def embed_image(image_input) -> List[float]:
    """Embed an image from a file path or PIL Image object.

    Kept for compatibility with retriever.search_by_image().
    """
    if isinstance(image_input, str):
        # File path — read bytes
        with open(image_input, "rb") as f:
            img_bytes = f.read()
        image_part = types.Part.from_bytes(data=img_bytes, mime_type="image/png")
    else:
        # PIL Image — convert to bytes
        import io
        buf = io.BytesIO()
        image_input.convert("RGB").save(buf, format="PNG")
        image_part = types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png")

    return _embed_with_retry(contents=[image_part])
