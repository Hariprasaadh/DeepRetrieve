# Embedding functions - CLIP with optional HuggingFace Space offloading

import torch
from PIL import Image
from typing import List
import io
import base64
import requests

from .config import CLIP_MODEL_NAME, USE_HF_SPACE, HF_SPACE_URL, EMBEDDING_DIM

# Global model instances (lazy loaded)
_clip_model = None
_clip_processor = None


def get_clip_model():
    """Get or initialize CLIP model (lazy loading)"""
    global _clip_model, _clip_processor
    
    # If using HF Space, don't load local model
    if USE_HF_SPACE:
        if not HF_SPACE_URL:
            raise ValueError("HF_SPACE_URL required when USE_HF_SPACE=true")
        print(f"Using HuggingFace Space for embeddings: {HF_SPACE_URL}")
        return None, None
    
    if _clip_model is None:
        from transformers import CLIPProcessor, CLIPModel
        print(f"Loading CLIP model locally: {CLIP_MODEL_NAME}...")
        _clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        _clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
        print("CLIP model loaded!")
    
    return _clip_model, _clip_processor


def _hf_space_embed_text(text: str) -> List[float]:
    """Embed text using HuggingFace Space API"""
    try:
        response = requests.post(
            f"{HF_SPACE_URL}/embed/text",
            json={"text": text},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["embedding"]
    except Exception as e:
        raise Exception(f"HF Space API failed: {str(e)}")


def _hf_space_embed_image(image: Image.Image) -> List[float]:
    """Embed image using HuggingFace Space API"""
    try:
        # Convert PIL image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)
        
        response = requests.post(
            f"{HF_SPACE_URL}/embed/image",
            files={"file": ("image.png", buffered, "image/png")},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["embedding"]
    except Exception as e:
        raise Exception(f"HF Space API failed: {str(e)}")


def embed_text(text: str) -> List[float]:
    """Embed text using CLIP (local or HF Space)"""
    if USE_HF_SPACE:
        return _hf_space_embed_text(text)
    
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
    """Embed image using CLIP (local or HF Space). Accepts file path or PIL Image"""
    if isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        image = image_input.convert("RGB")
    else:
        raise ValueError("image_input must be file path or PIL Image")
    
    if USE_HF_SPACE:
        return _hf_space_embed_image(image)
    
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
