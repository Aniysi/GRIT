from dataclasses import dataclass
import json
from pathlib import Path
from typing import Type


@dataclass
class Config:
    model_name: str

    @classmethod
    def from_json(cls: Type["Config"], json_path: str | Path) -> "Config":
        """Load configuration from a JSON file, prompting user if needed."""
        json_path = Path(json_path)

        if not json_path.exists():
            print(f"[INFO] Config file '{json_path}' does not exist. It will be created.")
            config_dict = {}
        else:
            with open(json_path, 'r') as f:
                config_dict = json.load(f)

        required_fields = ['model_name']
        was_updated = False

        for field in required_fields:
            if field not in config_dict or not config_dict[field]:
                config_dict[field] = input(f"Enter {field.replace('_', ' ')}: ")
                was_updated = True

        if was_updated:
            with open(json_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            print(f"[INFO] Configuration saved to '{json_path}'")

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