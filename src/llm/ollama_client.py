from llm.llm_client import LLMClient
from domain.chat import ChatSession
from domain.response_structure import LLMResponse

from ollama import Client
from typing import Tuple


class OllamaClient(LLMClient):
    def __init__(self, model: str = "qwen3-4B", host: str = "http://localhost:11434"):
        self.__model = model
        self.__client = Client(host=host)

    def generate_commit_message(self, chat_session: ChatSession) -> Tuple[str, str]:
        response = self.__client.chat(
            model=self.__model,
            messages=chat_session.to_dict_list(),
            format=LLMResponse.model_json_schema()
        )
        response = LLMResponse.model_validate_json(response.message.content)
        return response
