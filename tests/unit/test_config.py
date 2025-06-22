import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

import src.config.config as config_mod

def test_load_config_success(monkeypatch):
    fake_config = {"ollama": {"model": "test-model", "host": "localhost"}}
    m = mock_open(read_data=json.dumps(fake_config))
    monkeypatch.setattr("builtins.open", m)
    monkeypatch.setattr(config_mod, "save_config", lambda x: None)
    result = config_mod.load_config()
    assert result["ollama"]["model"] == "test-model"

def test_load_config_missing_model(monkeypatch):
    fake_config = {"ollama": {"model": "", "host": "localhost"}}
    m = mock_open(read_data=json.dumps(fake_config))
    monkeypatch.setattr("builtins.open", m)
    monkeypatch.setattr(config_mod, "save_config", lambda x: None)
    mock_userio = MagicMock()
    mock_userio.ask_query.return_value = "new-model"
    monkeypatch.setattr(config_mod, "UserIO", lambda: mock_userio)
    result = config_mod.load_config()
    assert result["ollama"]["model"] == "new-model"

def test_load_config_file_not_found(monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    with pytest.raises(FileNotFoundError):
        config_mod.load_config()

def test_save_config(monkeypatch):
    fake_config = {"ollama": {"model": "test-model", "host": "localhost"}}
    m = mock_open()
    monkeypatch.setattr("builtins.open", m)
    config_mod.save_config(fake_config)
    m.assert_called_once()
    handle = m()
    handle.write.assert_called()

def test_set_config_language(monkeypatch):
    fake_config = {"ollama": {"model": "test-model", "host": "localhost"}}
    monkeypatch.setattr(config_mod, "load_config", lambda: fake_config)
    monkeypatch.setattr(config_mod, "save_config", lambda x: x.update({"saved": True}))
    config_mod.set_config_language("it")
    assert fake_config["output-language"] == "it"
    assert fake_config["saved"]

def test_set_config_model(monkeypatch):
    fake_config = {"ollama": {"model": "test-model", "host": "localhost"}}
    monkeypatch.setattr(config_mod, "load_config", lambda: fake_config)
    monkeypatch.setattr(config_mod, "save_config", lambda x: x.update({"saved": True}))
    config_mod.set_config_model("new-model")
    assert fake_config["ollama"]["model"] == "new-model"
    assert fake_config["saved"]