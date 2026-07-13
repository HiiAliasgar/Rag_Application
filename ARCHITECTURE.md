# RAG Application Architecture

## System Overview

This document describes the architecture and design of the RAG (Retrieval-Augmented Generation) Application.

## Components

### 1. Document Processing Layer (`rag_core.py`)

**VectorStore Class**
- Manages ChromaDB vector database
- Handles document embedding using OpenAI embeddings
- Provides semantic search capabilities
- Persists embeddings to disk

**DocumentProcessor Class**
- Loads PDF documents using PyPDFLoader
- Implements recursive character-level text splitting
- Preserves document source metadata
- Handles chunk overlap for context preservation

### 2. RAG Chain Layer (`rag_chain.py`)

**RAGChain Class**
- Orchestrates LangChain's RetrievalQA
- Uses ChatOpenAI LLM with configurable temperature
- Implements custom prompt template for context-aware answers
- Returns both answers and source documents

### 3. API Layer (`app.py`)

**FastAPI Application**
- REST endpoints for document management
- Async request handling for scalability
- Input validation using Pydantic models
- Comprehensive error handling

**Endpoints**:
- `GET /health` - Service health check
- `POST /upload` - Upload and process PDF
- `POST /query` - Query documents with RAG
- `GET /documents` - List uploaded documents

### 4. UI Layer (`streamlit_ui.py`)

**Streamlit Interface**
- Multi-tab interface for document and query management
- Real-time API status monitoring
- Progress tracking for uploads
- Source attribution display

**Features**:
- Upload Documents tab
- Ask Questions tab
- Manage Documents tab

### 5. Configuration (`config.py`)

Centralized configuration management:
- Environment variable loading
- Directory path management
- API and model settings
- Logging configuration

## Data Flow

### Document Upload Flow

```
User Upload (PDF)
    ↓
FastAPI /upload endpoint
    ↓
DocumentProcessor.process_pdf()
    ├─ Load PDF with PyPDFLoader
    ├─ Split into chunks (1000 tokens, 200 overlap)
    └─ Create Document objects with metadata
    ↓
VectorStore.add_documents()
    ├─ Generate embeddings (OpenAI API)
    ├─ Store in ChromaDB
    └─ Persist to disk
    ↓
Response to client
```

### Query Processing Flow

```
User Question
    ↓
FastAPI /query endpoint
    ↓
RAGChain.query()
    ↓
Embed question → Search vector DB
    ↓
VectorStore.search() returns k=4 similar docs
    ↓
Pass context + question to LLM
    ↓
ChatOpenAI generates answer
    ↓
Return answer + source documents
    ↓
Display in UI
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | FastAPI | REST API & async handling |
| Vector DB | ChromaDB | Efficient semantic search |
| Embeddings | OpenAI | Text-to-vector conversion |
| LLM | GPT-3.5/4 | Answer generation |
| UI Framework | Streamlit | Web interface |
| Orchestration | LangChain | RAG pipeline |
| Document Loading | PyPDF2 | PDF parsing |

## Performance Characteristics

### Latency Breakdown (per query)
- Vector embedding: ~200-500ms
- Database search: ~50-100ms
- LLM inference: ~2000-4000ms
- **Total**: ~2.5-5s typical

### Scalability Considerations

**Bottlenecks**:
1. OpenAI API rate limits (3,500 RPM for standard)
2. ChromaDB in-memory index size
3. Token context window (4K for GPT-3.5, 8K for GPT-4)

**Optimization Strategies**:
- Cache embeddings for frequently asked questions
- Use smaller embedding models for speed
- Implement request batching
- Use ChromaDB with persistent storage

## Security Architecture

### Data Protection
- API keys stored in environment variables
- No sensitive data logged
- Uploaded files stored locally only
- Optional: Add API authentication

### Production Recommendations
1. Use HTTPS for all API calls
2. Implement API key authentication
3. Add rate limiting
4. Use secrets management service (e.g., AWS Secrets Manager)
5. Audit log all document uploads
6. Implement data retention policies

## Deployment Architecture

### Local Deployment
```
Developer Machine
├── FastAPI (port 8000)
└── Streamlit (port 8501)
```

### Docker Deployment
```
Docker Container
├── API Service (port 8000)
└── Streamlit Service (port 8501)
```

### Cloud Deployment (AWS Example)
```
AWS ECS Cluster
├── ECS Task 1: API Service (Fargate)
├── ECS Task 2: UI Service (Fargate)
├── RDS: PostgreSQL (metadata)
└── S3: Document storage
    with
└── DynamoDB: Vector index cache
```

## Extensibility

### Adding New Features

**Custom Embedding Models**:
```python
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

**Alternative Vector DBs**:
- Pinecone (cloud-hosted)
- Weaviate (open-source)
- FAISS (memory-based)
- Milvus (distributed)

**Different LLMs**:
- Anthropic Claude
- Open Source: Llama, Falcon, Mistral
- Azure OpenAI

## Monitoring and Logging

### Implemented
- Request logging in FastAPI
- Document processing logging
- Query execution logging

### Recommended Production Additions
- Performance metrics (latency, throughput)
- Error rate tracking
- Token usage monitoring
- User activity audit logs

## Testing Strategy

### Unit Tests
- `test_rag_core.py`: Document processing, vector store operations
- Test data chunking, embedding, retrieval

### Integration Tests
- `test_api.py`: API endpoints, error handling
- Mock external dependencies (OpenAI, ChromaDB)

### E2E Tests (Future)
- Full workflow: upload → query → verify
- Multiple document handling
- Concurrent user simulation

## Future Improvements

1. **Advanced Features**
   - Multi-modal (images, tables)
   - Cross-language support
   - Real-time collaboration
   - Citation with page numbers

2. **Performance**
   - Response caching
   - Embedding caching
   - Batch query processing
   - Async document processing

3. **Enterprise**
   - User authentication/authorization
   - Document access control
   - Audit logging
   - SLA monitoring

4. **ML**
   - Fine-tuned embeddings for domain
   - Custom reranking models
   - Feedback loop for improvement
