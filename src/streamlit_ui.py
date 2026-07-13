"""Streamlit UI for the RAG Application."""

from __future__ import annotations

import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RAG Document Q&A",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .main .block-container { padding-top: 2rem; max-width: 1180px; }
        .hero {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1.25rem 1.4rem;
            background: #f8fafc;
            margin-bottom: 1rem;
        }
        .hero h1 { margin: 0 0 .35rem 0; font-size: 2rem; }
        .hero p { margin: 0; color: #475569; }
        .source-box {
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: .65rem .8rem;
            margin-bottom: .5rem;
            background: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def api_get(path: str, timeout: int = 5):
    return requests.get(f"{API_BASE_URL}{path}", timeout=timeout)


def api_post(path: str, **kwargs):
    return requests.post(f"{API_BASE_URL}{path}", **kwargs)


def get_api_status() -> tuple[bool, str]:
    try:
        response = api_get("/health", timeout=2)
        if response.status_code == 200:
            return True, "Connected"
        return False, f"HTTP {response.status_code}"
    except requests.RequestException:
        return False, "Offline"


def get_documents() -> dict:
    try:
        response = api_get("/documents", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return {"documents": [], "count": 0}


st.markdown(
    """
    <div class="hero">
        <h1>RAG Document Q&A</h1>
        <p>Upload PDFs, index their content, and ask grounded questions with source-aware answers.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_ok, api_status = get_api_status()
documents_snapshot = get_documents() if api_ok else {"documents": [], "count": 0}

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("API Status", api_status)
metric_col2.metric("Indexed Documents", documents_snapshot.get("count", 0))
metric_col3.metric("Backend", "FastAPI + ChromaDB")

with st.sidebar:
    st.header("Workspace")
    st.caption("Start the FastAPI backend before uploading or asking questions.")
    st.code("python -m src.app", language="bash")
    st.code("streamlit run src/streamlit_ui.py", language="bash")

    st.divider()
    st.subheader("Question Ideas")
    for prompt in [
        "Summarize the uploaded document.",
        "What are the key points?",
        "List important definitions.",
        "What should I remember for exams?",
    ]:
        st.caption(prompt)

tab_upload, tab_query, tab_docs = st.tabs(
    ["Upload", "Ask Questions", "Documents"]
)

with tab_upload:
    st.subheader("Upload PDF Documents")
    st.write("Add one or more PDFs to build the local knowledge base.")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
    )

    if uploaded_files and st.button("Process uploaded files", use_container_width=True):
        progress_bar = st.progress(0)
        for index, uploaded_file in enumerate(uploaded_files, start=1):
            with st.status(f"Processing {uploaded_file.name}", expanded=True) as status:
                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getbuffer(),
                            "application/pdf",
                        )
                    }
                    response = api_post("/upload", files=files, timeout=60)
                    if response.status_code == 200:
                        data = response.json()
                        st.write(f"Chunks created: {data['chunks']}")
                        status.update(label=f"Processed {uploaded_file.name}", state="complete")
                    else:
                        st.error(response.json().get("detail", "Upload failed"))
                        status.update(label=f"Failed {uploaded_file.name}", state="error")
                except requests.RequestException as exc:
                    st.error(f"API request failed: {exc}")
                    status.update(label=f"Failed {uploaded_file.name}", state="error")

            progress_bar.progress(index / len(uploaded_files))

with tab_query:
    st.subheader("Ask a Grounded Question")
    question = st.text_area(
        "Question",
        placeholder="Ask something specific about your uploaded documents...",
        height=120,
    )

    ask_col, clear_col = st.columns([3, 1])
    with ask_col:
        ask_clicked = st.button("Search documents", use_container_width=True)
    with clear_col:
        if st.button("Clear", use_container_width=True):
            st.rerun()

    if ask_clicked:
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            with st.spinner("Retrieving context and generating an answer..."):
                try:
                    response = api_post(
                        "/query",
                        json={"question": question},
                        timeout=60,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown("### Answer")
                        st.write(data["answer"])

                        st.markdown("### Sources")
                        if data["sources"]:
                            for source in data["sources"]:
                                st.markdown(
                                    f"<div class='source-box'>{source}</div>",
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.info("No sources were returned.")
                    else:
                        st.error(response.json().get("detail", "Query failed"))
                except requests.RequestException as exc:
                    st.error(f"API request failed: {exc}")

with tab_docs:
    st.subheader("Indexed Documents")

    if st.button("Refresh list", use_container_width=True):
        st.rerun()

    documents = get_documents()
    if documents.get("documents"):
        for document in documents["documents"]:
            st.markdown(f"<div class='source-box'>{document}</div>", unsafe_allow_html=True)
    else:
        st.info("No PDFs are indexed yet.")

st.divider()
st.caption("Built with FastAPI, Streamlit, LangChain, ChromaDB, and OpenAI.")
