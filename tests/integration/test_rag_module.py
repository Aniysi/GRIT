import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pytest
from unittest.mock import MagicMock, patch

from src.infrastructure.embedding.reader import Reader
from src.infrastructure.embedding.chunker import Chunker
from src.infrastructure.embedding.embedder import Embedder

class DummyChunker:
    def split_text(self, text):
        # Simula il chunking in due parti
        return [text[:len(text)//2], text[len(text)//2:]]

@pytest.fixture
def rag_pipeline():
    # Crea la pipeline Reader -> Chunker -> Embedder
    reader = Reader()
    chunker = Chunker(DummyChunker())
    embedder = Embedder(model="fake-model")
    reader.set_next(chunker).set_next(embedder)
    return reader, chunker, embedder

@patch("src.infrastructure.embedding.reader.fitz")
@patch("src.infrastructure.embedding.embedder.ollama")
def test_rag_system_pipeline(mock_ollama, mock_fitz, rag_pipeline, tmp_path):
    # Prepara un PDF finto
    fake_text = "This is a test document for RAG pipeline."
    fake_page = MagicMock()
    fake_page.get_text.return_value = fake_text
    mock_doc = [fake_page]
    mock_fitz.open.return_value = mock_doc

    # Mock embedding
    mock_ollama.embed.return_value = {"embeddings": [[0.1, 0.2], [0.3, 0.4]]}

    # Simula un file PDF (il path è finto, fitz è mockato)
    fake_pdf_path = tmp_path / "fake.pdf"

    reader, chunker, embedder = rag_pipeline

    # Esegui la pipeline
    result_chunks, result_embeds = reader.handle(str(fake_pdf_path))

    # Verifica che il testo sia stato chunkato e embeddato
    # result è il valore di embedder.handle(chunks)
    print(type(result_embeds))
    assert isinstance(result_embeds, list)
    assert result_embeds == [[0.1, 0.2], [0.3, 0.4]]

    # Verifica che fitz.open sia stato chiamato
    mock_fitz.open.assert_called_once_with(str(fake_pdf_path))
    # Verifica che ollama.embed sia stato chiamato con i chunk giusti
    assert result_chunks == ['This is a test docum', 'ent for RAG pipeline.']