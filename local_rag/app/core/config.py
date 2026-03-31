import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Local RAG Platform"
    APP_ENV: str = "development"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_CHAT_MODEL: str = "llama3"
    
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    LANCEDB_PATH: str = "./data/lancedb"
    
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
