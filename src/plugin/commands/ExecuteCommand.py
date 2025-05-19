from plugin.commands.BaseCommand import Command
from plugin.utils.ResponseStructure import Response

import subprocess
import os
import sys
from colorama import Fore, Style


class ExecuteCommand(Command):
    def __init__(self, command: Response):
        self._command = command

    def execute(self):
        cmd = self._command.getCmdString()
        print(cmd)
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                env={**os.environ, 'GIT_PAGER': 'cat'}
            )
            output = result.stdout
            error = result.stderr
            if output:
                print(Fore.BLUE + "Output:" + Style.RESET_ALL + "\n" + output)
            if error:
                print(Fore.RED + "Error:\n" + error + Style.RESET_ALL, file=sys.stderr)
            return result
        except Exception as e:
            sys.stderr.write("An exception has occurred: ", e)
            sys.exit(1)

