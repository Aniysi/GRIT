from embedding.EmbeddingHandler import EmbeddingHandler
from embedding.chunkingLibs.base_chunker import BaseChunker

class Chunker(EmbeddingHandler):
    def __init__(self, chunker : BaseChunker):
        super().__init__()
        self.chunker = chunker

    def handle(self, data):
        chunks = self.chunker.split_text(data)
        # for chunk in chunks:
        #     print("\n----------------------------------------------------\n", chunk)
        return chunks, super().handle(chunks)