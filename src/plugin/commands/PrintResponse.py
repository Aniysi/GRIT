from plugin.commands.BaseCommand import Command
from plugin.utils.ResponseStructure import Response

from colorama import Fore, Style

class PrintResponse(Command):
    def __init__(self, resp: Response):
        if not isinstance(resp, Response):
            raise TypeError(f"Param command must be a Response object, not {type(resp)}")
        self._response = resp
    
    def execute(self):
        print(Fore.GREEN + "LLM: " + Style.RESET_ALL + self._response.explanation)
        print("\n\nCommand: ", self._response.command)