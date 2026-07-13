# RAG Application - Retrieval-Augmented Generation System

A production-ready Retrieval-Augmented Generation (RAG) application that enables AI-powered question answering over private documents. This system combines vector databases, embeddings, and large language models to provide accurate, context-aware answers.

## 🎯 Features

- **Document Upload**: Upload and process PDF documents with automatic chunking
- **Vector Database**: ChromaDB for efficient semantic search over documents
- **AI-Powered Q&A**: Use OpenAI's GPT models with document context
- **Web Interface**: Streamlit UI for easy interaction
- **REST API**: FastAPI backend for integration
- **Source Attribution**: Returns source documents for answer verification
- **Scalable Architecture**: Designed for enterprise document bases

## 🏗️ Architecture

```
┌─────────────────┐
│  User Interface │ (Streamlit)
└────────┬────────┘
         │
┌────────▼────────┐
│   FastAPI App   │ (REST API)
└────────┬────────┘
         │
    ┌────┴────┐
    │          │
┌───▼────┐ ┌──▼──────────┐
│  RAG   │ │Vector Store │ (ChromaDB)
│ Chain  │ │ + Embeddings│
└────────┘ └──────────────┘
    │
┌───▼──────────┐
│   OpenAI     │ (GPT-3.5/GPT-4)
└──────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API Key
- 4GB RAM minimum

### Installation

1. **Clone and setup environment**:
```bash
cd rag_application
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running the Application

#### Option 1: Use FastAPI + Streamlit

**Terminal 1 - Start API Server**:
```bash
python -m src.app
# API running on http://localhost:8000
```

**Terminal 2 - Start Streamlit UI**:
```bash
streamlit run src/streamlit_ui.py
# UI running on http://localhost:8501
```

#### Option 2: Using Docker

```bash
docker build -t rag-app .
docker run -p 8000:8000 -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  rag-app
```

## 📖 Usage

### Via Web Interface (Streamlit)

1. **Upload Documents**: 
   - Navigate to "Upload Documents" tab
   - Select PDF files
   - System automatically processes and indexes them

2. **Ask Questions**:
   - Go to "Ask Questions" tab
   - Enter your question
   - Click "Search" to get AI-powered answers
   - View sources for verification

3. **Manage Documents**:
   - See all uploaded documents
   - Track document count and status

### Via REST API

**Health Check**:
```bash
curl http://localhost:8000/health
```

**Upload Document**:
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload
```

**Query Documents**:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}' \
  http://localhost:8000/query
```

**List Documents**:
```bash
curl http://localhost:8000/documents
```

## 🔧 Configuration

Edit `.env` file:

```env
OPENAI_API_KEY=sk-your-key-here
CHROMA_DB_PATH=./data/chroma_db
UPLOAD_DIR=./data/uploads
LOG_LEVEL=INFO
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## 📚 How RAG Works

1. **Document Processing**:
   - PDFs are loaded and split into chunks
   - Each chunk is embedded into a vector representation

2. **Storage**:
   - Embeddings stored in ChromaDB for fast retrieval
   - Original text preserved for source attribution

3. **Query Processing**:
   - User question is embedded
   - Similar documents retrieved using semantic search
   - Context passed to LLM with the question

4. **Answer Generation**:
   - LLM generates answer based on retrieved context
   - Sources are returned for verification

## 🎓 Key Concepts

### Vector Embeddings
Convert text to high-dimensional vectors that capture semantic meaning. Similar documents have similar vectors.

### Semantic Search
Find documents based on meaning rather than keyword matching. "What is AI?" matches documents about artificial intelligence even without the exact phrase.

### Context Window
The amount of text sent to the LLM. Larger windows allow more context but cost more. Currently optimized for 4-6 documents.

### Chunking Strategy
Documents are split into overlapping chunks to preserve context across boundaries. Prevents important information from being split.

## 📊 Performance Metrics

- **Upload**: ~1-2 seconds per 10-page PDF
- **Query Response**: ~3-5 seconds (depends on OpenAI API)
- **Embeddings Generated**: ~10-50 per query
- **Storage**: ~100 KB per document (depends on size)

## 🔒 Security Considerations

- API keys stored in environment variables (never in code)
- Uploaded files stored locally with access control
- No data sent to third parties except OpenAI
- Consider adding authentication for production

## 🚧 Advanced Features (Future)

- [ ] Multi-language support
- [ ] Image and table extraction from PDFs
- [ ] Real-time collaboration
- [ ] Answer citations with page numbers
- [ ] Custom embedding models
- [ ] Pinecone integration for cloud storage
- [ ] Web UI deployment
- [ ] Caching and performance optimization

## 🐛 Troubleshooting

### "API key not found"
- Check `.env` file has `OPENAI_API_KEY` set correctly
- Verify key is valid in OpenAI dashboard

### "No documents found"
- Ensure PDFs are uploaded successfully
- Check `./data/uploads` directory
- Verify ChromaDB is initialized

### Slow queries
- Reduce number of retrieved documents (k parameter)
- Use faster embedding model
- Consider using GPT-4-turbo for faster responses

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📧 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/rag-application)
- Email: support@example.com

---

**Built with**: LangChain, ChromaDB, FastAPI, OpenAI GPT, Streamlit
