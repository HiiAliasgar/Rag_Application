"""Authenticated HTTP client for the RAG FastAPI service."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
RAG_API_TOKEN = os.getenv("RAG_API_TOKEN", "").strip()


def api_headers() -> dict[str, str]:
    if not RAG_API_TOKEN:
        return {}
    return {"Authorization": f"Bearer {RAG_API_TOKEN}"}


def api_get(path: str, timeout: int = 5):
    return requests.get(f"{API_BASE_URL}{path}", headers=api_headers(), timeout=timeout)


def api_post(path: str, **kwargs):
    headers = {**api_headers(), **kwargs.pop("headers", {})}
    return requests.post(f"{API_BASE_URL}{path}", headers=headers, **kwargs)
