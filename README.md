# RAG Application

A document question-answering project that explores Retrieval-Augmented Generation (RAG). Users can upload PDF documents, process their contents into chunks, retrieve relevant passages and ask questions through a Streamlit interface or API.

## Core workflow

1. Upload a PDF document.
2. Extract and split the document text into chunks.
3. Generate embeddings and store them in a ChromaDB vector store.
4. Retrieve relevant chunks for a user question.
5. Pass the retrieved context to an LLM to generate an answer with source references.

## Features

- PDF upload and document processing.
- Semantic retrieval using ChromaDB.
- LLM-generated responses grounded in retrieved context.
- Streamlit interface.
- FastAPI backend and API documentation.
- Docker and Docker Compose configuration.
- Tests for selected API and retrieval components.

## Technology

| Area | Technology |
|---|---|
| Language | Python |
| API | FastAPI |
| Interface | Streamlit |
| RAG framework | LangChain |
| Vector store | ChromaDB |
| Model provider | OpenAI API |
| Packaging / deployment | Docker |

## Run with Docker

```bash
git clone https://github.com/HiiAliasgar/Rag_Application.git
cd Rag_Application
cp .env.example .env
```

Add your `OPENAI_API_KEY` to `.env`, then run:

```bash
docker-compose up --build
```

## Upload safety

The API accepts PDF files up to 10 MB. Uploads are checked for a PDF signature and stored under a server-generated filename rather than a client-controlled path. The upload, document-listing and query endpoints are still intended for a trusted development environment; add authentication and authorization before exposing this service to untrusted users.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Start the API and UI in separate terminals:

```bash
python -m src.app
```

```bash
streamlit run src/streamlit_ui.py
```

The documented local endpoints are:

- Streamlit: `http://localhost:8501`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Tests

```bash
pytest -q
```

## Important limitations

Generated answers can be incomplete or incorrect. Verify important statements against the retrieved document passages. API access requires a valid model-provider key and may incur provider charges.

[Source code](https://github.com/HiiAliasgar/Rag_Application)

## API security

Set a unique server-side `RAG_API_TOKEN` in your environment. The `/upload`, `/query` and `/documents` endpoints require an `Authorization: Bearer <token>` header. The `/health` endpoint remains public for service health checks. Do not expose the API without configuring this token.

