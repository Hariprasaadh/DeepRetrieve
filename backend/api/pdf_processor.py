# Purpose: PDF document parsing and multimodal content extraction.
# Responsibilities: Parses text layout from files using PyMuPDF (with scanned fallback via EasyOCR),
# extracts images and captions them using BLIP/OCR, extracts tabular structures using img2table,
# and generates semantic embeddings for indexing inside the vector database.

import os
import io
import json
import uuid
import math
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Callable

import fitz  # PyMuPDF
from PIL import Image
from qdrant_client.http.models import PointStruct


from mcp_server.config import OUTPUT_FOLDER, IMAGES_FOLDER, TABLES_FOLDER
from mcp_server.embeddings import embed_text
from mcp_server.retriever import get_qdrant_client, COLLECTION_NAME

class _ImageCaptioner:
    """Orchestrates image description using BLIP for natural scenes/figures and EasyOCR for text-dense charts/slides."""

    def __init__(self):
        self._blip_model = None
        self._blip_processor = None
        self._ocr_reader = None
        self._device = None
        self._blip_load_failed = False
        self._ocr_load_failed = False

    def _load(self):
        """Lazy-loads inference models on-demand to optimize startup memory."""
        self._load_blip()
        self._load_ocr()

    def _load_blip(self):
        if self._blip_model is not None or self._blip_load_failed:
            return

        try:
            import torch
            from transformers import BlipProcessor, BlipForConditionalGeneration

            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"[ImageCaptioner] Loading BLIP on {self._device.upper()}...")

            self._blip_processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            self._blip_model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            ).to(self._device)
            self._blip_model.eval()
            print("[ImageCaptioner] BLIP ready.")

        except Exception as e:
            print(f"[ImageCaptioner] ⚠️  BLIP failed to load: {e}")
            print("[ImageCaptioner]    Images will use EasyOCR-only fallback.")
            self._blip_load_failed = True

    def _load_ocr(self):
        if self._ocr_reader is not None or self._ocr_load_failed:
            return

        try:
            import torch
            import easyocr

            if self._device is None:
                self._device = "cuda" if torch.cuda.is_available() else "cpu"

            print("[ImageCaptioner] Loading EasyOCR...")
            gpu_flag = (self._device == "cuda")
            self._ocr_reader = easyocr.Reader(["en"], gpu=gpu_flag, verbose=False)
            print("[ImageCaptioner] EasyOCR ready.")

        except Exception as e:
            print(f"[ImageCaptioner] ⚠️  EasyOCR failed to load: {e}")
            self._ocr_load_failed = True

    
    def _ocr_text(self, pil_image: Image.Image) -> str:
        """Extracts text from the image using EasyOCR."""
        import numpy as np
        arr = np.array(pil_image.convert("RGB"))
        results = self._ocr_reader.readtext(arr, detail=0)
        return " ".join(results).strip()

    def _blip_caption(self, pil_image: Image.Image) -> str:
        """Generates a contextual image description using BLIP."""
        import torch
        inputs = self._blip_processor(pil_image.convert("RGB"), return_tensors="pt").to(self._device)

        with torch.no_grad():
            output_ids = self._blip_model.generate(
                **inputs,
                max_new_tokens=150,
                num_beams=3
            )
        caption = self._blip_processor.decode(output_ids[0], skip_special_tokens=True)
        return caption.strip()

    def _is_text_dominant(self, ocr_text: str) -> bool:
        """Decides if the image is text-dense, signaling that OCR output should override general captioning."""
        return len(ocr_text) > 40

   
    def caption(self, pil_image: Image.Image) -> str:
        """Generates descriptions for images, routing through OCR or BLIP based on text density."""
        self._load()
        try:
            # --- OCR pass ---
            ocr_text = ""
            if self._ocr_reader is not None:
                ocr_text = self._ocr_text(pil_image)

            if self._is_text_dominant(ocr_text):
                return f"[Text in image]: {ocr_text}"

            # --- BLIP pass ---
            if self._blip_model is not None:
                blip_desc = self._blip_caption(pil_image)
                if blip_desc:
                    return f"[Figure]: {blip_desc}"

            # --- Fallbacks ---
            if ocr_text:
                return f"[Text in image]: {ocr_text}"

            if self._blip_load_failed and self._ocr_load_failed:
                return "[Image: captioning unavailable — both models failed to load]"

            return "[Image: no description available]"

        except Exception as e:
            print(f"[ImageCaptioner] Error captioning image: {e}")
            return "[Image: captioning failed]"


