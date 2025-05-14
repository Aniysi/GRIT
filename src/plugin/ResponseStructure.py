from pydantic import BaseModel
from typing import List
from dataclasses import asdict
import json

class ResponseCmd(BaseModel):
        command: str

        def getCommandList(self):
                return self.command.split()

class Response(BaseModel):
    explanation: str
    commands: List[ResponseCmd]

    def toJson(self) -> str:
        return json.dumps(self.dict(), indent=2, ensure_ascii=False)

           

