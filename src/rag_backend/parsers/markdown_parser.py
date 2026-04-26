# -*- coding: utf-8 -*-

from pathlib import Path
from .base import DocumentParser

class MarkdownParser(DocumentParser):
    def is_supported(self, file_path: str) -> bool:
        return Path(file_path).suffix.lower() == ".md"

    def parse(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        return md_content