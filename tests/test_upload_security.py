from io import BytesIO

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_upload_rejects_non_pdf_filename():
    response = client.post("/upload", files={"file": ("notes.txt", b"not a pdf", "text/plain")})
    assert response.status_code == 400


def test_upload_rejects_invalid_pdf_content():
    response = client.post("/upload", files={"file": ("notes.pdf", b"not a pdf", "application/pdf")})
    assert response.status_code == 400


def test_upload_rejects_oversized_file():
    response = client.post(
        "/upload",
        files={"file": ("large.pdf", b"%PDF-" + b"x" * app_module.MAX_UPLOAD_BYTES, "application/pdf")},
    )
    assert response.status_code == 413
