"""Tests for RAG core components."""

import os
from unittest.mock import patch, MagicMock
from src.rag_core import DocumentProcessor, VectorStore
from langchain.schema import Document

os.environ.setdefault("OPENAI_API_KEY", "test-key")


class TestDocumentProcessor:
    """Test document processing functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.processor = DocumentProcessor(chunk_size=500, chunk_overlap=100)

    def test_process_text_basic(self):
        """Test basic text processing."""
        text = "This is a test document. " * 20
        documents = self.processor.process_text(text, source="test")
        
        assert len(documents) > 0
        assert all(isinstance(doc, Document) for doc in documents)
        assert all(doc.metadata["source"] == "test" for doc in documents)

    def test_process_text_empty(self):
        """Test processing empty text."""
        documents = self.processor.process_text("", source="empty")
        assert documents == []

    def test_chunk_size_respected(self):
        """Test that chunks respect size limit."""
        text = "word " * 1000
        documents = self.processor.process_text(text)
        
        for doc in documents:
            assert len(doc.page_content) <= 600  # Some buffer for word boundaries

    def test_multiple_files_processing(self):
        """Test processing multiple files."""
        with patch.object(self.processor, 'process_pdf') as mock_process:
            mock_process.return_value = [
                Document(page_content="chunk1"),
                Document(page_content="chunk2")
            ]
            
            files = ["file1.pdf", "file2.pdf"]
            result = self.processor.process_multiple_files(files)
            
            assert len(result) == 4
            assert mock_process.call_count == 2


class TestVectorStore:
    """Test vector store functionality."""

    @patch('src.rag_core.OpenAIEmbeddings')
    @patch('src.rag_core.Chroma')
    def test_vectorstore_initialization(self, mock_chroma, mock_embeddings, tmp_path):
        """Test vector store initialization."""
        persist_directory = tmp_path / "chroma"
        vector_store = VectorStore(persist_directory=str(persist_directory))
        
        assert vector_store.persist_directory == str(persist_directory)
        mock_embeddings.assert_called_once()

    @patch('src.rag_core.OpenAIEmbeddings')
    @patch('src.rag_core.Chroma')
    def test_add_documents(self, mock_chroma, mock_embeddings):
        """Test adding documents to vector store."""
        mock_vs = MagicMock()
        mock_chroma.return_value = mock_vs
        
        vector_store = VectorStore()
        docs = [Document(page_content="test")]
        vector_store.add_documents(docs)
        
        mock_vs.add_documents.assert_called_once_with(docs)
        mock_vs.persist.assert_called_once()

    @patch('src.rag_core.OpenAIEmbeddings')
    @patch('src.rag_core.Chroma')
    def test_search_documents(self, mock_chroma, mock_embeddings):
        """Test searching documents."""
        mock_vs = MagicMock()
        mock_vs.similarity_search.return_value = [
            Document(page_content="result1"),
            Document(page_content="result2")
        ]
        mock_chroma.return_value = mock_vs
        
        vector_store = VectorStore()
        results = vector_store.search("test query", k=2)
        
        assert len(results) == 2
        mock_vs.similarity_search.assert_called_once_with("test query", k=2)
