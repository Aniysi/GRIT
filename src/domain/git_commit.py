from pydantic import BaseModel

class CommitMsg(BaseModel):
    title: str
    body: str

    def __str__(self) -> str:
        return f"Commit title: {self.title}\nCommit body: {self.body}"
