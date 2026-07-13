"""
RAG Application Configuration and Utilities
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", DATA_DIR / "uploads"))
CHROMA_DB_DIR = Path(os.getenv("CHROMA_DB_PATH", DATA_DIR / "chroma_db"))

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# RAG Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "4"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def require_openai_api_key() -> str:
    """Return the configured OpenAI API key or raise a clear runtime error."""
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. Copy .env.example to .env and set your key."
        )
    return OPENAI_API_KEY

__all__ = [
    "PROJECT_ROOT",
    "DATA_DIR",
    "UPLOAD_DIR",
    "CHROMA_DB_DIR",
    "API_HOST",
    "API_PORT",
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP",
    "RETRIEVAL_K",
    "TEMPERATURE",
    "LOG_LEVEL",
    "require_openai_api_key",
]
