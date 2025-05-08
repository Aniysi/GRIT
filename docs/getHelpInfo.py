import subprocess
import re
import os
import fitz
from pathlib import Path
import json

def get_git_help_text(command):
    process = subprocess.Popen(
        ['git', command, '-h'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=True,
        env={**os.environ, 'GIT_PAGER': 'cat'}  # Forza l'output su stdout
    )
    output, error = process.communicate()
    if "not a git command" in error.decode('utf-8') or "not a git command" in output.decode('utf-8'):
        command = command.replace(" ", "-")
        process = subprocess.Popen(
        ['git', command, '-h'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=True,
        env={**os.environ, 'GIT_PAGER': 'cat'}  # Forza l'output su stdout
    )
    output, error = process.communicate()
    # print(f"Git command execution: {output.decode('utf-8') if output else 'No output'}")
    # print(f"Error: {error.decode('utf-8') if error else 'No error'}")
    return error.decode('utf-8') if error else (output.decode('utf-8') if output else None)


def elaborate_text(help_text):
    elaborated_text = ""
    for line in help_text.splitlines():
        elaborated_text += line.replace("    ", "", 1) + "\n" # Replace first occurrence of 4 spaces
    return elaborated_text
    

def parse_git_command(command, pdf_path):
    help_text = get_git_help_text(command)
    if not help_text:
        return None
    usage = elaborate_text(help_text)
    doc = fitz.open(pdf_path)
    description = ""
    text = ""
    for page in doc:
        text += page.get_text()
        if "DESCRIPTION" in text and "OPTIONS" in text:
            start_idx = text.find("DESCRIPTION\n") + len("DESCRIPTION\n")
            end_idx = text.find("OPTIONS")
            description = text[start_idx:end_idx].strip() if end_idx != -1 else text[start_idx:].strip()
            break
    # print(f"Usage: {usage}")
    # print(f"Description: {description}")
    return {
        "command": f"git {command}",
        "description": description,
        "usage": usage
    }

def save_json(data, json_dir_path=Path(os.getcwd(), "jsondocs")):
    if data:
        # Try to load existing data from the JSON file
        json_file = Path(json_dir_path, data['command'].replace(" ", "-") + ".json")
        commands_list = []
        
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as file:
                    commands_list = json.load(file)
            except json.JSONDecodeError:
                commands_list = []
        
        # Add new command if it's not already in the list
        commands_list.append(result)
        
        # Save updated list back to JSON file
        with open(json_file, 'w') as f:
            json.dump(commands_list, f, indent=4)


# Walk through current directory and subdirectories
for root, dirs, files in os.walk(Path(os.getcwd(), "pdfdocs")):
    for file in files:
        if file.startswith('git-') and file.endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            command = file.replace('.pdf', '').replace('git-', '').replace('-', ' ')
            result = parse_git_command(command, pdf_path)
            save_json(result)
