"""FastAPI application for RAG system."""

import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src import config  # Load config and env variables first
from src.rag_core import VectorStore, DocumentProcessor
from src.rag_chain import RAGChain

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
vector_store = VectorStore(persist_directory="./data/chroma_db")
doc_processor = DocumentProcessor()
rag_chain = RAGChain(retriever=vector_store.get_retriever())

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
    """Upload and process a PDF document."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save file temporarily
        upload_dir = "./data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process document
        documents = doc_processor.process_pdf(file_path)
        vector_store.add_documents(documents)
        
        return {
            "filename": file.filename,
            "status": "processed",
            "chunks": len(documents),
            "message": f"Successfully processed {file.filename}"
        }
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        result = rag_chain.query(request.question)
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
    upload_dir = "./data/uploads"
    if not os.path.exists(upload_dir):
        return {"documents": []}
    
    documents = [f for f in os.listdir(upload_dir) if f.endswith(".pdf")]
    return {"documents": documents, "count": len(documents)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
