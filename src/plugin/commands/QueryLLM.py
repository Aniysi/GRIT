from plugin.commands.BaseCommand import Command
from plugin.utils.ResponseStructure import Response
import json
import ollama

class QueryLLM(Command):
    def __init__(self, model: str, messages):
        if not messages:
            raise ValueError("Messages cannot be empty")
            
        self._model = model
        self._messages = messages

    def execute(self):
        ollama_response = ollama.chat(
            model=self._model,
            messages=self._messages,
            format=Response.model_json_schema(),
        )
        return Response.model_validate_json(ollama_response.message.content)