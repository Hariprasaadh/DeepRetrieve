# CLIP Embedding API - Deploy this to Hugging Face Spaces
# This runs CLIP on HF's free GPU and provides embeddings via API

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import io
import base64

app = FastAPI(title="CLIP Embedding API", version="1.0.0")

# Enable CORS for your Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Render URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CLIP model once at startup
print("Loading CLIP model...")
MODEL_NAME = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(MODEL_NAME)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)

# Use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
print(f"CLIP model loaded on {device}!")


class TextRequest(BaseModel):
    text: str


class TextBatchRequest(BaseModel):
    texts: List[str]


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    dimension: int


class BatchEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    dimension: int
    count: int


@app.get("/")
def root():
    return {
        "service": "CLIP Embedding API",
        "model": MODEL_NAME,
        "device": device,
        "endpoints": {
            "text": "/embed/text",
            "text_batch": "/embed/text/batch",
            "image": "/embed/image"
        }
    }


@app.post("/embed/text", response_model=EmbeddingResponse)
def embed_text(request: TextRequest):
    """Embed a single text using CLIP"""
    try:
        inputs = processor(
            text=request.text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(device)
        
        with torch.no_grad():
            features = model.get_text_features(**inputs)
            features = features / features.norm(dim=-1, keepdim=True)
            embedding = features.squeeze().cpu().tolist()
        
        return EmbeddingResponse(
            embedding=embedding,
            dimension=len(embedding)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/embed/text/batch", response_model=BatchEmbeddingResponse)
def embed_text_batch(request: TextBatchRequest):
    """Embed multiple texts using CLIP"""
    try:
        inputs = processor(
            text=request.texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(device)
        
        with torch.no_grad():
            features = model.get_text_features(**inputs)
            features = features / features.norm(dim=-1, keepdim=True)
            embeddings = features.cpu().tolist()
        
        return BatchEmbeddingResponse(
            embeddings=embeddings,
            dimension=len(embeddings[0]) if embeddings else 0,
            count=len(embeddings)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/embed/image", response_model=EmbeddingResponse)
async def embed_image(file: UploadFile = File(...)):
    """Embed an image using CLIP"""
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        inputs = processor(images=image, return_tensors="pt").to(device)
        
        with torch.no_grad():
            features = model.get_image_features(**inputs)
            features = features / features.norm(dim=-1, keepdim=True)
            embedding = features.squeeze().cpu().tolist()
        
        return EmbeddingResponse(
            embedding=embedding,
            dimension=len(embedding)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
