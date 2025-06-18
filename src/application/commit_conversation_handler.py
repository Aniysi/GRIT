from infrastructure.git_service.git_repository import create_custom_commit
from infrastructure.llm.llm_client import LLMClient
from domain.chat import ChatSession
from cli.user_io import UserIO
from domain.prompts import GIT_COMMIT_SYSTEM_PROMPT, get_templated_prompt
from config.config import load_config
from infrastructure.git_service.git_diff import Diff
from domain.response_structure import Mode, CommitResponse
from cli.command_parser import CLICommandParser, CLICommandType
from application.cli_command_handlers.command_handlers import *

from typing import Dict


class CommitConversationHandler():
    def __init__(self, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO, parser: CLICommandParser):
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io
        self._parser = parser

        self._commit = {
            'commit_title': None,
            'commit_body': None
        }

        self._handlers: Dict[CLICommandType, CommandHandler] = {
            CLICommandType.QUIT: QuitHandler(user_io),
            CLICommandType.COMMIT: CommitHandler(user_io),
            CLICommandType.REFINE: RefineCommitHandler(llm_client, chat_session, user_io),
        }

    def prepare(self):

        # Get config 
        config=load_config()

        # Add first message to session
        self._chat_session.add_first_message(get_templated_prompt(GIT_COMMIT_SYSTEM_PROMPT, "[[language]]", config["output-language"]))

        # Get git diff in cleaned string format
        diff = Diff().get_staged_diff()

        # Add diff message
        self._chat_session.add_diff_message(diff)

    def handle(self):
        self.prepare()

        while (True):
            
             # Get llm response
            response = self._llm_client.generate_structured_response(self._chat_session, CommitResponse)
            self._chat_session.add_assistant_message(str(response))

            if response.mode == Mode.COMMIT:
                # Update commit dictionary
                self._commit['commit_title'] = response.commit.title
                self._commit['commit_body'] = response.commit.body

                # Display generated commit
                self._user_io.display_output(f"Commit title: {self._commit['commit_title']}\nCommit body: {self._commit['commit_body']}")

                # Get user query
                user_input = self._user_io.ask_query()

                # Parse and handle command
                parsed_command = self._parser.parse(user_input)
                handler = self._handlers[parsed_command.command_type]

                should_continue = handler.handle(parsed_command.content, self._commit)
                if not should_continue:
                    break
            elif response.mode == Mode.QUESTION:
                for i, question in enumerate(response.questions.questions):
                    user_response = self._user_io.ask(str(question))
                    self._chat_session.add_user_message(user_response)
            else:
                raise ValueError(f"Unexpected response mode: {response.mode}")
            

