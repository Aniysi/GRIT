from domain.response_structure import CommitMsg

from git import Repo
import os

#TODO: make it a context builder derived from IContextBuilder
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
    
def create_custom_commit(commit: CommitMsg, repo_path: str = os.getcwd()) -> bool:
    try:
        repo = Repo(repo_path)
        if not repo.git_dir:
            raise ValueError(f"'{repo_path}' is not a Git repository")
        
        # Create the commit with the provided title and message
        repo.index.commit(f"{commit.title}\n\n{commit.body}")
        return True
    except Exception as e:
        raise ValueError(f"Error creating commit in repository at '{repo_path}': {str(e)}")
        