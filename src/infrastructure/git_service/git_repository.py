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
    
def create_custom_commit(commit_title: str, commit_body: str, repo_path: str = os.getcwd()) -> bool:
    try:
        repo = Repo(repo_path)
        if not repo.git_dir:
            raise ValueError(f"'{repo_path}' is not a Git repository")
        
        # Create the commit with the provided title and message
        repo.index.commit(f"{commit_title}\n\n{commit_body}")
        return True
    except Exception as e:
        raise ValueError(f"Error creating commit in repository at '{repo_path}': {str(e)}")

def get_conflicted_files(path: str = None) -> list[Path]:
    if path is None:
        path = Path.cwd()
    else:
        path = Path(path)
    
    try:
        if path.is_file():
            repo = Repo(path.parent)
            if not repo.git_dir:
                raise ValueError(f"'{path.parent}' is not a Git repository")
            
            # Get all conflicted files
            conflicted_files_output = repo.git.ls_files(u=True)
            if not conflicted_files_output.strip():
                return []
            
            # Convert file path to relative path from repo root
            repo_root = Path(repo.working_dir)
            try:
                relative_path = path.relative_to(repo_root)
            except ValueError:
                # File is outside repo
                return []
            
            # Check if the specific file is in conflicts
            for line in conflicted_files_output.splitlines():
                parts = line.split('\t')  # Git output uses tabs
                if len(parts) >= 2:
                    conflicted_file = parts[1]  # File path is after the tab
                    if Path(conflicted_file) == relative_path:
                        return [path]
            
            return []
            
        elif path.is_dir():
            repo = Repo(path)
            if not repo.git_dir:
                raise ValueError(f"'{path}' is not a Git repository")

            # Get all conflicted files
            conflicted_files_output = repo.git.ls_files(u=True)
            if not conflicted_files_output.strip():
                return []
            
            # Parse the output to extract file paths
            conflicted_files = set()
            repo_root = Path(repo.working_dir)
            
            for line in conflicted_files_output.splitlines():
                parts = line.split('\t')  # Git output uses tabs
                if len(parts) >= 2:
                    file_path = parts[1]  # File path is after the tab
                    full_path = repo_root / file_path
                    conflicted_files.add(full_path)
            
            return sorted(list(conflicted_files))
        else:
            raise ValueError(f"'{path}' is neither a file nor a directory")
            
    except Exception as e:
        raise ValueError(f"Error getting conflicted files: {str(e)}")