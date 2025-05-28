from pydantic import BaseModel
from typing import Literal, Optional

class CommitMsg(BaseModel):
    title: str
    body: str

    def __str__(self) -> str:
        return f"Commit title: {self.title}\nCommit body: {self.body}"
    

class Question(BaseModel):
    question: str

    def __str__(self):
        return self.question

# TODO: make mode an enum
class LLMResponse(BaseModel):
    mode: Literal["commit", "question"]
    commit: Optional[CommitMsg] = None
    question: Optional[Question] = None

    def __str__(self) -> str:
        if self.mode == "commit":
            return str(self.commit)
        elif self.mode == "question":
            return str(self.question)
