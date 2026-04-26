# -*- coding: utf-8 -*-

from pathlib import Path
from .base import DocumentParser

class TextParser(DocumentParser):
    def is_supported(self, file_path: str) -> bool:
        return Path(file_path).suffix.lower() == ".txt"

    def parse(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text