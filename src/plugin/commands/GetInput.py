from plugin.commands.BaseCommand import Command

import sys
from colorama import Fore, Style

class GetInput(Command):

    def execute(self):
        print(Fore.YELLOW + ">>>" + Style.RESET_ALL , end=" ")
        query = input()
        if query == "/quit":
            sys.exit(0)
        return query