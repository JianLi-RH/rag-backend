# -*- coding: gbk -*-

import yaml
from pathlib import Path
from typing import Dict, Any


class Settings:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent.parent / "config.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"Config file not found: {config_path}")

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    @property
    def upload_dir(self) -> str:
        return self.get("upload_dir", "./uploaded_docs")

    @property
    def chunk_dir(self) -> str:
        return self.get("chunk_dir", "./chunks")

    @property
    def vector_store_path(self) -> str:
        return self.get("vector_store_path", "./vector_store_db")
    
    def get_chunk_config(self, file_extension: str) -> Dict[str, int]:
        return self.chunk_settings.get(file_extension, {"chunk_size": 1000, "overlap": 200})

    @property
    def parser_supported_types(self) -> list:
        return self.get("document_parser.supported_types", [])

    @property
    def chunk_settings(self) -> Dict[str, Dict[str, int]]:
        return self.get("document_chunker.chunk_settings", {})

    @property
    def chat_model(self) -> str:
        return self.get("chat_model", "qwen3:8b")

    @property
    def embeddings_provider(self) -> str:
        return self.get("embeddings_provider", "ollama")

    @property
    def embedding_model(self) -> str:
        return self.get("embedding_model", "nomic-embed-text-v2-moe:latest")

    @property
    def docs_paths(self) -> list:
        return self.get("docs_paths", ["./docs"])

    @property
    def max_batch_size(self) -> int:
        return self.get("max_batch_size", 50)

    @property
    def vector_store_type(self) -> str:
        return self.get("vector_store_type", "faiss")
    
settings = Settings()
