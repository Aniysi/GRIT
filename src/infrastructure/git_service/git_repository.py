from domain.response_structure import CommitMsg

from git import Repo
import os
from pathlib import Path

def get_remote_head_hash(repo_path: str = os.getcwd()) -> str:
    try:
        repo = Repo(repo_path)
        if not repo.git_dir:
            raise ValueError(f"'{repo_path}' is not a Git repository")
        
        # Ottieni l'hash del commit remoto
        remote_head_hash = repo.git.rev_parse("@{u}")
        return remote_head_hash
    except Exception as e:
        raise ValueError(f"Error getting remote head hash: {str(e)}")

def get_file_annotate(commit_hash: str, file_path: Path, repo_path: str = os.getcwd()):
    repo = Repo(repo_path)
    if not repo.git_dir:
        raise ValueError(f"'{repo_path}' is not a Git repository")
    
    try:
        # Get the git blame/annotate information for the file at the specific commit
        annotate_output = repo.git.annotate(commit_hash, str(file_path))
        return annotate_output
    except Exception as e:
        raise ValueError(f"Error getting file annotation for '{file_path}' at commit '{commit_hash}': {str(e)}")
    
def get_file_from_hash(commit_hash: str, file_path: Path, repo_path: str = os.getcwd()):
    try:
        repo = Repo(repo_path)
        if not repo.git_dir:
            raise ValueError(f"'{repo_path}' is not a Git repository")
        
        # Get the repository root as a Path object
        repo_root = Path(repo_path)
        
        # Ensure the file path is relative to the repository root
        if file_path.is_absolute():
            relative_file_path = file_path.relative_to(repo_root)
        else:
            relative_file_path = file_path
        
        # Convert to POSIX format (Unix separators) for Git
        git_file_path = relative_file_path.as_posix()
        
        # Get the file content at the specific commit
        file_content = repo.git.show(f"{commit_hash}:{git_file_path}")
        return file_content
    except Exception as e:
        raise ValueError(f"Error getting file content for '{file_path}' at commit '{commit_hash}': {str(e)}")
    
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
