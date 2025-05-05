from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama
import chromadb
from pydantic import BaseModel

def chunk_text(text, chunk_size=512, chunk_overlap=64):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators  = ["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)

def embed_chunk(chunk):
    return ollama.embed(
        model='mxbai-embed-large',
        input=chunk
    )["embeddings"]

def ask(message_history):
    query = input('>>> ')

    chunks = chunk_text(query)
    query_collection = []
    for chunk in chunks:
        embedded_chunk = embed_chunk(chunk)
        query_collection.append(embedded_chunk[0])

    # Connect to persistent client
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="docs")

    results = collection.query(
        query_embeddings=query_collection,
        n_results=3
    )

    context = ""
    for docs in results['documents']:
        for doc in docs:
            context += doc + "\n\n"

    message_history.append(
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
        messages=message_history,
        format=Commands.model_json_schema(),
    )

    command = Commands.model_validate_json(ollama_response.message.content)
    print(command)

    return message_history

if __name__ == "__main__":
    message_history=[
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
        message_history = ask(message_history)
