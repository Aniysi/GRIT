from pydantic import BaseModel
from typing import Literal, Optional
from enum import Enum


class Mode(str, Enum):
    COMMIT = "commit"
    QUESTION = "question"

class CommitMsg(BaseModel):
    title: str
    body: str

    def __str__(self) -> str:
        return f"Commit title: {self.title}\nCommit body: {self.body}"
    

class Questions(BaseModel):
    questions: list[str]

    def __str__(self) -> str:
        if not self.questions:
            return "Nessuna domanda disponibile."
        return "Domande per l'utente:\n" + "\n".join(
            [f"{i + 1}. {q}" for i, q in enumerate(self.questions)]
        )

class LLMResponse(BaseModel):
    mode: Mode
    commit: Optional[CommitMsg] = None
    questions: Optional[Questions] = None

    def __str__(self) -> str:
        if self.mode == "commit":
            return str(self.commit)
        elif self.mode == "question":
            return str(self.questions)
        
class GitCommand(BaseModel):
    explanation: str
    command: str

    def __str__(self) -> str:
        return f"Explanation: {self.explanation}\nCommand: {self.command}"