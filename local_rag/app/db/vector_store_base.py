from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStoreBase(ABC):
    @abstractmethod
    def initialize(self):
        """Initialize the vector store connection."""
        pass
        
    @abstractmethod
    def upsert_chunks(self, chunks: List[Dict[str, Any]]):
        """Insert or update chunks with embeddings."""
        pass
        
    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for similar chunks."""
        pass
        
    @abstractmethod
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all unique documents in the store."""
        pass
        
    @abstractmethod
    def health_check(self) -> bool:
        """Check if vector store is healthy."""
        pass
