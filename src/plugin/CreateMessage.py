from plugin.BaseCommand import Command

from enum import Enum

class Role(Enum):
    System = 1
    User = 2

class CreateMessage(Command):
    def __init__(self, role: Role, prompt: str, context: str = ""):
        self.__role = role
        self.__prompt = prompt
        self.__context = context
    
    def execute(self):
        if self.__context == "":
            return {
                "role": self.__role.name,
                "prompt": self.__prompt
            }
        else:
            return {
                "role": self.__role.name,
                "context": self.__context,
                "prompt": self.__prompt
            }

        