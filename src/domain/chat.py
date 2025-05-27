from domain.git_diff import Diff

from enum import Enum

class Role(str, Enum):
    user = 1
    system = 2
    assistant = 3

class ChatMessage:
    def __init__(self, role: Role, content: str):
        self._role = role
        self._content = content

    def to_dict(self):
        return {
            "role": self._role.name,
            "content": self._content
        }
    
class ChatSession:
    def __init__(self):
        self._messages: list[ChatMessage] = []

    def add_user_message(self, content: str):
        self._messages.append(ChatMessage(role=Role.user, content=content))

    def add_system_message(self, content: str):
        self._messages.append(ChatMessage(role=Role.system, content=content))

    def add_assistant_message(self, content: str):
        self._messages.append(ChatMessage(role=Role.assistant, content=content))

    def add_first_message(self, content: str):
        self.add_system_message(content)

    def add_diff_message(self, diff: Diff):
        self.add_user_message(f"Questo è il Git diff dei file attualmente nell'area di staging:\n\n {diff}")

    def to_dict_list(self):
        return [m.to_dict() for m in self._messages]
