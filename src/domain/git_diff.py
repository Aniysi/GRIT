import re

class Diff:

    def __init__(self, raw_diff: str):
        if not raw_diff:
            raise ValueError("No staged files to commit. Please add files you want to commit using 'git add ...'.")
        self.__raw = raw_diff

    def __str__(self) -> str:
        return self.__raw

    def cleaned(self) -> str:
        diff_text = self.__raw

        lines = diff_text.strip().splitlines()
        cleaned = []
        i = 0

        while i < len(lines):
            line = lines[i]

            if line.startswith('diff --git'):
                # Start of a new file diff
                match = re.match(r'diff --git a/(.+) b/(.+)', line)
                if match:
                    old_path, new_path = match.groups()
                    filename = new_path

                    # Look ahead to check for binary or null paths
                    lookahead = lines[i+1:i+6]
                    is_binary = any("Binary files" in l for l in lookahead)
                    is_added = any('--- /dev/null' in l for l in lookahead)
                    is_deleted = any('+++ /dev/null' in l for l in lookahead)

                    if is_binary:
                        cleaned.append(f"File binario modificato: {filename}")
                        # Skip all lines in this binary block
                        i += len(lookahead)
                        while i < len(lines) and not lines[i].startswith('diff --git'):
                            i += 1
                        continue
                    elif is_added:
                        cleaned.append(f"File aggiunto: {filename}")
                    elif is_deleted:
                        cleaned.append(f"File eliminato: {old_path}")
                    else:
                        cleaned.append(f"File modificato: {filename}")
            elif line.startswith('@@'):
                # Skip chunk header
                i += 1
                continue
            else:
                cleaned.append(line)

            i += 1

        return '\n'.join(cleaned)