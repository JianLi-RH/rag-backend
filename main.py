from rag_backend.vector_store.factory import VectorStoreFactory
import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import uvicorn
from rag_backend.util import file_status_manager
from rag_backend.util.api_helper import (
    save_uploaded_file,
    process_uploaded_file,
    get_rag_chain
)
from fastapi.middleware.cors import CORSMiddleware

from logger import logger

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload_document")
async def upload_document(
    file: UploadFile = File(...),
    target_directory: str = Form("./uploaded_docs"),
):
    """Uploads a document, saves it to a specified directory, and updates file-status.json."""
    try:
        logger.info(f"Target directory received: {target_directory}")

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


@app.get("/files")
def get_files():
    """Get all files from file-status.json."""
    try:
        files = file_status_manager.get_all_files()
        logger.info(f"There are {len(files)} files in file-status.json")
        return files
    except Exception as e:
        logger.error(f"Failed to get files: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get files: {e}")


@app.post("/embed_document")
async def embed_document(
    file_path: str = Form(...)
):
    """Embeds a document that has been uploaded but not yet vectorized."""
    from rag_backend.util.vector_helper import embed_document_svc
    from enums import EmbedStatus

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

class AskRequest(BaseModel):
    query: str


@app.post("/ask")
def ask_question(request: AskRequest):
    """Answers a question based on the knowledge base."""
    vector_store = VectorStoreFactory.create(collection_name="default")
    logger.info("Vector store loaded from disk.")
    if vector_store is None:
        raise HTTPException(status_code=500, detail="No documents found in the knowledge base. Please upload some documents first.")

    rag_chain = get_rag_chain(vector_store)
    try:
        logger.info(f"Received question: {request.query}")
        answer = rag_chain.invoke(request.query)
        logger.info(f"Answer: {answer}")
        return {"answer": answer}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to answer question: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001, timeout_keep_alive=900)
