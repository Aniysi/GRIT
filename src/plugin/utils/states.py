from plugin.commands.GetInput import GetInput
from plugin.commands.CreateMessage import CreateMessage, Role
from plugin.utils.prompts import CREATE_COMMAND_SYSTEM_PROMPT, GENERATION_LLM
from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from embedding.RAGPipelineBuilder import QueryRAGPipelineBuilder
from database.DBManager import ChromaDBManager
from plugin.commands.QueryDatabase import QueryDatabase
from plugin.commands.GetSparseEmbeddings import GetSparseEmbeddings
from plugin.commands.ComputeRRF import ComputeRRF
from plugin.commands.QueryLLM import QueryLLM
from plugin.commands.PrintResponse import PrintResponse
from plugin.commands.ExecuteCommand import ExecuteCommand

from abc import ABC, abstractmethod
from typing import List
import os


class State(ABC):
    @abstractmethod
    def handle(self, query: str):
        pass


class InitialState(State):
    def __init__(self, context, query: str =None):
        self._context = context
        self._context.deleteMessages()
        self._query = query

    def handle(self):
        # Retrive messages from context
        messages = self._context.getMessages()
        if self._query is None:
            # Create and append first message
            while True:
                self._query = GetInput().execute()
                if self._query.startswith("/exec"):
                    print("There are no commands to execute. Please provide a new query or quit (using /quit).")
                elif self._query.startswith("/fix"):
                    print("There are no commands to fix. Please provide a new query or quit (using /quit).")
                else:
                    break

        new_message = CreateMessage(Role.system, CREATE_COMMAND_SYSTEM_PROMPT).execute()
        messages.append(new_message)
        # Get embeddings
        chunker = RecursiveTokenChunker(
            chunk_size = 800, 
            chunk_overlap = 0, 
            separators = ["\n", ".", " ", ""]
        )
        # Build chain of responsibility
        # 1. Chunker: Split the text into smaller chunks
        # 2. Embedder: Generate embeddings for the chunks using a specified language model
        pipeline = QueryRAGPipelineBuilder().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()
        _, embeddings = pipeline.handle(self._query)
        # Get related chunks dense embeddings
        manager = ChromaDBManager(os.path.join("..", "test_db"), "test-nomic")
        closest_chunks = QueryDatabase(manager, embeddings).execute()
        # Get related chunks sparse embeddings
        closest_chunks = GetSparseEmbeddings(closest_chunks, self._query).execute()
        # Compute reciprocal rank fusion (RRF) scores
        results = ComputeRRF(closest_chunks).execute()
        #print_results(results
        # Create and append new message with context
        new_message = CreateMessage(Role.user, self._query, str(results)).execute()
        messages.append(new_message)# Query LLM
        response = QueryLLM(GENERATION_LLM, messages).execute() 
        # Append LLM response to messages
        new_message = CreateMessage(Role.assistant, response.toJson()).execute()
        messages.append(new_message)
        PrintResponse(response).execute()
        # Get user input
        self._query = GetInput().execute()
        
        while True:
            if self._query.startswith("/"):
                if self._query == "/exec":
                    self._context.changeState(ExecutionState(self._context, response.commands))
                    break
                elif self._query.startswith("/fix"):
                    self._context.changeState(RefinementState(self._context, self._query[5:]))
                    break
                else:
                    print("Unknown command")
                    self._query = GetInput().execute()
            else:
                # Instead of creating a new state, just update the current query
                self._query = self._query
                # Process the new query in the current state
                self.handle()
                break


class ExecutionState(State):
    def __init__(self, context, commands):
        self._context = context
        self._commands = commands

    def handle(self):
        # Retrive messages from context
        messages = self._context.getMessages()

        # Execute all commands passed
        exec_report = ExecuteCommand(self._commands).execute()

        if exec_report.returncode == 0:
            self._context.changeState(InitialState(self._context))
        else: 
            print("Query failed. Type /fix to retry, /quit to exit program or anything alse to try and execute another query")
            new_query = GetInput().execute()
            if new_query.startswith("/"):
                if new_query == "/fix":
                    exec_error = exec_report.stderr
                    self._context.changeState(RefinementState(self._context, exec_error))
                else:
                    print("Unknown command.")
            else:
                self._context.changeState(InitialState(self._context, new_query))


class RefinementState(State):
    def __init__(self, context, query: str):
        self._context = context
        self._query = query

    def handle(self):
        # Retrive messages from context
        messages = self._context.getMessages()

        correction_msg = "Correggi il precedente comando, secondo queste direttive: " + self._query
        messages.append(CreateMessage(Role.user, correction_msg).execute())
        response = QueryLLM(GENERATION_LLM, messages).execute() 
        messages.append(CreateMessage(Role.assistant, response.toJson()).execute())
        PrintResponse(response).execute()

        # Get user input
        self._query = GetInput().execute()

        while True:
            if self._query.startswith("/"):
                if self._query == "/exec":
                    self._context.changeState(ExecutionState(self._context, response.commands))
                    break
                elif self._query.startswith("/fix"):
                    # Instead of creating a new state, just update the current query
                    self._query = self._query
                    # Process the new query in the current state
                    self.handle()
                    break
                else:
                    print("Unknown command")
                    self._query = GetInput().execute()
            else:
                self._context.changeState(InitialState(self._context, self._query))
                break