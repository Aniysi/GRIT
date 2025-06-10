from infrastructure.llm.llm_client import LLMClient
from domain.chat import ChatSession
from domain.response_structure import LLMResponse, GitCommand, ImpactAnalisys
from config.config import load_config

from ollama import Client
from typing import Tuple


class OllamaClient(LLMClient):
    def __init__(self):
        config = load_config()
        self.__model = config['ollama']['model']
        self.__client = Client(host=config['ollama']['host'])

    def generate_commit_message(self, chat_session: ChatSession) -> LLMResponse:
        response = self.__client.chat(
            model=self.__model,
            messages=chat_session.to_dict_list(),
            format=LLMResponse.model_json_schema()
        )
        response = LLMResponse.model_validate_json(response.message.content)
        return response
    
    def generate_cmd(self, chat_session: ChatSession) -> GitCommand:
        response = self.__client.chat(
            model=self.__model,
            messages=chat_session.to_dict_list(),
            format=GitCommand.model_json_schema()
        )
        response = GitCommand.model_validate_json(response.message.content)
        return response
    
    def generate_impact_report(self, chat_session: ChatSession) -> str:
        response = self.__client.chat(
            model=self.__model,
            messages=chat_session.to_dict_list(),
            format=ImpactAnalisys.model_json_schema()
        )
        response = ImpactAnalisys.model_validate_json(response.message.content)
        return response