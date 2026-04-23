# -*- coding: utf-8 -*-
from typing import List, Any
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma
import chromadb
from rag_backend.config.settings import settings
from rag_backend.util import logger

from .base import BaseVectorStore

class ChromaVectorStore(BaseVectorStore):
    """Chroma vector store implementation"""
    
    def __init__(self, collection_name: str, embeddings: Embeddings, **kwargs):
        """Initialize Chroma vector store"""
        self.client = chromadb.PersistentClient(
            path=settings.vector_store_path,
        )
        self.collection_name = collection_name
        self.embeddings = embeddings

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to Chroma"""
        logger.info(f"Adding {len(documents)} documents to Chroma collection {self.collection_name}")
        
        # 使用 langchain_chroma.Chroma 来添加文档
        db = Chroma(
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=settings.vector_store_path
        )
        
        db.add_documents(documents=documents)
        logger.info(f"Successfully added {len(documents)} documents")
    
    def as_retriever(self, **kwargs: Any) -> None:
        """Return a retriever interface"""
        db = Chroma(
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=settings.vector_store_path
        )
        
        return db.as_retriever(**kwargs)
    
    