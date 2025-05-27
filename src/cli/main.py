from application.commit_service import generate_commit
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

    generate_commit(llm_client, chat_session)
    typer.echo(f"Generazione commento di commit")


if __name__ == "__main__":
    app()
