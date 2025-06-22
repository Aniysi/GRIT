import pytest
from unittest.mock import patch, MagicMock

from src.infrastructure.llm.ollama_client import OllamaClient

@patch("src.infrastructure.llm.ollama_client.load_config")
@patch("src.infrastructure.llm.ollama_client.Client")
def test_init_ollama_client(mock_client, mock_load_config):
    mock_load_config.return_value = {"ollama": {"model": "mymodel", "host": "localhost"}}
    client = OllamaClient()
    assert client._OllamaClient__model == "mymodel"
    mock_client.assert_called_once_with(host="localhost")

@patch("src.infrastructure.llm.ollama_client.load_config")
@patch("src.infrastructure.llm.ollama_client.Client")
def test_generate_structured_response(mock_client, mock_load_config):
    mock_load_config.return_value = {"ollama": {"model": "mymodel", "host": "localhost"}}
    mock_chat_session = MagicMock()
    mock_chat_session.to_dict_list.return_value = [{"role": "user", "content": "hi"}]
    mock_response_type = MagicMock()
    mock_response_type.model_json_schema.return_value = {"type": "object"}
    mock_response_type.model_validate_json.return_value = "validated"
    mock_response = MagicMock()
    mock_response.message.content = '{"some": "json"}'
    mock_client.return_value.chat.return_value = mock_response

    client = OllamaClient()
    result = client.generate_structured_response(mock_chat_session, mock_response_type)
    mock_client.return_value.chat.assert_called_once()
    mock_response_type.model_validate_json.assert_called_once_with('{"some": "json"}')
    assert result == "validated"

@patch("src.infrastructure.llm.ollama_client.load_config")
@patch("src.infrastructure.llm.ollama_client.Client")
def test_generate_response(mock_client, mock_load_config, capsys):
    mock_load_config.return_value = {"ollama": {"model": "mymodel", "host": "localhost"}}
    mock_chat_session = MagicMock()
    mock_chat_session.to_dict_list.return_value = [{"role": "user", "content": "hi"}]
    # Simula lo stream di chunk
    mock_client.return_value.chat.return_value = [
        {"message": {"content": "Hello "}},
        {"message": {"content": "World!"}}
    ]
    client = OllamaClient()
    result = client.generate_response(mock_chat_session)
    assert result == "Hello World!"
    # Verifica che la stampa sia avvenuta
    captured = capsys.readouterr()
    assert "Hello World!" in captured.out