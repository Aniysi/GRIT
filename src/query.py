from typing import List
from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
import ollama
import chromadb
from pydantic import BaseModel
import bm25s
import os

def chunk_text(text, chunk_size=512, chunk_overlap=64):
    splitter = RecursiveTokenChunker(
            chunk_size = 800, 
            chunk_overlap = 0, 
            separators = ["\n\n\n", "\n\n", "\n", ".", " ", ""]
        )
    return splitter.split_text(text)

def embed_chunk(chunk):
    return ollama.embed(
        model='nomic-embed-text',
        input=chunk
    )["embeddings"]

def ask(messages):
    query = input('>>> ')

    chunks = chunk_text(query)
    query_collection = []
    for chunk in chunks:
        embedded_chunk = embed_chunk(chunk)
        query_collection.append(embedded_chunk[0])

    # Connect to persistent client
    client = chromadb.PersistentClient(path=os.path.join("..", "chroma_db"))
    collection = client.get_collection(name="docs")

    corpus = collection.query(
        query_embeddings=query_collection,
        n_results=5
    )

    # # Flatten and convert to list of strings
    # documents = [doc for sublist in corpus['documents'] for doc in sublist]
    # corpus_tokens = bm25s.tokenize(documents)
    # retriver = bm25s.BM25(corpus=documents)  # Change this line to pass documents instead of corpus
    # retriver.index(corpus_tokens)

    # query_tokens = bm25s.tokenize(query)
    # try:
    #     docs, scores = retriver.retrieve(query_tokens, k=min(5, len(documents)))  # Add safety check for k
    #     print(f"Best result (score: {scores[0, 0]:.2f}): {docs[0, 0]}")
    # except Exception as e:
    #     print(f"Warning: Retrieval failed - {str(e)}")
    #     docs = documents[:1]  # Fallback to first document if retrieval fails
    #     scores = [[0.0]]

    context = ""
    for docs in corpus['documents']:
        for doc in docs:
            print(doc, "\n--------------------------------------------------------\n")
            context += doc + "\n\n"

    messages.append(
            {
                'role': 'user',
                'context': context,
                'content': query
            }
        )

    class Command(BaseModel):
        command: str

    class Commands(BaseModel):
        description: str
        commands: List[Command]

    ollama_response = ollama.chat(
        model="qwen3-4B",
        messages=messages,
        format=Commands.model_json_schema(),
    )

    command = Commands.model_validate_json(ollama_response.message.content)
    print(command)


if __name__ == "__main__":
    system_prompt=[
        {
            'role': 'system',
            'content':  '''You are a Git command assistant. You MUST:
                        1. Provide Git commands in the "commands" array
                        2. Each command as a separate object
                        3. Use format:
                        {
                            "description": "Brief description of the command(s) you chose and why",
                            "commands": [
                                {"command": "git command"}
                            ]
                        }
                        4. Never return empty commands array
                        5. Be concise
                        Note: Every command you provide will be executed on bash as is, so its 
                        execution MUST not require human intervention.'''
        }
    ]
    
    while(True):
        ask(system_prompt)