# Process-wide captioner singleton instance
_captioner = _ImageCaptioner()


def ensure_output_folders():
    """Ensures directories exist for writing extracted media and table JSONs."""
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    IMAGES_FOLDER.mkdir(parents=True, exist_ok=True)
    TABLES_FOLDER.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    """Sanitizes raw extracted text by removing model token sequences and normalizing spacing."""
    text = text.replace("<EOS>", "").replace("<pad>", "").replace("<eos>", "").replace("<PAD>", "")
    lines = text.split('\n')
    single_word_lines = sum(1 for line in lines if len(line.split()) <= 1)
    if single_word_lines > len(lines) * 0.5:
        text = ' '.join(line.strip() for line in lines if line.strip())
    text = ' '.join(text.split())
    return text.strip()


def _chunk_text(text: str, source: str, page_num: int, chunk_size: int = 512, overlap: int = 50) -> List[Dict]:
    """Slices extracted text into overlapping chunks to serve as indexing targets."""
    chunks = []
    words = text.split(" ")
    current_chunk: List[str] = []
    current_len = 0

    for word in words:
        word_len = len(word) + 1
        if current_len + word_len > chunk_size and current_chunk:
            chunk_str = " ".join(current_chunk)
            chunks.append({"content": chunk_str, "page": page_num, "source": source})
            overlap_words = current_chunk[-math.ceil(overlap / (len(current_chunk[-1]) + 1)):] if current_chunk else []
            current_chunk = overlap_words + [word]
            current_len = sum(len(w) + 1 for w in current_chunk)
        else:
            current_chunk.append(word)
            current_len += word_len

    if current_chunk:
        chunk_str = " ".join(current_chunk)
        if len(chunk_str) > 20:
            chunks.append({"content": chunk_str, "page": page_num, "source": source})

    return chunks


def _ocr_page(page: "fitz.Page") -> str:
    """Fallback OCR method for scanned/non-digital PDF pages. Renders the page and extracts text via EasyOCR."""
    import numpy as np

    _captioner._load_ocr()
    if _captioner._ocr_reader is None:
        return ""

    mat = fitz.Matrix(1.5, 1.5)
    pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
    img_bytes = pix.tobytes("png")

    pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    arr = np.array(pil_img)

    results = _captioner._ocr_reader.readtext(arr, detail=0, paragraph=True)
    return " ".join(results).strip()


def extract_text_from_pdf(pdf_path: str, progress_callback: Optional[Callable[[str, int], None]] = None) -> List[Dict]:
    """Parses text from PDF pages, falling back to OCR if a page lacks extractable digital text."""
    doc = fitz.open(pdf_path)
    texts: List[Dict] = []
    total = len(doc)
    source_name = os.path.basename(pdf_path)
    ocr_pages = 0

    for page_num in range(total):
        if progress_callback:
            progress_callback(f"Extracting text (Page {page_num+1}/{total})...", int(page_num / max(total, 1) * 15))

        page = doc[page_num]

        # Extract digital text
        text = clean_text(page.get_text())

        # Fallback to OCR if page yields insufficient characters
        if len(text) < 50:
            if progress_callback:
                progress_callback(f"OCR fallback (Page {page_num+1}/{total})...", int(page_num / max(total, 1) * 15))
            ocr_text = _ocr_page(page)
            if len(ocr_text) > 50:
                text = ocr_text
                ocr_pages += 1
                print(f"  [OCR] Page {page_num+1}: extracted {len(ocr_text)} chars via EasyOCR")

        if text and len(text) > 50:
            page_chunks = _chunk_text(text, source_name, page_num + 1)
            texts.extend(page_chunks)

    doc.close()
    if ocr_pages:
        print(f"  [OCR] {ocr_pages}/{total} pages used EasyOCR fallback")
    print(f"Extracted {len(texts)} text chunks from {pdf_path}")
    return texts


