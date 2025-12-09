# Embedding functions - CLIP with optional HuggingFace Inference API offloading

import torch
from PIL import Image
from typing import List
import io
import base64
import requests
import time

from .config import CLIP_MODEL_NAME, USE_HF_INFERENCE, HF_API_TOKEN, HF_INFERENCE_URL, EMBEDDING_DIM

# Global model instances (lazy loaded)
_clip_model = None
_clip_processor = None


def get_clip_model():
    """Get or initialize CLIP model (lazy loading)"""
    global _clip_model, _clip_processor
    
    # If using HF Inference API, don't load local model
    if USE_HF_INFERENCE:
        if not HF_API_TOKEN:
            raise ValueError("HF_API_TOKEN required when USE_HF_INFERENCE=true")
        print("Using Hugging Face Inference API for embeddings (no local model needed)")
        return None, None
    
    if _clip_model is None:
        from transformers import CLIPProcessor, CLIPModel
        print(f"Loading CLIP model locally: {CLIP_MODEL_NAME}...")
        _clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        _clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
        print("CLIP model loaded!")
    
    return _clip_model, _clip_processor


def _hf_inference_embed_text(text: str, max_retries: int = 3) -> List[float]:
    """Embed text using HuggingFace Inference API"""
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": text}
    
    for attempt in range(max_retries):
        try:
            response = requests.post(HF_INFERENCE_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 503:
                # Model is loading, wait and retry
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Model loading on HF... waiting {wait_time}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            
            response.raise_for_status()
            
            # HF returns embeddings directly for feature extraction models
            embeddings = response.json()
            
            # CLIP returns text_embeds, normalize it
            if isinstance(embeddings, list) and len(embeddings) > 0:
                # Take first embedding if batched
                embedding = embeddings[0] if isinstance(embeddings[0], list) else embeddings
                
                # Normalize
                import numpy as np
                embedding = np.array(embedding)
                norm = np.linalg.norm(embedding)
                if norm > 0:
                    embedding = embedding / norm
                
                return embedding.tolist()[:EMBEDDING_DIM]  # Ensure correct dimension
            
            raise ValueError(f"Unexpected HF API response format: {embeddings}")
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"HF Inference API failed after {max_retries} attempts: {str(e)}")
            time.sleep(2 ** attempt)
    
    raise Exception("Failed to get embeddings from HF Inference API")


def _hf_inference_embed_image(image: Image.Image, max_retries: int = 3) -> List[float]:
    """Embed image using HuggingFace Inference API"""
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    # Convert PIL image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                HF_INFERENCE_URL,
                headers=headers,
                data=img_bytes,
                timeout=30
            )
            
            if response.status_code == 503:
                wait_time = 2 ** attempt
                print(f"Model loading on HF... waiting {wait_time}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            
            response.raise_for_status()
            embeddings = response.json()
            
            if isinstance(embeddings, list) and len(embeddings) > 0:
                embedding = embeddings[0] if isinstance(embeddings[0], list) else embeddings
                
                # Normalize
                import numpy as np
                embedding = np.array(embedding)
                norm = np.linalg.norm(embedding)
                if norm > 0:
                    embedding = embedding / norm
                
                return embedding.tolist()[:EMBEDDING_DIM]
            
            raise ValueError(f"Unexpected HF API response format: {embeddings}")
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"HF Inference API failed after {max_retries} attempts: {str(e)}")
            time.sleep(2 ** attempt)
    
    raise Exception("Failed to get image embeddings from HF Inference API")


def embed_text(text: str) -> List[float]:
    """Embed text using CLIP (local or HF Inference API)"""
    if USE_HF_INFERENCE:
        return _hf_inference_embed_text(text)
    
    model, processor = get_clip_model()
    
    inputs = processor(
        text=text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=77
    )
    
    with torch.no_grad():
        features = model.get_text_features(**inputs)
        features = features / features.norm(dim=-1, keepdim=True)
        return features.squeeze().tolist()


def embed_image(image_input) -> List[float]:
    """Embed image using CLIP (local or HF Inference API). Accepts file path or PIL Image"""
    if isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        image = image_input.convert("RGB")
    else:
        raise ValueError("image_input must be file path or PIL Image")
    
    if USE_HF_INFERENCE:
        return _hf_inference_embed_image(image)
    
    model, processor = get_clip_model()
    
    inputs = processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        features = model.get_image_features(**inputs)
        features = features / features.norm(dim=-1, keepdim=True)
        return features.squeeze().tolist()


def embed_image_base64(base64_string: str) -> List[float]:
    """Embed a base64 encoded image using CLIP"""
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return embed_image(image)
