from git import Repo
import os

def get_staged_diff(repo_path: str = os.getcwd()) -> str:
    try:
        repo = Repo(repo_path)
        if not repo.git_dir:
            raise ValueError(f"'{repo_path}' is not a Git repository")
        
        # Get diff between HEAD and index (staged files)
        diff_text = repo.git.diff('--cached')
        return diff_text
    except Exception as e:
        raise ValueError(f"Error accessing Git repository at '{repo_path}': {str(e)}")