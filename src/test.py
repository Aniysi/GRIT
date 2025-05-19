def quote_flag_values(command: str) -> str:
    parts = command.strip().split()
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

import os
import subprocess
from colorama import Fore, Style
import sys
import re

cmd = 'git log --author="Leo" --pretty=format:%h %an %s --since="1 week ago"'
cleaned = quote_flag_values(cmd)
print(cleaned)
result = subprocess.run(
    cleaned,
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE,
    shell=True,
    text=True,
    env={**os.environ, 'GIT_PAGER': 'cat'}
)
output = result.stdout
error = result.stderr
if output:
    print(Fore.BLUE + "Output:" + Style.RESET_ALL + "\n" + output)
if error:
    print(Fore.RED + "Error:\n" + error + Style.RESET_ALL, file=sys.stderr)
