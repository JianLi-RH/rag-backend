# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class DocumentParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> str:
        pass

    @abstractmethod
    def is_supported(self, file_path: str) -> bool:
        pass