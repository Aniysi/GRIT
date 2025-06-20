from infrastructure.embedding.embedding_handler import EmbeddingHandler

import ollama

class Embedder(EmbeddingHandler):
    def __init__(self, model: str):
        super().__init__()
        self.model = model

    def handle(self, data):
        return ollama.embed(
            model=self.model,
            input=data
        )["embeddings"]