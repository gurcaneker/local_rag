# Local RAG Platform

A clean, modular, and extensible Retrieval-Augmented Generation (RAG) platform designed to run locally, with an architecture ready for production scaling.

## Architecture

The project follows a standard multi-layer pattern:
- **API Layer**: FastAPI routes.
- **Service Layer**: Ingestion, Retrieval, LLM generation, Document Processing.
- **Persistence Layer**: Abstract Vector Store interface (currently LanceDB).
- **Core Layer**: Config, logging, models.

## Prerequisites
- Python 3.11+
- Ollama installed locally (`ollama serve` and `ollama pull llama3`)

## Setup

1. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Configuration**:
   Copy `.env.example` to `.env` and adjust the variables.

## Running

1. **Start Ollama** backend in a separate terminal:
   ```bash
   ollama serve
   ```

2. **Start FastAPI**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage Example

### Ingesting Data
```bash
python scripts/ingest_sample.py my_document.pdf
```
Or via curl:
```bash
curl -X POST -F "file=@my_document.pdf" http://localhost:8000/documents/upload
```

### Chatting
```bash
curl -X POST http://localhost:8000/chat/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the main topic of the document?"}'
```

## Roadmap

This platform is structured to allow easy extensions:
- [ ] Multi-User / Workspace support (schema fields already exist)
- [ ] Hybrid Retrieval (Dense + Sparse)
- [ ] Reranker Service pipeline
- [ ] Vector Store swap to Qdrant based on `VectorStoreBase`
- [ ] Async chunking and ingestion workers
