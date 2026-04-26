# -*- coding: utf-8 -*-

import os
from typing import List, Dict, Any

from rag_backend.util import logger
from .base import DocumentChunker
from .word_chunker import WordChunker
from .markdown_chunker import MarkdownChunker
from .text_chunker import TextChunker
from .table_chunker import TableChunker
from .pdf_chunker import PDFChunker

class DocumentChunkerFactory:
    _chunkers = {
        "table": TableChunker(),
        "word": WordChunker(),
        "markdown": MarkdownChunker(),
        "text": TextChunker(),
        "pdf": PDFChunker(),
    }

    @classmethod
    def get_chunker(cls, doc_type: str) -> DocumentChunker:
        chunker = cls._chunkers.get(doc_type)
        if chunker is None:
            chunker = cls._chunkers["text"]
        return chunker

    @classmethod
    def chunk_document(cls, file_path: str, parsed_content: str) -> List[Dict[str, Any]]:
        file_extension = os.path.splitext(file_path)[1]
        logger.info(f"Starting to chunk document with extension: {file_extension}")

        if file_extension == ".docx":
            logger.debug("Using Word chunker for .docx file")
            word_chunker = cls.get_chunker("word")
            chunks = word_chunker.chunk(file_path, parsed_content)
        elif file_extension == ".md":
            logger.debug("Using Markdown chunker for .md file")
            markdown_chunker = cls.get_chunker("markdown")
            chunks = markdown_chunker.chunk(file_path, parsed_content)
        elif file_extension == ".txt":
            logger.debug("Using TextFile chunker for .txt file")
            text_chunker = cls.get_chunker("text")
            chunks = text_chunker.chunk(file_path, parsed_content)
        elif file_extension == ".pdf":
            logger.debug("Using PDF chunker for .pdf file")
            pdf_chunker = cls.get_chunker("pdf")
            chunks = pdf_chunker.chunk(file_path, parsed_content)
        elif file_extension == ".xlsx":
            logger.debug("Using Table chunker for .xlsx file")
            table_chunker = cls.get_chunker("table")
            chunks = table_chunker.chunk(file_path, parsed_content)
        else:
            logger.debug(f"Using default chunker for file type: {file_extension}")
            text_chunker = cls.get_chunker("text")
            chunks = text_chunker.chunk(file_path, parsed_content)

        logger.info(f"Document chunking completed. Total chunks created: {len(chunks)}")
        return chunks
