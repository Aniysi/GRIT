from plugin.BaseCommand import Command

import sys
from colorama import Fore, Style

class GetInput(Command):

    def execute(self):
        print(Fore.YELLOW + ">>>" + Style.RESET_ALL , end=" ")
        query = input()

        if query.startswith("/exec"):
            return None, 1
        elif query.startswith("/retry"):
            return query[7:], 0
        elif query.startswith("/quit"):
            sys.exit(0)
        elif query.startswith("/"):
            sys.stderr.write("Unknown command")
            sys.exit(1)
        else:
            return query, 0