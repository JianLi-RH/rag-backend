# -*- coding: gbk -*-
import os
import shutil
import logging
from fastapi import HTTPException
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from rag_backend.config.settings import settings
from rag_backend.util.file_status_helper import FileStatusManager
from rag_backend.util.file_helper import extract_archive, is_archive_file

from logger import logger


file_status_manager = FileStatusManager()
llm = ChatOllama(model=settings.chat_model)
vector_store = None
rag_chain = None


def save_uploaded_file(file_obj, target_directory: str):
    """Save uploaded file to target directory."""
    os.makedirs(target_directory, exist_ok=True)
    file_path = os.path.join(target_directory, file_obj.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_obj.file, buffer)
    return file_path

def process_uploaded_file(file_obj, file_path: str, target_directory: str):
    """Process uploaded file, handle archive extraction if needed."""
    extracted_files_relative = []
    is_archive = is_archive_file(file_path)

    if is_archive:
        logger.info(f"Detected archive file: {file_obj.filename}")
        return process_archive_file(file_obj, file_path, target_directory)
    else:
        logger.info(f"Processing non-archive file: {file_obj.filename}")
        rel_path = file_status_manager.get_relative_path(file_path)
        file_status_manager.add_file(file_obj.filename, rel_path, embeded=False)
        return is_archive, extracted_files_relative, rel_path

def process_archive_file(file_obj, file_path: str, target_directory: str):
    """Process archive file, extract and return extracted files."""
    extracted_files_relative = []
    archive_name = os.path.splitext(file_obj.filename)[0]
    extracted_directory = os.path.join(target_directory, archive_name)

    if os.path.exists(extracted_directory):
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"A folder with the name '{archive_name}' already exists. This archive may have been uploaded before.")

    os.makedirs(extracted_directory, exist_ok=True)
    logger.info(f"Created directory: {extracted_directory}")

    extracted_files = extract_archive(file_path, extracted_directory)
    logger.info(f"Extracted {len(extracted_files)} files from archive")

    for ext_file in extracted_files:
        rel_path = file_status_manager.get_relative_path(ext_file)
        extracted_files_relative.append(rel_path)
        file_name = os.path.basename(ext_file)
        file_status_manager.add_file(file_name, rel_path, embeded=False)

    os.remove(file_path)
    logger.info(f"Deleted archive file: {file_path}")

    return True, extracted_files_relative, None

def get_rag_chain(vector_store_instance):
    """Get or create RAG chain."""
    global rag_chain

    if rag_chain is None:
        try:
            retriever = vector_store_instance.as_retriever()
        except Exception as e:
            logger.error(f"Failed to create retriever: {e}")
            raise
        rag_chain = (
            {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    return rag_chain

def format_docs(docs):
    """Format documents for RAG chain."""
    return "\n\n".join(doc.page_content for doc in docs)

template = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
The answer should be in Chinese and contains title, source, chunk_index.
If you don't know the answer, just say that you don't know.
Question: {question}
Context: {context}
Answer:"""

# Use three sentences maximum and keep the answer concise.

prompt = ChatPromptTemplate.from_template(template)
