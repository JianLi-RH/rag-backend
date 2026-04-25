# -*- coding: utf-8 -*-
from typing import List, Any
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS

from rag_backend.config.settings import settings
from rag_backend.util import logger

from .base import BaseVectorStore

class FAISSVectorStore(BaseVectorStore):
    """FAISS vector store implementation"""
    
    def __init__(self, collection_name: str, embeddings: Embeddings, **kwargs):
        """Initialize FAISS vector store"""
        self.collection_name = collection_name
        self.embeddings = embeddings
        self.db_path = f"{settings.vector_store_path}/{collection_name}"

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to FAISS"""
        logger.info(f"Adding {len(documents)} documents to FAISS collection {self.collection_name}")
        
        # 尝试从文件加载现有的向量存储
        try:
            db = FAISS.load_local(
                self.db_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("Loaded existing FAISS index")
        except:
            # 如果不存在，创建新的
            db = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            logger.info("Created new FAISS index")
        else:
            # 如果存在，添加新文档
            db.add_documents(documents=documents)
        
        # 保存到磁盘
        db.save_local(self.db_path)
        logger.info(f"Successfully added {len(documents)} documents to FAISS")
    
    def as_retriever(self, **kwargs: Any) -> None:
        """Return a retriever interface"""
        try:
            db = FAISS.load_local(
                self.db_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("Loaded FAISS index for retrieval")
            return db.as_retriever(**kwargs)
        except Exception as e:
            logger.error(f"Failed to load FAISS index: {e}")
            raise