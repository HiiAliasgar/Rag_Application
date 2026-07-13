"""RAG chain using LangChain for Q&A over documents."""

import logging
from typing import Any
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import BaseRetriever

logger = logging.getLogger(__name__)

# Custom prompt for RAG
RAG_PROMPT_TEMPLATE = """Use the following pieces of context to answer the user's question. 
If you don't know the answer, just say you don't know. Do not make up information.

Context:
{context}

Question: {question}

Answer:"""


class RAGChain:
    """RAG chain for question answering."""

    def __init__(self, retriever: BaseRetriever, model: str = "gpt-3.5-turbo"):
        """Initialize RAG chain."""
        self.retriever = retriever
        self.llm = ChatOpenAI(
            model_name=model,
            temperature=0.7,
            max_tokens=512
        )
        
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=RAG_PROMPT_TEMPLATE
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        logger.info(f"RAG chain initialized with model: {model}")

    def query(self, question: str) -> dict[str, Any]:
        """Query the RAG chain and get answer."""
        logger.info(f"Processing query: {question}")
        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "sources": [doc.metadata.get("source", "unknown") for doc in result["source_documents"]],
            "documents": result["source_documents"]
        }

    def stream_query(self, question: str):
        """Stream query results (for future streaming support)."""
        return self.query(question)
