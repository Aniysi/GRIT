import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama
import os
import chromadb


def extract_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text


def chunk_text(text, chunk_size=512, chunk_overlap=64):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators  = ["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)


def embed_chunk(chunk):
    return ollama.embed(
        model='mxbai-embed-large',
        input=chunk
    )["embeddings"]


def generate_vectors(dir):
    # Create a persistent client
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or get existing collection
    client.delete_collection(name="docs")
    collection = client.create_collection(name="docs")

    # Populate collection
    for root, dirs, files in os.walk(dir):
        i = 0
        for file in files:
            if file.endswith('.pdf'):
                print(f'Embedding file {file}...')
                file_path = os.path.join(root, file)
                raw_text = extract_pdf(file_path)
                chunks = chunk_text(raw_text)

                j = 0
                for chunk in chunks:
                    print(f'   Embedding chunk {j} of file {file}')
                    collection.add(
                        ids=str(i),
                        documents=chunk,
                        embeddings=embed_chunk(chunk),
                        metadatas={file : "chunk "+str(j)}
                    )
                    i+=1
                    j+=1


if __name__ == "__main__":
    docs_dir = os.path.join("..", "docs", "pdfdocs")
    generate_vectors(docs_dir)