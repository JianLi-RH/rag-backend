# -*- coding: utf-8 -*-

from pathlib import Path
import pdfplumber
from .base import DocumentParser

class PDFParser(DocumentParser):
    def is_supported(self, file_path: str) -> bool:
        return Path(file_path).suffix.lower() == ".pdf"

    def parse(self, file_path: str) -> str:
        with pdfplumber.open(file_path) as pdf:
            # 丢失页码信息，但是我感觉数据更准确，因为文字内容不会被截断
            page_texts = [page.extract_text() or "" for page in pdf.pages]
            all_text = " ".join(page_texts)
            return all_text