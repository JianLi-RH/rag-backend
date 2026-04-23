# RAG Backend Project

This is a RAG (Retrieval-Augmented Generation) backend project that provides document parsing, chunking, and vector storage capabilities for intelligent question-answering.

## Features

- **Multi-format document parsing**: Supports .docx, .pdf, .md, .txt, .xlsx files
- **Intelligent document chunking**: Different chunking strategies for different document types
  - Word: Chunk by sections (headings)
  - Markdown: Chunk by headings
  - Text: Chunk by paragraphs
- **Vector store integration**: Uses FAISS for efficient similarity search
- **RESTful API**: Provides endpoints for document upload and question answering
- **Configurable settings**: All settings are stored in config.yaml

## Project Structure

```
rag_backend/
?????? config.yaml                # Configuration file
?????? pyproject.toml             # Project configuration
?????? main.py                    # FastAPI application
?????? src/rag_backend/
??   ?????? parsers/               # Document parsers
??   ??   ?????? factory.py         # Parser factory
??   ?????? chunkers/              # Document chunkers
??   ??   ?????? factory.py         # Chunker factory
??   ?????? config/                # Configuration management
??       ?????? settings.py        # Settings loader
```

## Installation

### Prerequisites
- Python 3.11+
- uv package manager

### Steps
1. Clone the repository
2. Install dependencies (this will automatically create and set up the virtual environment):
   ```bash
   uv sync
   ```
3. Run the application (uv will automatically use the virtual environment):
   ```bash
   uv run python main.py
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

- `document_parser.supported_types`: List of supported file extensions
- `document_chunker.chunk_settings`: Chunk size and overlap for each file type
- `ollama_model`: Ollama model for text generation
- `embedding_model`: Embedding model for vectorization
- `docs_paths`: Directories to scan for documents
- `vector_store_path`: Path to save vector store

## API Endpoints

### POST /upload_document
Upload a document and add it to the vector store.

**Request:**
- `file`: File to upload (multipart/form-data)
- `target_directory`: Directory to save the file (default: "./uploaded_docs")

**Response:**
```json
{
  "message": "File 'example.docx' uploaded and processed successfully.",
  "file_path": "./uploaded_docs/example.docx"
}
```

}

### GET /files
Get all files from file-status.json.

**Response:**
```json
[
  {
    "name": "example.docx",
    "path": "uploaded_docs/example.docx",
    "embedded": false
  },
  {
    "name": "test.pdf",
    "path": "uploaded_docs/test.pdf",
    "embedded": true
  }
]
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

### POST /embed_document
Vectorize a document that has been uploaded but not yet vectorized.

**Request:**
- `file_path`: Relative path to the file (multipart/form-data)

**Response:**
```json
{
  "message": "Document './uploaded_docs/example.docx' vectorized successfully.",
  "file_path": "./uploaded_docs/example.docx"
}
```

## Usage Examples

### Uploading a Document

#### Linux/macOS (curl)
```bash
curl -X POST "http://localhost:3001/upload_document" \
  -F "file=@example.docx" \
  -F "target_directory=./uploaded_docs"
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

$directoryContent = New-Object System.Net.Http.StringContent("./uploaded_docs")
$streamProvider.Add($directoryContent, "target_directory")

$response = $httpClient.PostAsync($uri, $streamProvider).Result
$response.Content.ReadAsStringAsync().Result

# Method 2: Using curl.exe (if installed)
curl.exe -X POST "http://localhost:3001/upload_document" `
  -F "file=@example.docx" `
  -F "target_directory=./uploaded_docs"
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

### Vectorizing a Document

#### Linux/macOS (curl)
```bash
curl -X POST "http://localhost:3001/embed_document" \
  -F "file_path=./uploaded_docs/example.docx"
```

#### Windows (PowerShell)
```powershell
# Using Invoke-WebRequest
$response = Invoke-WebRequest -Uri "http://localhost:3001/embed_document" `
  -Method Post `
  -Form @{
    file_path = "./uploaded_docs/example.docx"
  }
$response

# Or using curl.exe (if installed)
curl.exe -X POST "http://localhost:3001/embed_document" `
  -F "file_path=./uploaded_docs/example.docx"
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
| .docx     | By sections    | 1000              | 200            |
| .pdf      | By pages       | 1200              | 300            |
| .md       | By headings    | 800               | 150            |
| .txt      | By paragraphs  | 1000              | 200            |
| .xlsx     | By rows        | 500               | 100            |

## License

MIT
