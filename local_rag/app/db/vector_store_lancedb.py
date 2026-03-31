import lancedb
import os
import pyarrow as pa
from typing import List, Dict, Any
from .vector_store_base import VectorStoreBase
from app.core.config import settings
from app.core.logging import logger

class LanceDBStore(VectorStoreBase):
    def __init__(self):
        self.uri = settings.LANCEDB_PATH
        self.table_name = "document_chunks"
        self.db = None
        self.table = None

    def initialize(self):
        os.makedirs(os.path.dirname(self.uri), exist_ok=True)
        self.db = lancedb.connect(self.uri)
        
        if self.table_name in self.db.table_names():
            self.table = self.db.open_table(self.table_name)
            logger.info(f"Opened existing LanceDB table: {self.table_name}")
        else:
            logger.info("LanceDB table will be created on first upsert.")

    def upsert_chunks(self, chunks: List[Dict[str, Any]]):
        if not chunks:
            return
            
        data = []
        for c in chunks:
            row = {
                "id": c["id"],
                "vector": c["embedding"],
                "text": c["text"],
                "document_id": c["metadata"]["document_id"],
                "source_file": c["metadata"]["source_file"],
                "chunk_index": c["metadata"]["chunk_index"],
                "tenant_id": c["metadata"].get("tenant_id"),
                "workspace_id": c["metadata"].get("workspace_id")
            }
            data.append(row)
            
        if self.table is None:
            self.table = self.db.create_table(self.table_name, data=data)
            logger.info(f"Created table {self.table_name} and inserted {len(data)} rows.")
        else:
            self.table.add(data)
            logger.info(f"Inserted {len(data)} rows into {self.table_name}.")

    def search(self, query_embedding: List[float], top_k: int, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if self.table is None:
            return []
            
        query = self.table.search(query_embedding).limit(top_k)
        
        if filters:
            filter_strs = []
            for k, v in filters.items():
                if v is not None:
                    filter_strs.append(f"{k} = '{v}'")
            if filter_strs:
                query = query.where(" AND ".join(filter_strs))
                
        results = query.to_list()
        
        mapped_results = []
        for r in results:
            mapped_results.append({
                "id": r["id"],
                "text": r["text"],
                "score": r.get("_distance", 0.0),
                "metadata": {
                    "document_id": r["document_id"],
                    "source_file": r["source_file"],
                    "chunk_index": r["chunk_index"],
                    "tenant_id": r.get("tenant_id"),
                    "workspace_id": r.get("workspace_id")
                }
            })
        return mapped_results

    def list_documents(self) -> List[Dict[str, Any]]:
        if self.table is None:
            return []
        
        df = self.table.to_pandas()
        unique_docs = df[['document_id', 'source_file']].drop_duplicates()
        return unique_docs.to_dict('records')

    def health_check(self) -> bool:
        try:
            if self.db is None:
                self.initialize()
            return True
        except Exception as e:
            logger.error(f"LanceDB health check failed: {e}")
            return False
