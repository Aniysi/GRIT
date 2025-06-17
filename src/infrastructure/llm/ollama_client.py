from infrastructure.llm.llm_client import LLMClient
from domain.chat import ChatSession
from domain.response_structure import CommitResponse, GitCommand, ImpactAnalisys
from config.config import load_config

from ollama import Client
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class OllamaClient(LLMClient):
    def __init__(self):
        config = load_config()
        self.__model = config['ollama']['model']
        self.__client = Client(host=config['ollama']['host'])

    def generate_structured_response(self, chat_session: ChatSession, response_type: Type[T]) -> T:
        response = self.__client.chat(
            model=self.__model,
            messages=chat_session.to_dict_list(),
            format=response_type.model_json_schema()
        )
        return response_type.model_validate_json(response.message.content)
    
    def generate_response(self, chat_session: ChatSession) -> str:
        response = self.__client.chat(
            model=self.__model,
            messages=chat_session.to_dict_list(),
            stream=True
        )
        
        full_response = ""
        for chunk in response:
            content = chunk['message']['content']
            print(content, end='', flush=True)  # Print chunk immediately
            full_response += content
        
        print()  # Add newline after streaming is complete
        return full_response