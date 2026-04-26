# -*- coding: utf-8 -*-

from fastapi import HTTPException
from rag_backend.util import logger, file_status_manager

def get_files():
    """Get all files from file-status.json."""
    try:
        files = file_status_manager.get_all_files()
        logger.info(f"There are {len(files)} files in file-status.json")
        return files
    except Exception as e:
        logger.error(f"Failed to get files: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get files: {e}")