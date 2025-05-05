from chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from RAGPipelineBuilder import RAGPipelineBuilder

import os

if __name__ == "__main__":
    chunker = RecursiveTokenChunker(
            chunk_size = 400, 
            chunk_overlap = 0, 
            separators = ["\n\n", "\n", ".", "?", " ", ""]
        )
    pipeline = RAGPipelineBuilder().add_PDFReader().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()

    docs_path = os.path.join("..", "..", "docs", "pdfdocs")
    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                chunks, embeddings = pipeline.handle(file_path)
                # print(f'{len(chunks)} and {len(embeddings)} in file {file}')

    # file_path = os.path.join("..", "..", "docs", "pdfdocs", "git-add.pdf")
    # print(len(pipeline.handle(file_path)))
    # print(type(pipeline.handle(file_path)))
    