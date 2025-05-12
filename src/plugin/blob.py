from plugin.CompositeCommand import CompositeCommand
from plugin.prompts.prompts import CREATE_COMMAND_SYSTEM_PROMPT
from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from embedding.RAGPipelineBuilder import QueryRAGPipelineBuilder


from typing import List, Dict
import chromadb
import os
import json
import uuid

MODEL_NAME = "qwen3-4B"

class CreateGitCommand(CompositeCommand):
    def __init__(self):
        self.__messages: List[Dict] = []


    def help(self):
        pass


    def execute(self):
        # Prepare system prompt
        system_prompt = [
            {
                "role": "system",
                "content": CREATE_COMMAND_SYSTEM_PROMPT
            }   
        ]
        self.__messages.append(system_prompt)

        # Get query
        query = input(">>> ")

        # Get context

        # Create a persistent client and 'docs' collection
        client = chromadb.PersistentClient(path=os.path.join("..", "test_db"))
        # client.delete_collection(name="test-mxbai")
        # client.delete_collection(name="test-nomic")
        collection_mxbai = client.get_or_create_collection(name="test-mxbai")
        collection_nomic = client.get_or_create_collection(name="test-nomic")

        chunker = RecursiveTokenChunker(
            chunk_size = 400, 
            chunk_overlap = 0, 
            separators = ["\n\n\n", "\n\n", "\n", ".", " ", ""]
        )
        pipeline_mxbai = QueryRAGPipelineBuilder().add_Chunker(chunker).add_Embedder('mxbai-embed-large').build()
        pipeline_nomic = QueryRAGPipelineBuilder().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()
        # Read the JSON file
        # with open("./examples.json", "r") as file:
        #     data = json.load(file)

        # # Process each element's description through the pipeline
        # count = 0
        # for i, item in enumerate(data):
        #     for j, example in enumerate(item["examples"]):
        #         chunks, embeddings = pipeline_mxbai.handle(example["description"])

        #         collection_mxbai.add(
        #                 ids=[str(count+ number) for number in range(0, len(chunks))],
        #                 documents=chunks,
        #                 embeddings=embeddings,
        #                 metadatas=[{"command": example["command"], "keywords": " ".join(example["keywords"])} for _ in range(len(chunks))]
        #             )
        #         print(f'Embedded {len(chunks)} chunks from description of command: {item["command"]}')

        #         chunks, embeddings = pipeline_nomic.handle(example["description"])

        #         collection_nomic.add(
        #                 ids=[str(count+ number) for number in range(0, len(chunks))],
        #                 documents=chunks,
        #                 embeddings=embeddings,
        #                 metadatas=[{"command": example["command"], "keywords": " ".join(example["keywords"])} for _ in range(len(chunks))]
        #             )
        #         print(f'Embedded {len(chunks)} chunks from description of command: {item["command"]}')
        #         count += len(chunks)
            
                
        query_chunks, query_embeddings = pipeline_mxbai.handle(query)
        coherent_chunks = collection_mxbai.query(
            query_embeddings=query_embeddings,
            n_results=5
        )
        print("\nSearch results:")
        for i in range(len(coherent_chunks['documents'][0])):
            print(f"\n{i+1}. Document: {coherent_chunks['documents'][0][i]}")
            print(f"   Command: {coherent_chunks['metadatas'][0][i]['command']}")
            print(f"   Keywords: {coherent_chunks['metadatas'][0][i]['keywords']}")
            print(f"   Distance: {coherent_chunks['distances'][0][i]:.4f}")
            print("   " + "-"*80)

        print("#"*120)

        query_chunks, query_embeddings = pipeline_nomic.handle(query)
        coherent_chunks = collection_nomic.query(
            query_embeddings=query_embeddings,
            n_results=5
        )
        print("\nSearch results:")
        for i in range(len(coherent_chunks['documents'][0])):
            print(f"\n{i+1}. Document: {coherent_chunks['documents'][0][i]}")
            print(f"   Command: {coherent_chunks['metadatas'][0][i]['command']}")
            print(f"   Keywords: {coherent_chunks['metadatas'][0][i]['keywords']}")
            print(f"   Distance: {coherent_chunks['distances'][0][i]:.4f}")
            print("   " + "-"*80)






        
            
        