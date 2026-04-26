# -*- coding: utf-8 -*-

import os
from fastapi import HTTPException, Form
from rag_backend.util import file_status_manager
from rag_backend.util.vector_helper import embed_document_svc
from enums import EmbedStatus

async def embed_document(
    file_path: str = Form(...)
):
    """Embeds a document that has been uploaded but not yet vectorized."""

    file_status_obj = file_status_manager.get_file_status(file_path)
    if not file_status_obj:
        abs_path = file_status_manager.get_absolute_path(file_path)
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        file_name = os.path.basename(abs_path)
        file_status_obj = file_status_manager.add_file(file_name, file_path, embeded=EmbedStatus.not_started.name)

    if file_status_obj.get('embeded') == EmbedStatus.completed.name:
        raise HTTPException(status_code=400, detail=f"File already vectorized: {file_path}")

    res = await embed_document_svc(file_status_obj)

    if not res:
        raise HTTPException(status_code=400, detail=f"Failed to vectorize document: {file_path}")

    return {
        "message": f"Document '{file_path}' vectorized successfully.",
        "file_path": file_path
    }