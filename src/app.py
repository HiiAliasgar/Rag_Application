"""FastAPI application for RAG system."""

import logging
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src import config  # Load config and env variables first
from src.rag_core import VectorStore, DocumentProcessor
from src.rag_chain import RAGChain

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_UPLOAD_BYTES = 10 * 1024 * 1024

vector_store: VectorStore | None = None
doc_processor: DocumentProcessor | None = None
rag_chain: RAGChain | None = None


def get_document_processor() -> DocumentProcessor:
    """Create the document processor once and reuse it."""
    global doc_processor
    if doc_processor is None:
        doc_processor = DocumentProcessor(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
        )
    return doc_processor


def get_vector_store() -> VectorStore:
    """Create the vector store once and reuse it."""
    global vector_store
    if vector_store is None:
        config.require_openai_api_key()
        vector_store = VectorStore(persist_directory=str(config.CHROMA_DB_DIR))
    return vector_store


def get_rag_chain() -> RAGChain:
    """Create the RAG chain once and reuse it."""
    global rag_chain
    if rag_chain is None:
        store = get_vector_store()
        rag_chain = RAGChain(
            retriever=store.get_retriever(k=config.RETRIEVAL_K),
            model=config.OPENAI_MODEL,
            temperature=config.TEMPERATURE,
        )
    return rag_chain

app = FastAPI(
    title="RAG Application",
    description="Retrieval-Augmented Generation for document Q&A",
    version="0.1.0"
)


class QueryRequest(BaseModel):
    """Request model for queries."""
    question: str


class QueryResponse(BaseModel):
    """Response model for queries."""
    answer: str
    sources: list[str]
    question: str


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "RAG Application"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a PDF document with bounded, path-safe storage."""
    original_name = file.filename or "document.pdf"
    if not original_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        content = await file.read(MAX_UPLOAD_BYTES + 1)
        if len(content) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="PDF exceeds the 10 MB upload limit")
        if not content.startswith(b"%PDF-"):
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid PDF")

        upload_dir = config.UPLOAD_DIR
        upload_dir.mkdir(parents=True, exist_ok=True)
        stored_name = f"{uuid4().hex}.pdf"
        file_path = upload_dir / stored_name
        file_path.write_bytes(content)

        processor = get_document_processor()
        store = get_vector_store()
        documents = processor.process_pdf(str(file_path))
        store.add_documents(documents)

        return {
            "filename": original_name,
            "status": "processed",
            "chunks": len(documents),
            "message": f"Successfully processed {original_name}"
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error processing uploaded PDF")
        raise HTTPException(status_code=500, detail="Unable to process the uploaded PDF")

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        chain = get_rag_chain()
        result = chain.query(request.question)
        return QueryResponse(
            question=request.question,
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        logger.error(f"Error querying: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/documents")
async def list_documents():
    """List all uploaded documents."""
    upload_dir = config.UPLOAD_DIR
    if not upload_dir.exists():
        return {"documents": [], "count": 0}

    documents = sorted(f.name for f in upload_dir.iterdir() if f.suffix.lower() == ".pdf")
    return {"documents": documents, "count": len(documents)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
