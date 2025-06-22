import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from infrastructure.embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from infrastructure.embedding.rag_pipeline_builder import QueryRAGPipelineBuilder
from infrastructure.database.database_manager import ChromaDBManager

import os
import json


def embed(arg):
    # Prepare chunker
    chunker = RecursiveTokenChunker(
        chunk_size = 400, 
        chunk_overlap = 0, 
        separators = ["\n\n\n", "\n\n", "\n", ".", " ", ""]
    )
    
    # Build pipeline for embedding generation
    pipeline = QueryRAGPipelineBuilder().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()
    # Initialize ChromaDBManager
    db_path = Path(__file__).parent.parent.parent / "chroma_db"
    db_manager = ChromaDBManager(db_path, "git_commands")

    # Read examples.json
    examples_path = Path(__file__).parent.parent / "infrastructure" / "examples.json"
    with open(examples_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    base = 0
    for command_group in data:
        command = command_group["command"]
        descriptions = []
        metadata_list = []
        embeddings = []

        # Extract descriptions and prepare metadata
        for example in command_group["examples"]:
            example_chunks, example_embeddings = pipeline.handle(example["description"])
            for i in range(len(example_chunks)):
                descriptions.append(example_chunks[i])
                embeddings.append(example_embeddings[i])
                metadata_list.append({
                    "command": command,
                    "example_command": example["command"]
                })

        # Add to database
        if descriptions:
            db_manager.add_documents(
                documents=descriptions,
                embeddings=embeddings,
                metadata=metadata_list,
                base_id=base
            )

        print(f'Embedded {len(descriptions)} descriptions for command {command}')
        base += len(descriptions)

if __name__ == "__main__":
    embed([])