from cli.user_io import UserIO

import json
from pathlib import Path

def load_config():
    try:
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, "r") as f:
            config = json.load(f)
            if not config['ollama'] or not config['ollama']['model']:
                userIO = UserIO()
                userIO.display_error("Ollama model absent. Please provide an existing Ollama model name:")
                model = userIO.ask_query()
                config['ollama']['model'] = model
                save_config(config)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(
            f"config.json not found. Please create a config.json at {config_path.parent} with the following format:\n"
            "{\n"
            "   'ollama': {\n"
            "       'model': 'your-model-name',\n"
            "       'host': 'your-ollama-local-host',\n"
            "   }\n"
            "}\n"
        )

def save_config(config: dict):
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

def set_config_language(language: str):
    config = load_config()
    config["output-language"] = language
    save_config(config)

#TODO: check if model exists(?)
def set_config_model(model: str):
    config = load_config()
    config["ollama"]["model"] = model
    save_config(config)