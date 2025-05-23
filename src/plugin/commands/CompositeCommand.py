from plugin.commands.BaseCommand import Command

from abc import abstractmethod
from typing import List

class CompositeCommand(Command):
    @abstractmethod
    def execute(self):
        pass