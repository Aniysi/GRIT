from cli.user_io import UserIO
from application.commit_conversation_handler import CommitConversationHandler
from llm.ollama_client import OllamaClient
from domain.chat import ChatSession
from config.config import set_config_language, set_config_model

import typer

app = typer.Typer()

@app.command()
def cmd():
    typer.echo(f"Generazione comando")

@app.command()
def commit():

    # Create dependencies for dependency injection
    llm_client = OllamaClient()
    chat_session = ChatSession()
    user_io = UserIO()

    # Handle conversation
    handler = CommitConversationHandler(llm_client, chat_session, user_io)
    handler.handle()

@app.command()
def config(
    output_language: str = typer.Option("english", "--set-output-language", "-sl", help="Set output langauge"),
    model: str = typer.Option(None, "--set-model", "-sm", help="Set LLM model"),
):
    if output_language:
        set_config_language(output_language)
        typer.echo(f"Set language to {output_language}")

    if model:
        set_config_model(model)
        typer.echo(f"Set language to {model}")
    else:
        typer.echo(f"You must specify an existing Ollama model. To list avaible models use 'ollama list'")




if __name__ == "__main__":
    app()
