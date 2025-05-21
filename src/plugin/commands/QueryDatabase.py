from plugin.commands.BaseCommand import Command
from database.DBManager import DBManager

from typing import List

class QueryDatabase(Command):
    def __init__(self, manager: DBManager, embeddings: List[float]):
        if not isinstance(manager, DBManager):
            raise TypeError(f"Param manager must be a DBmanager object, not {type(manager)}")
        if embeddings is None:
            raise ValueError("Param embeddings cannot be None")
        self._DBmanager = manager
        self._embeddings = embeddings

    def execute(self):
        return self._DBmanager.query(self._embeddings)
    