import os
from git import Repo

class Diff:
    def __init__(self):
        try:
            self.repo = Repo(os.getcwd())
            if not self.repo.git_dir:
                raise ValueError(f"'{os.getcwd()}' is not a Git repository")
        except Exception as e:
            raise ValueError(f"Error accessing Git repository: {str(e)}")
    
    def get_staged_diff(self) -> str:
        try:
            # Check if there are any staged files
            staged_files = self.repo.git.diff('--cached', '--name-only')
            if not staged_files.strip():
                raise ValueError("No files are currently staged for commit. Please stage files first using 'git add .'")
            
            return self.repo.git.diff('--cached')
        except Exception as e:
            raise ValueError(f"Error getting staged diff: {str(e)}")
    
    def get_file_diff(self, file_path: str, commit_hash: str = "HEAD") -> str:
        if not os.path.isfile(file_path):
            raise ValueError(f"File '{file_path}' does not exist or is not a valid file.")
        
        try:
            return self.repo.git.diff(commit_hash, '--cached', file_path)
        except Exception as e:
            raise ValueError(f"Error getting diff for file '{file_path}': {str(e)}")