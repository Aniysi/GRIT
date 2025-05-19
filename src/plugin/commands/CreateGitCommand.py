from plugin.commands.CompositeCommand import CompositeCommand
from plugin.utils.states import State, InitialState

import os

GENERATION_LLM = "qwen3-4B"

class CreateGitCommand(CompositeCommand):
    def __init__(self):
        self._state = InitialState(self)
        self._messages = []

    def changeState(self, state: State):
        self._state = state

    def getMessages(self):
        return self._messages
    
    def deleteMessages(self):
        self._messages = []

    def execute(self):
        while True:
            self._state.handle()
            