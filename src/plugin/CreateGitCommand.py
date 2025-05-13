from plugin.CompositeCommand import CompositeCommand
from plugin.prompts.prompts import CREATE_COMMAND_SYSTEM_PROMPT
from plugin.CreateMessage import CreateMessage, Role
from plugin.DBManager import ChromaDBManager
from embedding.RAGPipelineBuilder import QueryRAGPipelineBuilder
from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from plugin.QueryDatabase import QueryDatabase
from plugin.GetSparseEmbeddings import GetSparseEmbeddings
from plugin.ComputeRRF import ComputeRRF
from plugin.QueryLLM import QueryLLM

import os

def print_results(results):
    print("\nTop", len(results['command'][0]), "Results:")
    for i in range(len(results['command'][0])):
        print(f"\n{i+1}. Command: {results['command'][0][i]}")
        print(f"   Description: {results['description'][0][i]}")
        print(f"   RRF Score: {results['rrf_scores'][i]}")

class CreateGitCommand(CompositeCommand):
    def execute(self):
        # Initialize messages list
        msgs = []

        # Append system prompt
        msgs.append(CreateMessage(Role.System, CREATE_COMMAND_SYSTEM_PROMPT).execute())

        # Get user query
        query = input(">>> ")

        # Get embeddings
        chunker = RecursiveTokenChunker(
            chunk_size = 800, 
            chunk_overlap = 0, 
            separators = ["\n", ".", " ", ""]
        )
        # Build chain of responsibility
        # 1. PDFReader: Read the PDF file and extract text
        # 2. Chunker: Split the text into smaller chunks
        # 3. Embedder: Generate embeddings for the chunks using a specified language model
        pipeline = QueryRAGPipelineBuilder().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()
        _, embeddings = pipeline.handle(query)

        # Get related chunks dense embeddings
        manager = ChromaDBManager(os.path.join("..", "test_db"), "test-nomic")
        closest_chunks = QueryDatabase(manager, embeddings).execute()

        # Get related chunks sparse embeddings
        closest_chunks = GetSparseEmbeddings(closest_chunks, query).execute()

        # Compute reciprocal rank fusion (RRF) scores
        results = ComputeRRF(closest_chunks).execute()
        #print_results(results)

        # Create and append new message
        msgs.append(CreateMessage(Role.User, query, "Ecco alcuni comandi che potresti trovare utili per eseguire questa query "+str(results)).execute())

        # Query LLM
        response = QueryLLM("qwen3-4B", msgs).execute() 
        print("QWEN: ", response.explanation, "\n\nCommands:")
        for command in response.commands:
            print(" - ",command.command)

        #print_results(closest_chunks)



        
