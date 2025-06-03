from dataclasses import dataclass
from enum import Enum

class CLICommandType(Enum):
    EXEC = "exec"
    REFINE = "refine" 
    FIX = "fix"
    QUIT = "quit"
    REGULAR = "regular"

@dataclass
class ParsedCLICommand:
    command_type: CLICommandType
    content: str=""

class CLICommandParser:
    def parse(self, user_input: str) -> ParsedCLICommand:
        stripped_input = user_input.strip()

        if not stripped_input:
            return ParsedCLICommand(CLICommandType.REGULAR, "")
            
        if stripped_input.lower() == "/quit":
            return ParsedCLICommand(CLICommandType.QUIT)
            
        if stripped_input.lower() == "/exec":
            return ParsedCLICommand(CLICommandType.EXEC)
            
        if stripped_input.lower() == "/fix":
            return ParsedCLICommand(CLICommandType.FIX)
            
        if stripped_input.lower().startswith("/refine "):
            refinement = stripped_input[8:].strip()  # Remove "/refine "
            return ParsedCLICommand(CLICommandType.REFINE, refinement)
        
        # Handle regular text input
        return ParsedCLICommand(CLICommandType.REGULAR, stripped_input)
