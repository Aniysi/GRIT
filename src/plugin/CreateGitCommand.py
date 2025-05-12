from plugin.CompositeCommand import CompositeCommand
from plugin.prompts.prompts import CREATE_COMMAND_SYSTEM_PROMPT
from plugin.CreateMessage import CreateMessage, Role
from plugin.DBManager import ChromaDBManager
from embedding.RAGPipelineBuilder import QueryRAGPipelineBuilder
from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from plugin.QueryDatabase import QueryDatabase
from plugin.GetSparseEmbeddings import GetSparseEmbeddings

import os

def print_results(closest_chunks):
    print("\nSearch results:")
    for i in range(len(closest_chunks['documents'][0])):
        print(f"\n{i+1}. Document: {closest_chunks['documents'][0][i]}")
        print(f"   Command: {closest_chunks['metadatas'][0][i]['command']}")
        print(f"   Keywords: {closest_chunks['metadatas'][0][i]['keywords']}")
        print(f"   Distance: {closest_chunks['distances'][0][i]:.4f}")
        print(f"   Sparse distance: {closest_chunks['sparse_distances'][i]:.4f}")
        print("   " + "-"*80)

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

        print_results(closest_chunks)



        
