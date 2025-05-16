import chromadb
import os
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from pathlib import Path

class DBManager(ABC):
    @abstractmethod
    def query(self, query_embeddings: List[float], n_results: int =10):
        pass

class ChromaDBManager(DBManager):
    def __init__(self, db_path: Path, collection_name: str):
        try:
            self.client = chromadb.PersistentClient(path=str(db_path))
            if not self.client:
                raise ConnectionError("Failed to create ChromaDB client")
            self.collection = self.client.get_collection(collection_name)
            if not self.collection:
                raise ConnectionError(f"Failed to get collection: {collection_name}")
        except Exception as e:
            print(f"Error initializing ChromaDB: {str(e)}")
            raise

    def add_documents(self, 
                     documents: List[str],
                     embeddings: List[List[float]],
                     metadata: List[Dict[str, Any]] = None,
                     base_id: int = 0) -> None:

        if metadata is None:
            metadata = [{}] * len(documents)
            
        self.collection.add(
            ids=[str(base_id + i) for i in range(len(documents))],
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata
        )

    def query(self,
                query_embeddings: List[float],
                n_results: int =20) -> Dict[str, Any]:

        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )