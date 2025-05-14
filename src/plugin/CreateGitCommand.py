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
from plugin.GetInput import GetInput
from plugin.ExecuteCommand import ExecuteCommand

import os

GENERATION_LLM = "qwen3-4B"

def print_results(results):
    print("\nTop", len(results['command'][0]), "Results:")
    for i in range(len(results['command'][0])):
        print(f"\n{i+1}. Command: {results['command'][0][i]}")
        print(f"   Description: {results['description'][0][i]}")
        print(f"   RRF Score: {results['rrf_scores'][i]}")

def print_response(response):
    print("LLM: ", response.explanation, "\n\nCommands:")
    for command in response.commands:
        print(" - ",command.command)

class CreateGitCommand(CompositeCommand):
    def execute(self):
        # Get user query
        query, status = GetInput().execute()
        firstMessageFlag = True
        while(status == 0):
            # Initialize messages list
            msgs = []

            # Append system prompt
            msgs.append(CreateMessage(Role.system, CREATE_COMMAND_SYSTEM_PROMPT).execute())

            if (firstMessageFlag):
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

                # Create and append new message with context
                msgs.append(CreateMessage(Role.user, query, str(results)).execute())
            else:
                # Create and append new message without context
                msgs.append(CreateMessage(Role.user, "Correggi il precedente comando: "+query).execute())

            # Query LLM
            response = QueryLLM(GENERATION_LLM, msgs).execute() 

            # Append LLM response to messages
            msgs.append(CreateMessage(Role.assistant, response.toJson()).execute())
            print(msgs)
            print_response(response)

            new_query, status = GetInput().execute()
            if status == 1:
                exec = ExecuteCommand(response.commands).execute()
            elif status == 0:
                if new_query != "":
                    query = new_query

            firstMessageFlag = False




        
