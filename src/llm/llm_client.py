from domain.chat import ChatSession

from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def generate_commit_message(self, chat_session: ChatSession) -> tuple[str, str]:
        pass