def extract_images_from_pdf(
    pdf_path: str,
    min_size: int = 100,
    progress_callback: Optional[Callable[[str, int], None]] = None
) -> List[Dict]:
    """Extracts embedded figures and visual charts, generating descriptions via BLIP/OCR.

    Filters out small decorative icons and identical image shapes across pages.
    """
    if progress_callback:
        progress_callback("Extracting images...", 15)

    ensure_output_folders()
    images = []
    source_name = os.path.basename(pdf_path)
    stem = Path(pdf_path).stem
    seen_xrefs: set = set()
    seen_fingerprints: set = set()

    def _image_fingerprint(pil_img: Image.Image) -> tuple:
        """Generates a perceptual key to match identical images."""
        small = pil_img.resize((8, 8), Image.LANCZOS).convert("L")
        return (pil_img.size, tuple(small.getdata()))

    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        for page_num in range(total_pages):
            page = doc[page_num]
            img_list = page.get_images(full=True)

            for img_idx, img_info in enumerate(img_list):
                xref = img_info[0]
                if xref in seen_xrefs:
                    continue
                seen_xrefs.add(xref)

                try:
                    base_image = doc.extract_image(xref)
                    w, h = base_image["width"], base_image["height"]

                    if w < min_size or h < min_size:
                        continue

                    img_bytes = base_image["image"]
                    pil_image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

                    fp = _image_fingerprint(pil_image)
                    if fp in seen_fingerprints:
                        print(f"  [Image] Skipping duplicate on page {page_num+1} (xref={xref})")
                        continue
                    seen_fingerprints.add(fp)

                    img_filename = f"{stem}_p{page_num+1}_img{img_idx+1}.png"
                    img_path = IMAGES_FOLDER / img_filename
                    pil_image.save(img_path, format="PNG")

                    if progress_callback:
                        pct = 15 + int(((page_num * len(img_list) + img_idx) /
                                        max(total_pages * max(len(img_list), 1), 1)) * 25)
                        progress_callback(
                            f"Captioning image (page {page_num+1}/{total_pages})...",
                            min(pct, 40)
                        )

                    caption = _captioner.caption(pil_image)
                    print(f"  [Image] page={page_num+1} size={w}x{h}\n         caption → {caption}")

                    images.append({
                        "content": caption,
                        "path": str(img_path),
                        "page": page_num + 1,
                        "source": source_name,
                    })

                except Exception as img_err:
                    print(f"  [Image] Error on page {page_num+1} xref={xref}: {img_err}")

        doc.close()

    except Exception as e:
        print(f"Error during image extraction: {e}")

    print(f"Extracted {len(images)} images from {pdf_path}")
    return images



def extract_tables_from_pdf(pdf_path: str, progress_callback: Optional[Callable[[str, int], None]] = None) -> List[Dict]:
    """Identifies and structures tabular layouts from PDF pages using img2table and OCR.

    Converts identified structures into serialized contexts for the LLM and indexes them.
    """
    from img2table.document import PDF
    from img2table.ocr import EasyOCR
    import pandas as pd

    if progress_callback:
        progress_callback("Extracting tables (visually)...", 45)

    ensure_output_folders()
    tables = []
    source_name = os.path.basename(pdf_path)
    table_index = 0

    _captioner._load_ocr()
    if _captioner._ocr_reader is None:
        print("[TableExtractor] EasyOCR not available. Skipping table extraction.")
        return []

    class SharedEasyOCR(EasyOCR):
        def __init__(self, reader_instance):
            self.reader = reader_instance

    ocr_engine = SharedEasyOCR(_captioner._ocr_reader)
    doc = PDF(pdf_path, detect_rotation=False, pdf_text_extraction=True)

    try:
        extracted_tables = doc.extract_tables(
            ocr=ocr_engine,
            implicit_rows=True,
            borderless_tables=False,
            min_confidence=50
        )

        for page_idx, page_tables in extracted_tables.items():
            for tab in page_tables:
                df = tab.df
                df = df.dropna(how='all').dropna(axis=1, how='all')
                if df.empty or len(df) < 2:
                    continue

                headers = [str(col).strip() if pd.notna(col) and str(col).strip() else f"Col{i}"
                           for i, col in enumerate(df.iloc[0])]
                
                records = []
                for idx_row in range(1, len(df)):
                    row_data = df.iloc[idx_row].tolist()
                    if all(pd.isna(x) or str(x).strip() == "" for x in row_data):
                        continue
                        
                    record = {}
                    for col_idx, value in enumerate(row_data):
                        col_name = headers[col_idx] if col_idx < len(headers) else f"Col{col_idx}"
                        record[col_name] = str(value).strip() if pd.notna(value) else ""
                    records.append(record)

                if not records:
                    continue

                table_context = [
                    f"Table {table_index + 1} (Page {page_idx + 1}, {source_name})",
                    f"Columns: {', '.join(headers)}"
                ]
                for r in records:
                    row_str = " | ".join(f"{k}: {v}" for k, v in r.items() if v)
                    table_context.append(row_str)

                table_str = "\n".join(table_context)

                json_filename = f"{Path(pdf_path).stem}_p{page_idx + 1}_t{table_index + 1}.json"
                json_path = TABLES_FOLDER / json_filename

                table_data = {
                    "source": source_name,
                    "page": page_idx + 1,
                    "headers": headers,
                    "rows": records
                }
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(table_data, f, indent=2, ensure_ascii=False)

                tables.append({
                    "content": table_str,
                    "json_path": str(json_path),
                    "page": page_idx + 1,
                    "source": source_name,
                    "headers": headers,
                    "table_index": table_index
                })
                table_index += 1

    except Exception as e:
        print(f"Error extracting tables via img2table: {e}")

    print(f"Extracted {len(tables)} tables from {pdf_path}")
    return tables


