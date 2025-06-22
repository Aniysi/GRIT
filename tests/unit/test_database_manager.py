import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.infrastructure.database.database_manager import ChromaDBManager

@patch("chromadb.PersistentClient")
def test_chromadbmanager_init_success(mock_client):
    mock_collection = MagicMock()
    mock_client.return_value.get_or_create_collection.return_value = mock_collection
    manager = ChromaDBManager(db_path=Path("/fake/path"), collection_name="test")
    assert manager.client is mock_client.return_value
    assert manager.collection is mock_collection

@patch("chromadb.PersistentClient")
def test_chromadbmanager_init_fail_collection(mock_client):
    mock_client.return_value.get_or_create_collection.return_value = None
    with pytest.raises(ConnectionError):
        ChromaDBManager(db_path=Path("/fake/path"), collection_name="test")

@patch("chromadb.PersistentClient")
def test_add_documents_calls_collection_add(mock_client):
    mock_collection = MagicMock()
    mock_client.return_value.get_or_create_collection.return_value = mock_collection
    manager = ChromaDBManager(db_path=Path("/fake/path"), collection_name="test")
    docs = ["doc1", "doc2"]
    embs = [[0.1, 0.2], [0.3, 0.4]]
    meta = [{"a": 1}, {"b": 2}]
    manager.add_documents(docs, embs, meta, base_id=5)
    mock_collection.add.assert_called_once()
    args, kwargs = mock_collection.add.call_args
    assert kwargs["ids"] == ["5", "6"]
    assert kwargs["documents"] == docs
    assert kwargs["embeddings"] == embs
    assert kwargs["metadatas"] == meta

@patch("chromadb.PersistentClient")
def test_add_documents_default_metadata(mock_client):
    mock_collection = MagicMock()
    mock_client.return_value.get_or_create_collection.return_value = mock_collection
    manager = ChromaDBManager(db_path=Path("/fake/path"), collection_name="test")
    docs = ["doc1"]
    embs = [[0.1, 0.2]]
    manager.add_documents(docs, embs)
    mock_collection.add.assert_called_once()
    assert mock_collection.add.call_args.kwargs["metadatas"] == [{}]

@patch("chromadb.PersistentClient")
def test_query_calls_collection_query(mock_client):
    mock_collection = MagicMock()
    mock_client.return_value.get_or_create_collection.return_value = mock_collection
    manager = ChromaDBManager(db_path=Path("/fake/path"), collection_name="test")
    manager.query([0.1, 0.2, 0.3], n_results=7)
    mock_collection.query.assert_called_once_with(query_embeddings=[0.1, 0.2, 0.3], n_results=7)