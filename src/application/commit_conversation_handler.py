from infrastructure.git_repository import get_staged_diff, create_custom_commit
from llm.llm_client import LLMClient
from domain.chat import ChatSession
from cli.user_io import UserIO
from domain.prompts import GIT_COMMIT_SYSTEM_PROMPT
from domain.git_diff import Diff

class CommitConversationHandler():
    def __init__(self, llm_client: LLMClient, chat_session: ChatSession, user_io: UserIO):
        self._llm_client = llm_client
        self._chat_session = chat_session
        self._user_io = user_io

    def prepare(self):
        # Add first message to session
        self._chat_session.add_first_message(GIT_COMMIT_SYSTEM_PROMPT)

        # Get git diff in cleaned string format
        raw_diff = get_staged_diff()
        diff = Diff(raw_diff)

        # Add diff message
        self._chat_session.add_diff_message(diff)
        #print(chat_session.to_dict_list(), "\n\n\n")

    def handle(self):
        self.prepare()

        while (True):
            # Get llm response
            response = self._llm_client.generate_commit_message(self._chat_session)
            self._chat_session.add_assistant_message(str(response))

            if response.mode == "commit":
                if self._user_io.confirm(str(response.commit)):
                    #create_custom_commit(response.commit)
                    quit()
                else:
                    user_response = self._user_io.ask_new_info()
                    self._chat_session.add_user_message(user_response)
            elif response.mode == "question":
                user_response = self._user_io.ask(str(response.question))
                self._chat_session.add_user_message(user_response)
            else:
                raise ValueError(f"Unexpected response mode: {response.mode}")
            

