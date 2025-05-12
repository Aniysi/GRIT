from plugin.CompositeCommand import CompositeCommand
from plugin.prompts.prompts import CREATE_COMMAND_SYSTEM_PROMPT
from plugin.CreateMessage import CreateMessage, Role
from plugin.DBManager import ChromaDBManager
from embedding.RAGPipelineBuilder import QueryRAGPipelineBuilder
from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from plugin.QueryDatabase import QueryDatabase

import os

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

        # Get related chunks
        manager = ChromaDBManager(os.path.join("..", "test_db"), "test-nomic")
        closest_chunks = QueryDatabase(manager, embeddings).execute()

        print(closest_chunks)




        
