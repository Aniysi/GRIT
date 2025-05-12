from plugin.BaseCommand import Command

from abc import abstractmethod
from typing import List

class CompositeCommand(Command):
    def __init__(self):
        self._commands: List[Command] = []

    def add_command(self, cmd: Command) -> None:
        self._commands.appen(cmd)

    def remove_command(self, cmd: Command) -> None:
        self._commands.remove(cmd)

    @abstractmethod
    def execute(self):
        pass