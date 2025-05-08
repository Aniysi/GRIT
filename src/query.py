from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from embedding.RAGPipelineBuilder import RAGPipelineBuilder

import ollama
import chromadb
from pydantic import BaseModel
from rank_bm25 import BM25Okapi
import os
import re
from typing import List

def normalize_scores(scores):
    """Normalize scores to a range of 0 to 1."""
    min_score = min(scores)
    max_score = max(scores)
    return [(score - min_score) / (max_score - min_score) for score in scores]


def reciprocal_rank_fusion(dense_results, sparse_results, k=60):
    all_docs = set(dense_results).union(sparse_results)
    # print(f"All documents: {all_docs}")
    scores = {}
    for doc in all_docs:
        rank_dense = dense_results.get(doc, float('inf'))
        rank_sparse = sparse_results.get(doc, float('inf'))
        scores[doc] = 1 / (k + rank_dense) + 1 / (k + rank_sparse)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def get_dense_scores(collection, embeddings):
    coherent_chunks = collection.query(
        query_embeddings=embeddings,
        n_results=10
    )

    dense_scores = coherent_chunks['distances'][0]

    # Instead of converting to set, create a dictionary with indices
    documents = [doc for sublist in coherent_chunks['documents'] for doc in sublist]
    return {doc: score for doc, score in zip(documents, dense_scores)}, documents


def get_sparse_scores(documents, query_text):
    # Create tokenized corpus maintaining the order
    tokenized_corpus = [doc.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query_text.split()
    sparse_scores = bm25.get_scores(tokenized_query)
    
    # Create dictionary for sparse scores
    return {doc: score for doc, score in zip(documents, sparse_scores)}


def get_context(query_text, n=5):

    # Prepare chunker to respect dependency injection
    chunker = RecursiveTokenChunker(
            chunk_size = 800, 
            chunk_overlap = 0, 
            separators = ["\n\n\n", "\n\n", "\n", ".", " ", ""]
        )
    
    # Build chain of responsibility
    # 1. PDFReader: Read the PDF file and extract text
    # 2. Chunker: Split the text into smaller chunks
    # 3. Embedder: Generate embeddings for the chunks using a specified language model
    pipeline = RAGPipelineBuilder().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()

    chunks, embeddings = pipeline.handle(query_text)

    # Connect to persistent client
    client = chromadb.PersistentClient(path=os.path.join("..", "chroma_db"))
    collection = client.get_collection(name="docs")

    # Clculate dense scores
    doc_to_dense_score, documents = get_dense_scores(collection, embeddings)
    
    # Calculate sparse scores
    doc_to_sparse_score = get_sparse_scores(documents, query_text)

    # Now you can perform RRF while maintaining the correct associations
    rrf_results = reciprocal_rank_fusion(doc_to_dense_score, doc_to_sparse_score)
    
    # Print results
    # for doc, score in rrf_results:
    #     print(f"Document: {doc}")
    #     print(f"Dense score: {doc_to_dense_score[doc]:.4f}")
    #     print(f"Sparse score: {doc_to_sparse_score[doc]:.4f}")
    #     print(f"RRF score: {score}\n")

    
    selected_docs = rrf_results[:n]

    # Get the context for these documents
    context = []
    for doc, score in selected_docs:
        context.append(doc)

    # Replace multiple newlines with a single newline
    context = re.sub(r'(\n\n)', r'\n', str(context))
    # Join the context into a single string
    context = "\n".join(context)


def ask(message, query): 
    # Get context from the database
    context = get_context(query)

    message.append(
            {
                'role': 'user',
                'context': context,
                'content': query
            }
        )

    class Command(BaseModel):
        command: str

    class Commands(BaseModel):
        explanation: str
        commands: List[Command]

    ollama_response = ollama.chat(
        model="qwen3-4B",
        messages=message,
        format=Commands.model_json_schema(),
    )

    return Commands.model_validate_json(ollama_response.message.content)

if __name__ == "__main__":
    system_prompt=[
        {
            'role': 'system',
            'content':  '''You are a Git command assistant. You MUST:
                        1. Provide Git commands in the "commands" array
                        2. Each command as a separate object
                        3. Use format:
                        {
                            "explanation": "Explanation of why ypu chose this command(s) (medium length)",
                            "commands": [
                                {"command": "git command"}
                            ]
                        }
                        4. Never return empty commands array
                        5. DO NOT return commands generated in previous interactions.
                        Note: Every command you provide will be executed on bash as is, so its 
                        execution MUST not require human intervention.'''
        }
    ]
    
    while(True):
        query = input(">>> ")
        response = ask(system_prompt, query)
        print("QWEN: ", response.explanation, "\n\nCommands:")
        for command in response.commands:
            print(" - ",command.command)
