from pydantic import BaseModel
from typing import List

class ResponseCmd(BaseModel):
        command: str

class Response(BaseModel):
    explanation: str
    commands: List[ResponseCmd]