# 🔍 DeepRetrieve


**DeepRetrieve** is an intelligent multimodal RAG (Retrieval-Augmented Generation) system that enables natural language querying of PDF documents. It extracts and understands text, images, and tables from PDFs, providing accurate, context-aware answers with source attribution.

<div align="center">
  <img src="frontend\public\hero-section.jpg" alt="DeepRetrieve Landing Page" width="800">
  <p><em>DeepRetrieve - The Next Generation of Agentic RAG</em></p>  <p>
    <a href="https://deep-retrieve.vercel.app/" target="_blank">
      <strong>🚀 Try Live Demo</strong>
    </a>
  </p></div>

## ✨ Features

### 🎯 Core Capabilities
- **📄 Multimodal PDF Processing**: Extracts text, images, and tables from PDF documents
- **🔍 Semantic Search**: Uses CLIP embeddings for unified text and image search
- **🤖 AI-Powered Responses**: Leverages Google Gemini for contextual answer generation
- **📊 Table Understanding**: Extracts and parses tables into queryable markdown format
- **🖼️ Visual Analysis**: Processes charts, diagrams, and images from documents
- **⚡ Fast Retrieval**: Powered by Qdrant vector database with binary quantization
- **📝 Source Attribution**: Every answer includes references to source documents and pages

### 🎨 User Interface
- **Modern Landing Page**: Engaging hero section with feature showcase
- **Interactive Chat**: Real-time Q&A interface with PDF viewing
- **Split View**: Simultaneous chat and document preview
- **Responsive Design**: Works seamlessly on desktop and mobile


## 🚀 Quick Start

### Prerequisites

- **Python** 3.8 or higher
- **Node.js** 18.0 or higher
- **Qdrant Cloud** account (free tier available)
- **Google AI Studio** API key (free tier available)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/Hariprasaadh/DeepRetrieve.git
cd DeepRetrieve
```

#### 2. Backend Setup

```bash
cd backend

# Install dependencies with uv
uv pip install -r requirements.txt
```

#### 3. Environment Configuration

Create a `.env` file in the `backend` directory:

```env
# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster-url.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key
```

**Getting API Keys:**
- **Qdrant**: Sign up at [cloud.qdrant.io](https://cloud.qdrant.io/) and create a free cluster
- **Google Gemini**: Get your API key from [ai.google.dev](https://ai.google.dev/)

#### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 5. Start the Backend

In a new terminal:
```bash
cd backend
python api/run.py
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 📖 Usage

### 1. Index Your PDFs

Using the Jupyter notebook (`backend/workflow.ipynb`):

```python
# Create collection
create_collection(COLLECTION_NAME, recreate=True)

# Index a PDF
pdf_path = "data/your_document.pdf"
index_pdf(pdf_path)
```

### 2. Query via API

```python
import requests

response = requests.post('http://localhost:5000/api/query', json={
    'query': 'What is the main topic of the document?',
    'top_k': 3
})

print(response.json()['answer'])
```

### 3. Using the Web Interface

1. Navigate to http://localhost:5173
2. Upload your PDF document
3. Ask questions in natural language
4. View answers with source references and page previews



## 🔧 API Reference

### POST `/api/query`
Query the RAG system with a question.

**Request:**
```json
{
  "query": "What is the main topic?",
  "top_k": 3
}
```

**Response:**
```json
{
  "answer": "The document focuses on...",
  "sources": [
    {
      "type": "text",
      "score": 0.89,
      "source": "document.pdf",
      "page": 1,
      "preview": "Content preview..."
    }
  ],
  "num_results": 3
}
```

### POST `/api/upload`
Upload and index a new PDF document.

**Request:**
- Content-Type: `multipart/form-data`
- Body: PDF file

**Response:**
```json
{
  "success": true,
  "message": "PDF indexed successfully",
  "text_chunks": 45,
  "images": 12,
  "tables": 3
}
```

## 🧪 Configuration

### Customization Options

```python
# Embedding Configuration
CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
EMBEDDING_DIM = 512

# RAG Configuration
TOP_K = 3              # Number of results to retrieve
CHUNK_SIZE = 500       # Text chunk size in words
CHUNK_OVERLAP = 50     # Overlap between chunks

# Collection Name
COLLECTION_NAME = "multimodal_rag"
```


## 📊 Performance

- **Indexing Speed**: ~2-5 pages/second (depends on content complexity)
- **Query Latency**: <2 seconds (including LLM generation)
- **Vector Database**: Binary quantization reduces storage by ~32x
- **Supported PDF Size**: Up to 500 pages per document

<div align="center">
  
### ⭐ Star this repo if you find it helpful!

*Empowering intelligent document understanding through multimodal RAG*

</div>


