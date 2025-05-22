import pytest
from pathlib import Path
import json
from unittest.mock import patch, mock_open
from plugin.utils.config import Config, config

class TestConfig:
    def setup_method(self):
        # Sample valid config data
        self.valid_config_json = '''{
            "database_path": "C:/Users/leona/Desktop/Unipd/Terzo anno/Stage/project/database",
            "model_name": "qwen3-0.6B"
        }'''

    @patch("builtins.open", new_callable=mock_open)
    def test_config_loads_database_path(self, mock_file):
        # Setup mock to return our valid config
        mock_file.return_value.__enter__.return_value.read.return_value = self.valid_config_json
        
        # Load config from mocked file
        loaded_config = Config.from_json("fake_path.json")
        
        # Verify database_path is defined and has correct value
        assert loaded_config.database_path is not None
        assert loaded_config.database_path == "C:/Users/leona/Desktop/Unipd/Terzo anno/Stage/project/database"

    @patch("builtins.open", new_callable=mock_open)
    def test_config_loads_model_name(self, mock_file):
        # Setup mock to return our valid config
        mock_file.return_value.__enter__.return_value.read.return_value = self.valid_config_json
        
        # Load config from mocked file
        loaded_config = Config.from_json("fake_path.json")
        
        # Verify model_name is defined and has correct value
        assert loaded_config.model_name is not None
        assert loaded_config.model_name == "qwen3-0.6B"

    @patch("builtins.open", new_callable=mock_open)
    def test_config_missing_fields(self, mock_file):
        # Setup mock with missing fields
        invalid_config = '''{}'''
        mock_file.return_value.__enter__.return_value.read.return_value = invalid_config
        
        # Verify loading raises error for missing fields
        with pytest.raises(ValueError) as exc_info:
            Config.from_json("fake_path.json")
        assert "Missing required fields" in str(exc_info.value)