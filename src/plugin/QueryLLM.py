from plugin.BaseCommand import Command
from plugin.ResponseStructure import Response
import json
import ollama

class QueryLLM(Command):
    def __init__(self, model: str, messages):
        self._model = model
        self._messages = self._format_messages(messages)

    def _format_messages(self, messages):
        formatted = []
        for msg in messages:
            message = {
                "role": msg["role"].lower(),
                "content": msg["prompt"]
            }
            if "context" in msg:
                # Clean up the context to be a readable string
                context = msg["context"].replace("np.float64", "")
                message["content"] = f"Context:\n{context}\n\nQuery:\n{msg['prompt']}"
            formatted.append(message)
        return formatted

    def execute(self):
        ollama_response = ollama.chat(
            model=self._model,
            messages=self._messages,
            format=Response.model_json_schema(),
        )
        return Response.model_validate_json(ollama_response.message.content)