from plugin.commands.BaseCommand import Command
from database.DBManager import DBManager

from typing import List

class QueryDatabase(Command):
    def __init__(self, manager: DBManager, embeddings: List[float]):
        self._DBmanager = manager
        self._embeddings = embeddings

    def execute(self):
        return self._DBmanager.query(self._embeddings)
    