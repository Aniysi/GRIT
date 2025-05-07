from embedding.PDFReader import PDFReader
from embedding.Chunker import Chunker
from embedding.Embedder import Embedder
from embedding.chunkingLibs.base_chunker import BaseChunker

class RAGPipelineBuilder:
    def __init__(self):
        self.first_handler = None

    def add_PDFReader(self):
        if not self.first_handler:
            self.first_handler = PDFReader()
        else:
            self.first_handler.set_next(PDFReader())
        return self
    
    def add_Chunker(self, chunker: BaseChunker):
        if not self.first_handler:
            self.first_handler = Chunker(chunker)
        else:
            self.first_handler.set_next(Chunker(chunker))
        return self
    
    def add_Embedder(self, model : str):
        if not self.first_handler:
            self.first_handler = Embedder(model)
        else:
            self.first_handler.get_next().set_next(Embedder(model))
        return self

    def build(self):
        return self.first_handler