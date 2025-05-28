from cli.user_io import UserIO
from application.commit_conversation_handler import CommitConversationHandler
from llm.ollama_client import OllamaClient
from domain.chat import ChatSession

import typer

app = typer.Typer()

@app.command()
def cmd():
    typer.echo(f"Generazione comando")

@app.command()
def commit():

    llm_client = OllamaClient()
    chat_session = ChatSession()
    user_io = UserIO()

    handler = CommitConversationHandler(llm_client, chat_session, user_io)
    handler.handle()


if __name__ == "__main__":
    app()
