import signal
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
import sys

console = Console()

class UserIO:    
    def ask_query(self) -> str:
        return console.input("[blue]❯ [/blue]").strip()
    
    def display_message(self, message: str) -> None:
        console.print(message)
    
    def display_error(self, error: str) -> None:
        console.print(f"[red]❌ {error}[/red]")
        
    def display_success(self, message: str) -> None:
        console.print(f"[green]{message}[/green]")
        
    def display_output(self, output: str) -> None:
        console.print(Panel(output, title="Output", border_style="blue"))
    
    def display_question(self, question: str):
        console.print(Panel(question, border_style="cyan", width=80))

    def display_cmd_help(self) -> None:
        help_text = """
[bold cyan]Available commands:[/bold cyan]
• [yellow]/exec[/yellow] - Executes the generated command
• [yellow]/refine <corrections>[/yellow] - Refines the command with new specifications
• [yellow]/fix[/yellow] - Fixes the command after an execution error
• [yellow]/quit[/yellow] - Exits the program
• [yellow]/help[/yellow] - Shows this help

Simply type your request to generate a new command.
        """
        
        console.print(Panel(help_text, border_style="cyan"))

    def display_commit_help(self) -> None:
        help_text = """
[bold cyan]Available commands:[/bold cyan]
• [yellow]/commit[/yellow] - Commits all staged files using the generated messages
• [yellow]/refine <corrections>[/yellow] - Refines the command with new specifications
• [yellow]/quit[/yellow] - Exits the program
• [yellow]/help[/yellow] - Shows this help

Simply type your request to generate a new command.
        """
        
        console.print(Panel(help_text, border_style="cyan"))


