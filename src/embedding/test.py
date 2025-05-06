from chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from RAGPipelineBuilder import RAGPipelineBuilder

import os
import chromadb
import sys
from pathlib import Path

if __name__ == "__main__":

    # Prepare chunker to respect dependency injection
    chunker = RecursiveTokenChunker(
            chunk_size = 800, 
            chunk_overlap = 0, 
            separators = ["\n\n\n", "\n\n", "\n", ".", " ", ""]
        )
    
    # Build chain of responsibility
    # 1. PDFReader: Read the PDF file and extract text
    # 2. Chunker: Split the text into smaller chunks
    # 3. Embedder: Generate embeddings for the chunks using a specified language model
    pipeline = RAGPipelineBuilder().add_PDFReader().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()

    file_path = os.path.join("..", "..", "docs", "pdfdocs", "gitignore.pdf")

    chunks, embeddings = pipeline.handle(file_path)
