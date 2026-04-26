# -*- coding: utf-8 -*-

from typing import List, Dict, Any
from .base import DocumentChunker

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