# -*- coding: gbk -*-
import os
from rag_backend.vector_store.factory import VectorStoreFactory
from rag_backend.config.settings import settings
from rag_backend.parsers.factory import DocumentParserFactory
from rag_backend.chunkers.factory import DocumentChunkerFactory

from rag_backend.util import file_status_manager
from logger import logger


async def embed_document_svc(file_path: str) -> bool:
    """Embed a document."""
    abs_path = file_status_manager.get_absolute_path(file_path)
    if not os.path.exists(abs_path):
        logger.error(f"File does not exist: {abs_path}")
        return False

    if not DocumentParserFactory.is_supported(abs_path):
        logger.error(f"Parser not supported for file: {abs_path}")
        return False

    logger.info(f"Parsing file: {abs_path}")
    parser = DocumentParserFactory.get_parser(abs_path)
    parsed_content = parser.parse(abs_path)
    logger.info(f"Parsed content length: {len(parsed_content)}")

    logger.info(f"Chunking file: {abs_path}")
    all_documents = DocumentChunkerFactory.chunk_document(abs_path, parsed_content)
    if not all_documents:
        logger.error(f"No chunks created from file: {abs_path}")
        return False
    logger.info(f"Chunked content length: {len(all_documents)}")

    batch_size = settings.max_batch_size
    import threading
    lock = threading.Lock()
    j = 0
    for i in range(0, len(all_documents), batch_size):
        try:
            logger.info(f"Embedding batch {j} of {int(len(all_documents)/batch_size)} with size {batch_size}") 
            batch = all_documents[i:i+batch_size]
            with lock:
                vector_store = VectorStoreFactory.create("default")
                vector_store.add_documents(
                    documents=batch
                )
            j += 1
        except Exception as e:
            logger.error(f"[embed_document_svc] Batch content: {batch}")
            raise Exception(f"[embed_document_svc] Failed to embed batch {j}: {e}")

    file_status_manager.update_file_status(file_path, 
                                        embeded=True, 
                                        provider=settings.embeddings_provider, 
                                        module=settings.embedding_model)
    logger.info("Vector store updated successfully.")
    return True
