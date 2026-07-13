# RAG Application

A document question-answering application built with FastAPI, Streamlit, LangChain, ChromaDB, and OpenAI. Upload PDF files, create a local vector index, and ask questions that are answered with retrieved document context.

## Highlights

- PDF upload and document chunking
- ChromaDB vector storage
- OpenAI-powered retrieval-augmented answers
- FastAPI backend with REST endpoints
- Streamlit dashboard for upload, search, and document management
- Source-aware responses
- Docker and local development support

## Tech Stack

| Layer | Tools |
| --- | --- |
| Backend | FastAPI, Uvicorn, Pydantic |
| UI | Streamlit |
| RAG | LangChain, OpenAI, ChromaDB |
| Documents | PyPDF2, LangChain PDF loaders |
| Testing | pytest, FastAPI TestClient |
| DevOps | Docker, GitHub Actions |

## Architecture

```text
PDF Upload -> Document Processor -> Text Chunks -> Embeddings -> ChromaDB
                                                        |
User Question -> FastAPI / Streamlit -> Retriever ------+
                                                        |
                                                   OpenAI LLM
                                                        |
                                                 Answer + Sources
```

## Quick Start

### 1. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

Then set your key:

```env
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_DB_PATH=./data/chroma_db
UPLOAD_DIR=./data/uploads
LOG_LEVEL=INFO
```

### 4. Run the API

```bash
python -m src.app
```

API docs will be available at:

```text
http://localhost:8000/docs
```

### 5. Run the Streamlit UI

```bash
streamlit run src/streamlit_ui.py
```

UI will be available at:

```text
http://localhost:8501
```

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

### Upload a PDF

```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload
```

### Ask a Question

```bash
curl -X POST http://localhost:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is this document about?\"}"
```

### List Uploaded Documents

```bash
curl http://localhost:8000/documents
```

## Project Structure

```text
.
├── src/
│   ├── app.py             # FastAPI backend
│   ├── config.py          # Configuration and environment handling
│   ├── rag_chain.py       # Retrieval QA chain
│   ├── rag_core.py        # Vector store and document processing
│   └── streamlit_ui.py    # Interactive Streamlit interface
├── tests/
│   ├── test_api.py
│   └── test_rag_core.py
├── .github/workflows/
│   └── python-tests.yml
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Testing

```bash
pytest -q
```

The test suite uses a dummy OpenAI key in CI and mocks external services where needed.

## Docker

```bash
docker build -t rag-application .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here rag-application
```

## Security Notes

- Keep `.env` out of Git.
- Do not commit uploaded documents or ChromaDB data.
- Add authentication before exposing this API publicly.
- Rotate API keys if they are ever shared accidentally.

## Status

This project is suitable as a learning and portfolio-ready RAG application. Good next improvements include authentication, per-document deletion, page-level citations, and deployment configuration.
