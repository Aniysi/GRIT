from infrastructure.embedding.embedding_handler import EmbeddingHandler
from infrastructure.embedding.reader import Reader
from infrastructure.embedding.chunker import Chunker
from infrastructure.embedding.embedder import Embedder
from infrastructure.embedding.chunkingLibs.base_chunker import BaseChunker

from enum import Enum, auto
from abc import ABC, abstractmethod

class BuilderState(Enum):
    EMPTY = auto()
    HAS_READER = auto()
    HAS_CHUNKER = auto()
    HAS_EMBEDDER = auto()

class AbstractRAGPipelineBuilder(ABC):
    def __init__(self):
        self._first_handler = None
        self._last_handler = None
        self._state = BuilderState.EMPTY

    def _add_to_chain(self, handler: EmbeddingHandler):
        if not self._first_handler:
            self._first_handler = handler
        else:
            self._last_handler.set_next(handler)
        self._last_handler = handler
        return self

class DocumentRAGPipelineBuilder(AbstractRAGPipelineBuilder):
    def add_Reader(self):
        if self._state != BuilderState.EMPTY:
            raise ValueError("PDFReader must be added first")
        self._add_to_chain(Reader())
        self._state = BuilderState.HAS_READER
        return self
    
    def add_Chunker(self, chunker: BaseChunker):
        if self._state != BuilderState.HAS_READER:
            raise ValueError("Chunker must be added after PDFReader")
        self._add_to_chain(Chunker(chunker))
        self._state = BuilderState.HAS_CHUNKER
        return self
    
    def add_Embedder(self, model: str):
        if self._state != BuilderState.HAS_CHUNKER:
            raise ValueError("Embedder must be added after Chunker")
        self._add_to_chain(Embedder(model))
        self._state = BuilderState.HAS_EMBEDDER
        return self

    def build(self):
        if self._state != BuilderState.HAS_EMBEDDER:
            raise ValueError("Pipeline not complete")
        return self._first_handler

class QueryRAGPipelineBuilder(AbstractRAGPipelineBuilder):
    def add_Chunker(self, chunker: BaseChunker):
        if self._state != BuilderState.EMPTY:
            raise ValueError("Chunker must be added first")
        self._add_to_chain(Chunker(chunker))
        self._state = BuilderState.HAS_CHUNKER
        return self
    
    def add_Embedder(self, model: str):
        if self._state != BuilderState.HAS_CHUNKER:
            raise ValueError("Embedder must be added after Chunker")
        self._add_to_chain(Embedder(model))
        self._state = BuilderState.HAS_EMBEDDER
        return self

    def build(self):
        if self._state != BuilderState.HAS_EMBEDDER:
            raise ValueError("Pipeline not complete")
        return self._first_handler