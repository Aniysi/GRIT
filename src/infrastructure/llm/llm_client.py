from domain.chat import ChatSession
from typing import Type, TypeVar
from pydantic import BaseModel

from abc import ABC, abstractmethod

T = TypeVar('T', bound=BaseModel)

class LLMClient(ABC):
    @abstractmethod
    def generate_structured_response(self, chat_session: ChatSession, response_type: Type[T]) -> T:
        """Generate a structured response with JSON schema validation."""
        pass