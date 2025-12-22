# Embedding functions 

import torch
from PIL import Image
from typing import List
import io
import base64

from .config import CLIP_MODEL_NAME, EMBEDDING_DIM

# Cache model instances (loaded on first use)
_clip_model = None
_clip_processor = None


def _ensure_model_loaded():
    """Load CLIP model once and cache it"""
    global _clip_model, _clip_processor
    if _clip_model is None:
        from transformers import CLIPProcessor, CLIPModel
        print(f"Loading CLIP model: {CLIP_MODEL_NAME}...")
        _clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        _clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
        print("✅ CLIP model loaded and ready!")


def embed_text(text: str) -> List[float]:
    """Embed text using local CLIP model"""
    _ensure_model_loaded()
    inputs = _clip_processor(
        text=text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=77
    )
    
    with torch.no_grad():
        features = _clip_model.get_text_features(**inputs)
        features = features / features.norm(dim=-1, keepdim=True)
        return features.squeeze().tolist()


def embed_image(image_input) -> List[float]:
    _ensure_model_loaded()
    """Embed image using local CLIP model. Accepts file path or PIL Image"""
    if isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        image = image_input.convert("RGB")
    else:
        raise ValueError("image_input must be file path or PIL Image")
    
    inputs = _clip_processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        features = _clip_model.get_image_features(**inputs)
        features = features / features.norm(dim=-1, keepdim=True)
        return features.squeeze().tolist()


def embed_image_base64(base64_string: str) -> List[float]:
    """Embed a base64 encoded image using local CLIP model"""
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return embed_image(image)
