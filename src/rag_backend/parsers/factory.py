# -*- coding: utf-8 -*-

# parser factory class
# create a parser instance based on .env config
# parser will get plain text content from the file
# parser will return the plain text content as a string
# parser will handle different file types

from pathlib import Path

from .base import DocumentParser
from .word_parser import WordParser
from .pdf_parser import PDFParser
from .markdown_parser import MarkdownParser
from .text_parser import TextParser
from .excel_parser import ExcelParser

class DocumentParserFactory:
    _parsers = {
        ".docx": WordParser,
        ".pdf": PDFParser,
        ".md": MarkdownParser,
        ".txt": TextParser,
        ".xlsx": ExcelParser,
    }

    @classmethod
    def get_parser(cls, file_path: str) -> DocumentParser:
        ext = Path(file_path).suffix.lower()
        parser_class = cls._parsers.get(ext)
        if parser_class is None:
            raise ValueError(f"Unsupported file type: {ext}")
        return parser_class()

    @classmethod
    def get_supported_extensions(cls) -> list:
        return list(cls._parsers.keys())

    @classmethod
    def is_supported(cls, file_path: str) -> bool:
        ext = Path(file_path).suffix.lower()
        return ext in cls._parsers


if __name__ == "__main__":
    abs_path = r"D:\code\AI\rag_backend\uploaded_docs\python-3.13-docs-pdf-a4\docs-pdf\library.pdf"
    import datetime
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    parser = DocumentParserFactory.get_parser(abs_path)
    parsed_content = parser.parse(abs_path)
    print(parsed_content[:10])
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
