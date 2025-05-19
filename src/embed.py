from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from embedding.RAGPipelineBuilder import DocumentRAGPipelineBuilder

import os
import chromadb
import sys
from pathlib import Path

if __name__ == "__main__":

    arg = sys.argv[1:]
    if len(arg) > 1:
        print("Usage: python src/embedding/__init__.py <path_to_pdf_directory>")
        sys.exit(1)

    # Prepare chunker to respect dependency injection
    chunker = RecursiveTokenChunker(
            chunk_size = 400, 
            chunk_overlap = 0, 
            separators = ["\n\n\n", "\n\n", "\n", ".", " ", ""]
        )
    
    # Build chain of responsibility
    # 1. PDFReader: Read the PDF file and extract text
    # 2. Chunker: Split the text into smaller chunks
    # 3. Embedder: Generate embeddings for the chunks using a specified language model
    pipeline = DocumentRAGPipelineBuilder().add_Reader().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()

    # Create a persistent client and 'docs' collection
    client = chromadb.PersistentClient(path=os.path.join("..", "chroma_db"))
    #client.delete_collection(name="docs400token")
    collection = client.create_collection(name="docs400token")

    # Recursively walk through the directory and process each PDF file
    if len(arg) == 1:
        docs_path = Path(arg[0])
    else:
        docs_path = os.path.join("..", "..", "docs", "pdfdocs")
    for root, dirs, files in os.walk(docs_path):
        base = 0
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)

                # Start chain of operations
                chunks, embeddings = pipeline.handle(file_path)

                # Add chunks and embeddings to the persistent collection
                if len(chunks) > 0:
                    collection.add(
                        ids=[str(base+number) for number in range(0, len(chunks))],
                        documents=chunks,
                        embeddings=embeddings,
                        metadatas=[{"source": file} for _ in range(len(chunks))]
                    )

                print(f'Embedded {len(chunks)} chunks from {file}')
                base+=len(chunks)





#---------------------------------------------------JSON VERSION---------------------------------------------------#
# #client.delete_collection(name="docs")
#     collection = client.create_collection(name="json_docs")

#     # Recursively walk through the directory and process each PDF file
#     if len(arg) == 1:
#         docs_path = Path(arg[0])
#     else:
#         docs_path = os.path.join("..", "..", "docs", "jsondocs")
#     for root, dirs, files in os.walk(docs_path):
#         base = 0
#         for file in files:
#             if file.endswith('.json'):
#                 file_path = os.path.join(root, file)

#                 # Start chain of operations
#                 metadata, chunks, embeddings = pipeline.handle(file_path)

#                 # Add chunks and embeddings to the persistent collection
#                 if len(chunks) > 0:
#                     collection.add(
#                         ids=[str(base+number) for number in range(0, len(chunks))],
#                         documents=chunks,
#                         embeddings=embeddings,
#                         metadatas=[metadata for _ in range(len(chunks))]
#                     )

#                 print(f'Embedded {len(chunks)} chunks from {file} relative to command {metadata["command"]}')
#                 base+=len(chunks)