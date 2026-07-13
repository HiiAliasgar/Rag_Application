"""Streamlit UI for RAG Application."""

import streamlit as st
import requests
import os
from pathlib import Path

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_BASE_URL = "http://localhost:8000"

st.title("📚 RAG Document Q&A System")
st.markdown("Upload documents and ask questions about their content using AI-powered retrieval.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("### API Status")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ Cannot reach API")
        st.info("Make sure the FastAPI server is running on port 8000")

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload Documents", "❓ Ask Questions", "📋 Manage Documents"])

# Tab 1: Upload
with tab1:
    st.header("Upload Documents")
    st.markdown("Upload PDF files to build your knowledge base.")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True
    )
    
    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, file in enumerate(uploaded_files):
            status_text.text(f"Processing {idx + 1}/{len(uploaded_files)}: {file.name}")
            
            try:
                files = {"file": (file.name, file.getbuffer(), "application/pdf")}
                response = requests.post(
                    f"{API_BASE_URL}/upload",
                    files=files,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ {file.name} - {data['chunks']} chunks processed")
                else:
                    st.error(f"❌ Error uploading {file.name}")
            except Exception as e:
                st.error(f"❌ Failed to upload {file.name}: {str(e)}")
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        status_text.empty()

# Tab 2: Query
with tab2:
    st.header("Ask Questions")
    st.markdown("Ask questions about the uploaded documents.")
    
    question = st.text_area(
        "Enter your question:",
        placeholder="What is the main topic of the documents?",
        height=100
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔍 Search", use_container_width=True):
            if question.strip():
                with st.spinner("Searching documents..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/query",
                            json={"question": question},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            st.markdown("### Answer")
                            st.markdown(f"> {data['answer']}")
                            
                            if data['sources']:
                                st.markdown("### Sources")
                                for source in data['sources']:
                                    st.markdown(f"- {source}")
                        else:
                            st.error("Error querying documents")
                    except Exception as e:
                        st.error(f"Failed to query: {str(e)}")
            else:
                st.warning("Please enter a question")

# Tab 3: Manage Documents
with tab3:
    st.header("Manage Documents")
    
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    try:
        response = requests.get(f"{API_BASE_URL}/documents", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            if data['documents']:
                st.markdown(f"### 📄 Uploaded Documents ({data['count']})")
                for doc in data['documents']:
                    st.markdown(f"- {doc}")
            else:
                st.info("No documents uploaded yet. Upload PDFs in the first tab.")
    except Exception as e:
        st.error(f"Failed to fetch documents: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "🤖 **RAG Application** v0.1.0 | "
    "Powered by LangChain, ChromaDB, and OpenAI"
)
