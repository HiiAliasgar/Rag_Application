# RAG Application - Setup and Quick Start Guide

## What is RAG?

Retrieval-Augmented Generation (RAG) enhances AI by letting it answer questions based on your documents. Instead of just relying on training data, it:

1. **Searches** your documents semantically
2. **Retrieves** the most relevant passages
3. **Generates** answers using the retrieved context

This ensures answers are based on actual content, with sources you can verify.

## Installation Steps

### 1. Prerequisites

Ensure you have:
- Python 3.11 or higher
- OpenAI API account with valid key
- 4GB RAM minimum
- 2GB disk space for databases

Check Python:
```bash
python --version
```

### 2. Setup Environment

**On Windows** (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**On macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

Get your key from: https://platform.openai.com/api-keys

### 5. Initialize Data Directories

```bash
mkdir -p data/uploads data/chroma_db
```

## Running the Application

### Method 1: Windows Batch File (Easiest)
```bash
start.bat
```

This opens two windows - one for API, one for UI.

### Method 2: Manual Start (Linux/macOS)

**Terminal 1 - API Server**:
```bash
python -m src.app
```
Wait until you see: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Streamlit UI**:
```bash
streamlit run src/streamlit_ui.py
```
Wait until you see: `You can now view your Streamlit app in your browser`

### Method 3: Docker

```bash
docker-compose up
```

## First Use Walkthrough

### Step 1: Upload a Document

1. Open http://localhost:8501 in your browser
2. Go to **"Upload Documents"** tab
3. Click **"Choose files"** and select any PDF
4. System will process it automatically

Example PDFs to try:
- Research papers
- Company documentation
- Books or textbooks
- Technical manuals

### Step 2: Ask Questions

1. Go to **"Ask Questions"** tab
2. Enter a question about your document, e.g.:
   - "What is the main topic?"
   - "Summarize the key findings"
   - "What dates are mentioned?"
3. Click **"Search"**
4. View the AI answer and source documents

### Step 3: Manage Documents

1. Go to **"Manage Documents"** tab
2. See all uploaded documents
3. Document count and status

## Testing Locally Without API Key

For development, you can use a mock LLM:

1. Edit `src/app.py` and replace:
```python
self.llm = ChatOpenAI(model_name=model, ...)
```

With:
```python
from langchain.llms.fake import FakeListLLM
self.llm = FakeListLLM(responses=["Test answer", "Example response"])
```

This allows testing without API costs!

## Common Issues & Solutions

### Issue: "OPENAI_API_KEY not found"
**Solution**: 
- Check `.env` file exists in project root
- Verify key is set correctly
- Restart Python after editing `.env`

### Issue: "No module named 'langchain'"
**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Port 8000 or 8501 already in use
**Solution**:
```bash
# Find process using port 8000
lsof -i :8000
# Or on Windows
netstat -ano | findstr :8000
# Kill it (replace PID with actual process ID)
kill -9 PID
```

### Issue: Slow uploads or queries
**Solution**:
- Check internet connection (OpenAI API calls)
- Reduce chunk size in `src/config.py`
- Use fewer retrieval documents (reduce `k`)
- Consider GPT-4-turbo for faster responses

## File Structure

```
rag_application/
├── src/
│   ├── __init__.py              # Package init
│   ├── app.py                   # FastAPI application
│   ├── config.py                # Configuration management
│   ├── rag_core.py              # Vector store & document processing
│   ├── rag_chain.py             # RAG chain orchestration
│   └── streamlit_ui.py          # Web interface
├── tests/
│   ├── __init__.py
│   ├── test_api.py              # API endpoint tests
│   └── test_rag_core.py         # Core logic tests
├── data/
│   ├── uploads/                 # Uploaded PDF files
│   └── chroma_db/               # Vector database
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata
├── README.md                    # User documentation
├── ARCHITECTURE.md              # Technical architecture
├── .env.example                 # Environment template
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker compose setup
├── start.sh                     # Linux/macOS startup
└── start.bat                    # Windows startup
```

## Development Tips

### Adding Custom Logic

**Custom prompt**:
Edit `src/rag_chain.py` - modify `RAG_PROMPT_TEMPLATE`

**Change retrieval count**:
Edit `src/config.py` - modify `RETRIEVAL_K`

**Different embedding model**:
Edit `src/rag_core.py` - change `OpenAIEmbeddings()`

### Running Tests

```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=src
```

### Monitoring Performance

Add to your query code:
```python
import time
start = time.time()
result = rag_chain.query(question)
elapsed = time.time() - start
print(f"Query took {elapsed:.2f}s")
```

## Advanced: Deployment

### AWS Deployment

See `ARCHITECTURE.md` for cloud deployment patterns.

### Performance Tuning

1. **Faster responses**: Use GPT-4-turbo (faster inference)
2. **Lower costs**: Use smaller embeddings model
3. **Better accuracy**: Increase retrieval documents (k=6-8)
4. **Caching**: Add Redis for query caching

## API Documentation

Once running, visit: http://localhost:8000/docs

This shows interactive API documentation (Swagger UI).

### Example curl commands:

**Upload file**:
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload
```

**Query**:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is this about?"}' \
  http://localhost:8000/query
```

**List documents**:
```bash
curl http://localhost:8000/documents
```

## Next Steps

1. ✅ Install and run locally
2. ✅ Upload sample document
3. ✅ Test with different questions
4. ✅ Read ARCHITECTURE.md for details
5. ✅ Customize for your use case
6. ✅ Deploy to production (see deployment section)

## Resources

- **LangChain Docs**: https://docs.langchain.com
- **ChromaDB Docs**: https://docs.trychroma.com
- **OpenAI API**: https://platform.openai.com/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **Streamlit**: https://docs.streamlit.io

## Support

Having issues? Check:
1. This guide's troubleshooting section
2. `.env` configuration
3. API key validity
4. Python version compatibility
5. GitHub Issues (future)

---

**Ready to go?** Run `start.bat` (Windows) or terminal commands (Mac/Linux) and visit http://localhost:8501!
