from EmbeddingHandler import EmbeddingHandler

import fitz

class PDFReader(EmbeddingHandler):
    def handle(self, path):
        doc = fitz.open(path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return super().handle(full_text)