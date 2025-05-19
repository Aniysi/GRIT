from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from embedding.RAGPipelineBuilder import QueryRAGPipelineBuilder

import os
import chromadb
import sys
from pathlib import Path
import json

if __name__ == "__main__":

    # Create a persistent client and 'docs' collection
        DBpath  = os.path.join("..", "prova")
        client = chromadb.PersistentClient(path=DBpath)
        #client.delete_collection(name="test-nomic")
        collection_nomic = client.create_collection(name="test-nomic")

        chunker = RecursiveTokenChunker(
            chunk_size = 200, 
            chunk_overlap = 0, 
            separators = [ "\n", ".", " ", ""]
        )
        pipeline_nomic = QueryRAGPipelineBuilder().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()
        # Read the JSON file
        with open("./examples.json", "r") as file:
            data = json.load(file)

        # Process each element's description through the pipeline
        for command_group in data:
            base_command = command_group["command"]
            for example in command_group["examples"]:
                if "description" in example:
                    chunks, embeddings = pipeline_nomic.handle(example["description"])
                    
                    # Create metadata for each chunk
                    metadatas = [{
                        "command": base_command,
                        "full_command": example["command"],
                        "keywords": " ".join(example["keywords"])  # Join keywords into a string
                    } for _ in range(len(chunks))]
                    
                    # Add to collection with enhanced metadata
                    collection_nomic.add(
                        ids=[f"{base_command}_{i}" for i in range(len(chunks))],
                        documents=chunks,
                        embeddings=embeddings,
                        metadatas=metadatas
                    )
                    
                    print(f'Embedded {len(chunks)} chunks from description of command: {example["command"]}')
