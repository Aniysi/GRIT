from pydantic import BaseModel
from dataclasses import asdict
import json
import re


class Response(BaseModel):
    explanation: str
    command: str

    def toJson(self) -> str:
        return json.dumps(self.dict(), indent=2, ensure_ascii=False)
    
    def getCmdString(self) -> str:
        parts = self.command.strip().split()
        result = []
        i = 0
        while i < len(parts):
            part = parts[i]
            # Match --flag=value
            match = re.match(r'(--[a-zA-Z0-9\-]+)=(.+)', part)
            if match:
                flag, value = match.groups()
                # Inizia ad accumulare i "valori", potenzialmente multipli
                values = [value]
                i += 1
                # Continua ad aggiungere finché non trovi un nuovo flag
                while i < len(parts) and not parts[i].startswith('--'):
                    values.append(parts[i])
                    i += 1
                full_value = ' '.join(values)
                # Aggiungi virgolette solo se non già presenti
                if not (full_value.startswith('"') and full_value.endswith('"')):
                    full_value = f'"{full_value}"'
                result.append(f"{flag}={full_value}")
            else:
                result.append(part)
                i += 1
        return ' '.join(result)

           

