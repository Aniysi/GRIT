from dataclasses import dataclass
from enum import Enum

class CommandType(Enum):
    EXEC = "exec"
    REFINE = "refine" 
    FIX = "fix"
    QUIT = "quit"
    REGULAR = "regular"

@dataclass
class ParsedCLICommand:
    command_type: CommandType
    content: str=""

class CommandParser:
    def parse(self, user_input: str) -> ParsedCLICommand:
        stripped_input = user_input.strip()

        if not stripped_input:
            return ParsedCLICommand(CommandType.REGULAR, "")
            
        if stripped_input.lower() == "/quit":
            return ParsedCLICommand(CommandType.QUIT)
            
        if stripped_input.lower() == "/exec":
            return ParsedCLICommand(CommandType.EXEC)
            
        if stripped_input.lower() == "/fix":
            return ParsedCLICommand(CommandType.FIX)
            
        if stripped_input.lower().startswith("/refine "):
            refinement = stripped_input[8:].strip()  # Remove "/refine "
            return ParsedCLICommand(CommandType.REFINE, refinement)
        
        # Handle regular text input
        return ParsedCLICommand(CommandType.REGULAR, stripped_input)
