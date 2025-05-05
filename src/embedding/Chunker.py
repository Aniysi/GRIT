from EmbeddingHandler import EmbeddingHandler
from chunkingLibs.base_chunker import BaseChunker

class Chunker(EmbeddingHandler):
    def __init__(self, chunker : BaseChunker):
        super().__init__()
        self.chunker = chunker

    def handle(self, data):
        chunks = self.chunker.split_text(data)
        return chunks, super().handle(chunks)