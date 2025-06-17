from infrastructure.git_service.git_diff import Diff
from infrastructure.git_service.git_repository import get_remote_head_hash, get_file_annotate, get_file_from_hash
from infrastructure.llm.llm_client import LLMClient
from domain.chat import ChatSession
from cli.user_io import UserIO
from config.config import load_config
from domain.prompts import get_templated_prompt, GIT_IMPACT_SYSTEM_PROMPT, GIT_IMPACT_USER_MESSAGE
from domain.response_structure import ImpactAnalisys

import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Tuple, Dict
import json

class CommitImpactHandler:
    def __init__(self, file: str, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO):
        self._file_path = Path(file)
        if not self._file_path.is_absolute():
            self._file_path = Path.cwd() / self._file_path
        if not self._file_path.exists():
            raise FileNotFoundError(f"File not found: {self._file_path}")
        
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io

    def parse_diff_changes(self) -> list[str]:
        lines = self._diff.split('\n')
        removed_lines = []
        for line in lines:
            if line.startswith('-') and not line.startswith('---'):
                removed_lines.append(line[1:])
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                if line[1:] in removed_lines:
                    removed_lines.remove(line[1:])
        return removed_lines

    def parse_annotate_line(self, line: str) -> Tuple[str, str, datetime, int, str, int]:
        # Regex pattern to retrive data
        pattern = r'^([a-f0-9]+)\s+\(\s*(.+?)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+([+-]\d{4})\s+(\d+)\)\s*(.*)$'
        
        match = re.match(pattern, line)
        if match:
            commit_hash = match.group(1)
            author = match.group(2)
            date_time_str = match.group(3)
            timezone_str = match.group(4)
            line_number = int(match.group(5))
            content = match.group(6)
            
            # Parse timestamp
            dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            
            # Parse time zone
            tz_sign = 1 if timezone_str[0] == '+' else -1
            tz_hours = int(timezone_str[1:3])
            tz_minutes = int(timezone_str[3:5])
            
            # Create time zone offset
            tz_offset = timedelta(hours=tz_sign * tz_hours, minutes=tz_sign * tz_minutes)
            
            # Apply time zone offset
            dt_with_tz = dt.replace(tzinfo=timezone(tz_offset))
            
            # UTC conversion
            timestamp_utc = dt_with_tz.astimezone(timezone.utc)
            
            age_days = (datetime.now(timezone.utc) - timestamp_utc).days
            return commit_hash, author, timestamp_utc, line_number, content, age_days
        else:
            raise ValueError(f"Cannot parse annotate line: {line}")

    def get_altered_commits_info(self, annotate: str, removed_lines: list[str]) -> list[Dict]:
        annotate_lines = annotate.split("\n")
        commits = []
        
        for line in annotate_lines:
            if line.strip():
                try:
                    # Controlla se questa riga contiene qualsiasi delle righe rimosse
                    contains_removed_line = any(removed_line.strip() in line for removed_line in removed_lines)
                    
                    if contains_removed_line:
                        commit_hash, author, timestamp, line_number, content, age_days = self.parse_annotate_line(line)
                        commits.append({
                            'line_number': line_number,
                            'current_line': content,
                            'author': author,
                            'last_modified': timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'),
                            'age_days': age_days,
                            'commit_hash': commit_hash,
                        })
                except ValueError as e:
                    print(f"Warning: {e}")
                    continue
        #print(json.dumps(commits, indent=2))
        return commits

    def get_info(self, hash):
        
        # Get changes from remote head and parse them to capture all modified lines
        self._diff = Diff().get_file_diff(self._file_path, hash)
        removed_lines = self.parse_diff_changes()
        # print(removed_lines)

        # Retrive remote head file blame
        annotate = get_file_annotate(hash, self._file_path)
        # print(annotate)

        return self.get_altered_commits_info(annotate, removed_lines)

    def handle(self):
        # Get config
        config = load_config()

        # Add first message to session
        self._chat_session.add_first_message(
            get_templated_prompt(GIT_IMPACT_SYSTEM_PROMPT, "[[language]]", config["output-language"])
        )

        # Read and format the current version of the file
        with open(self._file_path, "r", encoding="utf-8") as file:
            current_file_content = file.read()

        # Get remote head hash to compare changes
        hash = get_remote_head_hash()

        # Get remote file
        remote_file_content = get_file_from_hash(hash, self._file_path)

        # Get line info
        modified_lines_metadata = self.get_info(hash)

        user_message = get_templated_prompt(
            GIT_IMPACT_USER_MESSAGE, 
            ["[[current_file_content]]", "[[remote_file_content]]", "[[modified_lines_metadata]]"],
            [current_file_content, remote_file_content, json.dumps(modified_lines_metadata, indent=2)])

        self._chat_session.add_user_message(user_message)

        response = self._llm_client.generate_structured_response(self._chat_session, ImpactAnalisys)

        self._user_io.display_output(str(response))

