# RAG Backend Project

This is a RAG (Retrieval-Augmented Generation) backend project that provides document parsing, chunking, and vector storage capabilities for intelligent question-answering.

## Features

- **Multi-format document parsing**: Supports .docx, .pdf, .md, .txt, .xlsx files
- **Intelligent document chunking**: Different chunking strategies for different document types
- **Vector store integration**: Supports both FAISS and Chroma for efficient similarity search
- **RESTful API**: Provides endpoints for document upload, vectorization, and question answering
- **Configurable settings**: All settings are stored in config.yaml
- **Modular architecture**: Clean, organized code structure with separated components

## Project Structure

```
rag_backend/
©À©¤©¤ config.yaml                # Configuration file
©À©¤©¤ main.py                    # FastAPI application
©À©¤©¤ src/
©¦   ©À©¤©¤ api/                   # API endpoints (separated by function)
©¦   ©¦   ©À©¤©¤ __init__.py
©¦   ©¦   ©À©¤©¤ ask_question.py
©¦   ©¦   ©À©¤©¤ embed_document.py
©¦   ©¦   ©À©¤©¤ get_files.py
©¦   ©¦   ©¸©¤©¤ upload_document.py
©¦   ©À©¤©¤ rag_backend/
©¦   ©¦   ©À©¤©¤ chunkers/          # Document chunkers (separated by file type)
©¦   ©¦   ©¦   ©À©¤©¤ __init__.py
©¦   ©¦   ©¦   ©À©¤©¤ base.py
©¦   ©¦   ©¦   ©À©¤©¤ factory.py
©¦   ©¦   ©¦   ©À©¤©¤ markdown_chunker.py
©¦   ©¦   ©¦   ©À©¤©¤ pdf_chunker.py
©¦   ©¦   ©¦   ©À©¤©¤ table_chunker.py
©¦   ©¦   ©¦   ©À©¤©¤ text_chunker.py
©¦   ©¦   ©¦   ©¸©¤©¤ word_chunker.py
©¦   ©¦   ©À©¤©¤ config/            # Configuration management
©¦   ©¦   ©¦   ©À©¤©¤ __init__.py
©¦   ©¦   ©¦   ©¸©¤©¤ settings.py
©¦   ©¦   ©À©¤©¤ embeding/          # Embedding models
©¦   ©¦   ©¦   ©¸©¤©¤ factory.py
©¦   ©¦   ©À©¤©¤ parsers/           # Document parsers (separated by file type)
©¦   ©¦   ©¦   ©À©¤©¤ __init__.py
©¦   ©¦   ©¦   ©À©¤©¤ base.py
©¦   ©¦   ©¦   ©À©¤©¤ excel_parser.py
©¦   ©¦   ©¦   ©À©¤©¤ factory.py
©¦   ©¦   ©¦   ©À©¤©¤ markdown_parser.py
©¦   ©¦   ©¦   ©À©¤©¤ pdf_parser.py
©¦   ©¦   ©¦   ©À©¤©¤ text_parser.py
©¦   ©¦   ©¦   ©¸©¤©¤ word_parser.py
©¦   ©¦   ©À©¤©¤ util/              # Utility functions
©¦   ©¦   ©¦   ©À©¤©¤ __init__.py
©¦   ©¦   ©¦   ©À©¤©¤ api_helper.py
©¦   ©¦   ©¦   ©À©¤©¤ file_helper.py
©¦   ©¦   ©¦   ©À©¤©¤ file_status_helper.py
©¦   ©¦   ©¦   ©¸©¤©¤ vector_helper.py
©¦   ©¦   ©À©¤©¤ vector_store/      # Vector storage implementations
©¦   ©¦   ©¦   ©À©¤©¤ base.py
©¦   ©¦   ©¦   ©À©¤©¤ chroma.py
©¦   ©¦   ©¦   ©À©¤©¤ factory.py
©¦   ©¦   ©¦   ©¸©¤©¤ faiss.py
©¦   ©¦   ©¸©¤©¤ __init__.py
```

## Installation

### Prerequisites
- Python 3.11+
- uv package manager (recommended) or pip

### Steps
1. Clone the repository
2. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Using pip
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   # Using uv
   uv run python main.py
   
   # Using pip (with virtual environment activated)
   python main.py
   ```
   
   For production use, you can use uvicorn:
   ```bash
   # Development mode
   uv run uvicorn main:app --port 3001 --reload
   
   # Production mode
   uv run uvicorn main:app --workers 4 --port 3001
   ```

### Optional: Activate the virtual environment
If you need to run multiple commands in the virtual environment, you can activate it:

```bash
# For Windows
uv venv activate

