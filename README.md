<h1 align="center">RAG Application</h1>

<p align="center">
  <b>Document Q&A powered by Retrieval-Augmented Generation</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge" alt="LangChain" />
  <img src="https://img.shields.io/badge/ChromaDB-5B21B6?style=for-the-badge" alt="ChromaDB" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge" alt="PRs Welcome" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License" />
  <img src="https://img.shields.io/badge/Status-ProductionReady-brightgreen?style=for-the-badge" alt="Status" />
</p>

---

## Overview

A powerful document question-answering application that lets you upload PDF files, create a local vector index, and ask natural language questions with **source-aware answers**.

### Key Features

| Feature | Description |
|---------|-------------|
| 📄 PDF Upload | Upload and process multiple PDF documents |
| 🔍 Vector Search | ChromaDB-powered semantic search |
| 🤖 AI Answers | OpenAI-powered RAG responses |
| 🌐 Web Interface | Beautiful Streamlit dashboard |
| 🔌 REST API | FastAPI backend with full documentation |
| 🐳 Docker Ready | One-command deployment |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     RAG APPLICATION                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│   │   PDF    │───▶│ Processor│───▶│ Chunks   │            │
│   │  Upload  │    │          │    │          │            │
│   └──────────┘    └──────────┘    └────┬─────┘            │
│                                        │                    │
│                                        ▼                    │
│                                   ┌─────────┐              │
│                                   │Embedding│              │
│                                   │  Model  │              │
│                                   └────┬────┘              │
│                                        │                    │
│                                        ▼                    │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│   │  User    │───▶│  Query   │───▶│  RAG     │            │
│   │ Question │    │ Handler  │    │  Chain   │            │
│   └──────────┘    └──────────┘    └────┬─────┘            │
│                                        │                    │
│                                        ▼                    │
│                                   ┌─────────┐              │
│                                   │  OpenAI │              │
│                                   │   LLM   │              │
│                                   └────┬────┘              │
│                                        │                    │
│                                        ▼                    │
│                                   ┌─────────┐              │
│                                   │ Answer + │              │
│                                   │ Sources  │              │
│                                   └─────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/HiiAliasgar/Rag_Application.git
cd Rag_Application

# Set up environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Run with Docker Compose
docker-compose up --build
```

### Option 2: Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Set your OPENAI_API_KEY in .env

# 4. Start the API server
python -m src.app

# 5. In another terminal, start Streamlit UI
streamlit run src/streamlit_ui.py
```

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Streamlit UI | http://localhost:8501 | Interactive web interface |
| API Docs | http://localhost:8000/docs | Swagger documentation |
| Health Check | http://localhost:8000/health | API status endpoint |

---

## API Reference

### Health Check
```bash
curl http://localhost:8000/health
# Returns: {"status": "healthy", "service": "RAG Application"}
```

### Upload Document
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
# Returns: {"filename": "document.pdf", "chunks": 15, "status": "processed"}
```

### Ask Question
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
# Returns: {"answer": "...", "sources": ["document.pdf"], "question": "..."}
```

### List Documents
```bash
curl http://localhost:8000/documents
# Returns: {"documents": ["file1.pdf", "file2.pdf"], "count": 2}
```

---

## Project Structure

```
Rag_Application/
├── src/
│   ├── __init__.py         # Package init
│   ├── app.py              # FastAPI application
│   ├── config.py           # Configuration management
│   ├── rag_chain.py        # RAG chain implementation
│   ├── rag_core.py         # Vector store & document processing
│   └── streamlit_ui.py     # Streamlit web interface
├── tests/
│   ├── test_api.py         # API endpoint tests
│   └── test_rag_core.py    # Core functionality tests
├── .github/workflows/
│   └── python-tests.yml    # CI/CD pipeline
├── data/                   # Runtime data (gitignored)
├── .env.example            # Environment template
├── docker-compose.yml      # Docker orchestration
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (with defaults)
CHROMA_DB_PATH=./data/chroma_db
UPLOAD_DIR=./data/uploads
OPENAI_MODEL=gpt-3.5-turbo
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

---

## Testing

```bash
# Run all tests
pytest -q

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_api.py -v
```

---

## Docker Commands

```bash
# Build image
docker build -t rag-application .

# Run container
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here rag-application

# Docker Compose
docker-compose up --build -d    # Start
docker-compose down              # Stop
docker-compose logs -f           # View logs
```

---

## Security Best Practices

| Practice | Implementation |
|----------|----------------|
| ✅ Environment Variables | Use `.env` file (never commit!) |
| ✅ API Key Protection | Required key validation |
| ✅ Input Validation | File type checking, sanitization |
| ✅ Error Handling | Graceful error responses |

---

## Roadmap

- [ ] User authentication & authorization
- [ ] Per-document deletion
- [ ] Page-level citations
- [ ] Streaming responses
- [ ] Multi-language support
- [ ] Cloud deployment (AWS/GCP)

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Aliasgar Lohawala** - [@HiiAliasgar](https://github.com/HiiAliasgar)

<p align="center">
  Made with ❤️ and Python
</p>
