from chunkingLibs.recursive_token_chunker import RecursiveTokenChunker


from abc import ABC, abstractmethod
from typing import Any
import os
import fitz
import chromadb
import ollama

class EmbeddingHandler(ABC):
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler: 'EmbeddingHandler'):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, data: Any) -> Any:
        if self._next_handler:
            print("3 ")
            return self._next_handler.handle(data)
        return data
        

class PDFReader(EmbeddingHandler):
    def handle(self, path):
        print("1 ")
        doc = fitz.open(path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        print("2 ")
        return super().handle(full_text)
    
class Chunker(EmbeddingHandler):
    def __init__(self):
        super().__init__()
        self.chunker = RecursiveTokenChunker(
            chunk_size = 400, 
            chunk_overlap = 0, 
            separators = ["\n\n", "\n", ".", "?", " ", ""]
        )

    def handle(self, data):
        print("4 ")
        chunks = self.chunker.split_text(data)
        return super().handle(chunks)

class Embedder(EmbeddingHandler):
    def handle(self, data):
        print("5 ")
        return ollama.embed(
            model='nomic-embed-text',
            input=data
        )["embeddings"]
    
class RAGPipelineBuilder:
    def __init__(self):
        self.first_handler = None

    def add_PDFReader(self):
        if not self.first_handler:
            self.first_handler = PDFReader()
        else:
            self.first_handler.set_next(PDFReader())
        return self
    
    def add_Chunker(self):
        if not self.first_handler:
            self.first_handler = Chunker()
        else:
            self.first_handler.set_next(Chunker())
        return self
    
    def add_Embedder(self):
        if not self.first_handler:
            self.first_handler = Embedder()
        else:
            self.first_handler.set_next(Embedder())
        return self

