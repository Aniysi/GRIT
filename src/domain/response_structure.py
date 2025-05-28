from pydantic import BaseModel
from typing import Literal, Optional

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

# TODO: make mode an enum
class LLMResponse(BaseModel):
    mode: Literal["commit", "question"]
    commit: Optional[CommitMsg] = None
    questions: Optional[Questions] = None

    def __str__(self) -> str:
        if self.mode == "commit":
            return str(self.commit)
        elif self.mode == "question":
            return str(self.questions)