# For macOS/Linux
source .venv/bin/activate
```

## Configuration

Update `config.yaml` to customize settings:

- `document_chunker.chunk_settings`: Chunk size and overlap for each file type
- `docs_paths`: Directories to scan for documents
- `vector_store_path`: Path to save vector store
- `max_batch_size`: Batch size for vectorization
- `chat_model`: LLM model for text generation
- `embedding_model`: Embedding model for vectorization
- `embeddings_provider`: Embedding provider (e.g., "ollama")
- `vector_store_type`: Vector store type ("chroma" or "faiss")

## API Endpoints

### POST /upload_document
Upload a document to the server.

**Request:**
- `file`: File to upload (multipart/form-data)

**Response:**
```json
{
  "message": "File 'example.docx' uploaded successfully.",
  "file_path": "uploaded_docs/example.docx"
}
```

### GET /files
Get all files from file-status.json.

**Response:**
```json
[
  {
    "name": "example.docx",
    "path": "uploaded_docs/example.docx",
    "embeded": "not_started"
  },
  {
    "name": "test.pdf",
    "path": "uploaded_docs/test.pdf",
    "embeded": "completed"
  }
]
```

### POST /embed_document
Vectorize a document that has been uploaded but not yet vectorized.

**Request:**
- `file_path`: Relative path to the file (multipart/form-data)

**Response:**
```json
{
  "message": "Document 'uploaded_docs/example.docx' vectorized successfully.",
  "file_path": "uploaded_docs/example.docx"
}
```

### POST /ask
Ask a question based on the knowledge base.

**Request:**
```json
{
  "query": "What is the project about?"
}
```

**Response:**
```json
{
  "answer": "This is a RAG backend project that provides document parsing, chunking, and vector storage capabilities for intelligent question-answering."
}
```

## Usage Examples

### Uploading a Document

#### Linux/macOS (curl)
```bash
curl -X POST "http://localhost:3001/upload_document" \
  -F "file=@example.docx"
```

#### Windows (PowerShell)
```powershell
# Method 1: Using Invoke-WebRequest with manual multipart (PowerShell 5.x compatible)
$filePath = "example.docx"
$uri = "http://localhost:3001/upload_document"

Add-Type -AssemblyName System.Net.Http
$httpClient = New-Object System.Net.Http.HttpClient
$streamProvider = New-Object System.Net.Http.MultipartFormDataContent

$fileStream = [System.IO.File]::OpenRead($filePath)
$fileName = [System.IO.Path]::GetFileName($filePath)
$fileContent = New-Object System.Net.Http.StreamContent($fileStream)
$streamProvider.Add($fileContent, "file", $fileName)

$response = $httpClient.PostAsync($uri, $streamProvider).Result
$response.Content.ReadAsStringAsync().Result

# Method 2: Using curl.exe (if installed)
curl.exe -X POST "http://localhost:3001/upload_document" `
  -F "file=@example.docx"
```

### Getting All Files

#### Linux/macOS (curl)
```bash
curl -X GET "http://localhost:3001/files"
```

#### Windows (PowerShell)
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:3001/files" `
  -Method Get
$response

# Or using curl.exe (if installed)
curl.exe -X GET "http://localhost:3001/files"
```

### Vectorizing a Document

#### Linux/macOS (curl)
```bash
curl -X POST "http://localhost:3001/embed_document" \
  -F "file_path=uploaded_docs/example.docx"
```

#### Windows (PowerShell)
```powershell
# Using Invoke-WebRequest
$response = Invoke-WebRequest -Uri "http://localhost:3001/embed_document" `
  -Method Post `
  -Form @{
    file_path = "uploaded_docs/example.docx"
  }
$response

# Or using curl.exe (if installed)
curl.exe -X POST "http://localhost:3001/embed_document" `
  -F "file_path=uploaded_docs/example.docx"
```

### Asking a Question

#### Linux/macOS (curl)
```bash
curl -X POST "http://localhost:3001/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the key features?"}'
```

#### Windows (PowerShell)
```powershell
$body = @{
  query = "What are the key features?"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/ask" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

$response

# Or using curl.exe (if installed)
curl.exe -X POST "http://localhost:3001/ask" `
  -H "Content-Type: application/json" `
  -d '{"query": "What are the key features?"}'
```

## Supported File Types

- **Word (.docx)**: Parses headings and paragraphs
- **PDF (.pdf)**: Extracts text from pages
- **Markdown (.md)**: Parses headings and content
- **Text (.txt)**: Splits by paragraphs
- **Excel (.xlsx)**: Extracts sheets and rows
- **Archive files**: Supports .zip, .gz, .tar, .tar.gz, .tgz, .tar.bz2, .tar.xz

## Chunking Strategies

| File Type | Chunk Strategy | Default Chunk Size | Default Overlap |
|-----------|----------------|-------------------|----------------|
| .docx     | By sections    | 250               | 50             |
| .pdf      | By chapters    | 200               | 50             |
| .md       | By content     | 200               | 50             |
| .txt      | By content     | 150               | 50             |
| .xlsx     | By rows        | 200               | 50             |

## Vector Store Options

The project supports two vector store implementations:

1. **FAISS**: Fast, lightweight vector store suitable for smaller datasets
2. **Chroma**: Feature-rich vector store with more advanced capabilities

## License

MIT