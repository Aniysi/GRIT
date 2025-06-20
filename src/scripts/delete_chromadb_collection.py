import chromadb
import argparse
from pathlib import Path

def delete_chroma_collection(collection_name_to_delete):

    try:
        db_path = Path(__file__).parent.parent.parent / "chroma_db"

        client = chromadb.PersistentClient(path=str(db_path)) 

        print(f"Attempting to delete collection: '{collection_name_to_delete}'...")

        collections = client.list_collections()
        collection_exists = any(c.name == collection_name_to_delete for c in collections)

        if collection_exists:
            client.delete_collection(name=collection_name_to_delete)
            print(f"Collection '{collection_name_to_delete}' deleted successfully.")
        else:
            print(f"Collection '{collection_name_to_delete}' not found. No action taken.")

    except Exception as e:
        print(f"Error during operation on collection '{collection_name_to_delete}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deletes a collection from ChromaDB.")
    parser.add_argument("collection_name", type=str, help="The name of the collection to delete.")

    args = parser.parse_args()

    delete_chroma_collection(args.collection_name)
