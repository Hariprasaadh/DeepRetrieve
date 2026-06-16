# DeepRetrieve REST API Specifications

The DeepRetrieve backend is built using FastAPI and versioned under the `/api/v1` prefix. By default, the backend runs at `http://localhost:8000`.

---

## 📡 Base Endpoint Route Group

- **Base URL**: `http://localhost:8000/api/v1`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Alternate Redoc Docs**: `http://localhost:8000/redoc`

---

## 🛠️ Endpoint Index

### 1. `GET /ping`
Verifies API server status and system connection.

- **Request Headers**: None
- **Response Schema (`200 OK`)**:
  ```json
  {
    "status": "ok",
    "message": "DeepRetrieve API is running!"
  }
  ```

---

### 2. `GET /tools`
Retrieves names of tools registered to the Model Context Protocol (MCP) tool manager.

- **Request Headers**: None
- **Response Schema (`200 OK`)**:
  ```json
  {
    "tools": [
      { "name": "rag_retrieve" },
      { "name": "web_search" }
    ],
    "count": 2
  }
  ```

---

### 3. `POST /upload`
Ingests a single PDF file, performing text chunking, local GPU-accelerated OCR extraction (for tables/charts), local vision image captioning (BLIP), vector generation, and Qdrant database synchronization.

- **Content-Type**: `multipart/form-data`
- **Request Form Field**:
  - `file`: `UploadFile` (Required. File must have `.pdf` extension).
- **Response Schema (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Successfully indexed PDF file.",
    "filename": "Q3_Financial_Report.pdf",
    "texts_added": 42,
    "images_added": 12,
    "tables_added": 3
  }
  ```
- **Error Schema (`400 Bad Request`)**:
  ```json
  {
    "detail": "Only PDF files are supported"
  }
  ```

---

### 4. `GET /upload-progress/{filename}`
Retrieves a Server-Sent Events (SSE) stream tracking parsing percentage and task logs for the targeted file.

- **Path Parameters**:
  - `filename`: `str` (e.g. `Q3_Financial_Report.pdf`)
- **Headers**:
  - `Accept`: `text/event-stream`
- **Response Data Format**:
  Yields JSON chunks containing `status` message and `progress` percentage:
  ```text
  data: {"status": "Extracting images...", "progress": 25}

  data: {"status": "Generating vector embeddings...", "progress": 75}

  data: {"status": "Upload complete!", "progress": 100}
  ```

---

### 5. `POST /query`
Performs a synchronous query against the RAG system. The MCP Server coordinates the tool search to retrieve relevant text chunks or live web snippets, and feeds the resulting context to Gemini for final response synthesis.

- **Request JSON Schema**:
  ```json
  {
    "query": "What is the Q3 revenue growth compared to Q2?",
    "top_k": 5,
    "conversation_history": [
      {
        "role": "user",
        "content": "Who launched the product?"
      },
      {
        "role": "assistant",
        "content": "The product was launched in Q2 by the engineering division."
      }
    ]
  }
  ```
- **Response JSON Schema (`200 OK`)**:
  ```json
  {
    "success": true,
    "query": "What is the Q3 revenue growth compared to Q2?",
    "answer": "Q3 revenue grew to $3.8M compared to Q2's $2.4M (a 58% increase) driven by the product launch.",
    "sources": [
      {
        "type": "text",
        "content": "Financial summaries show a jump from $2.4M to $3.8M in Q3...",
        "source": "Q3_Financial_Report.pdf",
        "page": 3,
        "score": 0.82
      }
    ],
    "used_web_search": false,
    "error": null
  }
  ```

---

### 6. `POST /query-stream`
Establishes a Server-Sent Events (SSE) stream returning retrieval metadata overrides followed by typewriter-simulated reply text chunks.

- **Request JSON Schema**: (Same as `POST /query`)
- **Headers**:
  - `Accept`: `text/event-stream`
- **Event Flow Sequence**:

  1. **`event: metadata`** (Emitted first. Passes list of sources and web search indicator):
     ```text
     event: metadata
     data: {"sources": [{"type": "text", "content": "Sample content...", "source": "Report.pdf", "page": 3, "image_url": null, "score": 0.89}], "used_web_search": false}
     ```
  2. **`event: text`** (Emitted once to initialize text block):
     ```text
     event: text
     ```
  3. **`data: ...`** (Typewriter characters yielded sequentially for visual fluidity):
     ```text
     data: {"text": "Q3 r"}

     data: {"text": "evenue"}

     data: {"text": " grew"}
     ```
  4. **`event: done`** (Indicates stream completion):
     ```text
     event: done
     data: {}
     ```

- **Error Emitted Stream**:
  If an internal model exception occurs during generation:
  ```text
  event: error
  data: {"error": "Google Gemini API connection timed out."}
  ```

---

### 7. `DELETE /reset`
Wipes the active Qdrant vector collection and deletes all cached visual elements inside the extraction target directory (`backend/extracted_content`).

- **Response Schema (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Reset complete. Qdrant collection deleted and file caches cleared."
  }
  ```
