import signal
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
import sys

console = Console()

class UserIO:
    # TODO: improve commit cli interaction
    def _check_quit(self, input_str: str) -> None:
        if input_str.strip().lower() == "/quit":
            console.print("[yellow]👋 Programma terminato.[/yellow]")
            exit(0)

    def ask(self, question: str) -> str:
        console.print(Panel(question, border_style="cyan", width=80))
        response = console.input("[blue]❯ [/blue]")
        self._check_quit(response)
        return response

    def confirm(self, commit_data: str) -> bool:
        console.print(Panel(commit_data, title="[green]Messaggio di commit generato[/green]", border_style="green"))

        response = Confirm.ask("[blue]💬 Vuoi effettuare il commit?[/blue]")
        self._check_quit(str(response))
        
        if response:
            console.print("[green]✅ Commit confermato.[/green]")
            return True
        else:
            console.print("[yellow]⚠️  Operazione annullata.[/yellow]")
            return False

    def ask_new_info(self) -> str:
        response = Prompt.ask("[cyan]✏️  Fornisci nuove direttive[/cyan]")
        self._check_quit(response)
        return response
    
    def ask_query(self) -> str:
        response = console.input("[blue]❯ [/blue]")
        self._check_quit(response)
        return response
    
    def ask_query(self) -> str:
        return console.input("[blue]❯ [/blue]").strip()
    
    def display_message(self, message: str) -> None:
        console.print(message)
    
    def display_error(self, error: str) -> None:
        console.print(f"[red]❌ {error}[/red]")
        
    def display_success(self, message: str) -> None:
        console.print(f"[green]✅ {message}[/green]")
        
    def display_output(self, output: str) -> None:
        console.print(Panel(output, title="Output", border_style="blue"))
    
    def display_help(self) -> None:
        help_text = """
[bold cyan]Comandi disponibili:[/bold cyan]
• [yellow]/exec[/yellow] - Esegue il comando generato
• [yellow]/refine <correzioni>[/yellow] - Raffina il comando con nuove specifiche
• [yellow]/fix[/yellow] - Corregge il comando dopo un errore di esecuzione
• [yellow]/quit[/yellow] - Esce dal programma
• [yellow]help[/yellow] - Mostra questo aiuto

Digita semplicemente la tua richiesta per generare un nuovo comando.
        """
        console.print(Panel(help_text, border_style="cyan"))


