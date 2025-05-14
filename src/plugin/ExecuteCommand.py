from plugin.BaseCommand import Command
from plugin.ResponseStructure import Response, ResponseCmd

import subprocess
import os
import sys
from colorama import Fore, Style


class ExecuteCommand(Command):
    def __init__(self, commands: Response):
        self._commands = commands

    def execSingleCommand(self, command: ResponseCmd):
        cmd = command.getCommandList()
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                shell=True,
                env={**os.environ, 'GIT_PAGER': 'cat'}
            )
            output, error = process.communicate()
            if output != b'':
                print("Output:\n", output.decode("utf-8"))
            elif error != b'':
                print(Fore.RED + "Error:\n" + error.decode("utf-8") + Style.RESET_ALL, file=sys.stderr)
        except Exception as e:
            sys.stderr.write("An exception has occurred: ", e)
            sys.exit(1)

    def execute(self):
        for command in self._commands:
            self.execSingleCommand(command)