def add_texts_to_qdrant(texts: List[Dict], progress_callback: Optional[Callable[[str, int], None]] = None) -> int:
    """Embeds text chunks using the BGE model and upserts them to the Qdrant index."""
    client = get_qdrant_client()
    points = []
    total = len(texts)
    
    for i, text_data in enumerate(texts):
        if progress_callback and i % 5 == 0:
            progress_callback(f"Embedding text chunks ({i}/{total})...", 50 + int((i/max(total, 1)) * 20))
            
        embedding = embed_text(text_data["content"][:512])
        
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


def add_images_to_qdrant(images: List[Dict], progress_callback: Optional[Callable[[str, int], None]] = None) -> int:
    """Embeds generated image captions and upserts them as semantic payloads to Qdrant."""
    client = get_qdrant_client()
    points = []
    total = len(images)
    
    for i, image_data in enumerate(images):
        if progress_callback:
            progress_callback(f"Embedding image captions ({i}/{total})...", 70 + int((i/max(total, 1)) * 15))
            
        try:
            embedding = embed_text(image_data["content"])
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "type": "image",
                    "content": image_data["content"],
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


def add_tables_to_qdrant(tables: List[Dict], progress_callback: Optional[Callable[[str, int], None]] = None) -> int:
    """Embeds serialized tabular representation strings and registers them to Qdrant."""
    client = get_qdrant_client()
    points = []
    total = len(tables)

    for i, table_data in enumerate(tables):
        if progress_callback:
            progress_callback(f"Embedding tables ({i+1}/{total})...", 88 + int((i / max(total, 1)) * 9))

        embedding = embed_text(table_data["content"][:512])

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "type": "table",
                "content": table_data["content"],
                "json_path": table_data["json_path"],
                "page": table_data["page"],
                "source": table_data["source"],
                "table_index": table_data["table_index"],
                "headers": table_data["headers"],
            }
        )
        points.append(point)

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)

    return len(points)


def process_pdf(pdf_path: str, original_filename: Optional[str] = None, progress_callback: Optional[Callable[[str, int], None]] = None) -> Tuple[int, int, int]:
    """Orchestrates the ingestion lifecycle of a PDF document: extracting, captioning, embedding, and indexing."""
    
    def cb(msg: str, pct: int):
        if progress_callback:
            progress_callback(msg, pct)
            
    cb("Starting text extraction...", 5)
    texts = extract_text_from_pdf(pdf_path, cb)

    cb("Starting image extraction...", 15)
    images = extract_images_from_pdf(pdf_path, progress_callback=cb)

    cb("Starting table extraction...", 45)
    tables = extract_tables_from_pdf(pdf_path, cb)

    if original_filename:
        for item in texts + images + tables:
            item["source"] = original_filename

    cb("Embedding text chunks...", 55)
    texts_added = add_texts_to_qdrant(texts, cb)

    cb("Embedding image captions...", 75)
    images_added = add_images_to_qdrant(images, cb)

    cb("Embedding tables...", 88)
    tables_added = add_tables_to_qdrant(tables, cb)
    
    cb("Upload complete!", 100)
    return texts_added, images_added, tables_added

