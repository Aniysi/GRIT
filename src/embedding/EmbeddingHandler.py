from embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker

from abc import ABC, abstractmethod
from typing import Any

class EmbeddingHandler(ABC):
    def __init__(self):
        self._next_handler = None
    
    def get_last(self):
        current = self
        successor = self._next_handler
        while(successor is not None):
            current = successor
            successor = successor._next_handler
        return current

    def set_next(self, handler: 'EmbeddingHandler'):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, data: Any) -> Any:
        if self._next_handler:
            #print("Next type: ", type(self._next_handler))
            return self._next_handler.handle(data)
        return data