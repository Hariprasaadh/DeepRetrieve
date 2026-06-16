# DeepRetrieve Installation & Environment Setup Guide

Follow this guide to configure your development environment, set up local machine learning acceleration, and launch the DeepRetrieve workspace.

---

## Prerequisites

Ensure your system meets the following software requirements:
- **Python**: Version `3.10` to `3.12` (Python 3.13 is not fully supported by all compiled ML packages yet).
- **Node.js**: Version `18.0.0` or higher.
- **Package Manager**: `npm` (bundled with Node).
- **GPU (Optional)**: NVIDIA GPU with CUDA compatibility (Compute Capability 6.0+) for high-speed OCR and image caption extraction.

---

##  1. Backend Environment Setup

Navigate to the `backend/` directory to create a virtual environment and configure dependencies.

### Step 1.1: Create Virtual Environment
```bash
cd backend
python -m venv ai_env
```

Activate the environment:
- **Windows (Command Prompt)**:
  ```cmd
  ai_env\Scripts\activate.bat
  ```
- **Windows (PowerShell)**:
  ```powershell
  .\ai_env\Scripts\Activate.ps1
  ```
- **Linux/macOS**:
  ```bash
  source ai_env/bin/activate
  ```

### Step 1.2: Install ML Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Enabling GPU (CUDA) Acceleration

By default, PyTorch may install a CPU-only version. To run the local embedding model (`BAAI/bge-base-en-v1.5`), EasyOCR, and Salesforce BLIP captioner on your GPU, verify and install the CUDA-supported version of PyTorch.

### Step 2.1: Verify CUDA Status
Run this quick command inside your activated virtual environment:
```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('Device Count:', torch.cuda.device_count())"
```

If it prints `CUDA Available: False` but you have an NVIDIA GPU, you need to install the CUDA-linked wheel.

### Step 2.2: Install CUDA-linked PyTorch
Uninstall the default torch installation and pull the target CUDA wheel:
```bash
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```
*(Replace `cu121` with your corresponding CUDA version, e.g., `cu118` for CUDA 11.8).*

---

## 3. Environment Variable Configuration

Create a `.env` file in the root of the `backend/` directory:

```env
# Qdrant Cloud DB Credentials
QDRANT_URL=https://your-cluster-url-here.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_string

# Gemini Intelligence API
GOOGLE_API_KEY=your_gemini_api_key_from_ai_studio

# External Web Search API
TAVILY_API_KEY=your_tavily_api_key_from_tavily_dashboard
```

---

##  4. Frontend Workspace Setup

Open a separate terminal window and configure the React/Vite development server.

```bash
cd frontend
npm install
```

Start the local server:
```bash
npm run dev
```
The frontend will compile and launch at http://localhost:5173.

---

##  5. Running the Application

### Step 5.1: Start the Backend REST API
Ensure your virtual environment is active in the `backend/` directory, then start the FastAPI web server:
```bash
python main.py
```
- The backend API runs at http://localhost:8000.
- Interactive Swagger docs are available at http://localhost:8000/docs.

---

##  6. Troubleshooting Common Issues

### Issue 1: CUDA Out of Memory (OOM) Error
- **Symptom**: During a PDF upload, the console prints `RuntimeError: CUDA out of memory`.
- **Cause**: The local BLIP captioning model and EasyOCR are exceeding GPU VRAM thresholds.
- **Resolution**: You can force PyTorch to fall back to CPU for specific inference models. In `backend/mcp_server/embeddings.py` or `backend/api/pdf_processor.py`, replace device mappings from `"cuda"` to `"cpu"`.

### Issue 2: Qdrant Collection Schema Conflicts
- **Symptom**: Startup console shows connection errors or vector dimensions mismatch.
- **Cause**: An existing collection named `multimodal_rag` was initialized with a different dimension (e.g. 1536 dims for OpenAI embeddings) instead of 768 dims (for BAAI BGE model).
- **Resolution**: Use the reset endpoint to wipe the collection, or rename the collection identifier inside `backend/mcp_server/config.py`:
  ```python
  COLLECTION_NAME = "multimodal_rag_v2"
  ```

### Issue 3: Missing Visual C++ Redistributable (Windows)
- **Symptom**: `ImportError: DLL load failed` when loading `easyocr` or `cv2`.
- **Cause**: EasyOCR relies on OpenCV, which requires C++ runtimes.
- **Resolution**: Download and install the latest [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist).
