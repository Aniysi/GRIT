import pytest
from src.application.rag.rag_context_builder import RAGContextBuilder

import warnings
warnings.filterwarnings("ignore")

class DummyPipeline:
    def handle(self, query):
        # Simula l'embedding di una query
        return None, [0.1, 0.2, 0.3]

class DummyDBManager:
    def query(self, embeddings, n_results):
        # Simula il retrieval di documenti dal database
        return {
            "documents": [[
                "Linux: list files in a directory",
                "Git: commit changes",
                "Python: create a virtual environment"
            ]],
            "metadatas": [[
                {"example_command": "ls -l"},
                {"example_command": "git commit -m 'msg'"},
                {"example_command": "python -m venv venv"}
            ]],
            "distances": [[0.1, 0.2, 0.3]]
        }

def test_rag_context_builder_realistic():
    pipeline = DummyPipeline()
    db_manager = DummyDBManager()
    builder = RAGContextBuilder(pipeline, db_manager)

    query = "How do I commit changes in git?"
    context = builder.build_context(query, "fake-model")

    # Verifica che il contesto sia formattato e contenga i dati attesi
    assert "Description: Git: commit changes" in context
    assert "Command: git commit -m 'msg'" in context
    assert "Description: Linux: list files in a directory" in context
    assert "Description: Python: create a virtual environment" in context
    assert "Command: python -m venv venv" in context
    # Puoi anche stampare il contesto per vedere il risultato reale
    print(context)