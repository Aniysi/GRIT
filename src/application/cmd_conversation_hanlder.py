from infrastructure.llm.llm_client import LLMClient
from cli.user_io import UserIO
from domain.chat import ChatSession
from application.rag.rag_context_builder import RAGContextBuilder
from config.config import load_config
from domain.prompts import get_templated_prompt, CREATE_COMMAND_SYSTEM_PROMPT
from cli.command_parser import CLICommandParser, CLICommandType
from application.cli_command_handlers.command_handlers import *
from domain.response_structure import GitCommand

from typing import Dict


class CmdConversationHandler():
    def __init__(self, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO, context_builder: RAGContextBuilder, parser: CLICommandParser):
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io
        self._context_builder = context_builder
        self._parser = parser

        self._context = {
            'last_generated_command': None,
            'last_execution_success': None,
            'last_execution_error': None
        }

        self._handlers: Dict[CLICommandType, CommandHandler] = {
            CLICommandType.QUIT: QuitHandler(user_io),
            CLICommandType.EXEC: ExecHandler(user_io),
            CLICommandType.REFINE: RefineCmdHandler(llm_client, chat_session, user_io),
            CLICommandType.FIX: FixHandler(llm_client, chat_session, user_io),
            CLICommandType.REGULAR: RegularHandler(llm_client, chat_session, user_io, context_builder)
        }

    def prepare(self):

        # Get config 
        config=load_config()

        # Add first message to session
        self._chat_session.add_first_message(get_templated_prompt(CREATE_COMMAND_SYSTEM_PROMPT, "[[language]]", config["output-language"]))        

    def handle(self):
        self.prepare()

        while True:
            try:
                user_input = self._user_io.ask_query()

                # Handle help command
                if user_input.lower() in ['/help', 'help', '?']:
                    self._user_io.display_cmd_help()
                    continue
                
                # Parse and handle command
                parsed_command = self._parser.parse(user_input)
                handler = self._handlers[parsed_command.command_type]
                
                should_continue = handler.handle(parsed_command.content, self._context)
                if not should_continue:
                    break
                
                # Get llm response
                response = self._llm_client.generate_structured_response(self._chat_session, GitCommand)
                self._chat_session.add_assistant_message(str(response))

            except KeyboardInterrupt:
                self._user_io.display_message("\n[yellow]Program terminated.[/yellow]")
                break
            except Exception as e:
                self._user_io.display_error(f"Unexpected error: {str(e)}")
                self._user_io.display_cmd_help()
