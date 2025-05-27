from llm.llm_client import LLMClient
from domain.chat import ChatSession

from ollama import Client
from typing import Tuple


class OllamaClient(LLMClient):
    def __init__(self, model: str = "qwen3-4B", host: str = "http://localhost:11434"):
        self.__model = model
        self.__client = Client(host=host)

    def generate_commit_message(self, chat_session: ChatSession) -> Tuple[str, str]:
        response = self.__client.chat(
            model=self.__model,
            messages=chat_session.to_dict_list()
        )
        print(response["message"]["content"])

        # content = response["message"]["content"]
        # # Parsing semplice del formato Titolo: ..., Corpo: ...
        # lines = content.strip().splitlines()
        # title = ""
        # body_lines = []
        # in_body = False

        # for line in lines:
        #     if line.lower().startswith("titolo:"):
        #         title = line.split(":", 1)[1].strip()
        #     elif line.lower().startswith("corpo:"):
        #         in_body = True
        #         body_lines.append(line.split(":", 1)[1].strip())
        #     elif in_body:
        #         body_lines.append(line.strip())

        # return title, "\n".join(body_lines).strip()
