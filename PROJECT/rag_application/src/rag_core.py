"""Core RAG (Retrieval-Augmented Generation) components."""

import os
import logging
from typing import List, Optional
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages vector database operations using ChromaDB."""

    def __init__(self, persist_directory: str = "./data/chroma_db"):
        """Initialize vector store with ChromaDB."""
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory=persist_directory,
            collection_name="documents"
        )
        logger.info(f"Vector store initialized at {persist_directory}")

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        if not documents:
            logger.warning("No documents provided")
            return
        
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
        logger.info(f"Added {len(documents)} documents to vector store")

    def search(self, query: str, k: int = 4) -> List[Document]:
        """Retrieve relevant documents for a query."""
        results = self.vectorstore.similarity_search(query, k=k)
        logger.debug(f"Retrieved {len(results)} documents for query: {query}")
        return results

    def get_retriever(self, k: int = 4):
        """Get retriever for use in RAG chain."""
        return self.vectorstore.as_retriever(search_kwargs={"k": k})


class DocumentProcessor:
    """Handles document loading and chunking."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize document processor."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        logger.info(f"Document processor initialized (chunk_size={chunk_size})")

    def process_pdf(self, file_path: str) -> List[Document]:
        """Load and chunk a PDF file."""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Processed PDF: {file_path} into {len(chunks)} chunks")
        return chunks

    def process_text(self, text: str, source: str = "text") -> List[Document]:
        """Process raw text into chunks."""
        documents = [Document(page_content=text, metadata={"source": source})]
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Processed text ({source}) into {len(chunks)} chunks")
        return chunks

    def process_multiple_files(self, file_paths: List[str]) -> List[Document]:
        """Process multiple PDF files."""
        all_chunks = []
        for file_path in file_paths:
            chunks = self.process_pdf(file_path)
            all_chunks.extend(chunks)
        return all_chunks
