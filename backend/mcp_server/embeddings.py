# Embedding functions using CLIP

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List
import io
import base64

from .config import CLIP_MODEL_NAME

# Global model instances (lazy loaded)
_clip_model = None
_clip_processor = None


def get_clip_model():
    """Get or initialize CLIP model (lazy loading)"""
    global _clip_model, _clip_processor
    
    if _clip_model is None:
        print("Loading CLIP model...")
        _clip_model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        _clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
        print("CLIP model loaded!")
    
    return _clip_model, _clip_processor


def embed_text(text: str) -> List[float]:
    """Embed text using CLIP"""
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
    """Embed image using CLIP. Accepts file path or PIL Image"""
    model, processor = get_clip_model()
    
    if isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        image = image_input.convert("RGB")
    else:
        raise ValueError("Input must be a file path or PIL Image")
    
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
