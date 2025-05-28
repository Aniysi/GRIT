from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

class UserIO:
    def ask(self, question: str) -> str:
        console.print(Panel(question, border_style="cyan", width=80))
        return console.input("[blue]❯ [/blue]")

    def confirm(self, commit_data: str) -> bool:
        console.print(Panel(commit_data, title="[green]Messaggio di commit generato[/green]", border_style="green"))

        if Confirm.ask("[blue]💬 Vuoi effettuare il commit?[/blue]"):
            console.print("[green]✅ Commit confermato.[/green]")
            return True
        else:
            console.print("[yellow]⚠️  Operazione annullata.[/yellow]")
            return False

    def ask_new_info(self) -> str:
        return Prompt.ask("[cyan]✏️  Fornisci nuove direttive[/cyan]")

