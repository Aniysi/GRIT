from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class Config:
    database_path: str
    model_name: str

    @classmethod
    def from_json(cls, json_path: str | Path) -> "Config":
        """Load configuration from a JSON file."""
        with open(json_path, 'r') as f:
            config_dict = json.load(f)
        
        # Check if required fields exist
        required_fields = ['database_path', 'model_name']
        missing_fields = [field for field in required_fields if field not in config_dict]
        if missing_fields:
            raise ValueError(f"Missing required fields in config: {', '.join(missing_fields)}")
        
        # If fields are empty, prompt for input
        was_updated = False
        if not config_dict['database_path']:
            config_dict['database_path'] = input("Enter database path: ")
            was_updated = True
        if not config_dict['model_name']:
            config_dict['model_name'] = input("Enter model name: ")
            was_updated = True
            
        # Save updated config if needed
        if was_updated:
            with open(json_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
        return cls(**config_dict)

    def to_json(self, json_path: str | Path) -> None:
        """Save configuration to a JSON file."""
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=2)

# Automatically load config when module is imported
CONFIG_PATH = Path(__file__).parent.parent.parent / "config.json"
try:
    config = Config.from_json(CONFIG_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")
except json.JSONDecodeError:
    raise ValueError(f"Invalid JSON in configuration file at {CONFIG_PATH}")