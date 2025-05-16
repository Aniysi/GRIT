from plugin.commands.BaseCommand import Command

from enum import Enum

class Role(Enum):
    system = 1
    user = 2
    assistant = 3

class CreateMessage(Command):
    def __init__(self, role: Role, prompt: str, context: str = ""):
        self.__role = role
        self.__prompt = prompt
        self.__context = context
    
    def execute(self):
        if self.__context == "":
            return {
                "role": self.__role.name,
                "content": self.__prompt + "/no_think"
            }
        else:
            polished_context = self.__context.replace("np.float64", "")
            return {
                "role": self.__role.name,
                "content": f"Context:\n{polished_context}\n\nQuery:\n{self.__prompt}"
            }

        