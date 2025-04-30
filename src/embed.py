import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama
import os
import chromadb


def extract_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text


def chunk_text(text, chunk_size=512, chunk_overlap=64):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators  = ["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)


def embed_chunk(chunk):
    return ollama.embed(
        model='mxbai-embed-large',
        input=chunk
    )["embeddings"]


def generate_vectors(dir):
    client = chromadb.Client()
    collection = client.create_collection(name="docs")

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                raw_text = extract_pdf(file_path)
                chunks = chunk_text(raw_text)

                for chunk in chunks:
                    collection.add(
                        ids=[chunk],
                        
                    )





pdf_path = "C:/Users/leona/Desktop/Unipd/Terzo anno/Stage/project/docs/pdfdocs/git-tag.pdf"
raw_text = extract_pdf(pdf_path)
chunks = chunk_text(raw_text)


for chunk in chunks:
    print(str(embed_chunk(chunk)) + "\n\n\n\n\n")