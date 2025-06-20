from infrastructure.embedding.embedding_handler import EmbeddingHandler

import fitz
import unicodedata
import re

class Reader(EmbeddingHandler):
    def preprocess(self, text):
        # Normalize Unicode characters and ligatures
        text = unicodedata.normalize('NFKD', text)
        # Add extra newline before uppercase sentences
        text = re.sub(r'(\n)([A-Z][A-Z\s]+)(\n)', r'\1\n\2\3', text)
        # Add extra newline after periods followed by newline
        text = re.sub(r'(\.)(\n)', r'\1\2\2', text)
        return text

    def handle(self, path):
        doc = fitz.open(path)
        full_text = ""
        for page in doc:
            text = page.get_text()
            full_text += self.preprocess(text)
        #print(full_text)
        return super().handle(full_text)
    
    # def handle(self, path):
    #     with open(path, 'r') as file:
    #         data = json.load(file)
            
    #     chunks, embeds = super().handle(unicodedata.normalize('NFKD', data['description']))
    #     return {"command": data['command'],"usage": data['usage']}, chunks, embeds