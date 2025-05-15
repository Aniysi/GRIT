from pydantic import BaseModel
from typing import List
from dataclasses import asdict
import json
import re

class ResponseCmd(BaseModel):
        command: str

        # TODO: Make sure the first split doesn't split inside of ""
        def getCommandList(self):
                args = self.command.split()
                # Flag noti che non devono contenere virgolette esterne
                regex_flags = ['--author', '--committer', '--grep']

                cleaned_args = []
                for arg in args:
                    for flag in regex_flags:
                        if arg.startswith(flag + '='):
                            # Estraggo il valore
                            value = arg.split('=', 1)[1]
                            # Rimuovo virgolette solo se racchiudono l'intero valore
                            if re.match(r'^".*"$', value) or re.match(r"^'.*'$", value):
                                value = value[1:-1]
                            cleaned_args.append(f"{flag}={value}")
                            break
                    else:
                        # Lascia gli altri argomenti invariati (es. --pretty=format:"%h %an")
                        cleaned_args.append(arg)

                return cleaned_args


class Response(BaseModel):
    explanation: str
    commands: List[ResponseCmd]

    def toJson(self) -> str:
        return json.dumps(self.dict(), indent=2, ensure_ascii=False)

           

