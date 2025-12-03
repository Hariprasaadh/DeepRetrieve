# PDF processing utilities for the API

import os
import base64
import uuid
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import fitz  # PyMuPDF

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False

from mcp_server.config import OUTPUT_FOLDER, IMAGES_FOLDER, TABLES_FOLDER
from mcp_server.embeddings import embed_text, embed_image_base64
from mcp_server.retriever import get_qdrant_client, COLLECTION_NAME

from qdrant_client.http.models import PointStruct


def ensure_output_folders():
    """Ensure output folders exist"""
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    IMAGES_FOLDER.mkdir(parents=True, exist_ok=True)
    TABLES_FOLDER.mkdir(parents=True, exist_ok=True)


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """Extract text from PDF pages"""
    doc = fitz.open(pdf_path)
    texts = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        if text.strip():
            texts.append({
                "content": text.strip(),
                "page": page_num + 1,
                "source": os.path.basename(pdf_path)
            })
    
    doc.close()
    return texts


def extract_images_from_pdf(pdf_path: str, min_size: int = 100) -> List[Dict]:
    """Extract images from PDF"""
    ensure_output_folders()
    doc = fitz.open(pdf_path)
    images = []
    source_name = os.path.basename(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Check minimum size
                if len(image_bytes) < min_size:
                    continue
                
                # Save image
                image_filename = f"{Path(pdf_path).stem}_page{page_num+1}_img{img_index+1}.{image_ext}"
                image_path = IMAGES_FOLDER / image_filename
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                # Convert to base64
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                
                images.append({
                    "image_base64": image_base64,
                    "path": str(image_path),
                    "page": page_num + 1,
                    "source": source_name,
                    "content": f"Image from {source_name}, page {page_num + 1}"
                })
            except Exception as e:
                print(f"Error extracting image: {e}")
                continue
    
    doc.close()
    return images


def extract_tables_from_pdf(pdf_path: str) -> List[Dict]:
    """Extract tables from PDF using Camelot"""
    if not CAMELOT_AVAILABLE:
        print("Camelot not available, skipping table extraction")
        return []
    
    ensure_output_folders()
    tables = []
    source_name = os.path.basename(pdf_path)
    
    try:
        # Extract tables
        table_list = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")
        
        if len(table_list) == 0:
            # Try stream flavor
            table_list = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
        
        for i, table in enumerate(table_list):
            df = table.df
            
            if df.empty or (df.shape[0] < 2 and df.shape[1] < 2):
                continue
            
            # Save as CSV
            csv_filename = f"{Path(pdf_path).stem}_table_{i+1}.csv"
            csv_path = TABLES_FOLDER / csv_filename
            df.to_csv(csv_path, index=False)
            
            # Convert to string
            table_content = df.to_string()
            
            tables.append({
                "content": table_content,
                "csv_path": str(csv_path),
                "page": table.page,
                "source": source_name,
                "table_index": i + 1
            })
    except Exception as e:
        print(f"Error extracting tables: {e}")
    
    return tables


def add_texts_to_qdrant(texts: List[Dict]) -> int:
    """Add text chunks to Qdrant"""
    client = get_qdrant_client()
    points = []
    
    for i, text_data in enumerate(texts):
        embedding = embed_text(text_data["content"][:512])  # Limit text length
        
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "type": "text",
                "content": text_data["content"],
                "page": text_data["page"],
                "source": text_data["source"]
            }
        )
        points.append(point)
    
    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    return len(points)


def add_images_to_qdrant(images: List[Dict]) -> int:
    """Add images to Qdrant"""
    client = get_qdrant_client()
    points = []
    
    for image_data in images:
        try:
            embedding = embed_image_base64(image_data["image_base64"])
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "type": "image",
                    "content": image_data["content"],
                    "image_base64": image_data["image_base64"][:1000],  # Store thumbnail
                    "path": image_data["path"],
                    "page": image_data["page"],
                    "source": image_data["source"]
                }
            )
            points.append(point)
        except Exception as e:
            print(f"Error embedding image: {e}")
            continue
    
    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    return len(points)


def add_tables_to_qdrant(tables: List[Dict]) -> int:
    """Add tables to Qdrant"""
    client = get_qdrant_client()
    points = []
    
    for table_data in tables:
        embedding = embed_text(table_data["content"][:512])
        
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "type": "table",
                "content": table_data["content"],
                "csv_path": table_data["csv_path"],
                "page": table_data["page"],
                "source": table_data["source"],
                "table_index": table_data["table_index"]
            }
        )
        points.append(point)
    
    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    return len(points)


def process_pdf(pdf_path: str) -> Tuple[int, int, int]:
    """Process a PDF file and add all content to Qdrant"""
    # Extract content
    texts = extract_text_from_pdf(pdf_path)
    images = extract_images_from_pdf(pdf_path)
    tables = extract_tables_from_pdf(pdf_path)
    
    # Add to Qdrant
    texts_added = add_texts_to_qdrant(texts)
    images_added = add_images_to_qdrant(images)
    tables_added = add_tables_to_qdrant(tables)
    
    return texts_added, images_added, tables_added
