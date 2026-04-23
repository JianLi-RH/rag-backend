# -*- coding: gbk -*-

from rag_backend.config.settings import settings


class EmbeddingsFactory:
    @staticmethod
    def create():
        """
        Factory method to create an embeddings instance based on .env config.
        """
        embeddings_provider = settings.embeddings_provider
        vector_store_type = settings.vector_store_type
        
        if embeddings_provider == "ollama":
            from langchain_community.embeddings import OllamaEmbeddings
            if vector_store_type == "chroma":
                return OllamaEmbeddings(model=settings.embedding_model)
            else:
                raise ValueError(f"Unsupported vector store type: {vector_store_type}")
        else:
            raise ValueError(f"Unsupported embeddings provider: {embeddings_provider}")