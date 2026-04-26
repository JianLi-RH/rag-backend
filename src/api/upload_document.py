# -*- coding: utf-8 -*-

import os

from fastapi import HTTPException, UploadFile, File, Form

from rag_backend.util import logger
from rag_backend.util.api_helper import save_uploaded_file, process_uploaded_file
from rag_backend.config.settings import settings

async def upload_document(
    file: UploadFile = File(...),
):
    """Uploads a document, saves it to a specified directory, and updates file-status.json."""
    try:
        logger.info(f"Target directory received: {settings.upload_dir}")
        target_directory = settings.upload_dir
        os.makedirs(target_directory, exist_ok=True)
        
        file_path = save_uploaded_file(file, target_directory)
        logger.info(f"Attempting to save file to: {file_path}")

        is_archive, extracted_files_relative, rel_path = process_uploaded_file(file, file_path, target_directory)

        if is_archive:
            return {
                "message": f"Archive '{file.filename}' uploaded successfully.",
                "extracted_files": extracted_files_relative,
                "processed_files": len(extracted_files_relative)
            }
        else:
            return {
                "message": f"File '{file.filename}' uploaded successfully.",
                "file_path": rel_path
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {e}")