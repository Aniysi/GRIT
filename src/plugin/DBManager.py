import chromadb
import os
from typing import List, Dict, Any
from abc import ABC, abstractmethod

class DBManager(ABC):
    @abstractmethod
    def query(self, query_embeddings: List[float], n_results: int =5):
        pass

class ChromaDBManager(DBManager):
    def __init__(self, db_path: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(collection_name)

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
                n_results: int =5) -> Dict[str, Any]:

        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )