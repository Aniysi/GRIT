from cli.user_io import UserIO
from application.cmd_conversation_hanlder import CmdConversationHandler
from application.commit_conversation_handler import CommitConversationHandler
from application.commit_impact_handler import CommitImpactHandler
from application.merge_conflict_handler import MergeConflictHandler
from infrastructure.llm.ollama_client import OllamaClient
from domain.chat import ChatSession
from cli.command_parser import CLICommandParser
from infrastructure.embedding.chunkingLibs.recursive_token_chunker import RecursiveTokenChunker
from infrastructure.embedding.rag_pipeline_builder import QueryRAGPipelineBuilder
from infrastructure.database.database_manager import ChromaDBManager
from application.rag.rag_context_builder import RAGContextBuilder
from config.config import set_config_language, set_config_model

from pathlib import Path
import typer

app = typer.Typer()

@app.command()
def cmd():
    # Create dependencies for dependency injection
    llm_client = OllamaClient()
    chat_session = ChatSession()
    user_io = UserIO()
    parser = CLICommandParser()

    chunker = RecursiveTokenChunker(
        chunk_size = 400, 
        chunk_overlap = 0, 
        separators = ["\n\n\n", "\n\n", "\n", ".", " ", ""]
    )
    pipeline = QueryRAGPipelineBuilder().add_Chunker(chunker).add_Embedder('nomic-embed-text').build()
    db_path = Path(__file__).parent.parent.parent / "chroma_db"
    db_manager = ChromaDBManager(db_path, "git_commands")
    context_builder = RAGContextBuilder(pipeline, db_manager)

    # Handle conversation
    handler = CmdConversationHandler(llm_client, chat_session, user_io, context_builder, parser)
    handler.handle()
    
@app.command()
def commit():

    # Create dependencies for dependency injection
    llm_client = OllamaClient()
    chat_session = ChatSession()
    user_io = UserIO()
    parser = CLICommandParser()

    # Handle conversation
    handler = CommitConversationHandler(llm_client, chat_session, user_io, parser)
    handler.handle()#caccaboia

@app.command()
def impact(file_path: str = typer.Argument(..., help="Relative file path to analyze impact")):
    
    # Create dependencies for dependency injection
    llm_client = OllamaClient()
    chat_session = ChatSession()
    user_io = UserIO()

    handler = CommitImpactHandler(file_path, llm_client, chat_session, user_io)
    handler.handle()

@app.command()
def merge(path: str = typer.Argument(None, help="Path to file or directory to search for conflicts. If not provided, uses current directory")):

    # Set default to current directory if no path provided
    if path is None:
        path = "."

    # Create dependencies for dependency injection
    llm_client = OllamaClient()
    chat_session = ChatSession()
    user_io = UserIO()

    # Handle conversation
    handler = MergeConflictHandler(path, llm_client, chat_session, user_io)
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
