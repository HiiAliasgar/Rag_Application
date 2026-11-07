import pytest

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def configure_test_token(monkeypatch):
    monkeypatch.setattr(app_module.config, "RAG_API_TOKEN", "test-rag-token")


AUTH = {"Authorization": "Bearer test-rag-token"}


def test_upload_rejects_non_pdf_filename():
    response = client.post("/upload", files={"file": ("notes.txt", b"not a pdf", "text/plain")}, headers=AUTH)
    assert response.status_code == 400


def test_upload_rejects_invalid_pdf_content():
    response = client.post("/upload", files={"file": ("notes.pdf", b"not a pdf", "application/pdf")}, headers=AUTH)
    assert response.status_code == 400


def test_upload_rejects_oversized_file():
    response = client.post(
        "/upload",
        files={"file": ("large.pdf", b"%PDF-" + b"x" * app_module.MAX_UPLOAD_BYTES, "application/pdf")},
        headers=AUTH,
    )
    assert response.status_code == 413


def test_document_endpoints_require_token():
    assert client.get("/documents").status_code == 401
    assert client.post("/query", json={"question": "What is in my PDF?"}).status_code == 401
    assert client.post("/upload", files={"file": ("doc.pdf", b"%PDF-", "application/pdf")}).status_code == 401


def test_health_remains_public():
    assert client.get("/health").status_code == 200


def test_missing_server_token_disables_protected_endpoints(monkeypatch):
    monkeypatch.setattr(app_module.config, "RAG_API_TOKEN", "")
    response = client.get("/documents", headers=AUTH)
    assert response.status_code == 503
