import chromadb

class DBConnection:
    def __init__(self, db_path):
        self.client = chromadb.PersistentClient(path=db_path)
    
    def connect(self, collection_name):
        return self.client.get_collection(name=collection_name)
    
    def insert(self, collection, chunks, embeddings, file):
        collection.add(
            ids=str(),
            documents=chunks,
            embeddings=embeddings,
            metadatas=file
        )