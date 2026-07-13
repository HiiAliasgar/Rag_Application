"""Tests for RAG API endpoints."""

import os
from fastapi.testclient import TestClient
from unittest.mock import patch

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from src.app import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self):
        """Test health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestQueryEndpoint:
    """Test query endpoint."""

    @patch('src.app.rag_chain')
    def test_query_success(self, mock_rag):
        """Test successful query."""
        mock_rag.query.return_value = {
            "answer": "Test answer",
            "sources": ["source1.pdf"]
        }
        
        response = client.post("/query", json={"question": "Test question?"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Test answer"
        assert data["question"] == "Test question?"

    def test_query_empty_question(self):
        """Test query with empty question."""
        response = client.post("/query", json={"question": ""})
        assert response.status_code == 400

    @patch('src.app.rag_chain')
    def test_query_error_handling(self, mock_rag):
        """Test query error handling."""
        mock_rag.query.side_effect = Exception("API Error")
        
        response = client.post("/query", json={"question": "Test?"})
        assert response.status_code == 500


class TestDocumentsEndpoint:
    """Test documents listing."""

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_list_documents(self, mock_listdir, mock_exists):
        """Test listing documents."""
        mock_exists.return_value = True
        mock_listdir.return_value = ["doc1.pdf", "doc2.pdf", "other.txt"]
        
        response = client.get("/documents")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        assert len(data["documents"]) == 2

    @patch('os.path.exists')
    def test_list_documents_empty(self, mock_exists):
        """Test listing documents when none exist."""
        mock_exists.return_value = False
        
        response = client.get("/documents")
        
        assert response.status_code == 200
        assert response.json()["count"] == 0
