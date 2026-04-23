# -*- coding: gbk -*-

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from rag_backend.util import logger
import re
import os
import uuid
from rag_backend.config.settings import settings
from langchain_core.documents import Document


class DocumentChunker(ABC):

    @abstractmethod
    def chunk(self, file_path: str, parsed_content: str) -> List[Dict[str, Any]]:
        pass

    def get_settings(self, ext: str) -> Dict[str, Any]:
        return settings.get_chunk_config(ext)
    
    def _split_long_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """split long text by chunk_size"""
        text = text.strip()
        if not text:
            return []
        sentences = re.split(r'[\n\r]+', text)
        logger.info(f"sentences: {sentences}")
        sentences_length = len(sentences)
        max_chunk_size = chunk_size + overlap
        chunks = []
        start_index, index = 0, 1
        while index < sentences_length:
            tmp = "\n".join(sentences[start_index:index])
            if len(tmp) > max_chunk_size:
                index -= 1
                chunks.append(tmp)
                start_index = index
                index += 1
            else:
                index += 1

        if index < sentences_length:
            chunks.append("\n".join(sentences[start_index:]))
        
        logger.info(f"chunks: {chunks}")
        return chunks

    def _split_by_chapters(self, text: str) -> List[tuple]:
        """split by contents"""
        import re
        # ƥ���½ڷ��ţ���1.1��2.4��10.8
        chapter_pattern = r'^\s*(\d+\.\d+)(\s|$)'
        lines = text.split('\n')
        chunks = []
        current_title = ""
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            match = re.match(chapter_pattern, line)
            if match:
                # �ҵ����½�
                if current_text:
                    # ���浱ǰ�½�
                    chunks.append((current_title, '\n'.join(current_text)))
                    current_text = []
                # ���½�
                current_title = match.group(1)
                # ���½ڱ���Ҳ�����ı�
                current_text.append(line)
            else:
                # ��ͨ�ı�
                current_text.append(line)
        
        # �������һ���½�
        if current_text:
            chunks.append((current_title, '\n'.join(current_text)))
        return chunks


class WordChunker(DocumentChunker):
    def chunk(self, file_path: str, parsed_content: str) -> List[Dict[str, Any]]:
        chunk_settings = self.get_settings(".docx")
        chunk_size = chunk_settings.get("chunk_size", 500)
        overlap = chunk_settings.get("overlap", 50)

        chunks = []
        if parsed_content.strip():
            if len(parsed_content) > chunk_size:
                text_chunks = self._split_long_text(parsed_content, chunk_size, overlap)
                for chunk_text in text_chunks:
                    chunks.append({
                        "text": chunk_text,
                        "chunk_index": len(chunks),
                        "source": file_path,
                        "original_type": "document"
                    })
            else:
                chunks.append({
                    "text": parsed_content,
                    "chunk_index": len(chunks),
                    "source": file_path,
                    "original_type": "document"
                })
        return chunks


class MarkdownChunker(DocumentChunker):
    def chunk(self, file_path: str, parsed_content: str) -> List[Dict[str, Any]]:
        chunk_settings = self.get_settings(".md")
        chunk_size = chunk_settings.get("chunk_size", 500)
        overlap = chunk_settings.get("overlap", 50)

        chunks = []
        if parsed_content.strip():
            if len(parsed_content) > chunk_size:
                text_chunks = self._split_long_text(parsed_content, chunk_size, overlap)
                for chunk_text in text_chunks:
                    chunks.append({
                        "text": chunk_text,
                        "chunk_index": len(chunks),
                        "source": file_path,
                        "original_type": "markdown"
                    })
            else:
                chunks.append({
                    "text": parsed_content,
                    "chunk_index": len(chunks),
                    "source": file_path,
                    "original_type": "markdown"
                })
        return chunks


class TextChunker(DocumentChunker):
    def chunk(self, file_path: str, parsed_content: str) -> List[Dict[str, Any]]:
        chunk_settings = self.get_settings(".txt")
        chunk_size = chunk_settings.get("chunk_size", 500)
        overlap = chunk_settings.get("overlap", 50)

        chunks = []
        if parsed_content.strip():
            if len(parsed_content) > chunk_size:
                text_chunks = self._split_long_text(parsed_content, chunk_size, overlap)
                for chunk_text in text_chunks:
                    chunks.append({
                        "text": chunk_text,
                        "chunk_index": len(chunks),
                        "source": file_path,
                        "original_type": "text"
                    })
            else:
                chunks.append({
                    "text": parsed_content,
                    "chunk_index": len(chunks),
                    "source": file_path,
                    "original_type": "text"
                })
        return chunks


class TableChunker(DocumentChunker):
    def chunk(self, file_path: str, parsed_content: str) -> List[Dict[str, Any]]:
        chunk_settings = self.get_settings(".xlsx")
        chunk_size = chunk_settings.get("chunk_size", 500)
        overlap = chunk_settings.get("overlap", 50)

        chunks = []
        if parsed_content.strip():
            if len(parsed_content) > chunk_size:
                text_chunks = self._split_long_text(parsed_content, chunk_size, overlap)
                for chunk_text in text_chunks:
                    chunks.append({
                        "text": chunk_text,
                        "chunk_index": len(chunks),
                        "source": file_path,
                        "original_type": "table"
                    })
            else:
                chunks.append({
                    "text": parsed_content,
                    "chunk_index": len(chunks),
                    "source": file_path,
                    "original_type": "table"
                })
        return chunks


class PDFChunker(DocumentChunker):
    def chunk(self, file_path: str, parsed_content: str) -> List[Dict[str, Any]]:
        chunk_settings = self.get_settings(".pdf")
        chunk_size = chunk_settings.get("chunk_size", 500)
        overlap = chunk_settings.get("overlap", 50)

        parsed_content = parsed_content.strip()
        if not parsed_content:
            return []
        
        chunks = []
        paragraphs = self._split_by_chapters(parsed_content)
        logger.info(f"Split into {len(paragraphs)} chapters")
        for title, content in paragraphs:
            if len(content) > chunk_size + overlap:
                text_chunks = self._split_long_text(content, chunk_size, overlap)
                logger.info(f"text_chunks: {text_chunks}")
                for chunk_text in text_chunks:

                    chunks.append(Document(
                    page_content=chunk_text,
                    metadata={
                        "chunk_index": len(chunks),
                        "source": file_path,
                        "original_type": "pdf",
                        "title": title if title else " - ",
                        "id": str(uuid.uuid4()),
                        'chunk_size': chunk_size,
                        'overlap': overlap
                    }
                ))
            else:
                logger.info(f"chunk_text2: {content}")
                chunks.append(Document(
                    page_content=content,
                    metadata={
                        "chunk_index": len(chunks),
                        "source": file_path,
                        "original_type": "pdf",
                        "title": title if title else " - ",
                        "id": str(uuid.uuid4()),
                        'chunk_size': chunk_size,
                        'overlap': overlap
                    }
                ))
        return chunks


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

        # �����ļ�����ѡ��ͬ����Ƭ����
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
