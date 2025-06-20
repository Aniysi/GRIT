import chromadb
from pathlib import Path

def list_chroma_collections():
    """List all collections in the ChromaDB database."""
    # Get the database path (assuming it's in the project root)
    db_path = Path(__file__).parent.parent.parent / "chroma_db"
    
    # Create ChromaDB client
    client = chromadb.PersistentClient(path=str(db_path))
    
    # Get all collections
    collections = client.list_collections()
    
    print(f"ChromaDB collections in {db_path}:")
    print("-" * 50)
    
    if not collections:
        print("No collections found.")
    else:
        for collection in collections:
            print(f"Name: {collection.name}")
            print(f"ID: {collection.id}")
            print(f"Metadata: {collection.metadata}")
            
            # Get collection count
            count = collection.count()
            print(f"Document count: {count}")
            print("-" * 30)

if __name__ == "__main__":
    # List all collections
    list_chroma_collections()