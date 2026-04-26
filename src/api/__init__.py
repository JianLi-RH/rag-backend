# -*- coding: utf-8 -*-

from .upload_document import upload_document
from .get_files import get_files
from .embed_document import embed_document
from .ask_question import ask_question, AskRequest

__all__ = [
    'upload_document',
    'get_files',
    'embed_document',
    'ask_question',
    'AskRequest'
]

__version__ = "1.0.0"