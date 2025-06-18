from infrastructure.git_service.git_diff import Diff
from infrastructure.git_service.git_repository import get_conflicted_files, git_add_to_staging
from infrastructure.llm.llm_client import LLMClient
from domain.chat import ChatSession
from cli.user_io import UserIO
from config.config import load_config
from domain.prompts import get_templated_prompt, RESOLVE_CONFLICT_SYSTEM_PROMPT, RESOLVE_CONFLICT_USER_PROMPT
from domain.response_structure import ConflictResolutionResponse, Status

import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Tuple, Dict
import json

class MergeConflictHandler:
    def __init__(self, path: str, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO):
        self.path = Path(path)
        if not self.path.is_absolute():
            self.path = Path.cwd() / self.path
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")
        
        self._files = get_conflicted_files(path)
        
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io

    def handle(self):
         
        system_prompt = RESOLVE_CONFLICT_SYSTEM_PROMPT

        self._chat_session.add_system_message(system_prompt)

        for file in self._files:

            with open(file, "r") as f:
                file_content = f.read()

            self._chat_session.add_user_message(RESOLVE_CONFLICT_USER_PROMPT.format(conflicted_code=file_content))

            response = self._llm_client.generate_structured_response(self._chat_session, ConflictResolutionResponse)

            if response.status == Status.RESOLVED and response.content:
                with open(file, "w") as f:
                    f.write(response.content)
                git_add_to_staging(file)
                self._user_io.display_success(f"Conflict in file {file} resolved!")
            elif response.status == Status.UNRESOLVED and response.reason:
                self._user_io.display_message(f"Could not resolve conflict in file {file}\nReason: {response.reason}")
            else:
                raise ValueError(f"Unexpected response status and data: {response.status}")

            self._chat_session.pop_last_message()