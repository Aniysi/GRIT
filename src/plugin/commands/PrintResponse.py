from plugin.commands.BaseCommand import Command
from plugin.utils.ResponseStructure import Response, ResponseCmd

from colorama import Fore, Style

class PrintResponse(Command):
    def __init__(self, resp: Response):
        self._response = resp
    
    def execute(self):
        print(Fore.GREEN + "LLM: " + Style.RESET_ALL + self._response.explanation + "\n\nCommands:")
        for command in self._response.commands:
            print(" - ", command.command)