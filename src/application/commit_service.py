from infrastructure.git_repository import get_staged_diff
from llm.llm_client import LLMClient
from domain.chat import ChatSession
from domain.prompts import GIT_COMMIT_SYSTEM_PROMPT
from domain.git_commit import Commit
from domain.git_diff import Diff


def generate_commit(llm_client: LLMClient, chat_session: ChatSession) -> Commit:

    # Add first message to session
    chat_session.add_first_message(GIT_COMMIT_SYSTEM_PROMPT)

    # Get git diff in cleaned string format
    raw_diff = get_staged_diff()
    diff = Diff(raw_diff)

    # Add diff message
    chat_session.add_diff_message(diff)
    print(chat_session.to_dict_list(), "\n\n\n")

    llm_client.generate_commit_message(chat_session)
    # return Commit(title, body)