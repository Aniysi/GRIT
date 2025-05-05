from EmbeddingHandler import EmbeddingHandler, PDFReader, Chunker, Embedder

import os


file_path = os.path.join("..", "..", "docs", "pdfdocs", "git-add.pdf")

reader = PDFReader()
chunker = Chunker()
embedder = Embedder()

reader.set_next(chunker)
chunker.set_next(embedder)
print(type(reader.handle(file_path)[0][0]))